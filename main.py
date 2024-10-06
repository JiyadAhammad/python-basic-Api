from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, TEXT, VARCHAR, LargeBinary, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid


app = FastAPI()

DATABASE = "postgresql://postgres:jiyad123@localhost:5432/Flutter test"

engine = create_engine(DATABASE)

sessionLocal = sessionmaker(autoflush=False, bind=engine)

db = sessionLocal()


## Signup Model
class CreateUser(BaseModel):
    email: str
    name: str
    password: str


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(TEXT, primary_key=True)
    name = Column(VARCHAR(50))
    email = Column(VARCHAR(50))
    password = Column(TEXT)


## Create a API for Signup User:
@app.post("/signup")
def singupUser(user: CreateUser):
    # Extract the data from Request
    print(user.email + "this is email")
    print(user.name + "this is name")
    print(user.password + "this is password")
    # Check if the user already registser or not
    userDb = db.query(User).filter(User.email == user.email).first()

    if userDb:
        return "User Already Exist"

    # Add New User to DB
    userDb = User(
        id=str(uuid.uuid4()),
        name=user.name,
        email=user.email,
        password=user.password,
    )

    db.add(userDb)
    db.commit()

    return userDb

    pass


Base.metadata.create_all(engine)


## one way of sending request
# @app.post('/')
# async def testApi(request: Request):
#     print((await request.body()).decode())
#     return 'somthing printing'

# --------------------------------------------------

## another way
# class Test(BaseModel):
#     name:str
#     age:int
# ==============================
# @app.post('/')
# def testApi(t: Test):
#     print(t)
#     return 'somthing printing'
