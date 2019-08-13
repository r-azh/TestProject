from django.shortcuts import render

from rest_framework import generics
from .serializers import PollSerializer, ChoiceSerializer,\
    VoteSerializer, UserSerializer
from django.contrib.auth.models import User


class PollList(generics.ListCreateAPIView):
    from .models import Poll
    """
    List all polls, or create a new poll.
    """
    # queryset: This will be used to return objects from the view.
    queryset = Poll.objects.all()
    # This will be used for validating and deserializing the input and for seraizling the output.
    serializer_class = PollSerializer


class PollDetail(generics.RetrieveDestroyAPIView):
    from .models import Poll
    """
    Create a Poll, delete a poll
    """

    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class ChoiceDetail(generics.RetrieveUpdateAPIView):
    from .models import Choice
    """
    Retrieves a Choice, Updates a Choice
    """

    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class CreateVote(generics.CreateAPIView):
    """
    Create a vote
    """

    serializer_class = VoteSerializer


class UserCreate(generics.CreateAPIView):
    """
    Create an User
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    Retrieve a User
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
