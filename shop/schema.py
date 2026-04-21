import graphene
from graphene_django import DjangoObjectType
from .models import Shop


# ──────────────────────────────────────────────
# GraphQL Type
# ──────────────────────────────────────────────

class ShopType(DjangoObjectType):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'email', 'phone', 'address', 'created_at', 'updated_at')

    # JSONField arrays exposed as List of String
    email = graphene.List(graphene.String)
    phone = graphene.List(graphene.String)

    def resolve_email(self, info):
        return self.email or []

    def resolve_phone(self, info):
        return self.phone or []


# ──────────────────────────────────────────────
# Queries
# ──────────────────────────────────────────────

class Query(graphene.ObjectType):
    all_shops = graphene.List(ShopType, description="Fetch all shops")
    shop = graphene.Field(
        ShopType,
        id=graphene.Int(required=True),
        description="Fetch a single shop by ID"
    )

    def resolve_all_shops(self, info):
        return Shop.objects.all()

    def resolve_shop(self, info, id):
        try:
            return Shop.objects.get(pk=id)
        except Shop.DoesNotExist:
            return None


# ──────────────────────────────────────────────
# Mutations
# ──────────────────────────────────────────────

class CreateShop(graphene.Mutation):
    """Create a new Shop"""
    class Arguments:
        name    = graphene.String(required=True)
        email   = graphene.List(graphene.String, required=True)
        phone   = graphene.List(graphene.String, required=True)
        address = graphene.String(required=True)

    shop    = graphene.Field(ShopType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, name, email, phone, address):
        shop = Shop.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address
        )
        return CreateShop(shop=shop, success=True, message="Shop created successfully.")


class UpdateShop(graphene.Mutation):
    """Update an existing Shop (partial updates supported)"""
    class Arguments:
        id      = graphene.Int(required=True)
        name    = graphene.String()
        email   = graphene.List(graphene.String)
        phone   = graphene.List(graphene.String)
        address = graphene.String()

    shop    = graphene.Field(ShopType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id, name=None, email=None, phone=None, address=None):
        try:
            shop = Shop.objects.get(pk=id)
        except Shop.DoesNotExist:
            return UpdateShop(shop=None, success=False, message=f"Shop with id {id} not found.")

        if name    is not None: shop.name    = name
        if email   is not None: shop.email   = email
        if phone   is not None: shop.phone   = phone
        if address is not None: shop.address = address
        shop.save()

        return UpdateShop(shop=shop, success=True, message="Shop updated successfully.")


class DeleteShop(graphene.Mutation):
    """Delete a Shop by ID"""
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            shop = Shop.objects.get(pk=id)
            shop.delete()
            return DeleteShop(success=True, message=f"Shop with id {id} deleted successfully.")
        except Shop.DoesNotExist:
            return DeleteShop(success=False, message=f"Shop with id {id} not found.")


class Mutation(graphene.ObjectType):
    create_shop = CreateShop.Field()
    update_shop = UpdateShop.Field()
    delete_shop = DeleteShop.Field()
