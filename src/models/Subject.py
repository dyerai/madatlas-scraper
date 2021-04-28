class Subject:

    def __init__(self, name, abbrev, code):
        self.name = name
        self.abbrev = abbrev
        self.code = code

    def __str__(self):
        return f"{self.code} {self.abbrev} {self.name}"
