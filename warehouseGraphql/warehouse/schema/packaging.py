import graphene
from graphene_django import DjangoObjectType

from ..models import Packaging


class PackagingType(DjangoObjectType):
    class Meta:
        model = Packaging


class Query(graphene.ObjectType):
    packagings = graphene.List(PackagingType)

    def resolve_packagings(self, info, **kwargs):
        return Packaging.objects.all()


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


#4
class Mutation(graphene.ObjectType):
    create_packaging = CreatePackaging.Field()