[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# django-identities

## Releases

This project follows the [semantic versioning specification](https://semver.org/) for its releases.

## Development

### Requirements

- Python >=3.7
- Django >=3.2
- django-rest-framework >=3.12

### Setup

- Create and activate a python3 venv.
- Install the library in the editable mode `pip install -e .[test]`
- Install dev requirements `pip install -r requirements-dev.txt`.
- Install git hooks to automatically format code using black with `pre-commit install`

## Installation

### From git in `requirements.txt`

1. To install this package from this git repository, add the `django-identities` package to the `requirements.txt` file.

2. Add `guardian` and `identities` to `settings.INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    #...
    'guardian',
    'identities',
    #...
)
```

3. Add the following to your `settings`, replacing all values with `REPLACE` with your configuration:

```python
AUTH_USER_MODEL = "identities.User"
GUARDIAN_MONKEY_PATCH = False
GUARDIAN_GET_INIT_ANONYMOUS_USER = "identities.models.get_anonymous_user_instance"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
]

AUTHLIB_OAUTH_CLIENTS = {
    "identity_provider": {
        "client_id": "REPLACE OIDC client_id",
        "client_secret": "REPLACE OIDC client_secret",
        "server_metadata_url": "REPLACE OIDC config_url",
        "client_kwargs": {"scope": "openid email profile"},
    }
}
LOGIN_REDIRECT_URL = "REPLACE OIDC login_redirect_url"
LOGOUT_REDIRECT_URL = "REPLACE OIDC logout_redirect_url"
```

4. In `<app>/urls.py`, extend `urlpatterns` like this:

```python
urlpatterns = [
    #...
    re_path(r"^backend/identity/", include("identities.urls")),
    re_path(
        r"^backend/identity/auth/local/",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
    #...
]
```

5. Extend the file `<app>/templates/rest_framework/base.html` with the following:

```html
{% if user.is_authenticated %}
<li class="dropdown">
  <a href="#" class="dropdown-toggle" data-toggle="dropdown">
    {{ user.email }}
    <b class="caret"></b>
  </a>
  <ul class="dropdown-menu" style="padding: 0;">
    <form action="{% url 'identities:oidc-logout' %}" method="post">
      {% csrf_token %}
      <button name="logout" value="logout" class="btn btn-default btn-block">
        Log out
      </button>
    </form>
  </ul>
</li>
{% else %}
<li>
  <a href="{% url 'identities:oidc-authenticate' %}">Log in (federation)</a>
</li>
<li>
  <a href="{% url 'rest_framework:login' %}">Log in (local)</a>
</li>
{% endif %}
```

6. Run `./manage.py migrate`

7. Restart your application server
