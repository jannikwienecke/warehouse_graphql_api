import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from ..graphql_jwt.decorators import login_required

from ..models import Row, Compartment, Product, Warehouse
from .compartment import CompartmentType
from .warehouse import WarehouseType
from .product import ProductType


from ..utils import Filter


class RowType(DjangoObjectType):
    class Meta:
        model = Row


class Query(graphene.ObjectType):
    rows = graphene.List(
        RowType,
        search=graphene.String(description='FUZZY SEARCH'),
        name=graphene.String(),
        compartment_id=graphene.Int(),
        product_id=graphene.Int(),
        warehouse_id=graphene.Int(),
        total_stock_positions=graphene.Int(),
        stock=graphene.Int(),
        current_stock_positions=graphene.Int(),
    )

    @login_required
    def resolve_rows(self, info, **kwargs):

        queryset = Row.objects.all()

        if kwargs:

            fuzzy_search_fields = ['name']

            queryset = Filter(queryset, kwargs, None, fuzzy_search_fields)()

        return queryset


class CreateRow(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    total_stock_positions = graphene.Int()
    stock = graphene.Int()
    current_stock_positions = graphene.Int()
    compartment = graphene.Field(CompartmentType)
    product = graphene.Field(ProductType)
    warehouse = graphene.Field(WarehouseType)

    class Arguments:
        name = graphene.String()
        total_stock_positions = graphene.Int()
        stock = graphene.Int()
        current_stock_positions = graphene.Int()
        compartment_id = graphene.Int()
        product_id = graphene.Int()
        warehouse_id = graphene.Int()

    def mutate(self, info, name, compartment_id, warehouse_id,
               total_stock_positions, current_stock_positions=0,
               product_id=None, stock=0):

        compartment = Compartment.objects.filter(id=compartment_id).first()
        if not compartment:
            raise GraphQLError("Ungültige Abteilungs ID")

        product = Product.objects.filter(id=product_id).first()
        if product_id and not product:
            raise GraphQLError("Ungültige Produkt ID")

        warehouse = Warehouse.objects.filter(id=warehouse_id).first()
        if not warehouse:
            raise GraphQLError("Ungültige Lager ID")

        user = info.context.user or None

        row = Row(
            name=name, total_stock_positions=total_stock_positions,
            compartment_id=compartment_id, product_id=product_id,
            warehouse_id=warehouse_id, created_by=user)

        row.save()

        return row


class UpdateRow(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    total_stock_positions = graphene.Int()
    stock = graphene.Int()
    current_stock_positions = graphene.Int()
    compartment = graphene.Field(CompartmentType)
    product = graphene.Field(ProductType)
    warehouse = graphene.Field(WarehouseType)

    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        total_stock_positions = graphene.Int()
        stock = graphene.Int()
        current_stock_positions = graphene.Int()
        compartment_id = graphene.Int()
        product_id = graphene.Int()
        warehouse_id = graphene.Int()

    def mutate(self, info, id=None, **kwargs):

        # if not ('compartment_id' in kwargs
        #     and 'warehouse_id' in kwargs):
        #     raise GraphQLError("ID Fehlt")

        if 'compartment_id' in kwargs:

            compartment = Compartment.objects.filter(
                id=kwargs['compartment_id']).first()
            if kwargs['compartment_id'] and not compartment:
                raise GraphQLError("Ungültige Abteilungs ID")

        if 'product_id' in kwargs:
            product = Product.objects.filter(id=kwargs['product_id']).first()
            if kwargs['product_id'] and not product:
                raise GraphQLError("Ungültige Produkt ID")

        if 'warehouse_id' in kwargs:

            warehouse = Warehouse.objects.filter(
                id=kwargs['warehouse_id']).first()
            if kwargs['warehouse_id'] and not warehouse:
                raise GraphQLError("Ungültige Lager ID")

        try:
            row = Row.objects.get(id=id)
        except:
            raise GraphQLError(f"'Row' mit ID {id} Nicht vorhanden")

        for key, val in kwargs.items():
            setattr(row, key, val)

        row.save()

        return row


class DeleteRow(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id=None, **args):

        try:
            Row.objects.get(id=id).delete()
        except:
            raise GraphQLError(f"'Produkt' mit ID {id} Nicht vorhanden")

        return id


class Mutation(graphene.ObjectType):
    create_row = CreateRow.Field()
    update_row = UpdateRow.Field()
    delete_row = DeleteRow.Field()
