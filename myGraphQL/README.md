https://github.com/Getmrahul/Flask-Graphene-SQLAlchemy 의 코드에 주석을 달고 일부 수정하였음.


# GraphQL 기본  

- GET, POST 만 사용함
- Single URL
- Edges? Node?
    - https://stackoverflow.com/questions/42622912/in-graphql-whats-the-meaning-of-edges-and-node
- GraphQL connection
    - The most popular method for pagination in GraphQL are GraphQL connections
    - These are often associated with Relay, a JavaScript GraphQL client open sourced by Facebook
    - However, connections are not specific to Relay at all
    - Connections were designed at Facebook as part of their internal GraphQL server design

## R (Read)

### Request

```graphql
query {
  allUsers {
    edges {
      node {
        name,
        email,
        username
      }
    }
  }
}
```

### Response

```graphql
{
  "data": {
    "allUsers": {
      "edges": [
        {
          "node": {
            "name": "shitman",
            "email": "fucking@asshole.com",
            "username": "fucker"
          }
        },
        {
          "node": {
            "name": "abc",
            "email": "hello@abc.com",
            "username": "newabc"
          }
        },
        {
          "node": {
            "name": "하하하",
            "email": "댐쉿@abc.com",
            "username": "abc"
          }
        }
      ]
    }
  }
}
```

## C (Read)

### Request

```graphql
query {
	allUsers {
	  edges {
	    node {
	      id,
        email,
        username,
        name
	    }
	  }
	}
}
```

또는
```graphql
query {
	findUser(username:"user alias") {
	  id,
    username,
    email
	}
}
```


### Response
```graphql
{
  "data": {
    "allUsers": {
      "edges": [
        {
          "node": {
            "id": "VXNlcnM6NQ==",
            "email": "user@email.com",
            "username": "user alias"
          }
        }
      ]
    }
  }
}
```

또는

```graphql
{
  "data": {
    "findUser": {
      "id": "VXNlcnM6NQ==",
      "username": "user alias",
      "email": "user@email.com"
    }
  }
}
```

## U (Update)

### Request

```graphql
mutation {
  changeUsername(email:"쉬@닷컴", username:"껒여") {
    user {
      id,
      username,
      email
    }
  }
}
```

# References

- https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/
- https://media.readthedocs.org/pdf/graphene-sqlalchemy/stable/graphene-sqlalchemy.pdf
- https://blog.apollographql.com/explaining-graphql-connections-c48b7c3d6976
- 
