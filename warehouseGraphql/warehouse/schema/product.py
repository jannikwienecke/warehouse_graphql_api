import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.db.models import Q
from ..graphql_jwt.decorators import login_required
# from graphql_jwt.decorators import login_required

from ..models import Product, Packaging
from .packaging import PackagingType
from users.schema import UserType

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
        id=graphene.Int(),
        notes_picking=graphene.String(),
        notes_putaway=graphene.String(),
        )

    @login_required
    def resolve_products(self, info, search=None, name=None, product_number=None,
        packaging_id=None, three_in_row=None, id=None, notes_picking=None,
        notes_putaway=None, **kwargs):

        queryset = Product.objects.all()

        if search:
            filter_search = (
                Q(name__icontains=search) |
                Q(product_number__icontains=search) | 
                Q(notes_picking__icontains=search) | 
                Q(notes_putaway__icontains=search) 
            )

            queryset = queryset.filter(filter_search)

        if id:
            filter_id = Q(id__icontains=id)
            queryset = queryset.filter(filter_id)         

        if name:
            filter_name = Q(name__icontains=name)
            queryset = queryset.filter(filter_name)

        if product_number:
            filter_product_number = Q(product_number__icontains=product_number)
            queryset = queryset.filter(filter_product_number)

        if notes_picking:
            filter_notes_picking = Q(notes_picking__icontains=notes_picking)
            queryset = queryset.filter(filter_notes_picking)

        if notes_putaway:
            filter_notes_putaway = Q(notes_putaway__icontains=notes_putaway)
            queryset = queryset.filter(filter_notes_putaway)

        if three_in_row is not None:
            filter_three_in_row = Q(three_in_row=three_in_row)
            queryset = queryset.filter(filter_three_in_row)

        if packaging_id:
            queryset = queryset.select_related('packaging').filter(
                packaging_id=packaging_id
            )

        return queryset


class CreateProduct(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    product_number = graphene.String()
    notes_picking = graphene.String()
    notes_putaway = graphene.String()
    three_in_row = graphene.Boolean()
    packaging = graphene.Field(PackagingType)
    created_by = graphene.Field(UserType)

    class Arguments:
        name = graphene.String()
        product_number = graphene.String()
        notes_picking = graphene.String()
        notes_putaway = graphene.String()
        three_in_row = graphene.Boolean()
        packaging_id = graphene.Int()

    def mutate(self, info, name, product_number, three_in_row, packaging_id,
        notes_picking=None, notes_putaway=None):
        
        packaging = Packaging.objects.filter(id=packaging_id).first()
        if not packaging:
            raise GraphQLError("Ungültige Verpackungs-ID")

        user = info.context.user or None

        product = Product(
            name=name, product_number=product_number,
            notes_picking=notes_picking, notes_putaway=notes_putaway,
            three_in_row=three_in_row, packaging_id=packaging_id,
            created_by=user)

        product.save()

        return CreateProduct(
            name=name, product_number=product.product_number,
            notes_picking=product.notes_picking, notes_putaway=product.notes_putaway,
            three_in_row=product.three_in_row, packaging=product.packaging,
            created_by=product.created_by)


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()