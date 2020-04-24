import graphene

from graphene_django import DjangoObjectType
from ..models import Null


class NullType(DjangoObjectType):
    class Meta:
        model = Null


class Query(graphene.ObjectType):
    nulls = graphene.List(
        NullType,
    )

    def resolve_nulls(self, info, **kwargs):
        return None


class CreateNull(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        pass

    def mutate(self, info):
        return None


class Mutation(graphene.ObjectType):
    null_mutation = CreateNull.Field()
