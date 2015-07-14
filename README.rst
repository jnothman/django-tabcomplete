Django TabComplete
==================

What?
-----

Tab completion over Django model fields in IPython.

Example::

    User.objects.filter(us<tab>

becomes::

    User.objects.filter(username

and::

    User.objects.filter(username__st<tab>

becomes::

    User.objects.filter(username__startswith=

Related fields are also supported::

    User.objects.filter(grou<tab>ps__<tab>permis<tab>sions__n<tab>ame__sta<tab>rtswith

How?
----

Install it from PyPI with::

    $ pip install django-tabcomplete

then add it to your Django project's ``settings.py``::

    INSTALLED_APPS = [
        ...
        'django_tabcomplete',
    ]


Why?
----

For users of the Django ORM who frequently construct custom queries in
interactive shells, it can be a challenge to remember field names on
inter-related models. For such situations was tab completion invented,
but while IPython provides tab completion for named function arguments,
this does not extend to dynamic keyword arguments (i.e. whose names are
not provided in the code or docstring).

Limitations
-----------

Currently tab completion is only supported on ``filter`` and ``exclude``
methods of ``Manager`` or ``QuerySet`` objects that are referred to by a
variable name or a sequence of attribute lookups. Thus no completion is
provided for::

    User.objects.all().filter(us<tab>

Nor can we currently provide tab completion in ``Q`` objects, though they can
perform the same function, or in aggregates to name fields, because the target
model cannot be identified locally.

More?
-----

We intend to add tab completion for other ``QuerySet`` methods that take
field names as keyword arguments or as positional strings.

Pull requests are welcome!
