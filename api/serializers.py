from rest_framework import serializers
from . import models
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'password']

        # Without the following line all users with username and password with be listed if anyone make a get
        # request, but with the following line password will not be listed again
        extra_kwargs = {"password" : {"write_only":True, "required":True }}


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Meal
        fields = ['id', 'title', 'description', 'no_of_ratings', 'avg_ratings']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rating
        fields = ['id', 'meal', 'user', 'stars']