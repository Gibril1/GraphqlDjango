from graphene_django import DjangoObjectType

from .models import Link, Vote


class LinkType(DjangoObjectType):
    class Meta:
        model = Link

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote