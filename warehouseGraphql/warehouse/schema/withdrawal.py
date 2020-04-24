from datetime import datetime

import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from ..graphql_jwt.decorators import login_required

from ..models import Withdrawal, Employee, Product, Customer, Row, Tour
from .employee import EmployeeType
from .customer import CustomerType
from .product import ProductType
from .row import RowType
from .tour import TourType

from ..utils import Filter


class WithdrawalType(DjangoObjectType):
    class Meta:
        model = Withdrawal


class Query(graphene.ObjectType):
    withdrawals = graphene.List(
        WithdrawalType,
        id=graphene.Int(),
        name=graphene.String(
            description="Date + Number Withdrawal of this day"),
        search=graphene.String(description='FUZZY SEARCH'),
        row_id=graphene.Int(),
        quantity=graphene.Int(),
        employee_id=graphene.Int(),
        customer_id=graphene.Int(),
        product_id=graphene.Int(),
        tour_id=graphene.Int(),
        is_open=graphene.Boolean(),
        notes=graphene.String(),
    )

    # @login_required
    def resolve_withdrawals(self, info, **kwargs):

        queryset = Withdrawal.objects.all()

        if kwargs:

            fuzzy_search_fields = [
                'employee_id', 'customer_id', 'product_id', 'tour_id',
                'row_id', 'notes']

            queryset = Filter(queryset, kwargs, None, fuzzy_search_fields)()

        return queryset


class CreateWithdrawal(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    quantity = graphene.Int()
    employee = graphene.Field(EmployeeType)
    customer = graphene.Field(CustomerType)
    product = graphene.Field(ProductType)
    row = graphene.Field(RowType)
    tour = graphene.Field(TourType)
    notes = graphene.String()
    is_open = graphene.Boolean()
    created_at = graphene.DateTime()

    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        quantity = graphene.Int()
        employee_id = graphene.Int()
        customer_id = graphene.Int()
        product_id = graphene.Int()
        tour_id = graphene.Int()
        row_id = graphene.Int()
        is_open = graphene.Boolean()
        notes = graphene.String()

    def mutate(self, info, employee_id, customer_id, quantity,
               product_id, tour_id, row_id, notes='', name='', is_open=True):

        row = Row.objects.filter(id=row_id).first()
        if not row:
            raise GraphQLError("Ungültige Reihen ID")

        tour = Tour.objects.filter(id=tour_id).first()
        if not tour:
            raise GraphQLError("Ungültige Tour ID")

        product = Product.objects.filter(id=product_id).first()
        if not product:
            raise GraphQLError("Ungültige Mitarbeiter ID")

        employee = Employee.objects.filter(id=employee_id).first()
        if not employee:
            raise GraphQLError("Ungültige Mitarbeiter ID")

        customer = Customer.objects.filter(id=customer_id).first()
        if not customer:
            raise GraphQLError("Ungültige Fahrzeug ID")

        user = info.context.user or None

        today = datetime.now().date()
        withdrawal_today = Withdrawal.objects.filter(
            created_at__year=today.year, created_at__month=today.month,
            created_at__day=today.day,
        )

        number_withdrawal_today = len(withdrawal_today) + 1

        name = str(today).replace('-', '_') + "_auslagerung_" + \
            str(number_withdrawal_today)

        withdrawal = Withdrawal(
            employee_id=employee_id, product_id=product_id, tour_id=tour_id,
            customer_id=customer_id, row_id=row_id,
            created_by=user, notes=notes, quantity=quantity,
            name=name, is_open=is_open)

        withdrawal.save()

        return withdrawal


class UpdateWithdrawal(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    quantity = graphene.Int()
    employee = graphene.Field(EmployeeType)
    customer = graphene.Field(CustomerType)
    product = graphene.Field(ProductType)
    row = graphene.Field(RowType)
    tour = graphene.Field(TourType)
    notes = graphene.String()
    is_open = graphene.Boolean()
    created_at = graphene.DateTime()

    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        quantity = graphene.Int()
        employee_id = graphene.Int()
        customer_id = graphene.Int()
        product_id = graphene.Int()
        tour_id = graphene.Int()
        row_id = graphene.Int()
        is_open = graphene.Boolean()
        notes = graphene.String()

    def mutate(self, info, id=None, **kwargs):

        if 'quantity' in kwargs and kwargs['quantity'] == 0:
            raise GraphQLError("fieldValidation: 'quantity' muss > 0 sein")

        if 'product_id' in kwargs:

            product = Product.objects.filter(id=kwargs['product_id']).first()
            if kwargs['product_id'] and not product:
                raise GraphQLError("Ungültige Produkt ID")

        if 'tour_id' in kwargs:

            tour = Tour.objects.filter(id=kwargs['tour_id']).first()
            if kwargs['tour_id'] and not tour:
                raise GraphQLError("Ungültige Tour ID")

        if 'row_id' in kwargs:

            row = Row.objects.filter(id=kwargs['row_id']).first()
            if kwargs['row_id'] and not row:
                raise GraphQLError("Ungültige Row ID")

        if 'employee_id' in kwargs:

            employee = Employee.objects.filter(
                id=kwargs['employee_id']).first()
            if kwargs['employee_id'] and not employee:
                raise GraphQLError("Ungültige Mitarbeiter ID")

        if 'customer_id' in kwargs:

            customer = Customer.objects.filter(
                id=kwargs['customer_id']).first()
            if kwargs['customer_id'] and not customer:
                raise GraphQLError("Ungültige Kunden ID")

        try:
            withdrawal = Withdrawal.objects.get(id=id)
        except:
            raise GraphQLError(f"'Withdrawal' mit ID {id} Nicht vorhanden")

        if 'row_id' in kwargs:
            _updateStockRow(id, kwargs)

        for key, val in kwargs.items():
            setattr(withdrawal, key, val)

        withdrawal.save()

        return withdrawal


def _updateStockRow(id, kwargs):

    def _removeQuantityFromOldRow():
        row = Row.objects.get(id=withdrawal['row_id'])
        stock = getattr(row, 'stock')
        setattr(row, 'stock', stock + withdrawal['quantity'])
        row.save()

    def _addQuantityToNewRow():
        row = Row.objects.get(id=kwargs['row_id'])
        stock_before = getattr(row, 'stock')
        stock = stock_before - quantity if stock_before >= quantity else 0
        setattr(row, 'stock', stock)
        row.save()

    quantity = kwargs['quantity']
    withdrawal = Withdrawal.objects.filter(id=id).values()[0]

    if withdrawal['row_id'] is kwargs['row_id']:
        return

    _removeQuantityFromOldRow()
    _addQuantityToNewRow()


class DeleteWithdrawal(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id=None, **args):

        print(Withdrawal.objects.all().values())
        try:
            withdrawal = Withdrawal.objects.get(id=id)
            print(withdrawal)
            withdrawal.delete()

        except Exception as e:
            print('error', e)
            raise GraphQLError(f"'Produkt' mit ID {id} Nicht vorhanden", e)

        return id


class Mutation(graphene.ObjectType):
    create_withdrawal = CreateWithdrawal.Field()
    update_withdrawal = UpdateWithdrawal.Field()
    delete_withdrawal = DeleteWithdrawal.Field()
