class Organization:
    def __init__(self, name=None, owner=None, amount_in=0, amount_out=0):
        self.name = name
        self.owner = owner
        self.amount_in = amount_in
        self.amount_out = amount_out


class Form:
    def __init__(self, id=0, organization=None, status="In Progress", comments=None,
                 submitter=None):
        self.id = id
        self.organization = organization
        self.amount_in = organization.amount_in
        self.amount_out = organization.amount_out
        self.status = status
        self.comments = comments
        self.submitter = submitter


class User:
    def __init__(self, id=0, name=None, user_type="Budget"):
        self.id = id
        self.name = name
        self.user_type = user_type