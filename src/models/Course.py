from dataclasses import dataclass


@dataclass
class Course:
    subjects: list
    name: str
    number: int
    credits: list
    description: str
    requisites: str
    designation: str
    repeatable: bool
    lastTaught: str
    requiresFreshmanStanding: bool = False
    requiresSophomoreStanding: bool = False
    requiresJuniorStanding: bool = False
    requiresSeniorStanding: bool = False
    requiresGraduateOrProfessionalStanding: bool = False
    requiresInstructorConsent: bool = False

