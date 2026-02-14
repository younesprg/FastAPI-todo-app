from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # otomatik 'commit' yapma; # otomatik 'flush' yapma(session içindeki 
                                                                                                       # değişiklikleri Dbye gönderme yani)

Base = declarative_base()


""" Engine = DB motoru

    Session = transaction yöneticisi

    sessionmaker = session üretici fabrika

    Base = ORM temel sınıfı

    Model class = tablo  """