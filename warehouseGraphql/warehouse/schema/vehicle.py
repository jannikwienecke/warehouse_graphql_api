import graphene

from graphene_django import DjangoObjectType
from graphql import GraphQLError

from django.db.models import Q
from ..graphql_jwt.decorators import login_required

from ..models import Vehicle
from ..utils import Filter
from users.schema import UserType


class VehicleType(DjangoObjectType):
    class Meta:
        model = Vehicle


class Query(graphene.ObjectType):
    vehicles = graphene.List(
        VehicleType,
        search=graphene.String(description='FUZZY SEARCH'),
        id=graphene.Int(),
        name=graphene.String(),
        width=graphene.Int(),
        length=graphene.Int(),
        length_loading=graphene.Int(),
    )

    def resolve_vehicles(self, info, **kwargs):

        queryset = Vehicle.objects.all()

        if kwargs:

            fuzzy_search_fields = ['name']
            queryset = Filter(queryset, kwargs, None, fuzzy_search_fields)()

        return queryset


class CreateVehicle(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    width = graphene.Int()
    length = graphene.Int()
    length_loading = graphene.Int()

    class Arguments:
        name = graphene.String()
        width = graphene.Int()
        length = graphene.Int()
        length_loading = graphene.Int()

    @login_required
    def mutate(self, info, name, width, length, length_loading):

        user = info.context.user or None

        vehicle = Vehicle(name=name, width=width, length_loading=length_loading,
                          length=length, created_by=user)
        vehicle.save()

        return vehicle


class UpdateVehicle(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    width = graphene.Int()
    length = graphene.Int()
    length_loading = graphene.Int()

    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        width = graphene.Int()
        length = graphene.Int()
        length_loading = graphene.Int()

    def mutate(self, info, id=None, **args):

        user = info.context.user or None

        try:
            vehicle = Vehicle.objects.get(id=id)
        except Exception as e:
            print("Err", e)
            raise GraphQLError(f"'Vehicle' mit ID {id} Nicht vorhanden", e)

        for key, val in args.items():
            setattr(vehicle, key, val)

        vehicle.save()

        return vehicle


class DeleteVehicle(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id=None, **args):

        try:
            Vehicle.objects.get(id=id).delete()
        except:
            raise GraphQLError(f"'Vehicle' mit ID {id} Nicht vorhanden")

        return id


class Mutation(graphene.ObjectType):
    create_vehicle = CreateVehicle.Field()
    update_vehicle = UpdateVehicle.Field()
    delete_vehicle = DeleteVehicle.Field()
