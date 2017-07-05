Steps to create visualization of database:

1. `pip install django-extensions`

2. Add it in installed apps. In settings.py
```
INSTALLED_APPS = (
    ...
    'django_extensions',
    ...
)
```

3. `sudo apt-get install -y python-pygraphviz`

4. Generate pic: `python manage.py graph_models -a -o myapp_models.png`