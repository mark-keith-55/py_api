# from sqlalchemy import Column, Integer, String, create_engine
# from sqlalchemy.orm import declarative_base

# DB_style = 'mysql'
# name = 'root'
# host = 'localhost'
# password = ''
# DB_NAME = 'voicies'
# engine = create_engine(f"{DB_style}://{name}:{password}@{host}:3306/{DB_NAME}?charset=utf8mb4")
# Base = declarative_base()

# class User(Base):
#     __tablename__ = 'voicies'

#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     audio_path = Column(String)

# engine = create_engine('sqlite:///users.db')
# Base.metadata.create_all(engine)


# # ユーザーの取得
# users = session.query(User).all()
# for user in users:
#     print(user.name, user.email)


import mysql.connector

DB_style = 'mysql'
name = 'root'
host = 'localhost'
password = ''
DB_NAME = 'voicies'

conn = mysql.connector.connect(
    host=host,
    user=name,
    password=password,
    database=DB_NAME
)

# consultations table

    # consultation_id INT PRIMARY KEY,
    # dictation_text TEXT NULL COMMENT '文字起こしテキスト（最大65535文字）',
    # summary_text TEXT NULL COMMENT '要約テキスト（最大1023文字）',
    # audio_file_path VARCHAR(255) NULL COMMENT '音声ファイルのパス',
    # created_at TIMESTAMP NULL,
    # updated_at TIMESTAMP NULL
    
cursor = conn.cursor()
cursor.execute("SELECT * FROM consultations")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
