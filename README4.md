# Django User Login

To implement a user login system, we'll follow the pattern of URL, Form, View, then Template.

In `main_app/urls.py` add the login route:

```python
...
path('login/', views.login_view, name="login")
...
```

In `main_app/forms.py`, add a login form:

```python
class LoginForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())
```

Lets add the `login_view` function in `main_appviews.py`:

```python
...
# Add LoginForm to this line...
from .forms import CatForm, LoginForm
# ...and add the following line...
from django.contrib.auth import authenticate, login, logout
...
def login_view(request):
    if request.method == 'POST':
        # if post, then authenticate (user submitted username and password)
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user. is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("The account has been disabled.")
            else:
                print("The username and/or password is incorrect.")
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
```

Finally, we'll add a new file for the `login.html` template:

```html
{% extends 'base.html' %}
{% load staticfiles %}

{% block content %}
<h1>Login</h1>
<form method="POST" action=".">
  {% csrf_token %}
  {{ form.as_p}}
  <input type="submit" value="Submit" />
</form>

{% endblock %}
```

Go ahead and test out the login route!

# Log Out!

This will be a similar pattern of URL and view, but no form or template.

In `urls.py`:

```python
...
path('logout/', views.logout_view, name="logout"),
...
```

Create the corresponding `views.py` logout_view function:

```python
...
# This line is already there
from django.contrib.auth import authenticate, login, logout
...
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
...
```

Finally, lets add the log in and log out functionality to our website. Lets add it to our `base.html` since we want it to be accessible from every view:

```html
{% if user.is_authenticated %}
  <a  href="{% url 'profile' user.username %}">Hello, {{ user.username }}!</a> |
  <a  href="{% url 'logout' %}">Logout</a>
{% else %}
  <a  href="{% url 'login' %}">Login</a>
{% endif %}
```

Awesome! Now we have login and logout functionality and the ability to see if you're currently logged in!

# What about that Profile?

We link to the 'profile' url from our username display, now we need that url, view, and template! At this point your `urls.py` should look like this:

```python
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:cat_id>/', views.show, name='show'),
    path('post_url/', views.post_cat, name='post_cat'),
    path('user/<username>/', views.profile, name='profile'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
]
```

Next is the view! Remember a good pattern is url, form (if needed), view, then template. This should already be in your `views.py` file:

```python
def profile(request, username):
    user = User.objects.get(username=username)
    cats = Cat.objects.all()
    return render(request, 'profile.html', {'username': username, 'cats': cats})
```

Then create the template `profile.html` (already done in part 3) This adds code to it:

```html
{% extends 'base.html' %}
{% load staticfiles %}

{% block content %}

<h4>{{ username }}'s collection:</h4>

<hr/>
{% for cat in cats %}
  <a href="/{{cat.id}}">
    <p>Name: {{ cat.name }}</p>
    {% if cat.age > 0 %}
      <p>Age: {{ cat.age }}</p>
    {% else %}
      <p>Age: Kitten</p>
    {% endif %}
  </a>
<hr/>
{% endfor %}

{% endblock %}
```

# Like Button, anyone?

Lets add some fun to our site! Lets allow users to like cats!

We will use the URL -> View -> Template pattern to implement this addition, but with an extra step of implementing some AJAX and include a like field to our Cat model.

Lets start with the model. Update our `models.py` to include a likes field:

```python
  ...
  likes = models.IntegerField(default=0)
  ...
```

We will then make then run a migration to make this change reflect in our database:

```bash
  python3 manage.py makemigrations
  python3 manage.py migrate
```

Now we can create a like button in our `index.html` page. Place this inside our `cats` iterator:

```html
<!-- Below the last endif and above the hr -->
<a class="waves-effect waves-light btn" data-id="{{cat.id}}">
  Likes: {% if cat.likes > 0 %} {{ cat.likes }} {% else %} None :( {% endif %}
</a>
```

Let's also grab the latest version of JQuery CDN and link it in our `base.html` as well as add an `app.js` file inside our `static` folder. That's where we'll put our AJAX!

We will include our javascript files **below** our html in `base.html`:

```html
...
<footer>
  All Rights Reserved, CatCollectr 2017
</footer>
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script src="{% static 'app.js' %}"></script>
</body>
</html>
```

In `app.js` lets create a button listener:

```javascript
  $('.btn').on('click', function(event){
    event.preventDefault();
    var element = $(this);
    $.ajax({
      url: '/like_cat/',
      method: 'GET',
      data: {cat_id: element.attr('data-id')},
    })
  })
```

We will now create a url path in `urls.py` for our like button:

```python
path('like_cat/', views.like_cat, name='like_cat')
```

Now we can update our `views.py` to execute a function that will update our like count:

```python
def like_cat(request):
    cat_id = request.GET.get('cat_id', None)

    likes = 0
    if (cat_id):
        cat = Cat.objects.get(id=int(cat_id))
        if cat is not None:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)
```

Update our button listener to handle a successful return of the like quantity:

```javascript
$('.btn').on('click', function(event){
  event.preventDefault();
  var element = $(this);
  $.ajax({
    url: '/like_cat/',
    method: 'GET',
    data: {cat_id: element.attr('data-id')},
    success: function(response){
      element.html('Likes: ' + response);
    }
  })
})
```

Wowee! Good job! You did it! That's the end! Though there is so much more you could do...

![](http://www.reactiongifs.us/wp-content/uploads/2013/10/jeremiah_johnson_nodding.gif)
