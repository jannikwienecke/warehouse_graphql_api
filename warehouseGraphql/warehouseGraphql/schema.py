import graphene
import graphql_jwt

import users.schema
from warehouse.schema import (
    product, packaging, employee, warehouse, compartment,
    customer, symbuilding, symfactory, row, vehicle,
    tour, withdrawal,
)

# class Query(product.Query,  employee.Query, users.schema.Query, graphene.ObjectType):
#     pass

class Query(
    product.Query, customer.Query, symfactory.Query, row.Query,
    symbuilding.Query, warehouse.Query, compartment.Query,
    packaging.Query, employee.Query, users.schema.Query,
    vehicle.Query, tour.Query, withdrawal.Query,
    graphene.ObjectType):
    pass

class Mutation(
    users.schema.Mutation,
    product.Mutation,
    packaging.Mutation,
    employee.Mutation,
    vehicle.Mutation,
    customer.Mutation,
    symfactory.Mutation,
    symbuilding.Mutation,
    warehouse.Mutation,
    compartment.Mutation,
    row.Mutation,
    tour.Mutation,
    withdrawal.Mutation,
    graphene.ObjectType,
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)