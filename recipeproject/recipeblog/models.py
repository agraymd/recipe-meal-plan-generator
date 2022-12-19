from distutils.text_file import TextFile
from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Ingredient(models.Model):
    ingredient = models.CharField(max_length=200)

    def __str__(self):
       return self.ingredient

class RecipeCategory(models.Model):
    category = models.CharField(max_length=15)

    def __str__(self):
       return self.category

class Recipe(models.Model): 
    recipe_name = models.CharField(max_length=200)
    recipe_description = models.TextField()
    recipe_instructions = models.TextField(null=True, blank=True)
    recipe_category = models.ManyToManyField(RecipeCategory, blank=True)
    recipe_photo = models.ImageField(upload_to="recipe_photo", null=True)

    recipe_ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients',
        through_fields=('recipe_name', 'ingredient'),
    )

    def __str__(self):
       return self.recipe_name

# Class to hold the possible quantities of ingredients, integer/decimal values.
class MeasurementQuantity(models.Model):
    measurement_quantity = models.IntegerField()
    
    def __str__(self):
       return str(self.measurement_quantity)

# Class to make a table for descriptions of units of measurement ie; Cup, Tbps, Tsp, etc. 
class MeasurementUnit(models.Model):
    measurement_description = models.CharField(max_length=200)

    def __str__(self):
       return self.measurement_description

# Through table to associate ingredients and their quantities to recieps. 
class RecipeIngredients(models.Model): 
    recipe_name = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.ForeignKey(MeasurementQuantity, on_delete=models.CASCADE)
    unit = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE, blank=True, null=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)








# How to print all ingredients for a recipe.
'''
ri = RecipeIngredients.objects.filter(recipe_name=X)

X = pk of recipe that you need list of ingredients for. 

Using for loop, you can print each ingredient:

for e in ri:
    print(str(e.quantity) + ' ', end='')
    if e.unit == None:
        print(e.ingredient)
    else:
        print(e.unit, end=' ')
        print(e.ingredient)
        pass
'''


