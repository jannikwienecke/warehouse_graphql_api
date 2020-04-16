import graphene

from graphene_django import DjangoObjectType
from graphql import GraphQLError

from django.db.models import Q

from ..models import Packaging
from ..utils import Filter

class PackagingType(DjangoObjectType):
    class Meta:
        model = Packaging


class Query(graphene.ObjectType):
    packagings = graphene.List(
        PackagingType,
        search=graphene.String(description='FUZZY SEARCH'),
        id=graphene.Int(),
        name=graphene.String(),
        width=graphene.Int(),
        length=graphene.Int(),
        )

    def resolve_packagings(self, info, **kwargs):

        queryset = Packaging.objects.all()

        if kwargs:
                
            fuzzy_search_fields = ['name', 'width', 'length']
            queryset = Filter(queryset, kwargs, None, fuzzy_search_fields)()
                    
        return queryset


class CreatePackaging(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    width = graphene.Int()
    length = graphene.Int()
    

    class Arguments:
        name = graphene.String()
        width = graphene.Int()
        length = graphene.Int()


    def mutate(self, info, name, width, length):

        user = info.context.user or Non

        package = Packaging(name=name, width=width, length=length, created_by=user)
        package.save()

        return PackagingType(
            id=package.id,
            name=package.name,
            width=package.width,
            length=package.length
        )

class UpdatePackaging(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    width = graphene.Int()
    length = graphene.Int()
    

    class Arguments:
        id =graphene.Int()
        name = graphene.String()
        width = graphene.Int()
        length = graphene.Int()

    def mutate(self, info, id=None, **args):

        user = info.context.user or Non

        try:
            packaging = Packaging.objects.get(id=id)
        except:
            raise GraphQLError(f"'Packaging' mit ID {id} Nicht vorhanden")

        for key, val in args.items():
            setattr(packaging, key, val)

        packaging.save()

        return packaging


class Mutation(graphene.ObjectType):
    create_packaging = CreatePackaging.Field()
    update_packaging = UpdatePackaging.Field()