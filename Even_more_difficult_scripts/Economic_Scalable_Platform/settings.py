# ecommerce/settings.py
INSTALLED_APPS = [
    # ...
    'accounts.apps.AccountsConfig',
    'products.apps.ProductsConfig',
    # ...
]

AUTH_USER_MODEL = 'accounts.User'