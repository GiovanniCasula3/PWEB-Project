from sqlmodel import create_engine, SQLModel, Session, select
from typing import Annotated
from fastapi import Depends
import os
from faker import Faker
from app.config import config
from app.models.event import Event
from app.models.user import User
from app.models.registration import Registration

sqlite_file_name = config.root_dir / "data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)

def init_database() -> None:
    ds_exists = os.path.isfile(sqlite_file_name)
    SQLModel.metadata.create_all(engine)
    if not ds_exists:
        f = Faker("it_IT")
        with Session(engine) as session:
            for i in range(10):
                user = User(
                    username=f.user_name(),
                    email=f.email(),
                    name=f.name(),
                )
                session.add(user)
            session.commit()
            for i in range(10):
                event = Event(
                    title=f.sentence(),
                    desctription=f.text(),
                    date=f.date_time_this_year(),
                    location=f.city(),
                )
                session.add(event)
            session.commit()
            statment = select(User)
            result = session.exec(statment)
            users = result.all()
            for i in range(10):
                registration = Registration(
                    username=users[f.random_int(min=0, max=len(users) - 1)].username,
                    event_id=f.random_int(min=1, max=10),
                )
                session.add(registration)
            session.commit()

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]