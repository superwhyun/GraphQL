import graphene



Episode = graphene.Enum('EP', [('NewHope', 4), ('Empire', 5), ('Jedi', 6)])

class Query(graphene.ObjectType):
  hello = graphene.String(name=graphene.String(default_value="World"))

  def resolve_hello(self, info, name):
    return 'Hello ' + name

  

schema = graphene.Schema(query=Query)
result = schema.execute('{ hello }')
print(result.data['hello']) # "Hello World"
