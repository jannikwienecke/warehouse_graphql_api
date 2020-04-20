import graphene

from graphene_django import DjangoObjectType
from graphql import GraphQLError

from django.db.models import Q
from ..graphql_jwt.decorators import login_required

from ..models import Symbuilding, Symfactory
from ..utils import Filter
from users.schema import UserType
from ..schema.symfactory import SymfactoryType


class SymbuildingType(DjangoObjectType):
    class Meta:
        model = Symbuilding

class Query(graphene.ObjectType):
    symbuildings = graphene.List(
        SymbuildingType,
        search=graphene.String(description='FUZZY SEARCH'),
        id=graphene.Int(),
        name=graphene.String(),
        symfactory_id=graphene.Int()
        )
    
    

    def resolve_symbuildings(self, info, **kwargs):

        queryset = Symbuilding.objects.all()

        if kwargs:
                
            fuzzy_search_fields = ['name']
            queryset = Filter(queryset, kwargs, None, fuzzy_search_fields)()
                    
        return queryset


class CreateSymbuilding(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    symfactory = graphene.Field(SymfactoryType)

    class Arguments:
        name = graphene.String()
        symfactory_id = graphene.Int()

    @login_required
    def mutate(self, info, name, symfactory_id):

        user = info.context.user or None

        symfactory = Symfactory.objects.filter(id=symfactory_id).first()
        if not symfactory:
            raise GraphQLError("Ungültiges Werk")
        
        symbuilding = Symbuilding(name=name,
            created_by=user, symfactory_id=symfactory_id)
        symbuilding.save()

        return symbuilding

class UpdateSymbuilding(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    symfactory = graphene.Field(SymfactoryType)
    created_by = graphene.Field(UserType)
    
    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        symfactory_id = graphene.Int()

    def mutate(self, info, id=None, **args):

        user = info.context.user or None

        try:
            symbuilding = Symbuilding.objects.get(id=id)
        except:
            raise GraphQLError(f"'Symbuilding' mit ID {id} Nicht vorhanden")

        for key, val in args.items():
            setattr(symbuilding, key, val)

        symbuilding.save()

        return symbuilding

class DeleteSymbuilding(graphene.Mutation):
    id = graphene.Int()
    created_by = graphene.Field(UserType)

    class Arguments:
        id =graphene.Int()

    def mutate(self, info, id=None, **args):

        try:
            Symbuilding.objects.get(id=id).delete()
        except:
            raise GraphQLError(f"'Symbuilding' mit ID {id} Nicht vorhanden")

        return id



class Mutation(graphene.ObjectType):
    create_symbuilding = CreateSymbuilding.Field()
    update_symbuilding = UpdateSymbuilding.Field()
    delete_symbuilding = DeleteSymbuilding.Field()