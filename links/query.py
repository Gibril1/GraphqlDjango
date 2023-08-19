from django.db.models import Q
import graphene
from graphql import GraphQLError
from .schema import LinkType, VoteType
from .models import Link, Vote
from accounts.schema import UserType


    
class Query(graphene.ObjectType):
    votes = graphene.List(VoteType)
    links = graphene.List(LinkType, search=graphene.String())

    def resolve_links(self, info, search=None, **kwargs):
        if search:
            filter = (
                Q(url__icontains=search) |
                Q(description__icontains=search)
            )
            return Link.objects.filter(filter)
        return Link.objects.all()

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()
    
class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)
    
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    
    def mutate(self, info, url, description):
        user = info.context.user or None
        link = Link(url=url, description=description, posted_by=user)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            posted_by=link.posted_by,
        )


# #############################################################################################

#      PAGINATION IN GRAPHQL

####################################################################################################
# class Query(graphene.ObjectType):
#     # Add the first and skip parameters
#     links = graphene.List(
#         LinkType,
#         search=graphene.String(),
#         first=graphene.Int(),
#         skip=graphene.Int(),
#     )
#     votes = graphene.List(VoteType)

#     # Use them to slice the Django queryset
#     def resolve_links(self, info, search=None, first=None, skip=None, **kwargs):
#         qs = Link.objects.all()

#         if search:
#             filter = (
#                 Q(url__icontains=search) |
#                 Q(description__icontains=search)
#             )
#             qs = qs.filter(filter)

#         if skip:
#             qs = qs[skip:]

#         if first:
#             qs = qs[:first]

#         return qs
class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int(required=True)

    def mutate(self, info, link_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')

        link = Link.objects.filter(id=link_id).first()
        if not link:
            raise Exception('Invalid Link!')

        Vote.objects.create(
            user=user,
            link=link,
        )

        return CreateVote(user=user, link=link)


class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()



schema = graphene.Schema(query=Query, mutation=Mutation)
