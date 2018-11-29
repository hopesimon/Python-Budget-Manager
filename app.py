from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
import os
import db
import objects

port = int(os.getenv('PORT', 8000))


def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    app.config['SECRET_KEY'] = 'devkey'
    db.connect()

    global user
    user = None

    @app.route('/', methods=('GET', 'POST'))
    @app.route('/index', methods=('GET', 'POST'))
    def index():
        # gain access to the global user so we can set it
        global user
        # if a submission hasn't been made (method is not post)
        if request.method != "POST":
            # if user is not logged in
            if user is None:
                # render the login page
                return render_template('index.html')
            # if a manager is attempting to access login
            if user.user_type == 'Manager':
                # redirect to admin page
                return redirect('/admin')
            # if a budgeter is attempting to access login
            elif user.user_type == 'Budget':
                # redirect to form submission page
                return redirect('/form')
            else:
                # render the login page
                return render_template('index.html')
        # if a submission has been made (method is post)
        elif request.method == "POST":
            # set the user
            user = db.get_user(request.form['username'])
            # if the user is None (i.e. entered username is not found
            if user is None:
                # render corresponding error message
                return render_template('incorrect.html', data=request.form['username'])
            elif user.user_type == 'Manager':
                # if a manager has logged in, redirect to admin page
                return redirect('/admin')
            elif user.user_type == 'Budget':
                # if a budgeter has logged in, redirect to budget submission page
                return redirect('/form')

    @app.route('/logout')
    def logout():
        # set user to none
        global user
        user = None
        # redirect to login page
        return redirect('/index')

    @app.route('/form', methods=['POST', 'GET'])
    def form():
        global user
        # if user is not logged in, redirect to login page
        if user is None:
            return redirect('/index')
        # if user is a manager, redirect to admin page
        elif user.user_type == 'Manager':
            return redirect('/admin')
        # if not post
        # set organizations to be essentially empty
        if request.method != "POST":
            organization = objects.Organization(owner=user, name="Organization name")
            request_form = objects.Form(organization=organization, submitter=organization.owner)
            return render_template('submitter/submit.html', user=user, form=request_form)

        # if post & UPDATE not SUBMIT
        # update the net amount
        elif request.method == "POST" and request.form['btn'] == 'update':
            organization = objects.Organization(name=request.form['orgname'], owner=user,
                                                amount_in=float(request.form['amount_in']),
                                                amount_out=float(request.form['amount_out']))

            request_form = objects.Form(organization=organization, submitter=user)
            return render_template('submitter/submit.html', user=user, form=request_form)

        # if post & SUBMIT not UPDATE
        # submit the app
        elif request.method == "POST" and request.form['btn'] == 'submit':
            organization = objects.Organization(name=request.form['orgname'], owner=user,
                                                amount_in=float(request.form['amount_in']),
                                                amount_out=float(request.form['amount_out']))
            request_form = objects.Form(organization=organization, submitter=user)
            request_form.add_to_db()
            return render_template('submitter/submit_success.html')

    @app.route('/myapps')
    def myapps():
        global user
        # if user is not logged in, redirect to login page
        if user is None:
            return redirect('/index')
        # else if user is manager, redirect to admin page
        elif user.user_type == 'Manager':
            return redirect('/admin')
        # else display all forms
        else:
            forms = db.get_forms_by_creator(user.name)
            return render_template('submitter/apps.html', forms=forms)

    @app.route('/admin')
    def admin():
        global user
        # if user is not logged in, redirect to login page
        if user is None:
            return redirect('/index')
        # if user is not a manager, redirect to form submission page
        elif user.user_type != 'Manager':
            return redirect('/form')
        # get all forms, organized by category
        accepted = db.get_forms_by_status("Accepted")
        denied = db.get_forms_by_status("Denied")
        progress = db.get_forms_by_status("In Progress")
        # display all forms on page
        return render_template('admin/admin.html', accepted_forms=accepted, denied_forms=denied,
                               in_progress_forms=progress)

    @app.route('/forms', methods=['POST', 'GET'])
    def requests():
        global user
        # if user is not logged in, redirect to login page
        if user is None:
            return redirect('/index')
        # if user is not a manager, redirect to form submission page
        elif user.user_type != 'Manager':
            return redirect('/form')
        # if method is post (i.e. submit button was pressed)
        if request.method == "POST":
            # save the form as an object
            request_form = db.get_form(request.form['form_id'])
            # set the comments and status from admin entries
            request_form.comments = request.form['comments']
            request_form.status = request.form['status']
            # update the form
            request_form.update_db()
            # display success
            return render_template('admin/success.html')
        else:
            # find out which ID this form is
            form_id_to_get = request.args.get("id")
            # get the form from the ID
            budget_form = db.get_form(form_id_to_get)
            # if the form doesn't exist, display error
            if budget_form is None:
                return render_template('admin/error.html')
            # else if the form has status 'In Progress' display screen with editable content
            elif budget_form.status == 'In Progress':
                return render_template('admin/in_progress.html', form=budget_form)
            # else just display form with all info
            else:
                return render_template('admin/forms.html', form=budget_form)

    return app


# create an app instance
app = create_app()

app.run(host='0.0.0.0', port=port, debug=True)

# close db after app finishes running
db.close()
