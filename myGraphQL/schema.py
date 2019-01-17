
#
# 실제 GraphQL로 주고받는 데이터를 핸들링하는 모든 기능이 여기에 담겨 있다고 보면 됨
#

# GraphQLSchema Object를 사용하기 위해서리 그래핀을 import함
import graphene

# Graphene에서 relay 클래스(?)를 가져 옴... 뭐에 쓰는 건지는 찬찬히 알아보자.
from graphene import relay

# Graphene_sqlalchemy 패키지에서 관련된 녀석들을 가져 옴.
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

# 전역변수인 db_session과 User Class를 import 한다.
from database import db_session, User as UserModel



# 아래 import는 SQLAlchemy에서 SQL select 문장을 만들때 'and' 조건을 넣기 위한 거라는군.
# http://www.mapfish.org/doc/tutorials/sqlalchemy.html
from sqlalchemy import and_

class Users(SQLAlchemyObjectType):
    # TODO: 이것도 무슨 규약인가 보지? 반드시 Meta라는 클래스가 있어야 하는건가?
    # TODO: 또 그 안에 model, interfaces가 있어야 하나?
    # TODO: graphene의 relay가 하는 역할은 뭘까요?
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )     # 리스트로 넘겨주네? 여러개 달 수 있다는 얘기??


# 이 함수가 나중에 웹에 api function으로 노출된다.
# graphene과 연결은 어떻게....? createUser 클래스 인스턴스를 만드는 데는 어디?
class createUser(graphene.Mutation):

    # Mutation 동작과 관련해서 넘겨받을 인자를 선언함.
    class Arguments:
        name=graphene.String()
        email=graphene.String()
        username=graphene.String()

    # 얘네는 클래스 변수 (self.xx 로 된 것은 인스턴스 변수)
    #   - https://wikidocs.net/1744
    ok = graphene.Boolean()
    user=graphene.Field(Users)

    # 이 함수는 그냥 무조건 쓰는 규약이라고 보자.
    def mutate(self, context, **kwargs):
        # kwargs로부터 읽고자 하는 값들을 끌어온다. 

        # TODO: 여기서 name, email, username은 UserMode 클래스의 내부변수? 아님 이 클래스의 내부변수??
        user=UserModel(name=kwargs.get('name'), email=kwargs.get('email'), username=kwargs.get('username'))
        db_session.add(user)
        db_session.commit()
        ok=True

        # TODO: 에? 생성자? 이건 무슨 문법이래???
        # TODO: 이건 정말 모르겠다.
        return createUser(user=user, ok=ok)
        
class changeUsername(graphene.Mutation):
    class Arguments:
        username=graphene.String()
        email=graphene.String()

    ok = graphene.Boolean()
    user=graphene.Field(Users)    

    def mutate(self, context, **kwargs):

        # TODO: 이건 뭐지? Users 클래스가 SQLAlchemyObjectType를 상속받은 것이니.. 그렇다고는 쳐도..
        # TODO: context는 또 뭘까? 
        # save의 경우에는 db_session.add(...)만 하면 되지만, update 등과 같은 경우에는 query를 만들어야 하므로..
        # 아래처럼 해야 하는 듯.
        #   1. query=get_query(...)
        #   2. data=query.filter(...)
        #   3. data=data+1
        #   4. db_session.commit()
        query=Users.get_query(context)
        email=kwargs.get('email')
        username = kwargs.get('username')

        # SQLAlchemy에서 쓰는 방법인것 같은데...
        # db_session에 맵핑하는 과정이 없네? ==> database.py에서 해 놨음.
        user=query.filter(UserModel.email==email).first()
        user.username = username
        db_session.commit()
        ok=True

        return changeUsername(user=user, ok = ok)


## DELETE에 관련된 거 함 만들어 봄.

class deleteUser(graphene.Mutation):
    class Arguments:
        username=graphene.String()
        email=graphene.String()

    ok = graphene.Boolean()
    user=graphene.Field(Users)     

    def mutate(self, context, **kwargs):
        query=Users.get_query(context)
        email=kwargs.get('email')
        username = kwargs.get('username')


        user=query.filter(UserModel.email==email, UserModel.username==username).delete()
        db_session.commit()
        ok=True        

        return deleteUser(user=user, ok = ok)


# GET에 해당되는 기능인데...
# 구동후에 웹페이지에서 손을 대다보면,
#   - findUser 명령
#   - allUser 명령
# 이 지원된다. (힌트로도 나온다.)
# TODO: 근데, 난 allUser에 대해 함수를 만든 적이 없는데 어찌하여 이게 지원되는겐가?
class Query(graphene.ObjectType):
    node=relay.Node.Field()                         # TODO: 이걸 왜하지? 아무데도 사용하지 않는데?? 주석처리해도 아무 문제 없이 동작함.


    # 노출시켜 외부에서 데이터를 가져갈 수 있도록 하려면 다음과 같이 한다.
    user=SQLAlchemyConnectionField(Users)           # 웹 화면에 user 라는 키워드가 나온다. user(first:1)로 쓸수 있다.
    all_users = SQLAlchemyConnectionField(Users)    # 웹 화면에 allUsers 라는 키워드가 나온다. allUsers()로 쓸 수 있다.
                                                    # 변수명을 shit_users로 하면, 웹 화면에서 shitUsers()로 나온다. 
                                                    # 어떻게 된걸까? 변수명일뿐인데 어떻게 연결된거지????
    
    # 검색 키워드를 집어넣어서 조건에 맞는 녀석을 가져오고 싶을때는 다음과 같이 한다.
    findUser = graphene.Field(lambda: Users, username = graphene.String())
    shitUser = graphene.Field(lambda: Users, username = graphene.String())
    
    # 위에 만들어진 변수와 동일한 이름으로 "resolve_"+변수명으로 함수를 만들어 줌.
    # 변수명이 외부에 노출되도록 만든다는건... 음... 좀 많이 색다르네..
    def resolve_findUser(self, info, **kwargs):
        query = Users.get_query(info)
        username = kwargs.get('username')

        ret=query.filter(UserModel.username==username).first()
        print(type(ret), ret)  # ==>  <class 'database.User'> <database.User object at 0x1075f6e10>
        return ret

    def resolve_shitUser(self, info, **kwargs):
        query = Users.get_query(info)
        username = kwargs.get('username')

        ret=query.filter(UserModel.username==username).first()
        print(type(ret), ret)
        return ret


class MyMutations(graphene.ObjectType):

    # 아래처럼 하지 않으면, graphQL 홈페이지에서 힌트가 뜨지 않는다. 뭐, 당연히 정상메시지가 와도 지원도 하지 않겠지.
	create_user = createUser.Field()
	change_username = changeUsername.Field()
	delete_user=deleteUser.Field()


# schema를 선언해 줘야한다. 이거 빼먹으면 실행 타이밍에 import error 가 나온다.
# 얘가 GraphQLView.as_view()함수를 통해 flask와 연결된다.
# app.py에서 아래처럼 import 한다.
#   from schema import schema
# TODO: 근데 from의 schema는 schema.py이고,... import의 schema는 이건가 부지?
#       --> 아래 변수명을 바꾸고 import에서 바꿧는데 걍 에러 뱉는다.
#       --> 외부에서 import가 가능하려면, 파일명과 같아야 하나? 그건 아닐건데... db_session도 있었잖여..
schema = graphene.Schema(query=Query, mutation=MyMutations, types=[Users])




