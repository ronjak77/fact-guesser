# Fact Guesser App

This is an API for a fact listing application. The users of the application can give Yes/No answers to propositions that have been entered into the system by authenticated users. 
The purpose of the project is to learn more about Django Rest Framework and web development in general.

# Instructions for installation

The project uses Python 2.7.6, Django 1.9 and Django Rest Framework 3.7.1. 
To install Django and other python packages, you need pip (https://pip.pypa.io/en/stable/installing/). 
You also need virtualenv (installation instructions here https://virtualenv.pypa.io/en/stable/installation/).
To clone the codebase, you need git (https://git-scm.com/downloads).

### Create a virtualenv to isolate our package dependencies locally
virtualenv env
source env/bin/activate  # On Windows use `env\Scripts\activate` with no 'source'

### Install Django and Django REST framework into the virtualenv
To run this program, you need version 1.9 of Django at the moment. You also need Django Rest Framework.

    pip install django==1.9
    pip install djangorestframework

The documentation has also some additional dependencies, install these like this:

    pip install coreapi
    pip install pygments
    pip install markdown

## Cloning the project

Clone the repository:

    git clone https://github.com/ronjak77/fact-guesser.git

## Setting environment variable 'SECRET_KEY'

Depending on your operating system, this is done differently. For example, for Windows you can do it using Powershell with this command:

    $env:SECRET_KEY = "key here"
    
and for Ubuntu using bash

    export SECRET_KEY="key here"
    
For some environments, such as Heroku or c9.io, you might need to consult their documentation to figure out how to set this.

## Starting the server from the Terminal

To start the server, run 

    $ python manage.py runserver
    
### Other notes

To create a new Admin user, use

    $ python manage.py createsuperuser

You can run the included tests with

    $ python manage.py test

# Support & Documentation

The documentation for the API endpoints for this project can be found at https://fact-guesser-ronjak77.c9users.io/docs/

An CoreAPI Schema can be found at https://fact-guesser-ronjak77.c9users.io/schema/

A live version of the API is located at https://fact-guesser-ronjak77.c9users.io/ 

For troubleshooting purposes, you can find a list of installed Python packages included as a text file in the repository ("installed packages.txt"). 

Django docs can be found at https://www.djangoproject.com/

You may also want to follow the Django tutorial to create your first application:
https://docs.djangoproject.com/en/1.9/intro/tutorial01/