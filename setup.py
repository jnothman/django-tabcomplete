try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup  # NOQA

import django_tabcomplete


setup(
    name='django-tabcomplete',
    version=django_tabcomplete.__version__,
    description="IPython tab completion for Django ORM models",
    author='Joel Nothman',
    author_email='joel.nothman@gmail.com',
    url='http://github.com/jnothman/django-tabcomplete',
    license='BSD License',
    platforms=['any'],
    install_requires=['IPython', 'django', 'six>=1.2'],
    tests_require=[],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Utilities',
    ],
)
