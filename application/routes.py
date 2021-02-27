from application import app, db
from flask import render_template, request, json, Response, redirect, flash, url_for
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm

course_data = [{"courseID":"1111","title":"PHP 111","description":"Intro to PHP","credits":"3",
"term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1",
"description":"Intro to Java Programming","credits":"4","term":"Spring"}, 
{"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":"3",
"term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular",
"credits":"3","term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2",
"description":"Advanced Java Programming","credits":"4","term":"Fall"}]

@app.route("/")
@app.route("/index")
@app.route("/home")
def index(): # usually index/home/default
    return render_template("index.html", index=True)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): # if no errors
        email       = form.email.data
        password    = form.password.data

        user = User.objects(email=email).first() # returns a single object of the user
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            return redirect("/index")
        else:
            flash("Sorry, something went wrong.", "danger")
    return render_template("login.html", title="Login", form=form, login=True)

@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term="Winter 2021"):
    classes = Course.objects.order_by("+courseID") #+:asc order; -: desc
    return render_template("courses.html", course_data=classes, courses=True, term=term)

@app.route("/register", methods=['GET', 'POST'])
def register(): 
    form = RegisterForm()
    if form.validate_on_submit():
        id     = User.objects.count()
        id     += 1

        email       = form.email.data
        password    = form.password.data
        first_name  = form.first_name.data
        last_name   = form.last_name.data

        user = User(id=id, email=email, first_name=first_name, 
            last_name=last_name)
        user.set_password(password)
        user.save()
        flash("You are successfully registered", "success")
        return redirect(url_for('index'))
    return render_template("register.html", title="Register", form=form, register=True)

@app.route("/enrollment", methods=["GET", "POST"])
def enrollment(): 
    courseID = request.form.get('courseID')
    courseTitle = request.form.get('title')

    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(f"You are already registered in this course {courseTitle}", "danger")
            return redirect(url_for("courses"))
        else: 
            Enrollment(user_id=user_id, courseID=courseID)
            flash(f"You are enrolled in {courseTitle}!", "success")

    classes = None

    term = request.form.get('term')
    return render_template("enrollment.html", enrollment=True, title="Enrollment",
        classes=classes)

@app.route("/api/")
@app.route("/api/<int:idx>")
def api(idx=None):
    if idx == None:
        jdata = course_data
    else:
        jdata = course_data[idx]
    return Response(json.dumps(jdata), mimetype="application/json")

@app.route("/user")
def user():
    # User(user_id=1, first_name="Frank", last_name="Ho", email="frank.ho@uta.com", password="password123").save()
    # User(user_id=2, first_name="Mary", last_name="Jane", email="mary.jane@uta.com", password="abc1234").save()
    users = User.objects.all()
    return render_template("user.html", users=users)
