# Users (Crazy Cat People)

We will now add Users to our application. We'll also set up a One-to-Many Relationship with Users having many Cats.

We will do this by assigning foreign keys to Cats. What is a foreign key? Let's draw up a table of two example users and a table of 4 example Cats.

## Let's Get a User!

In `main_app/models.py`, let's include Django's built-in User model from their auth library:

```python
  from django.contrib.auth.models import User
```

We can also add a foreign key to the Cat and set it as the user. This establishes the relationship of 1:M

```python
  # main_app/models.py (in Cat model)
  ...
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  ...
```

We should now run the `python3 manage.py makemigrations` command to integrate our foreign key. We will get a prompt from Django asking for one of two options. You should see something like this:

```
You are trying to add a non-nullable field 'user' to a cat without a default; we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit, and let me add a default in models.py
Select an option:
```

Let's choose option 1.

This will create a 'dummy' field of User that will be populated with null value row for us. We want this.

It will ask you one more time to enter a default value:

```bash
Please enter the default value now, as valid Python
The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now
Type 'exit' to exit this prompt
```

Go ahead and enter the number `1`. This will set a row to simply `1`. This will then trigger a migration file creation called `XXXX_cat_user.py`. Excellent!

Now run the migration by running

```bash
python3 manage.py migrate
```

Play with our Admin view and bask in the joy of being able to create Users and assigning Users to Cats! Make that assignment for all of your Cats.

Now go to your `main_app/views.py` file and lets update our view for the cats:

```python
# main_app/views.py
def post_cat(request):
    form = CatForm(request.POST)
    if form.is_valid():
        cat = form.save(commit = False)
        # Add this line...
        cat.user = request.user
        cat.save()
    return HttpResponseRedirect('/')
```

We are calling `commit = False`, which will create the DB entry for our new cat, but won't actually save it. Since the user object is sent along inside the `request` object (like Express) we can insert the current User into the cat by calling `request.user`. Lastly, we can save our cat and we are finished!

Now we need to add a view to see a User's profile. This will repeat the same pattern as

1. Set up a URL in `urls.py`
2. Create a view in `views.py`
3. Make an HTML template in `/templates`

### Create the User Profile URL

Let's go to our URL dispatcher in our `main_app` folder and update our `urlpatterns`:

```python
# main_app/urls.py
...
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:cat_id>/', views.show, name='show'),
    path('post_url/', views.post_cat, name='post_cat'),
    path('user/<username>/', views.profile, name='profile'), # this line is new
]
...
```

The stuff in the angle brackets lets us grab a passed-in username and store it in a variable called `username`.  Lets add to our `main_app/views.py` file:

```python
...
from django.contrib.auth.models import User
...
def profile(request, username):
    user = User.objects.get(username=username)
    cats = Cat.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'cats': cats})
```

Lastly, let's create a `profile.html` template to show a single User and all of the Cats they have collected:
(THIS PART IS DUPLICATED IN THE NEXT README)

```html
{% extends 'base.html' %}
{% load staticfiles %}

{% block content %}

<h1>{{ username }}'s collection:</h1>

{% for cat in cats %}
<a href="/{{ cat.id }}">
  <h3>{{ cat.name }}</h3>
</a>

{% endfor %}

{% endblock %}
```

Let's also update our `index.html` page to allow us to inspect each user:

```html
<!-- main_app/templates/index.html -->
{% extends 'base.html' %}
{% load staticfiles %}

  {% block content %}
  {% for cat in cats %}
    <a href="/{{cat.id}}">
      <p>Name: {{ cat.name }}</p>
    </a>
    <a href="/user/{{cat.user.username}}"
      <p>Adopted By: {{cat.user.username }}</p>
    </a>
    {% if cat.age > 0 %}
      <p>Age: {{ cat.age }}</p>
    {% else %}
      <p>Age: Kitten</p>
    {% endif %}
    <hr />
  {% endfor %}
  <form action="post_url/" method="post">
      {% csrf_token %}
      {{ form.as_p }}
      <input type="submit" value="Submit" />
  </form>
{% endblock %}
```
## But wait! There's more! [How do we login?!](https://github.com/sixhops/catcollectr-lesson/blob/master/README4.md)
