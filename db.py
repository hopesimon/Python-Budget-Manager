import sqlite3
from contextlib import closing

from objects import Form
from objects import User
from objects import Organization

conn = None

# db connection function
def connect():
    global conn
    if not conn:
        DB_FILE = "db/budget.sqlite"
        conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        conn.row_factory = sqlite3.Row


# db close function
def close():
    if conn:
        conn.close()


# make a Form object out of row received from database
def make_form(row):
    submitter = get_user(row["user"])
    organization = make_org(row["name"], submitter, row["amount_in"], row["amount_out"])
    return Form(row["id"], organization, row["status"], row["comments"], submitter)


# make a User object out of row received from database
def make_user(row):
    return User(row["id"], row["name"], row["type"])


# make an Organization object out of parameters passed
def make_org(name, owner, amount_in, amount_out):
    return Organization(name, owner, amount_in, amount_out)


# get a User object from a passed username string
def get_user(username):
    # select all data with the name
    query = '''SELECT * FROM Users WHERE name = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (username,))
        # only fetch one entry... there shouldn't be multiple of the same name (names are unique)
        row = c.fetchone()
    # if a user was fetched, make a User object and return it
    if row:
        return make_user(row)
    # else return None (user not found)
    else:
        return None


# get a Form object from a passed form_id integer
def get_form(form_id):
    # select all data from the form with the specified ID (form IDs are unique)
    query = '''SELECT * FROM Forms WHERE id = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (form_id,))
        # get only one form
        row = c.fetchone()
        # if a form is found, return it
        if row:
            return make_form(row)
        # else return None
        else:
            return None


# get a list of Form objects from a passed submitter (based on username string of User object who submitted form)
def get_forms_by_creator(username):
    # select all data from the form with the specified submitter
    query = '''SELECT * FROM Forms WHERE user = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (username,))
        # get all
        results = c.fetchall()
        forms = []
        # for each row [data entry] add it to the list as a Form object
        for row in results:
            forms.append(make_form(row))
        # return the list
        return forms


# get a list of Form objects with a specified status (based on status string)
def get_forms_by_status(status):
    # select all data from the form with the specified status
    query = '''SELECT * FROM Forms WHERE status = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (status,))
        # get all
        results = c.fetchall()
        forms = []
        # for each row [data entry] add it to the list as a Form object
        for row in results:
            forms.append(make_form(row))
        # return the list
        return forms


# get all forms
def get_all_forms():
    # select all data from all forms
    query = '''SELECT * FROM Forms'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        # get all
        results = c.fetchall()
        forms = []
        # for each row [data entry] add it to the list as a Form object
        for row in results:
            forms.append(make_form(row))
        # return the list
        return forms


# update a form, with a Form object passed in to be updated
def update_form(form):
    query = '''UPDATE `Forms` SET `status`=?, `comments`=? WHERE id=?;'''
    with closing(conn.cursor()) as c:
        c.execute(query, (form.status, form.comments, form.id))
        conn.commit()


# add a form, with a Form object passed in to be added to the Forms table
def add_form(form):
    query = '''INSERT INTO `Forms`(`name`,`amount_in`,`amount_out`,`comments`,`user`) VALUES (?,?,?,?,?);'''
    with closing(conn.cursor()) as c:
        c.execute(query, (form.organization.name, form.amount_in, form.amount_out, form.comments, form.submitter.name))
        conn.commit()