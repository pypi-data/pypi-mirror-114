# Flask-Meld

Official Website - [Flask-Meld.dev](https://www.flask-meld.dev)

Project inspiration - [Ditch Javascript Frameworks For Pure Python Joy](https://michaelabrahamsen.com/posts/flask-meld-ditch-javascript-frameworks-for-pure-python-joy/) 

Join the community on Discord - https://discord.gg/DMgSwwdahN

Meld is a framework for Flask to meld your frontend and backend code. What does
that mean? It means you can enjoy writing dynamic user interfaces in pure Python.

Less context switching.
No need to write javascript.
More fun!

# Fastest way to get started

Install flask-meld to your Python environment: `pip install flask-meld`

```sh
# 1. Replace "project_name" with the name of your project
meld new project name_of_project

# 2. Change to your project_name directory and install requirements
cd project_name; pip install -r requirements.txt

# 3. Run the flask-meld development server
flask run

## Bonus (optional) - create a component
meld new component name_of_component
```



# Initialize Meld in an existing project (Alternative method to get started)

For the sake of example, here is a minimal Flask application to get things
running:

```py
from flask import Flask, render_template
from flask_meld import Meld

app = Flask(__name__)
app.config['SECRET_KEY'] = 'big!secret'

meld = Meld()
meld.init_app(app)

socketio = app.socketio

@app.route('/')
def index():
    return render_template("base.html")

if __name__ == '__main__':
    socketio.run(app, debug=True)
```

# Add `{% meld_scripts %}` to your base html template

This sets up the application and initializes Flask-Meld.

```html

<!DOCTYPE html>
<html>
    <head>
        <title>Meld Example</title>
    </head>
    <body>
        <div>
        <!-- Add the line below to include the necessary meld scripts-->
        {% meld_scripts %}

        {% block content %}
            <!-- Using a component in your template is easy! -->
            {% meld 'counter' %}
        {% endblock %}
        </div>
        <style>
        </style>
    </body>
</html>
```

# Components

Components are stored in `meld/components` either within your application folder or in the base directory of your project.

Components are simple Python classes.

The `counter` component:

```py
# app/meld/components/counter.py

from flask_meld import Component


class Counter(Component):
    count = 0

    def add(self):
        self.count = int(self.count) + 1

    def subtract(self):
        self.count = int(self.count) - 1
```

# Templates

Create a component template in `templates/meld/counter.html`. By creating a file
within the `templates/meld` directory just include `{% meld 'counter' %}` where
you want the component to load.

Here is an example for counter:

```html
{# templates/meld/counter.html #}
<div>
    <button meld:click="subtract">-</button>
    <input type="text" meld:model="count" readonly></input>
    <button meld:click="add">+</button>
</div>
```
Let's take a look at that template file in more detail.

The buttons use `meld:click` to call the `add` or `subtract` function of the
Counter component.
The input uses `meld:model` to bind the input to the `count` property on the
Counter component.  

Note, to avoid errors, when adding a comment to a component template use the
Jinja syntax, `{# comment here #}`, rather than the HTML syntax.

### Pass data to a component

You can, of course, pass data to your meld component. Meld is passing **kwargs 
to the render function of the *meld* templatetag, so you can pass any number of 
named arguments. The component is found based on the first parameter, aka name 
of the component, and any number of data passed afterwards. 

Providing a very basic component as an example to display a greeting message using
the passed value for the keyword "name" in the corresponding template.

```html
{# templates/meld/greeter.html #}
<div>
    Hello, {{name or "Nobody"}}
</div>
```
which can be invoked using:

```html
{# templates/base.html #}
{% meld 'greeter', name="John Doe" %}
```

### Use passed values in a component (advanced use)

If you want to use the passed arguments from the meld template tag in your component (e.g. configuring the component or adding initial data), you can simply use them from the constructor: 

```py
class Greeter(Component):

    def __init__(self, **kwargs):
        super().__init__()
        name = kwargs.get('name', 'Nobody')
```

```html
<div>
    Hello, {{name}}
</div>
```

### Modifiers

Use modifiers to change how Meld handles network requests.

`debounce`: `<input meld:model.debounce-500="search">` Delay network requests for an 
amount of time after a keypress.  Used to increase performance and sync when 
the user has paused typing for an amount of time. `debounce-250` will wait 250ms before
it syncs with the server. The default is 150ms.

`defer`: `<input meld:model.defer="search">` Pass the `search` field with the next network
request. Used to improve performance when realtime databinding is not necessary.

`prevent`: Use to prevent a default action. 
The following example uses `defer` to delay sending a network request until the form is
submitted. Idea of how this can be used: instead of adding a keydown event listener to the input field to capture 
the press of the `enter` key, a form with `meld:submit.prevent="search"` can be used to 
to invoke a component's `search` function instead of the default form handler on form
submission.

```html
<form meld:submit.prevent="search">
    <input meld:model.defer="search_text" type="text" name="name" id="name" placeholder="Search for name">
    <button meld:click="search">Search</button>

    <!-- To get the same functionality without using meld:submit.prevent="search" you
    would need to add an event listener for the enter key 
    <input meld:model.defer="search_text" meld:keydown.Enter="search" type="text" name="name" id="name" placeholder="Search for name">
    -->
</form>
```

# Form Validation

A big part of creating web applications is using forms. Flask-Meld integrates with
Flask-WTF to give you real-time form validation without writing any Javascript.

## Use WTForms for validation

Define your form with Flask-WTF just as you always do. 

```py
# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
```

## Create your template

Use WTForm helpers to create your form in your HTML template. 

```html
<!-- templates/meld/register.html -->
<div>
    <form method="POST">
        <div>
            {{ form.email.label }}
            {{ form.email }}
            <span> {{ errors.password | first }} </span>
        </div>

        <div>
            {{ form.password.label }}
            {{ form.password }}
            <span> {{ errors.password | first }} </span>
        </div>
        <div>
            {{ form.password_confirm.label }}
            {{ form.password_confirm }}
            <span> {{ errors.password_confirm | first }} </span>
        </div>
        <div>
            {{ form.submit }}
        </div>
    </form>
</div>
```

Using the WTForm helpers saves you some typing. 
Alternatively, you can define your HTML form without using the helpers. 
For example, to make a field use
`<input id="email" meld:model="email" name="email" required="" type="text" value="">`
Make sure that `meld:model="name_of_field"` exists on each field.

## Define the form in the component

```py
# meld/components/register.py
from flask_meld import Component
from forms import RegistrationForm


class Register(Component):
    form = RegistrationForm()
```

## Realtime form validation

To make your form validate as a user types use the `updated` function. This will provide
the form field and allow you to validate on the fly. Simply call `validate` on the
field.

```py
# meld/components/register.py
from flask_meld import Component
from forms import RegistrationForm


class Register(Component):
    form = RegistrationForm()

    def updated(self, field):
        self.validate(field)
```

## Your routes can stay the same when using real-time validation

You have options here, you can create a custom method on your component to handle
submissions or you can use your regular old Flask routes. 

```py
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # do anything you need with your form data...
        return redirect(url_for("index"))
    return render_template("register_page.html")
```

# Custom events

You can use custom events to call a method in one component from a different component.
Let's extend the `counter` component above to listen for a `set-count` event, then build
a new component that emits it. To listen for the event, we just need to define a method
on the component and use the `@flask_meld.listen` decorator. No changes are needed to
the template.

```py
# app/meld/components/counter.py

from flask_meld import Component, listen


class Counter(Component):
    count = 0

    def add(self):
        self.count = int(self.count) + 1

    def subtract(self):
        self.count = int(self.count) - 1

    @listen("set-count")
    def set_count(self, count):
      self.count = count
```

Now let's define a second component `SetCount` that will have a text box and a button.
When a user clicks the button, we want to emit an event with the value from the text
box that can be picked up by the counter. To do this, we just use `flask_meld.emit`.


```py
# app/meld/components/set_count.py

from flask_meld import Component, emit


class SetCount(Component):
    value = 0

    def set_count(self):
        emit("set-count", count=self.value)
```

Note that the `count` argument to `emit` will be passed as a keyword argument to
the listening function. The template for this component is pretty simple,
we just need to define the text box and button and hook them to the Component.

```html
{# templates/meld/set_count.html #}
<div>
    <input type="text" meld:model="value"></input>
    <button meld:click="set_count">Set Count</button>
</div>
```

Finally, add `{% meld 'set_count' %}` to your page template and run the app!

Pretty simple right? You can use this to create very dynamic user interfaces
using pure Python and HTML. We would love to see what you have built using Meld
so please share!
