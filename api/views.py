from django.shortcuts import render
from . import models
from . import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from rest_framework.authtoken.models import Token


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    
    # We override the following method from the ViewSet to create a user and a token then return that token
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        json = {
            "token" : token.key
        }
        return Response(json, status=status.HTTP_201_CREATED)
    

    def list(self, request, *args, **kwargs):
        json = {
            "message" : "Error, you cann't list users."
        }
        return Response(json, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        json = {
            "message" : "Error, you cann't update this user."
        }
        return Response(json, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        json = {
            "message" : "Error, you cann't delete this user."
        }
        return Response(json, status=status.HTTP_400_BAD_REQUEST)

class MealViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = models.Meal.objects.all()
    serializer_class = serializers.MealSerializer

    # Only the users that have a tokenauthentication and also authenticated users can access this viewset
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["POST"])
    def rate_meal(self, request, pk=None):
        if 'stars' in request.data:
            meal = models.Meal.objects.get(id=pk)
            stars = request.data["stars"]  
            user = request.user          
            
            # We disabled the following two lines because we use the tokenauthentication
            # username = request.data["username"]
            # user = User.objects.get(username=username)
            stars = int(stars)
            if stars in range(1, 6):
                try:
                    # Update the rate
                    rating = models.Rating.objects.get(user=user.id, meal=meal.id)
                    rating.stars = stars
                    rating.save()
                    serializer = serializers.RatingSerializer(rating, many=False)
                    json = {
                        'message' : "Meal rating updated successfully",
                        'result' : serializer.data
                    }
                    return Response(json, status=status.HTTP_200_OK)
                except:
                    # Create new rate
                    rating = models.Rating.objects.create(user=user, meal=meal, stars=stars)
                    serializer = serializers.RatingSerializer(rating, many=False)
                    json = {
                        'message' : "Meal rating created successfully",
                        'result' : serializer.data
                    }
                    return Response(json, status=status.HTTP_200_OK)
            else:
                json = {
                    'message' : "Error, stars exceed limits"
                }
                return Response(json, status=status.HTTP_400_BAD_REQUEST)
        else:
            json = {
                'message' : "Error, stars not provieded"
            }
            return Response(json, status=status.HTTP_400_BAD_REQUEST)



class RatingViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = models.Rating.objects.all()
    serializer_class = serializers.RatingSerializer

    # Only the users that have a tokenauthentication and also authenticated users  can access this viewset
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    """
        we override the update and create functions of this viewset to deny any user from
        updating or creating a rate from this viewset because we update and create a rate from 
        our custom method (rate_meal) which we create in the above viewset (MealViewSet) to do this action.
    """
    def update(self, request, *args, **kwargs):
        json = {
            "message" : "Invalid way to update a rate."
        }
        return Response(json, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        json = {
            "message" : "Invalid way to create a rate."
        }
        return Response(json, status=status.HTTP_400_BAD_REQUEST)





# class Meal_List(APIView):
#     def get(self, request):
#         meals = models.Meal.objects.all()
#         serializer = serializers.MealSerializer(meals, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = serializers.MealSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# class Meal_PK(APIView):
#     def get_object(self, pk):
#         try:
#             meal = models.Meal.objects.get(pk=pk)
#             return meal
#         except models.Meal.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#     def get(self, request, pk):
#         meal = self.get_object(pk)
#         serializer = serializers.MealSerializer(meal, many=False)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         meal = self.get_object(pk)
#         serializer = serializers.MealSerializer(meal, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     def delete(self, request, pk):
#         meal = self.get_object(pk)
#         meal.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)





# class Rating_List(APIView):
#     def get(self, request):
#         rates = models.Rating.objects.all()
#         serializer = serializers.RatingSerializer(rates, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = serializers.RatingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# class Rating_PK(APIView):
#     def get_object(self, pk):
#         try:
#             rate = models.Rating.objects.get(pk=pk)
#             return rate
#         except models.Rating.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#     def get(self, request, pk):
#         rate = self.get_object(pk)
#         serializer = serializers.RatingSerializer(rate, many=False)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         rate = self.get_object(pk)
#         serializer = serializers.RatingSerializer(rate, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     def delete(self, request, pk):
#         rate = self.get_object(pk)
#         rate.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



