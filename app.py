from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
import os
import db

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
        if request.method != "POST":
            return render_template('submitter/submit.html', user=user)
        elif request.method == "POST":
            name = request.form['orgname']
            amount_in = request.form['amount_in']
            amount_out = request.form['amount_out']
            db.add_form(name=name, amount_in=amount_in, amount_out=amount_out, user=user.name)
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
            form_id = request.form['form_id']
            comments = request.form['comments']
            status = request.form['status']
            db.update_form(form_id=form_id, status=status, comments=comments)
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
