import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.db.models import Q
from ..graphql_jwt.decorators import login_required

from ..models import Tour, Employee, Product, Vehicle
from .employee import EmployeeType
from .vehicle import VehicleType

from users.schema import UserType

from ..utils import Filter


class TourType(DjangoObjectType):
    class Meta:
        model = Tour

class Query(graphene.ObjectType):
    tours = graphene.List(
        TourType,
        search=graphene.String(description='FUZZY SEARCH'),
        tour_number=graphene.Int(),
        employee_id=graphene.Int(),
        vehicle_id=graphene.Int(),
        )

    @login_required
    def resolve_tours(self, info, **kwargs):

        queryset = Tour.objects.all()

        if kwargs:
                
            fuzzy_search_fields = ['employee_id', 'vehicle_id', 'tour_number']

            queryset = Filter(queryset, kwargs, None, fuzzy_search_fields)()

        return queryset


class CreateTour(graphene.Mutation):
    id = graphene.Int()
    tour_number=graphene.Int(),
    employee = graphene.Field(EmployeeType)
    vehicle =graphene.Field(VehicleType)

    class Arguments:
        tour_number = graphene.Int()
        employee_id = graphene.Int()
        vehicle_id=graphene.Int()

    def mutate(self, info, employee_id, vehicle_id,
        tour_number):
        

        employee = Employee.objects.filter(id=employee_id).first()
        if not employee:
            raise GraphQLError("Ungültige Mitarbeiter ID")

        vehicle = Vehicle.objects.filter(id=vehicle_id).first()
        if not vehicle:
            raise GraphQLError("Ungültige Fahrzeug ID")

        user = info.context.user or None

        tour = Tour(
            employee_id=employee_id,
            vehicle_id=vehicle_id, tour_number=tour_number,
             created_by=user)

        tour.save()

        return tour

class UpdateTour(graphene.Mutation):
    id = graphene.Int()
    employee = graphene.Field(EmployeeType)
    vehicle=graphene.Field(VehicleType)
    tour_number = graphene.Int()

    class Arguments:
        id = graphene.Int()
        employee_id = graphene.Int()
        vehicle_id=graphene.Int()
        tour_number = graphene.Int()

    def mutate(self, info, id=None, **kwargs):

        if 'employee_id' in kwargs:
                
            employee = Employee.objects.filter(id=kwargs['employee_id']).first()
            if kwargs['employee_id'] and not employee:
                raise GraphQLError("Ungültige Abteilungs ID")

        if 'vehicle_id' in kwargs:
                
            vehicle = Vehicle.objects.filter(id=kwargs['vehicle_id']).first()
            if kwargs['vehicle_id'] and not vehicle:
                raise GraphQLError("Ungültige Lager ID")
        
        try:
            tour = Tour.objects.get(id=id)
        except:
            raise GraphQLError(f"'Tour' mit ID {id} Nicht vorhanden")

        for key, val in kwargs.items():
            setattr(tour, key, val)

        tour.save()

        return tour


class DeleteTour(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id =graphene.Int()

    def mutate(self, info, id=None, **args):

        try:
            Tour.objects.get(id=id).delete()
        except:
            raise GraphQLError(f"'Produkt' mit ID {id} Nicht vorhanden")

        return id



class Mutation(graphene.ObjectType):
    create_tour = CreateTour.Field()
    update_tour = UpdateTour.Field()
    delete_tour = DeleteTour.Field()