#! usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_graphql import GraphQLView
from database import db_session
from schema import schema


app = Flask(__name__)
app.debug = True

# add_url_rule(
    # rule,                             ==> url
    # endpoint=None,                    ==> ??
    # view_func=None,                   ==> view를 위해 필요한 페이지를 만들어주는데 사용되는 함수명
    # provide_automatic_options=None, 
    # **options
    # )

# GraphQLView.as_view 는 flask-graphql에서 사용하는 함수 (그냥 이렇게 쓰래... just use)
#   - https://github.com/graphql-python/flask-graphql
    # schema : The GraphQLSchema object that you want the view to execute when it gets a valid request
    # context: A value to pass as the context to the graphql() function.
    # graphiql: If True, may present GraphiQL when loaded directly from a browser (a useful tool for debugging and exploration).

app.add_url_rule('/graphql', 
            view_func=GraphQLView.as_view(
                'graphql',
                schema=schema, 
                graphiql=True, 
                context={'session': db_session}))


@app.route('/')
def index():
	return "Go to /graphql"

if __name__ == "__main__":
	app.run(port=5001)                