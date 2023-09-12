from django.contrib import admin
from . import models
# Register your models here.

# The following two classes used to edit the admin panel 
class MealAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']
    search_fields = ['title', 'description']
    list_filter = ['title', 'description']


class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'meal', 'user', 'stars']
    list_filter = ['meal', 'user']



admin.site.register(models.Meal, MealAdmin)
admin.site.register(models.Rating, RatingAdmin)