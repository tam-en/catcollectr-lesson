# Django! Part 2!

We have created an application that will display our cats that we've adopted/found/seen/collected (no judgements).  In this section we will break out our views into a detail page, and a new Cat form (/ᐠ｡▿｡ᐟ\\!!)!

# Read One Cat
So far we have collected their names, breed, description, and age we collected them.  That's a lot of information to have in one place, so we like to keep it simple in our index view.  In our detail or 'show' page we will give each Cat its own view to give us an uncluttered breakdown of its attributes.

The pattern of creating a new url in `urls.py`, a new view function in `views.py`, and a new html file in `/template` will apply here.

1.  Lets add our `show` url to capture a route with an id ( '/34', '/5', etc.) In the `urls.py` file in our `main_app`:

	```python
	# main_app/urls.py
	from django.urls import path
	from . import views

	urlpatterns = [
	    path('', views.index, name='index'),
	    path('<int:cat_id>/', views.show, name='show')
	]
	```
	The stuff in the pointy brackets is how we read URL parameters in Django. We say the data will be an integer (int) and then identify it with the variable named `cat_id`.

2.  In our `main_app/views.py` file we will need to write a function to handle the HTTP Request received for a single view page of a particular item.  Lets update our file to include this function:

	```python
	# main_app/views.py
	...
	def show(request, cat_id):
  	cat = Cat.objects.get(id=cat_id)
    return render(request, 'show.html', {'cat': cat})
	```

	You'll notice that we are searching by id.  Django automatically assigns our models incrementing id numbers to organize our tables.  Thanks Django!  That way we can look up every single cat by their unique `id` given to us.  That `id` will travel with every model so we don't have to worry about assigning them one or trying to maintain it in the back-end!  SO SWEET!

	After we have made the DB call to retrieve our model, we will render a new view of the `show.html` template and pass in our model as an object for the template to use.

3.  We will now create a `show.html` template page to render our single model view:

	```html
	<!-- main_app/templates/show.html -->
	{% load staticfiles %}
	<!DOCTYPE html>
	<html>
	  <head>
	    <title>CatCollectr</title>
	    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.css">
	    <link rel="stylesheet" type="text/css" href="{% static 'style.css' %}">

	  </head>
	  <body>
	    <h1>CatCollectr</h1>

	    <h2> Name: {{ cat.name }}</h1>
	    <p> Breed: {{ cat.breed }}</p>
	    <p> Description: {{ cat.description }}</p>
	    <p> Age: {{ cat.age }}</p>
	  </body>
	</html>
	```

4.  We can now view a single Cat on its dedicated show page!  Awesome!  To make our application actually useful, we need to create a link from our `index.html` listing of the Cats over to our `show.html` page.  Wrap the entire iteration of each Cat in an anchor tag in our `index.html` page:

	```html
	<!-- main_app/templates/index.html -->
	...
	{% for cat in cats %}
	  <a href="/{{cat.id}}">
	    <p>Name: {{ cat.name }}</p>
	  {% if cat.age > 0 %}
	    <p>Age: {{ cat.age }}</p>
	  {% else %}
	    <p>Age: Kitten</p>
	  {% endif %}
	  </a>
		<hr />
	{% endfor %}

	```

	Now we can navigate to the show from the index!  Add a link to the `CatCollectr` header to go back to our index to make our site fully navigable.


## Let's get partial!

We're beginning to see repeated code in our html templates so it makes sense to break our templates into partials to save on code reuse and increase scalability.  We'll use a base template to hold our initial `head` code, our `header` section, and our `footer` section.  The partials will only contain the necessary html for each specific task.

1.  Create a new `base.html` file within our templates folder. This will be our beginning 'layout' html file similar to a layout EJS file in Express:

	```html
	{% load staticfiles %}
	<!DOCTYPE html>
	<html>
	  <head>
	    <title>CatCollectr</title>
	    <link rel="stylesheet" type="text/css" href="{% static 'style.css' %}">
	    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.css">
	  </head>
	  <body>
			<h1>CatCollectr</h1>
    	<hr />

			{% block content %}
			{% endblock %}

	  	<footer>
	    	All Rights Reserved, CatCollectr 2017
	  	</footer>
	  </body>
	</html>
	```

	The `block content` and `endblock` statements are the placeholders for where our 'child' html will load into our base.html template.

2.  In `index.html` we will tell the templating language to send our html to `base.html` with a single line added to the top of the page.  We will also wrap our pertinent Cat iterator in the `block content` and `endblock` template tags to designate what gets loaded into our `base.html` dynamically.

	```html
	<!-- main_app/templates/index.html -->
	{% extends 'base.html' %}
	{% load staticfiles %}

	{% block content %}
		... index's iterator code ...
	{% endblock %}
	```

	Now try out our root route on the browser and you should see no change.  Apply this code refactor to our show.html as well. Good work!

# Create a Cat

Let us add the ability to create Cats in our application.  We will now study the wonderful world of forms and how to capture data to create new models.

1.  To use a Django form, we need to define a new class that inherits from forms.Form. Add the following new file `forms.py` to your `main_app` directory:

	```python
	# main_app/forms.py
	from django import forms

	class CatForm(forms.Form):
	    name = forms.CharField(label='Name', max_length=100)
	    breed = forms.CharField(label='Breed', max_length=100)
	    description = forms.CharField(label='Description', max_length=250)
			age = forms.IntegerField(label='Age')
	```

2.  Now lets head to `main_app/urls.py` to set up our route to post a new Cat. Lets add a route called `post_url` to listen for a post request:

	```python
	from django.urls import path
	from . import views

	urlpatterns = [
		path('', views.index, name='index'),
		path('<int:cat_id>/', views.show, name='show'),
		path('post_url/', views.post_cat, name='post_cat')
	]
	```

3. Now we can head to our `main_app/views.py` to create a post function. (Hot tip: later on you will learn a more declarative way to do this...with class views. But let's get some imperative practice)

	```python
	# main_app/views.py
	...
	from .forms import CatForm
	from django.http import HttpResponse, HttpResponseRedirect

	...
	def post_cat(request):
			form = CatForm(request.POST)
			if form.is_valid():
	        cat = Cat(
	            name=form.cleaned_data['name'],
	            breed=form.cleaned_data['breed'],
	            description=form.cleaned_data['description'],
	            age=form.cleaned_data['age'])
	        cat.save()
	    return HttpResponseRedirect('/')
	```

4.  We'll also need to update our `index` view to also render our form along with our iterated view of Cats.

	```python
	# main_app/views.py
	def index(request):
	    cats = Cat.objects.all()
	    form = CatForm()
	    return render(request, 'index.html', {'cats':cats, 'form':form})

	```

5.  Let's include the form in our `index.html` below our iterations:

```html
<!-- main_app/index.html -->
  <form action="post_url/" method="post">
      {% csrf_token %}
      {{ form.as_p }}
      <input type="submit" value="Submit" />
  </form>
```

The csrf token is for your protection! You can read more about [Cross Site Request Forgeries here!](https://docs.djangoproject.com/en/2.0/ref/csrf/)
Now check out your `index.html` page! We can now create new Cats!

6.  Our `CatForm` and our `CatModel` look awfully the same to be repeated that much.  Lets reuse our code with the `meta` class!

	```python
	# main_app/forms.py
	from django import forms
	# Add this line...
	from .models import Cat
	# Change the line below to use ModelForm...
	class CatForm(forms.ModelForm):
			# Replace the contents with these lines...
	    class Meta:
	        model = Cat
	        fields = ['name', 'breed', 'description', 'age']
	```

	We will link our form directly to our model and list the fields we want users to fill out in the fields variable.  The `Meta` class dictates that we will be doing just this.

7.  Update our `views.py` file to allow us to use this smaller code form:

	```python
	#main_app/views.py
	def post_cat(request):
	    form = CatForm(request.POST)
			if form.is_valid:
				cat = form.save(commit = False)
				cat.save()
	    return HttpResponseRedirect('/')
	```
## Moving on! [Let's add some Crazy Cat People! Or uh... Users](https://github.com/sixhops/catcollectr-lesson/blob/master/README3.md)
