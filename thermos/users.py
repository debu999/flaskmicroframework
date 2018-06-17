"""Users class for thermos project"""

class Userobj:
    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname

    def initials(self):
        return "{}.{}".format(self.fname.upper()[0], self.lname.upper()[0])

    def __repr__(self):
        return "User is {} {}".format(self.fname, self.lname)

