
#
# SQLAlchemy를 ORM으로 이용하는 것..
#   - http://yujuwon.tistory.com/entry/SQLAlchemy-사용하기
# SQLite 사용법
#   - https://hermeslog.tistory.com/181



from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func, String


# 먼저 sqlite3 명령을 이용해서 database를 만들어주고, SQL을 이용해 table을 만들어 줘야 함.
# 파일명은 일단 user.db로 만들어보고..
# 
#   $ sqlite3 user.db
#   % create table users(
# 	 id INTEGER primary key autoincrement,
# 	 name text,
# 	 email text,
# 	 username char(255)
#    );


engine = create_engine('sqlite:///user.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# 아래 두 줄은 뭔 소리인지 모르겠지만, 그냥 이렇게 해..
#   - 데이터베이스내의 데이터를 가져오기 위한 기본 base 클래스를 만들자.
#   - db_session을 이 기본 base 클래스에 연결시키자
# 왜 이렇게 하는지는 궁금해 하지 말자. 얘네가 그냥 그렇게 만들어 놓은거고, 그냥 따를 수 밖에 없지 않겠음?
Base = declarative_base()  
Base.query = db_session.query_property()


# 테이블이 여러개면 이런 클래스가 여러개여야 하겠지.
class User(Base):
    __tablename__ = 'users'         # 뭔가 예약어인듯?
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    email = Column(Text)
    username = Column(String(255))      # TODO: String과 Text의 차이는 뭘까요?


