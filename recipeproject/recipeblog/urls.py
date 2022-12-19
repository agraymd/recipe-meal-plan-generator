from django.urls import path
from . import views 

urlpatterns = [
    path("", views.recipe_index, name="recipe_index"),
    path("<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("mealplan", views.mealplan, name="mealplan"),    

]