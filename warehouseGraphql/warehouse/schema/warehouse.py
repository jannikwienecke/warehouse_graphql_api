import graphene

from graphene_django import DjangoObjectType
from graphql import GraphQLError

from django.db.models import Q
from ..graphql_jwt.decorators import login_required

from ..models import Warehouse
from ..utils import Filter
from users.schema import UserType


class WarehouseType(DjangoObjectType):
    class Meta:
        model = Warehouse

class Query(graphene.ObjectType):
    warehouses = graphene.List(
        WarehouseType,
        search=graphene.String(description='FUZZY SEARCH'),
        id=graphene.Int(),
        name=graphene.String(),
        )

    def resolve_warehouses(self, info, **kwargs):

        queryset = Warehouse.objects.all()

        if kwargs:
                
            fuzzy_search_fields = ['name']
            queryset = Filter(queryset, kwargs, None, fuzzy_search_fields)()
                    
        return queryset


class CreateWarehouse(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()

    class Arguments:
        name = graphene.String()

    @login_required
    def mutate(self, info, name):

        user = info.context.user or Non
        
        warehouse = Warehouse(name=name, created_by=user)
        warehouse.save()

        return warehouse

class UpdateWarehouse(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    created_by = graphene.Field(UserType)
    
    class Arguments:
        id = graphene.Int()
        name = graphene.String()

    def mutate(self, info, id=None, **args):

        user = info.context.user or Non

        try:
            warehouse = Warehouse.objects.get(id=id)
        except:
            raise GraphQLError(f"'Warehouse' mit ID {id} Nicht vorhanden")

        for key, val in args.items():
            setattr(warehouse, key, val)

        warehouse.save()

        return warehouse

class DeleteWarehouse(graphene.Mutation):
    id = graphene.Int()
    created_by = graphene.Field(UserType)

    class Arguments:
        id =graphene.Int()

    def mutate(self, info, id=None, **args):

        try:
            Warehouse.objects.get(id=id).delete()
        except:
            raise GraphQLError(f"'Warehouse' mit ID {id} Nicht vorhanden")

        return id



class Mutation(graphene.ObjectType):
    create_warehouse = CreateWarehouse.Field()
    update_warehouse = UpdateWarehouse.Field()
    delete_warehouse = DeleteWarehouse.Field()