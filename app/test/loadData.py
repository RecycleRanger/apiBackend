import json

from app import crud, schemas, models
from app.models import Teacher, Student, Waste
from app.api import deps
from app.db.session import SessionLocal


db = SessionLocal()

def checkForAlreadyExists(func):
    def inner():
        try:
            print(f"Loading {func.__name__.capitalize()}")
            func()
        except:
            print("Data already exists in the database")
    return inner

@checkForAlreadyExists
def teacherTable():
    with open("./app/test/teacher.json", "r") as fh:
        data = json.load(fh)
        for i in data["teacherDummyData"]:

            teacher = Teacher(
                id=i["id"],
                username=i["username"],
                hashed_password=i["hashed_password"],
                date_started=i["date_started"]
            )

            db.add(teacher)
            db.commit()
            db.refresh(teacher)

@checkForAlreadyExists
def studentTable():
    with open("./app/test/student.json", "r") as fh:
        data = json.load(fh)
        for i in data["studentDummyData"]:

            student = Student(
                id=i["id"],
                student_name=i["student_name"],
                hashed_password=i["hashed_password"],
                score=i["score"],
                numOfTrash=i["numOfTrash"],
                class_id=i["class_id"]
            )

            db.add(student)
            db.commit()
            db.refresh(student)

@checkForAlreadyExists
def wasteTable():
    with open("./app/test/waste.json", "r") as fh:
        data = json.load(fh)
        for i in data["wasteDummyData"]:

            waste = Waste(
                id=i["id"],
                student_id=i["student_id"],
                createdAt=i["createdAt"],
                trash_type=i["trash_type"],
                trash_score=i["trash_score"]
            )

            db.add(waste)
            db.commit()
            db.refresh(waste)


if __name__=="__main__":
    teacherTable()
    studentTable()
    wasteTable()
