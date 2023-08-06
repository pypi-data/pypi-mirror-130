# Mad Oauth2

Mad Oauth2 app is an extention of django-oauth-toolkit that implements scopes and schemes in detail

## Quick start

1. Add "mad_oaut2" to your INSTALLED_APPS setting like this:

    ```python
    INSTALLED_APPS = [
        ...
        'mad_oauth2',
        'oauth2_provider',
    ]

    OAUTH2_PROVIDER_APPLICATION_MODEL="mad_oauth2.Oauth2Application"
    OAUTH2_PROVIDER = {
        "SCOPES_BACKEND_CLASS": "mad_oauth2.scopes.ApplicationScopes"
    }
    ```

2. Run ``python manage.py migrate`` to create mad_oauth2 models.
