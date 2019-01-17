

# GraphQL을 사용하기 위해 그래핀을 import함
import graphene

# Graphene에서 relay 클래스(?)를 가져 옴
from graphene import relay

# Graphene_sqlalchemy 패키지에서 관련된 녀석들을 가져 옴.
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType


# database.py 파일에서 User 클래스와 db_sessino 변수를 가져오는데 UserModel이란 모듈에 
# 포함된 것으로 불러온다.
from database import db_session,User as UserModel

# TODO: 이건 도대체 뭔가..
from sqlalchemy import and_

class Users(SQLAlchemyObjectType):
	class Meta:
	    model = UserModel
	    interfaces = (relay.Node, )

# Used to Create New User
class createUser(graphene.Mutation):
	# graphene 2.0 ; changed class name to be in accordance with 2.0 version
	class Arguments:
		name = graphene.String()
		email = graphene.String()
		username = graphene.String()
	ok = graphene.Boolean()
	user = graphene.Field(Users)

	# graphene 2.0 ; removed the declaration for classmethod 
	# @classmethod 

	# graphene 2.0 ; rename the mutate function
	# def mutate(cls, _, args, context, info):
	def mutate(self, context, **kwargs):
		user = UserModel(name=kwargs.get('name'), email=kwargs.get('email'), username=kwargs.get('username'))
		db_session.add(user)
		db_session.commit()
		ok = True
		return createUser(user=user, ok=ok)
# Used to Change Username with Email
class changeUsername(graphene.Mutation):
	class Arguments:
		username = graphene.String()
		email = graphene.String()

	ok = graphene.Boolean()
	user = graphene.Field(Users)

	# @classmethod
	# def mutate(cls, _, args, context, info):
	def mutate(self, context, **kwargs):	
		query = Users.get_query(context)
		email = kwargs.get('email')
		username = kwargs.get('username')
		user = query.filter(UserModel.email == email).first()
		user.username = username
		db_session.commit()
		ok = True

		return changeUsername(user=user, ok = ok)


class Query(graphene.ObjectType):
	node = relay.Node.Field()
	user = SQLAlchemyConnectionField(Users)
	findUser = graphene.Field(lambda: Users, username = graphene.String())
	# find_user = graphene.String(description='A fuck...')
	all_users = SQLAlchemyConnectionField(Users)

	def resolve_findUser(self, info, **kwargs):
		query = Users.get_query(info)
		username = kwargs.get('username')
		
		# you can also use and_ with filter() eg: filter(and_(param1, param2)).first()
		return query.filter(UserModel.username == username).first()



class MyMutations(graphene.ObjectType):
	create_user = createUser.Field()
	change_username = changeUsername.Field()

schema = graphene.Schema(query=Query, mutation=MyMutations, types=[Users])
