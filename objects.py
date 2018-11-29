class Organization:
    def __init__(self, name=None, owner=None, amount_in=0, amount_out=0):
        self.__name = name
        self.__owner = owner
        self.__amount_in = amount_in
        self.__amount_out = amount_out

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, owner):
        self.__owner = owner

    @property
    def amount_in(self):
        return self.__amount_in

    @amount_in.setter
    def amount_in(self, amount_in):
        self.__amount_in = amount_in

    @property
    def amount_out(self):
        return self.__amount_out

    @amount_out.setter
    def amount_out(self, amount_out):
        self.__amount_out = amount_out

    def get_net(self):
        return self.__amount_in - self.__amount_out


class Form:
    def __init__(self, id=0, organization=None, status="In Progress", comments=None,
                 submitter=None):
        self.__id = id
        self.__organization = organization
        self.__amount_in = organization.amount_in
        self.__amount_out = organization.amount_out
        self.__status = status
        self.__comments = comments
        self.__submitter = submitter

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, form_id):
        self.__id = form_id

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def comments(self):
        return self.__comments

    @comments.setter
    def comments(self, comments):
        self.__comments = comments

    @property
    def submitter(self):
        return self.__submitter

    @submitter.setter
    def submitter(self, submitter):
        self.__submitter = submitter

    @property
    def organization(self):
        return self.__organization

    @organization.setter
    def organization(self, organization):
        self.__organization = organization

    @property
    def amount_out(self):
        return self.__amount_out

    @amount_out.setter
    def amount_out(self, amount_out):
        self.__amount_out = amount_out

    @property
    def amount_in(self):
        return self.__amount_in

    @amount_in.setter
    def amount_in(self, amount_in):
        self.__amount_in = amount_in

    def get_net(self):
        return self.__amount_in - self.__amount_out


class User:
    def __init__(self, id=0, name=None, user_type="Budget"):
        self.__id = id
        self.__name = name
        self.__user_type = user_type

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, user_id):
        self.__id = user_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def user_type(self):
        return self.__user_type

    @user_type.setter
    def user_type(self, user_type):
        self.__user_type = user_type
