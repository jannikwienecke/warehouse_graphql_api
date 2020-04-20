import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.db.models import Q
from ..graphql_jwt.decorators import login_required
# from graphql_jwt.decorators import login_required

from ..models import Compartment, Warehouse
from .warehouse import WarehouseType
from users.schema import UserType

from ..utils import Filter


class CompartmentType(DjangoObjectType):
    class Meta:
        model = Compartment

class Query(graphene.ObjectType):
    compartments = graphene.List(
        CompartmentType,
        search=graphene.String(description='FUZZY SEARCH'),
        name=graphene.String(),
        warehouse_id=graphene.Int(),
        width = graphene.Int(),
        height = graphene.Int(),
        position_top = graphene.Int(),
        position_left = graphene.Int(),
        real_position = graphene.String(),
        direction = graphene.String(),
        color = graphene.String(),
        )

    @login_required
    def resolve_compartments(self, info, **kwargs):

        queryset = Compartment.objects.all()

        if kwargs:
                
            fuzzy_search_fields = ['name', 'direction',
                ]

            queryset = Filter(queryset, kwargs, None, fuzzy_search_fields)()

        return queryset


class CreateCompartment(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    warehouse = graphene.Field(WarehouseType)
    width = graphene.Int()
    height = graphene.Int()
    position_top = graphene.Int()
    position_left = graphene.Int()
    real_position = graphene.String()
    direction = graphene.String()
    color = graphene.String()

    class Arguments:
        name = graphene.String()
        warehouse_id = graphene.Int()
        width = graphene.Int()
        height = graphene.Int()
        position_top = graphene.Int()
        position_left = graphene.Int()
        real_position = graphene.String()
        direction = graphene.String()
        color = graphene.String()


    def mutate(self, info, name, warehouse_id, width, height,
        position_top, position_left, real_position, direction, color='#ddd'):
        
        warehouse = Warehouse.objects.filter(id=warehouse_id).first()
        if not warehouse:
            raise GraphQLError("Ungültige Verpackungs-ID")

        user = info.context.user or None

        compartment = Compartment(
            name=name, warehouse_id=warehouse_id, direction=direction,
            width=width, height=height, real_position=real_position,
            position_left=position_left, position_top= position_top,
            color=color, created_by=user)

        compartment.save()

        return compartment

class UpdateCompartment(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    warehouse = graphene.Field(WarehouseType)
    width = graphene.Int()
    height = graphene.Int()
    position_top = graphene.Int()
    position_left = graphene.Int()
    real_position = graphene.String()
    direction = graphene.String()
    color = graphene.String()

    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        warehouse_id = graphene.Int()
        width = graphene.Int()
        height = graphene.Int()
        position_top = graphene.Int()
        position_left = graphene.Int()
        real_position = graphene.String()
        direction = graphene.String()
        color = graphene.String()

    def mutate(self, info, id=None, **kwargs):

        if 'warehouse_id' in kwargs:
            warehouse = Warehouse.objects.filter(id=kwargs['warehouse_id']).first()
            if not warehouse:
                raise GraphQLError("Ungültige Lager-ID")
        
        try:
            compartment = Compartment.objects.get(id=id)
        except:
            raise GraphQLError(f"'Warehouse' mit ID {id} Nicht vorhanden")

        for key, val in kwargs.items():
            print(key)
            print(val)
            print('------------')
            setattr(compartment, key, val)

        compartment.save()

        return compartment


class DeleteCompartment(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id =graphene.Int()

    def mutate(self, info, id=None, **args):

        try:
            print("ID = ", id)
            Compartment.objects.get(id=id).delete()
        except Exception as e:
            print("ERROR : ", e)
            raise GraphQLError(f"'Abteilung' mit ID {id} Nicht vorhanden")

        return id



class Mutation(graphene.ObjectType):
    create_compartment = CreateCompartment.Field()
    update_compartment = UpdateCompartment.Field()
    delete_compartment = DeleteCompartment.Field()