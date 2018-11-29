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
        global user
        if request.method != "POST":
            return render_template('index.html')
        elif request.method == "POST":
            user = db.get_user(request.form['username'])
            if user is None:
                return render_template('incorrect.html', data=request.form['username'])
            elif user.user_type == 'Manager':
                return redirect('/admin')
            elif user.user_type == 'Budget':
                return redirect('/form')

    @app.route('/logout')
    def logout():
        global user
        user = None
        return redirect('/index')

    @app.route('/form', methods=['POST', 'GET'])
    def form():
        global user
        if user is None:
            return redirect('/index')
        elif user.user_type == 'Manager':
            return redirect('/admin')
        # if not post
        # set organizations to be essentially empty
        if request.method != "POST":
            organization = objects.Organization(owner=user, name="Organization name")
            request_form = objects.Form(organization=organization, submitter=organization.owner)
            print(request_form.amount_out)
            return render_template('submitter/submit.html', user=user, form=request_form)

        # if post & UPDATE not SUBMIT
        # update the net amount
        elif request.method == "POST" and request.form['btn'] == 'update':
            organization = objects.Organization(name=request.form['orgname'], owner=user,
                                                amount_in=float(request.form['amount_in']),
                                                amount_out=float(request.form['amount_out']))

            request_form = objects.Form(organization=organization, submitter=user)
            print(request_form.amount_in)
            return render_template('submitter/submit.html', user=user, form=request_form)

        # if post & SUBMIT not UPDATE
        # submit the app
        elif request.method == "POST" and request.form['btn'] == 'submit':
            organization = objects.Organization(name=request.form['orgname'], owner=user,
                                                amount_in=float(request.form['amount_in']),
                                                amount_out=float(request.form['amount_out']))
            request_form = objects.Form(organization=organization, submitter=user)
            db.add_form(request_form)
            return render_template('submitter/submit_success.html')

    @app.route('/myapps')
    def myapps():
        global user
        if user is None:
            return redirect('/index')
        else:
            forms = db.get_forms_by_creator(user.name)
            return render_template('submitter/apps.html', forms=forms)

    @app.route('/admin')
    def admin():
        global user
        if user is None:
            return redirect('/index')
        elif user.user_type != 'Manager':
            return redirect('/form')
        accepted = db.get_forms_by_status("Accepted")
        denied = db.get_forms_by_status("Denied")
        progress = db.get_forms_by_status("In Progress")
        return render_template('admin/admin.html', accepted_forms=accepted, denied_forms=denied,
                               in_progress_forms=progress)

    @app.route('/forms', methods=['POST', 'GET'])
    def requests():
        global user
        if user is None:
            return redirect('/index')
        elif user.user_type != 'Manager':
            return redirect('/form')
        if request.method == "POST":
            request_form = db.get_form(request.form['form_id'])
            request_form.comments = request.form['comments']
            request_form.status = request.form['status']
            db.update_form(request_form)
            return render_template('admin/success.html')
        else:
            form_id_to_get = request.args.get("id")
            budget_form = db.get_form(form_id_to_get)
            if budget_form is None:
                return render_template('admin/error.html')
            elif budget_form.status == 'In Progress':
                return render_template('admin/in_progress.html', form=budget_form)
            else:
                return render_template('admin/forms.html', form=budget_form)

    return app


# create an app instance
app = create_app()

app.run(host='0.0.0.0', port=port, debug=True)

# close db after app finishes running
db.close()
