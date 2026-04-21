import json
import re
import graphene
from graphene_django import DjangoObjectType
from .models import Shop


def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    return re.match(r'^\d{7,15}$', phone) is not None


class ShopType(DjangoObjectType):
    email = graphene.List(graphene.String)
    phone = graphene.List(graphene.String)

    class Meta:
        model = Shop
        fields = ("id", "name", "email", "phone", "address", "created_at", "updated_at")

    def resolve_email(self, info):
        val = self.email
        if isinstance(val, str):
            return json.loads(val)
        return val or []

    def resolve_phone(self, info):
        val = self.phone
        if isinstance(val, str):
            return json.loads(val)
        return val or []


class Query(graphene.ObjectType):
    all_shops = graphene.List(
        ShopType,
        search=graphene.String(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )
    shop = graphene.Field(ShopType, id=graphene.Int(required=True))

    def resolve_all_shops(self, info, search=None, limit=None, offset=None):
        qs = Shop.objects.all()
        if search:
            qs = qs.filter(name__icontains=search) | qs.filter(address__icontains=search)
        if offset:
            qs = qs[offset:]
        if limit:
            qs = qs[:limit]
        return qs

    def resolve_shop(self, info, id):
        try:
            return Shop.objects.get(pk=id)
        except Shop.DoesNotExist:
            return None


class CreateShop(graphene.Mutation):
    shop = graphene.Field(ShopType)
    errors = graphene.List(graphene.String)

    class Arguments:
        name = graphene.String(required=True)
        email = graphene.List(graphene.String, required=True)
        phone = graphene.List(graphene.String, required=True)
        address = graphene.String(required=True)

    def mutate(self, info, name, email, phone, address):
        errors = []
        if not name.strip():
            errors.append("Name cannot be empty.")
        for e in email:
            if not validate_email(e):
                errors.append(f"Invalid email: {e}")
        for p in phone:
            if not validate_phone(p):
                errors.append(f"Invalid phone (digits only, 7-15 chars): {p}")
        if errors:
            return CreateShop(shop=None, errors=errors)
        shop = Shop.objects.create(name=name, email=email, phone=phone, address=address)
        return CreateShop(shop=shop, errors=[])


class UpdateShop(graphene.Mutation):
    shop = graphene.Field(ShopType)
    errors = graphene.List(graphene.String)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        email = graphene.List(graphene.String)
        phone = graphene.List(graphene.String)
        address = graphene.String()

    def mutate(self, info, id, name=None, email=None, phone=None, address=None):
        errors = []
        try:
            shop = Shop.objects.get(pk=id)
        except Shop.DoesNotExist:
            raise Exception(f"Shop with id {id} does not exist.")
        if email:
            for e in email:
                if not validate_email(e):
                    errors.append(f"Invalid email: {e}")
        if phone:
            for p in phone:
                if not validate_phone(p):
                    errors.append(f"Invalid phone: {p}")
        if errors:
            return UpdateShop(shop=None, errors=errors)
        if name is not None:
            shop.name = name
        if email is not None:
            shop.email = email
        if phone is not None:
            shop.phone = phone
        if address is not None:
            shop.address = address
        shop.save()
        return UpdateShop(shop=shop, errors=[])


class DeleteShop(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        try:
            Shop.objects.get(pk=id).delete()
            return DeleteShop(success=True, message=f"Shop with id {id} deleted successfully.")
        except Shop.DoesNotExist:
            return DeleteShop(success=False, message=f"Shop with id {id} does not exist.")


class Mutation(graphene.ObjectType):
    create_shop = CreateShop.Field()
    update_shop = UpdateShop.Field()
    delete_shop = DeleteShop.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)