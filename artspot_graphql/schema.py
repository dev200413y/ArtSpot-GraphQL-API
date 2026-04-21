import graphene
from shop.schema import Query, Mutation

schema = graphene.Schema(query=Query, mutation=Mutation)
