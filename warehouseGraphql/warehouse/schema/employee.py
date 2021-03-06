import graphene

from graphene_django import DjangoObjectType
from graphql import GraphQLError

from ..graphql_jwt.decorators import login_required

from ..models import Employee
from ..utils import Filter
from users.schema import UserType


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

        user = info.context.user or None

        employee = Employee(name=name, created_by=user)
        employee.save()

        return employee


class UpdateEmployee(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    created_by = graphene.Field(UserType)

    class Arguments:
        id = graphene.Int()
        name = graphene.String()

    def mutate(self, info, id=None, **args):

        try:
            employee = Employee.objects.get(id=id)
        except:
            raise GraphQLError(f"'Employee' mit ID {id} Nicht vorhanden")

        for key, val in args.items():
            setattr(employee, key, val)

        employee.save()

        return employee


class DeleteEmployee(graphene.Mutation):
    id = graphene.Int()
    created_by = graphene.Field(UserType)

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id=None, **args):

        try:
            Employee.objects.get(id=id).delete()
        except:
            raise GraphQLError(f"'Employee' mit ID {id} Nicht vorhanden")

        return id


class Mutation(graphene.ObjectType):
    create_employee = CreateEmployee.Field()
    update_employee = UpdateEmployee.Field()
    delete_employee = DeleteEmployee.Field()
