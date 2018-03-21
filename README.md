# Lets create CatCollectr w/ Django!

1. Create a Django application with the following command:

	```bash
	django-admin startproject CatCollectr
	```

	This will create a folder labeled CatCollectr as well as a few support files and a folder within with the same name. Spend some time familiarizing yourself with the file structure.
	- settings.py will hold the settings for our application
	- urls.py will hold all of the routing for our application
	- manage.py will house common functions we'll perform on our app (server, migrations, etc.)

2.  To see a barebones website automatically created for us run the following command:

	```bash
	python3 manage.py runserver
	```

	Head to the location given in your terminal and you should see a boilerplate greeting page for Django!

3.  We have created a project for django but not yet our **application**. In Django a project consists of many smaller applications (think of them as widgets.) Lets use the manage.py utility `startapp` to create our first `app` inside our Django `project`:

	```bash
	python3 manage.py startapp main_app
	```

	This will create a folder for `main_app` and many support files inside.  Familiarize yourself with these files before heading on.

4.  We will now work on our first view. A view is a function that takes in a web request and returns a web response.

	```python
	# main_app/views.py
	from django.shortcuts import render
	from django.http import HttpResponse

	def index(request):
		return HttpResponse('<h1>Hello World! /ᐠ｡‸｡ᐟ\ﾉ</h1>')
	```

5.  Now we will map this particular view to a url.  We want to use the route `/index` for now as an example.  Lets add a url for our view in the `url dispatcher` file in `CatCollector/CatCollectr/urls.py`:

	```python
	# CatCollectr/CatCollectr/urls.py
	from django.conf.urls import url
	from django.contrib import admin
	from main_app import views

	urlpatterns = [
		url(r'^admin/', admin.site.urls),
		# add the line below to your urlpatterns array
		url(r'^index/', views.index)
	]
	```

	The r is a regular expression matcher that will listen for a route that matches the particular pattern in the first argument. The second argument is the specific path to the view function we want to associate with our route.


6.  The route `/index` is great for debugging and proof of concepts but lets make this mirror the normal pattern of launching the index view when we hit the `/` route. In the urlpatterns array change the following:

	```python
	# CatCollectr/CatCollectr/urls.py
	from django.conf.urls import url
	from django.contrib import admin
	from main_app import views

	urlpatterns = [
		url(r'^admin/', admin.site.urls),
		# add the line below to your urlpatterns array
		url(r'^', views.index)
	]
	```

	Now head to the `/` root route and you should see our greeting! Sweet!

7.  Too keep our routes clean and separated in an orderly fashion we will now separate our routes into our separate `apps` away from the main url dispatcher in `CatCollectr`.  


	```python
	# CatCollectr/CatCollectr/urls.py
	from django.conf.urls import include, url
	from django.contrib import admin

	urlpatterns = [
		url(r'^admin/', admin.site.urls),
		# add the line below to your urlpatterns array
		url(r'^', include('main_app.urls'))
	]
	```

	Make a `urls.py` file and we'll start our urlpatterns here as well. We will directly import our view functions from the view file:

	```python
	# main_app/urls.py
	from django.conf.urls import url
	from . import views


	urlpatterns = [
    	url(r'^$', views.index, name='index'),
	]

	```


# Lets start showing data!

1.  We will now start working on our front-end view and templating.   We have a bit of a shopping list of actions to do within our app.  

	- In settings.py inside `CatCollectr/CatCollectr` include our 'main_app':


	```python
	INSTALLED_APPS = [
		'main_app',

		'django.contrib.admin',
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.messages',
		'django.contrib.staticfiles',
	]

	```

	- Create a `templates` folder within the `main_app` folder

	- Create an `index.html` file inside your `templates` folder and fill it with some basic html:

	```html
	<!DOCTYPE html>
	<html>
	  <head>
		<title>CatCollectr</title>
	  </head>
	  <body>
        <h1>CatCollectr</h1>
        <hr />
        <footer>All Rights Reserved, CatCollectr 2018</footer>
	  </body>
   	 </html>

	```

	- In our `views.py` we will now be **rendering** our template instead of sending HTTP responses, so so we can update our views.py to only import render from django.shortcuts.  Feel free to delete the line importing HttpResponse.

	- Finally, in our index function in our views.py file, lets update the render to show our index.html:

	```python
	def index(request):
    	return render(request, 'index.html')

	```


1.  In `views.py` lets create a Cat class with all of the attributes we want to see displayed on our index page. We can also create an array of Cat objects to populate our view. Add this code to the bottom of the file.

	```python
	# main_app/views.py
	...
	class Cat:
	    def __init__(self, name, breed, description, age):
	        self.name = name
	        self.breed = breed
	        self.description = description
	        self.age = age

	cats = [
	    Cat('Lolo', 'tortoise shell', 'diluted tortoise shell', 0),
	    Cat('Sachi', 'tortoise shell', 'diluted tortoise shell', 0),
	    Cat('Raven', 'black tripod', '3 legged cat', 4)
	]
	```

2.  We can pass this cats list into our index function to be viewed on the index page!  We will pass in a JSON datatype that will have the key `cats` and the value of the array of cats we just made! (yay, JSON!)  Update the index request to reflect the following change:

	```python
	def index(request):
	    return render(request, 'index.html', {'cats': cats})

	```

	You'll notice that we are now sending a **third** argument, the actual data we want to display! (Which is often called the 'context')

3.  In our `index.html` file we will use specific Django templating language to iterate and display our data in `cats`.  


	```html
	{% for cat in cats %}
      <p>Name: {{ cat.name }}</p>
		<p>Age: {{ cat.age }}</p>
      <hr />
    {% endfor %}
	```

	Check out our index file on your browser and you should see our cats displayed on the screen!


4. Lets add some conditional checking to format our values.  If we have a 0 value for a cats age, lets set it to display 'Kitten':

	```html
	{% for cat in cats %}
      	  <p>Name: {{ cat.name }}</p>
      	{% if cat.age > 0 %}
          <p>Age: {{ cat.age }}</p>
      	{% else %}
          <p>Age: Kitten</p>
      	{% endif %}
      	  <hr />
	{% endfor %}

	```


5. We need to spruce up our view with some style!
	- Create a `static` folder in our `main_app` folder. This will house our static files.
	- Create a `style.css` file within our `static` folder.

6. Create a simple attribute for an h1 tag to check to see if our style is loaded in our html file:

	```css
	h1 {
		color: turquoise;
	}
	```

7.  In our index.html we need to connect our static folder and files to our templating language. We do so by declaring our usage of static files at the top of the page. We'll also show you how to link your style.css file as well:

	```html
	{% load staticfiles %}
	<!DOCTYPE html>
	<html>
	  <head>
	    <title>CatCollectr</title>
	    <link rel="stylesheet" type="text/css" href="{% static 'style.css' %}">
	  </head>
	...
	```


8.  We can also add our good friend bootstrap or materialize!  Let's use materialize just because I said so.

	```html
	{% load staticfiles %}
	<!DOCTYPE html>
	<html>
	  <head>
	    <title>CatCollectr</title>
	    <link rel="stylesheet" type="text/css" href="{% static 'style.css' %}">
	    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.css">
	  </head>
	...
	```

You should now have a boring but completely functional application that will pull data from a hardcoded array of Cat objects and display it on your index view. Congrats! What fun!



# Connecting a model to our view

1.  Lets create a `model` of our Cat instead of storing it hardcoded in our views.py. This will allow us to easily create new Cats and keeps the 'MVC' framework robust. In our `main_app/models.py` file, change the code to reflect the following:

	```python
	# main_app/models.py
	from django.db import models

	class Cat(models.Model):
	    name = models.CharField(max_length=100)
	    breed = models.CharField(max_length=100)
	    description = models.CharField(max_length=250)
        age = models.IntegerField()

	```

2.  We will also need to run a `migration`. A migration is a database action that makes any necessary changes to your db tables to prepare for storing specific data attributes of your models. Think of it as a construction team building a house to your specifications. But wait a minute! Django defaults to using sqlite... I want to use postgresql! Let's fix that before we do any migrating! Let's go back into the `settings.py` file in the CatCollectr directory and change a few things.

```python
# CatCollectr/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': ('cats'),
    }
}
```
Good! Oh, and importantly, we must create our db in the terminal with psql by running:

```bash
createdb cats
```

Okay now prepare to migrate:

- Enter the following into your terminal:

```bash
python3 manage.py makemigrations
```
This will prepare a file to execute your database changes

- Enter this command to execute the migration:

```bash
python3 manage.py migrate
```
Separate steps let you review the migration before you actually run `migrate`

3.  Lets jump into the `Django Interactive Shell` to play with the database for our Cats!

	In your terminal:

	```bash
	python3 manage.py shell
	```

	Now lets connect to our Cat db:

	```bash
	from main_app.models import Cat
	```
	To see all of our Cat models, enter this command:

	```bash
	Cat.objects.all()
	```
	Looks like we have an empty array, which means we have no data yet!

	Lets add some data!

	```bash
	c = Cat(name="Biscuit", breed='Sphinx', description='Evil looking cuddle monster. Hairless', age=2)
	c.save()

	```

	If you call `Cat.objects.all()` again you'll see a Cat Object exists!  Lets add a `__str__` method in our model to make this prettier:

	```python
	# main_app/models.py
	...
	def __str__(self):
	  return self.name

	```

4. 	Now lets update our views.py to use our models! Remember to remove your Cat class definition, we won't need that where we're going.

	```python
	# main_app/views.py
	from django.shortcuts import render
	from .models import Cat

	def index(request):
	    cats = Cat.objects.all()
	    return render(request, 'index.html', { 'cats':cats })

	```

5.  Reload your page and you should see a single Cat displayed from your database!  You're a wizard, Harry!

![](https://media.giphy.com/media/IN8gg3Gci335S/giphy.gif)

# I am the ADMIN!

6.  One last really really REALLY neat thing:  Django comes with a admin back-end administrator baked in!  Let's use it!

We need to create a super user ( a mega admin ) to allow us to log in initially and create other users and data.  Run this command in the terminal:


```bash
python3 manage.py createsuperuser
```


You will prompted to enter a username, email address, and a password. You are now creating a 'web master' for your site!

Now go to your webpage and head over to the `/admin` route to see an admin portal!  

Did you mess up your password? It's okay. Forgive yourself. Go back to your terminal and use this handy-dandy command:

```bash
python3 manage.py changepassword <user_name>
```

7.  We need to **register** our Cat model in our admin page to be able to see them in this new cool view.  To do this let's alter our admin.py page to allow our model to be seen.

	```python
	from django.contrib import admin
	from .models import Cat

	# Register your models here.
	admin.site.register(Cat)
	```

8.  Now when we go back to our admin page, we'll see a link to our Cat model.  We can add, update, and remove Cat models at our leisure from this section.  Neat!


## Next up! [Django! Part 2!](https://github.com/ladydangerdame/CatCollectr/blob/master/README2.md)
