import sqlite3
from contextlib import closing

from objects import Form
from objects import User
from objects import Organization

conn = None


def connect():
    global conn
    if not conn:
        DB_FILE = "db/budget.sqlite"
        conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        conn.row_factory = sqlite3.Row


def close():
    if conn:
        conn.close()


def make_form(row):
    submitter = get_user(row["user"])
    organization = make_org(row["name"], submitter, row["amount_in"], row["amount_out"])
    return Form(row["id"], organization, row["status"], row["comments"], submitter)


def make_user(row):
    return User(row["id"], row["name"], row["type"])


def make_org(name, owner, amount_in, amount_out):
    return Organization(name, owner, amount_in, amount_out)


def get_user(username):
    query = '''SELECT * FROM Users WHERE name = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (username,))
        row = c.fetchone()
    if row:
        return make_user(row)
    else:
        return None


def create_user(new_user):
    query = '''INSERT INTO `Users`(`name`,`type`) VALUES (?,?);'''
    if new_user.user_type == 'Manager':
        with closing(conn.cursor()) as c:
            c.execute(query,
                      (new_user.name, 'Manager',))
            conn.commit()
    else:
        with closing(conn.cursor()) as c:
            c.execute(query,
                      (new_user.name, 'Budget',))
            conn.commit()


def get_form(form_id):
    query = '''SELECT * FROM Forms WHERE id = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (form_id,))
        row = c.fetchone()
        if row:
            return make_form(row)
        else:
            return None


def get_forms_by_creator(username):
    query = '''SELECT * FROM Forms WHERE user = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (username,))
        results = c.fetchall()
        forms = []
        for row in results:
            forms.append(make_form(row))
        return forms


def get_forms_by_status(status):
    query = '''SELECT * FROM Forms WHERE status = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (status,))
        results = c.fetchall()
        forms = []
        for row in results:
            forms.append(make_form(row))
        return forms


def get_all_forms():
    query = '''SELECT * FROM Forms'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()
        forms = []
        for row in results:
            forms.append(make_form(row))
        return forms


def update_form(form):
    query = '''UPDATE `Forms` SET `status`=?, `comments`=? WHERE id=?;'''
    with closing(conn.cursor()) as c:
        c.execute(query, (form.status, form.comments, form.id))
        conn.commit()


def add_form(form):
    query = '''INSERT INTO `Forms`(`name`,`amount_in`,`amount_out`,`comments`,`user`) VALUES (?,?,?,?,?);'''
    with closing(conn.cursor()) as c:
        c.execute(query, (form.organization.name, form.amount_in, form.amount_out, form.comments, form.submitter.name))
        conn.commit()