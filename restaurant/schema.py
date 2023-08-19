from graphene_django import DjangoObjectType
from .models import Restaurant

class RestaurantType(DjangoObjectType):
  class Meta:
    model = Restaurant
    fields = ("id", "name", "address")


