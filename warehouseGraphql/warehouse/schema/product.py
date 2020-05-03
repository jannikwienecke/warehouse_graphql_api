import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from ..graphql_jwt.decorators import login_required
# from graphql_jwt.decorators import login_required

from ..models import Product, Packaging
from .packaging import PackagingType
from users.schema import UserType

from ..utils import Filter


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class Query(graphene.ObjectType):
    products = graphene.List(
        ProductType,
        search=graphene.String(description='FUZZY SEARCH'),
        name=graphene.String(),
        product_number=graphene.String(),
        packaging_id=graphene.Int(),
        three_in_row=graphene.Boolean(),
        quantity_unit=graphene.Int(),
        units_per_truck_space=graphene.Int(),
        units_per_storage_space=graphene.Int(),
        id=graphene.Int(),
        notes_picking=graphene.String(),
        notes_putaway=graphene.String(),
    )

    @login_required
    def resolve_products(self, info, **kwargs):

        queryset = Product.objects.all()

        if kwargs:

            fuzzy_search_fields = ['name', 'product_number', 'notes_picking',
                                   'notes_putaway']

            queryset = Filter(queryset, kwargs, None, fuzzy_search_fields)()

        return queryset


class CreateProduct(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    product_number = graphene.String()
    notes_picking = graphene.String()
    notes_putaway = graphene.String()
    three_in_row = graphene.Boolean()
    quantity_unit = graphene.Int()
    units_per_truck_space = graphene.Int()
    units_per_storage_space = graphene.Int()
    packaging = graphene.Field(PackagingType)
    created_by = graphene.Field(UserType)
    created_at = graphene.DateTime()

    class Arguments:
        name = graphene.String()
        product_number = graphene.String()
        notes_picking = graphene.String()
        notes_putaway = graphene.String()
        three_in_row = graphene.Boolean()
        quantity_unit = graphene.Int()
        units_per_truck_space = graphene.Int()
        units_per_storage_space = graphene.Int()
        packaging_id = graphene.Int()

    def mutate(self, info, name, product_number, three_in_row, packaging_id,
               quantity_unit, units_per_truck_space,
               units_per_storage_space, notes_picking=None,
               notes_putaway=None):

        packaging = Packaging.objects.filter(id=packaging_id).first()
        if not packaging:
            raise GraphQLError("Ungültige Verpackungs-ID")

        user = info.context.user or None

        product = Product(
            name=name, product_number=product_number,
            quantity_unit=quantity_unit,
            units_per_storage_space=units_per_storage_space,
            units_per_truck_space=units_per_truck_space,
            notes_picking=notes_picking,
            notes_putaway=notes_putaway, three_in_row=three_in_row,
            packaging_id=packaging_id, created_by=user)

        product.save()

        return product


class UpdateProduct(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    product_number = graphene.String()
    notes_picking = graphene.String()
    notes_putaway = graphene.String()
    three_in_row = graphene.Boolean()
    quantity_unit = graphene.Int()
    units_per_truck_space = graphene.Int()
    units_per_storage_space = graphene.Int()
    packaging = graphene.Field(PackagingType)
    created_by = graphene.Field(UserType)
    created_at = graphene.DateTime()

    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        product_number = graphene.String()
        notes_picking = graphene.String()
        notes_putaway = graphene.String()
        three_in_row = graphene.Boolean()
        packaging_id = graphene.Int()
        quantity_unit = graphene.Int()
        units_per_truck_space = graphene.Int()
        units_per_storage_space = graphene.Int()

    def mutate(self, info, id=None, **kwargs):
        if 'packaging_id' in kwargs:
            packaging = Packaging.objects.filter(
                id=kwargs['packaging_id']).first()
            if not packaging:
                raise GraphQLError("Ungültige Verpackungs-ID")

        try:
            product = Product.objects.get(id=id)
        except Exception as e:
            print('Error=', e)
            raise GraphQLError(f"'Product' mit ID {id} Nicht vorhanden", e)

        for key, val in kwargs.items():
            setattr(product, key, val)

        product.save()

        return product


class DeleteProduct(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id=None, **args):

        try:
            Product.objects.get(id=id).delete()
        except Exception as e:
            raise GraphQLError(f"'Produkt' mit ID {id} Nicht vorhanden", e)

        return id


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()
