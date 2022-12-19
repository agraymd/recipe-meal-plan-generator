# Cookbook-Mealplan-Generator
# Table of contents

- [Cookbook-Mealplan-Generator](#cookbook-mealplan-generator)
  - [Description](#description)
  - [Technologies / Skills Used](#technologies--skills-used)
  - [Interesting Challenges](#interesting-challenges)
- [Installing and Starting the App on Windows](#installing-and-starting-the-app-on-windows)
  - [Shutting down the Containers:](#shutting-down-the-containers)
  - [Checking container logs for errors:](#checking-container-logs-for-errors)
  - [Permissions Issues](#permissions-issues)
- [Using the app](#using-the-app)
  - [Room For Improvement](#room-for-improvement)
  - [Admin User](#admin-user)
  - [Need to make nginx and db non-root users in Docker](#need-to-make-nginx-and-db-non-root-users-in-docker)
  - [Improved commenting.](#improved-commenting)
  - [Image handling](#image-handling)
  - [Other](#other)
- [Conclusion](#conclusion)


## Description 

This Django application allows an admin to upload recipes and specify the title, description, instructions, category, ingredients, and image.

The application will display each recipe preview on the home page, with detailed view available for ingrients/instructions. 

The application takes random meals from the database and generates a weekly meal plan, linking to the recipe used for each day on another webpage. 

For more information about installing and using the project, see the respective sections later in this README. 


## Technologies / Skills Used

The application is primarily built with HTML and Django/Python. Bootstrap is used for styling.

The application is “Dockerized” and uses alpine linux base, gunicorn, nginx, and postgresql.

Application is version controlled with Git. 


## Interesting Challenges 

Aside from overall usage of Django and python, I had a good time thinking about the database design for this application. See the rough sketch of the table schema below: 

![Database Schema](https://i.imgur.com/igG9Wu2.jpg)

The most interesting part of this was using Django’s “through” or associative table for the RecipeIngredients table.

Each recipe has a unique set of ingredients, but each ingredient can have many recipes associated with it. Each recipe can have many ingredients. Not only can it have many ingredients, but each ingredient will have a different quantity per recipe.

This is why we store the collection of ingredients per recipe separately!

 This essentially allows us to make the following (pseudo) query: 

`SELECT * FROM RECIPE-INGREDIENTS WHERE RECIPE_ID = X`

This means give me every item from the entry (what quantity, unit, and ingredient) for a certain recipe. Basically, give me all the ingredients for Chicken Noodle Soup. 

After the challenge of figuring out how to design the relationships in the first place, figuring out how to make the query in Python/Django was a fun challenge.


### How to print all ingredients for a recipe.

```
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
```

#### The final template/view logic looks like this: 


```
views.py: 

def recipe_detail(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    recipe_ingredients = RecipeIngredients.objects.filter(recipe_name=pk)
    context = {
        'recipe': recipe,
        'recipe_ingredients': recipe_ingredients
    }
    return render(request, 'recipe_detail.html', context)

```

```
HTML template: 

        <h5>Recipe Igredients:</h5>

        <ul id="recipe_ingredient_list" class="list-unstyled">
            {% for ingredient in recipe_ingredients %} 
                <li>
                    {{ ingredient.quantity }} 
                    {% if ingredient.unit == None %}
                    {{ ingredient.ingredient }}               
                    {% else %}
                    {{ ingredient.unit }} 
                    {{ ingredient.ingredient }}
                    {% endif %}                
                </li>
            {% endfor %}
        </ul>
```


Storing the data in this way allows for the potential of adding robust filtering and searching to the recipes. It is also part of how the mealplan generation works. 

I feel like I learned a lot about Django’s MVC design as well as python, Docker, nginx, and the other various technologies used during this project. 


# Installing and Starting the App on Windows

You need to create your own .env.dev and .env.prod files for the Docker build to complete.

Once the container is running there are a few things you should do in this order if you want to actually test this app for your self. The main thing is that once the app is running, the first three categories you create should be Breakfast, Lunch, Dinner — as this is what the app will consider them as for the mealplan generator (PK 1,2,3) and that page of the site will not work until the categories exist. 

### Requirements: 

-Docker 

1. Once you clone the repository, replace the values of the .env.prod and .env.prod.db files with your own password. Here is a django key you can use: 

`27w6q#=n_n)3j!09hv-lfj2az0ca5w57=ue=t+pos(hst%)^qv`


2. Correct the CSRF_TRUSTED_ORIGINS in settings.py as needed for your system. Example: 

```
CSRF_TRUSTED_ORIGINS = ['http://192.168.1.165:1337', 'http://localhost:1337']

```
Add your IP to DJANGO_ALLOWED_HOSTS .env.prod: 

```
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 192.168.1.165**
```

3. Run the following docker commands to build the containers, migrate the database, collect static, and create an admin user: 

```
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python3 manage.py makemigrations recipeblog --noinput
docker-compose -f docker-compose.prod.yml exec web python3 manage.py migrate recipeblog --noinput
docker-compose -f docker-compose.prod.yml exec web python3 manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec -u 0 web chown -R app:app ./mediafiles/
docker-compose -f docker-compose.prod.yml exec -u 0 web chown -R app:app ./staticfiles/
docker-compose -f docker-compose.prod.yml exec web python3 manage.py collectstatic --no-input
docker-compose -f docker-compose.prod.yml exec web python3 manage.py createsuperuser
```

## Shutting down the Containers: 

```
docker-compose -f docker-compose.prod.yml down -v 
```

## Checking container logs for errors: 

```
docker-compose -f docker-compose.prod.yml logs -f
```


## Permissions Issues 

For some reason on windows, the staticfiles and mediafiles directory in the container is owned by root, and collect static does not work as the user 'app'. That is why chown for user app to own the files in the commands above, where we specify root with -u 0 flag.

This was not required on mac and seems like it should be handled in the compose or Dockerfile. Will need to check into this. 

This should be all you need to access the application at http://your-host-ip:1337

# Using the app

### Logging in:

1. Login at http://your-host-ip:1337/admin or clicking login on the navigation bar. 

The username and password you should create from the terminal after running `docker-compose -f docker-compose.prod.yml exec web python3 manage.py createsuperuser`. 


### Creating categories

Go to add recipe from the admin panel. Add a recipe and complete all fields, including picture upload. 

When you create the categories, create breakfast, lunch, and dinner in that order if you want the meals to be searched correctly in the mealplan generator. 

## Room For Improvement

There are a multitude of issues to improve this if it were an actual app. The main goal was to build something that may or may not be useful to my wife and I, as sometimes meal planning and keeping recipes we like is a challenge. 

However the real goal was to practice python fundamentals and use Docker to run an application. 

That being said, here are some ideas / notes for the project idea itself that could improve it.


## Admin User

Need to make the admin user on app startup or similar. Currently you have to exec a command to the docker container to create the user. 


### Mealplan is broken until you make 3 categories 

Currently the “mealplan generator” view relies on there being recipes that exist, and that breakfast, lunch, and dinner categories have PK values in the database of 1, 2, and 3. 

Until meals exist with the categories needed, the page will 500 error. 

The mealplan generator basically uses python to get a random breakfast lunch or dinner from the database using filter queries and populates an HTML page with the results.

This functionality of searching for breakfast, lunch, and dinner would have to be reworked in some way or error handled. Perhaps if these categories exist then work, if they do not tell the user to create them. Then you would need to search by NAME instead of PK. 


## Need to make nginx and db non-root users in Docker 

Self explanatory, maybe in a future commit. 


## Improved commenting.

After a few days of trying to get this done, I already forget some of the logic between the different parts. To an experienced programmer, this small app could be figured out quick. However normally I comment the actual code a little better than I did here, explaining how things work or what they rely on, mostly explaining to my self. 


## Image handling

Currently, if you replace a recipe image it will not delete the previous one, wasting server space. 

Images should also be resized to be consistent on upload or at least on display. 

Images should not be required. 


## Other 

There are a lot of other features that could be added if this were a real app. User signup forms, enhanced searching and filtering. 

You could make the meal plan generator collect the list of all required ingredients to build a shopping list for the week. There could be an option to remove items from the list that you already have. 

In the interest of moving on and continuing my studies I will stop work on this app but I wanted to document it and show it as a finished project. 

I think that me and my wife will actually use it in some capacity, and if we like it maybe I will use it as an opportunity to learn more about some aspect of programming and application design. Hopefully someday after learning all this stuff, I can make a lot of money and buy a house :P 

# Conclusion

That is pretty much it. I had a lot of fun overcoming the various challenges I faced building this, including troubleshooting the Docker deployment. 

Now I have a cool little app I can spin up anywhere I have Docker. This concept is cool and the concepts I learned about Django and how to achieve various tasks there should make my next project even more interesting! 

I can even reuse components of this one! 

Thanks for checking it out and let me know if you have any cool projects to work on :D 

