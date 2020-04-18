import graphene

from graphene_django import DjangoObjectType
from graphql import GraphQLError

from django.db.models import Q
from ..graphql_jwt.decorators import login_required

from ..models import Employee
from ..utils import Filter

class EmployeeType(DjangoObjectType):
    class Meta:
        model = Employee

class Query(graphene.ObjectType):
    employees = graphene.List(
        EmployeeType,
        search=graphene.String(description='FUZZY SEARCH'),
        id=graphene.Int(),
        name=graphene.String(),
        )

    def resolve_employees(self, info, **kwargs):

        queryset = Employee.objects.all()

        if kwargs:
                
            fuzzy_search_fields = ['name']
            queryset = Filter(queryset, kwargs, None, fuzzy_search_fields)()
                    
        return queryset


class CreateEmployee(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()

    class Arguments:
        name = graphene.String()

    @login_required
    def mutate(self, info, name):

        user = info.context.user or Non
        
        employee = Employee(name=name, created_by=user)
        employee.save()

        return employee

# class UpdatePackaging(graphene.Mutation):
#     id = graphene.Int()
#     name = graphene.String()
#     width = graphene.Int()
#     length = graphene.Int()
    

#     class Arguments:
#         id =graphene.Int()
#         name = graphene.String()
#         width = graphene.Int()
#         length = graphene.Int()

#     def mutate(self, info, id=None, **args):

#         user = info.context.user or Non

#         try:
#             packaging = Packaging.objects.get(id=id)
#         except:
#             raise GraphQLError(f"'Packaging' mit ID {id} Nicht vorhanden")

#         for key, val in args.items():
#             setattr(packaging, key, val)

#         packaging.save()

#         return packaging

# class DeletePackaging(graphene.Mutation):
#     id = graphene.Int()

#     class Arguments:
#         id =graphene.Int()

#     def mutate(self, info, id=None, **args):

#         try:
#             Packaging.objects.get(id=id).delete()
#         except:
#             raise GraphQLError(f"'Packaging' mit ID {id} Nicht vorhanden")

#         return id



class Mutation(graphene.ObjectType):
    create_employee = CreateEmployee.Field()
#     update_packaging = UpdatePackaging.Field()
#     delete_packaging = DeletePackaging.Field()