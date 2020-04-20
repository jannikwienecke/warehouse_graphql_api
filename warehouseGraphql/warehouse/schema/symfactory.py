import graphene

from graphene_django import DjangoObjectType
from graphql import GraphQLError

from django.db.models import Q
from ..graphql_jwt.decorators import login_required

from ..models import Symfactory, Employee
from ..utils import Filter
from users.schema import UserType


# class EmployeeType(DjangoObjectType):
#     class Meta:
#         model = Employee

# class Query(graphene.ObjectType):
#     employees = graphene.List(
#         EmployeeType,
#         search=graphene.String(description='FUZZY SEARCH'),
#         id=graphene.Int(),
#         name=graphene.String(),
#         )

#     def resolve_employees(self, info, **kwargs):

#         queryset = Employee.objects.all()

#         if kwargs:
                
#             fuzzy_search_fields = ['name']
#             queryset = Filter(queryset, kwargs, None, fuzzy_search_fields)()
                    
#         return queryset


class SymfactoryType(DjangoObjectType):
    class Meta:
        model = Symfactory

class Query(graphene.ObjectType):
    symfactories = graphene.List(
        SymfactoryType,
        search=graphene.String(description='FUZZY SEARCH'),
        id=graphene.Int(),
        name=graphene.String(),
        )

    def resolve_symfactories(self, info, **kwargs):

        queryset = Symfactory.objects.all()

        if kwargs:
                
            fuzzy_search_fields = ['name']
            queryset = Filter(queryset, kwargs, None, fuzzy_search_fields)()
                    
        return queryset


class CreateSymfactory(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()

    class Arguments:
        name = graphene.String()

    @login_required
    def mutate(self, info, name):

        user = info.context.user or Non
        
        symfactory = Symfactory(name=name, created_by=user)
        symfactory.save()

        return symfactory

class UpdateSymfactory(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    created_by = graphene.Field(UserType)
    
    class Arguments:
        id = graphene.Int()
        name = graphene.String()

    def mutate(self, info, id=None, **args):

        user = info.context.user or Non

        try:
            symfactory = Symfactory.objects.get(id=id)
        except:
            raise GraphQLError(f"'Symfactory' mit ID {id} Nicht vorhanden")

        for key, val in args.items():
            setattr(symfactory, key, val)

        symfactory.save()

        return symfactory

class DeleteSymfactory(graphene.Mutation):
    id = graphene.Int()
    created_by = graphene.Field(UserType)

    class Arguments:
        id =graphene.Int()

    def mutate(self, info, id=None, **args):

        try:
            Symfactory.objects.get(id=id).delete()
        except:
            raise GraphQLError(f"'Symfactory' mit ID {id} Nicht vorhanden")

        return id



class Mutation(graphene.ObjectType):
    create_symfactory = CreateSymfactory.Field()
    update_symfactory = UpdateSymfactory.Field()
    delete_symfactory = DeleteSymfactory.Field()