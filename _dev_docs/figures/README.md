Steps to create visualization of database:
==========================================

1. `pip3 install django-extensions`

2. Add it in installed apps. In settings.py
```
INSTALLED_APPS = (
    ...
    'django_extensions',
    ...
)
```

3. `sudo apt-get install -y python-pygraphviz`

4. Generate pic: `python3 manage.py graph_models -a -o myapp_models.png`
