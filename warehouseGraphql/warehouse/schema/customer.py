import graphene

from graphene_django import DjangoObjectType
from graphql import GraphQLError

from django.db.models import Q
from ..graphql_jwt.decorators import login_required

from ..models import Customer
from ..utils import Filter
from users.schema import UserType


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class Query(graphene.ObjectType):
    customers = graphene.List(
        CustomerType,
        search=graphene.String(description='FUZZY SEARCH'),
        id=graphene.Int(),
        name=graphene.String(),
        customer_id=graphene.String()
        )

    def resolve_customers(self, info, **kwargs):

        queryset = Customer.objects.all()

        if kwargs:
                
            fuzzy_search_fields = ['name']
            queryset = Filter(queryset, kwargs, None, fuzzy_search_fields)()
                    
        return queryset


class CreateCustomer(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    customer_id=graphene.String()

    class Arguments:
        name = graphene.String()
        customer_id=graphene.String()

    @login_required
    def mutate(self, info, name, customer_id):

        user = info.context.user or Non
        if len(customer_id) is not 10:
            print('customer', customer_id)
            raise GraphQLError("Kunden ID muss 6 Stellig sein")

        exitsAlready = Customer.objects.filter(customer_id=customer_id)
        if exitsAlready:
            raise GraphQLError("Kunde mit der Kunden ID bereits vorhanden")

        customer = Customer(name=name, created_by=user, customer_id=customer_id.upper())
        customer.save()
        return customer

class UpdateCustomer(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    customer_id=graphene.String()
    
    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        customer_id=graphene.String()

    def mutate(self, info, id=None, **args):

        user = info.context.user or None

        print(args)
        customer_id = args.get('customer_id', None)
        print("CUSTOMEROD", customer_id)
        if customer_id and len(customer_id) is not 10:
            print(customer_id)
            # raise GraphQLError("Kunden ID muss 10 Stellig sein")

        try:
            customer = Customer.objects.get(id=id)
        except:
            raise GraphQLError(f"'Customer' mit ID {id} Nicht vorhanden")

        for key, val in args.items():
            setattr(customer, key, val)

        customer.save()

        return customer

class DeleteCustomer(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id =graphene.Int()

    def mutate(self, info, id=None, **args):

        try:
            Customer.objects.get(id=id).delete()
        except:
            raise GraphQLError(f"'Customer' mit ID {id} Nicht vorhanden")

        return id



class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    update_customer = UpdateCustomer.Field()
    delete_customer = DeleteCustomer.Field()