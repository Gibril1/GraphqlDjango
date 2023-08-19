import graphene
from .schema import RestaurantType
from .models import Restaurant

class Query(graphene.ObjectType):
  """
  Queries for the Restaurant model
  """
  restaurants = graphene.List(RestaurantType)
  get_restaurant = graphene.Field(RestaurantType, id=graphene.String())


  def resolve_restaurants(self, info, **kwargs):
    if not info.context.user.is_authenticated:
            return Restaurant.objects.none()
    return Restaurant.objects.all()
  
  def resolve_get_restaurant(self, info, id):
    return Restaurant.objects.get(id=id)

class DeleteRestaurant(graphene.Mutation):
  class Arguments:
    id = graphene.Int()

  ok = graphene.Boolean()

  def mutate(self, info, id):
    restaurant = Restaurant.objects.get(id=id)
    restaurant.delete()
    return DeleteRestaurant(ok=True)

class UpdateRestaurant(graphene.Mutation):
  class Arguments:
    id = graphene.Int()
    name = graphene.String()
    address = graphene.String()

  ok = graphene.Boolean()
  restaurant = graphene.Field(RestaurantType)

  def mutate(self, info, id, name, address):
    restaurant = Restaurant.objects.get(id=id)
    restaurant.name = name
    restaurant.address = address
    restaurant.save()
    return UpdateRestaurant(ok=True, restaurant=restaurant)

class CreateRestaurant(graphene.Mutation):
  class Arguments:
    name = graphene.String()
    address = graphene.String()

  ok = graphene.Boolean() 
  restaurant = graphene.Field(RestaurantType)

  def mutate(self, info, name, address):
    restaurant = Restaurant(name=name, address=address)
    restaurant.save()
    return CreateRestaurant(ok=True, restaurant=restaurant)

class Mutation(graphene.ObjectType):
  create_restaurant = CreateRestaurant.Field()
  delete_restaurant = DeleteRestaurant.Field()
  update_restaurant = UpdateRestaurant.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

