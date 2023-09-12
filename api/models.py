from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Meal(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)

    def no_of_ratings(self):
        ratings = Rating.objects.filter(meal=self)
        return len(ratings)
    
    def avg_ratings(self):
        sum = 0
        ratings = Rating.objects.filter(meal=self)

        for rating in ratings:
            sum+=int(rating.stars)

        if len(ratings) > 0:
            avg = int(sum/len(ratings))
        else:
            avg = 0

        return avg
        
    def __str__(self):
        return self.title
    

class Rating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])


    def __str__(self):
        return self.meal.title
    
    class Meta:
        unique_together = (('user', 'meal', ))  # the user and meal is unique together.. the user can not rate the meal twice, only on rate
        index_together = (('user', 'meal', ))   # make the user and meal as index together
