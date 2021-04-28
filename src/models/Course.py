class Course:

    def __init__(self, subjects, name, number, credits, description, requisites, designation, repeatable, lastTaught):
        self.subjects = subjects
        self.name = name
        self.number = number
        self.credits = credits
        self.description = description
        self.requisites = requisites
        self.designation = designation
        self.repeatable = repeatable
        self.lastTaught = lastTaught

    def __str__(self):
        return f'{self.name}'
