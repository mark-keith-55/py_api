from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

DB_style = 'mysql'
name = 'root'
host = 'localhost'
password = ''
DB_NAME = 'voicies'
engine = create_engine(f"{DB_style}://{name}:{password}@{host}:3306/{DB_NAME}?charset=utf8mb4")
Base = declarative_base()

class User(Base):
    __tablename__ = 'voicies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    audio_path = Column(String)

engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)


# ユーザーの取得
users = session.query(User).all()
for user in users:
    print(user.name, user.email)