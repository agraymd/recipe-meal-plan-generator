import random
from django.shortcuts import render
from recipeblog.models import Recipe, RecipeIngredients
from random import choice
# Create your views here.

def recipe_index(request):
    recipes = Recipe.objects.all()
    context = {
        'recipes': recipes
    }
    return render(request, 'recipe_index.html', context)

def recipe_detail(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    recipe_ingredients = RecipeIngredients.objects.filter(recipe_name=pk)
    context = {
        'recipe': recipe,
        'recipe_ingredients': recipe_ingredients
    }
    return render(request, 'recipe_detail.html', context)

# Create the view for generating weekly mealplan. 
def mealplan(request):
    active = 'mealplan'
    # Get a random breakfast
    all_breakfasts = Recipe.objects.filter(recipe_category=1)
    breakfast_pks = all_breakfasts.values_list(flat=True)
    random_breakfast_pk = choice(breakfast_pks)
    random_breakfast = Recipe.objects.get(pk=random_breakfast_pk)

    # Get a random lunch for M - W. 
    all_lunches = Recipe.objects.filter(recipe_category=2)
    lunch_pks = all_lunches.values_list(flat=True)
    random_mw_lunch_pk = choice(lunch_pks)
    random_mw_lunch = Recipe.objects.get(pk=random_mw_lunch_pk)  

    # Get a random lunch for TH - S
    random_ts_lunch_pk = choice(lunch_pks)
    random_ts_lunch = Recipe.objects.get(pk=random_ts_lunch_pk)  

    # Get a random dinner for each day.
    # Define function to get random dinner, use while to call it 7 times appending results to list.

    def get_random_dinner():
        all_dinners = Recipe.objects.filter(recipe_category=3)
        dinner_pks = all_dinners.values_list(flat=True)
        random_dinner_pk = choice(dinner_pks)
        return random_dinner_pk  
    
    dinner_pk_list = []
    dinner_list = []

    counter = 0
    while counter < 7:
        random_dinner_pk = get_random_dinner()
        dinner_pk_list.append(random_dinner_pk)
        random_dinner = Recipe.objects.get(pk=random_dinner_pk)
        dinner_list.append(random_dinner)
        counter = counter + 1 

    # For each item in the list, asign its value to a variable for the day of the week.   
    md_pk, tud_pk, wd_pk, thd_pk, fd_pk, sad_pk, sud_pk = dinner_pk_list
    md, tud, wd, thd, fd, sad, sud = dinner_list

    context = {
        'random_breakfast_pk': random_breakfast_pk,
        'random_breakfast': random_breakfast,
        
        'random_mw_lunch_pk': random_mw_lunch_pk,
        'random_mw_lunch': random_mw_lunch,

        'random_ts_lunch_pk': random_ts_lunch_pk,
        'random_ts_lunch': random_ts_lunch,

        'md_pk': md_pk,
        'md': md,

        'tud_pk': tud_pk,
        'tud': tud,

        'wd_pk': wd_pk,
        'wd': wd,

        'thd_pk': thd_pk,
        'thd': thd,

        'fd_pk': fd_pk,
        'fd': fd,

        'sad_pk': sad_pk,
        'sad': sad,

        'sud_pk': sud_pk,
        'sud': sud,
    }

    return render(request, 'mealplan.html', context)