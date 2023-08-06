# Mad Oauth2

Mad Oauth2 app is an extention of django-oauth-toolkit that implements scopes and schemes in detail

## Quick start

1. Add "mad_oaut2" to your INSTALLED_APPS setting like this:

    ```python
    INSTALLED_APPS = [
        ...
        'oauth2_provider',
        'mad_oauth2',
    ]

    OAUTH2_PROVIDER_APPLICATION_MODEL="mad_oauth2.Application"
    OAUTH2_PROVIDER = {
        "SCOPES_BACKEND_CLASS": "mad_oauth2.oauth2.ApplicationScopes"
    }
    ```

2. Run ``python manage.py migrate`` to create mad_oauth2 models.

## Clearing Expired Tokens

Run celery periodic task to clear expired tokens
`mad_oauth2.tasks.removeExpiredTokens`
