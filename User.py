class User:
    'Info about the user object'

    def __init__(self,username=''):
        #self.firstname=firstname
        self.username=username

    def setUsername(self, username):
        self.username=username
    def getUsername(self):
        return self.username

    def setFirstname(self, firstname):
        self.firstname=firstname
    def getFirstname(self):
        return self.firstname

    def setLastname(self, lastname):
        self.lastname=lastname
    def getLastname(self):
        return self.lastname

    def setID(self, id):
        self.id=id
    def getID(self):
        return self.id