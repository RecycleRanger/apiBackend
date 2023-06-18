from typing import Any, Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app.api import deps
from app import schemas
from app import crud
from app.core.auth import authenticate, create_access_token
from app.core.myTypes import UsrType, CurrentUsr, AdditionalUserDataForm

from app.models.teacher import Teacher
from app.models.student import Student

from app.core.auth import teacher_oauth2_scheme


router = APIRouter()

@router.post("/login/teacher")
def login_teacher(
        db: Session = Depends(deps.get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Get the JWT for a teacher with data from OAuth2 request form body.
    """

    teacher = authenticate(
        username=form_data.username,
        password=form_data.password,
        db=db,
        usrType=UsrType.teacher
    )
    if not teacher:
        raise HTTPException(
            status_code=400,
            detail="Incorect username or password"
        )
    teacher = jsonable_encoder(teacher)
    del teacher["hashed_password"]
    teacher = Teacher(**teacher)
    return {
        "access_token": create_access_token(sub=teacher.id, usr=UsrType.teacher),
        "token_type": "bearer",
        "usr": teacher,
        "type": UsrType.teacher,
    }

@router.post("/login/student")
def login_student(
        db: Session = Depends(deps.get_db),
        form_data: OAuth2PasswordRequestForm = Depends(),
        additional_form_data: AdditionalUserDataForm = Depends()
) -> Any:
    """
    Get the JWT for a student with data from OAuth2 request form body.
    """

    student = authenticate(
        id=additional_form_data.id,
        username=form_data.username,
        password=form_data.password,
        db=db,
        usrType=UsrType.student
    )
    if not student:
        raise HTTPException(
            status_code=400,
            detail="Incorect username or password"
        )

    student = jsonable_encoder(student)
    del student["hashed_password"]
    student = Student(**student)
    return {
        "access_token": create_access_token(sub=student.id, usr=UsrType.student),
        "token_type": "bearer",
        "usr": student,
        "type": UsrType.student,
    }


@router.get("/me")
def read_users_me(
        current_user: CurrentUsr = Depends(deps.get_user)
):
    """
    Fetch the current logged in user.
    """

    user = current_user
    user = jsonable_encoder(user)
    del user["user"]["hashed_password"]
    return user

@router.post("/signup/teacher", response_model=schemas.Teacher, status_code=201)
def create_teacher_signup(
        *,
        db: Session = Depends(deps.get_db),
        teacher_in: schemas.teacher.TeacherCreate,
) -> Any:
    """
    Create new teacher with signup
    """

    if teacher_in.username == "" or teacher_in.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't have empty username or password"
        )

    teacher = db.query(Teacher) \
                .filter(Teacher.username == teacher_in.username) \
                .first()
    if teacher:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists"
        )
    teacher = crud.teacher.create(db=db, obj_in=teacher_in)

    return teacher

@router.post("/signup/student", response_model=schemas.Student, status_code=201)
def create_student_signup(
        *,
        db: Session = Depends(deps.get_db),
        student_in: schemas.student.StudentCreate
) -> Any:
    """
    Create new student with signup
    """

    student = db.query(Student) \
                .filter(Student.student_name == student_in.student_name) \
                .first()

    if student:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists"
        )

    student = crud.student.create(db=db, obj_in=student_in)

    return student
