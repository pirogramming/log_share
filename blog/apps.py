from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'
    default_app_config = 'full.python.path.to.your.app.foo.apps.blog'