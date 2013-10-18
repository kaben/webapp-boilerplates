webapp-boilerplates
===================

Web application boilerplates.

This will be a set of web application boilerplates using various frameworks.

Currently it contains a single Flask boilerplate based on the RealPython
project at https://github.com/mjhea0/flask-boilerplate . The configuration
files 'Procfile' and 'requirements.txt' are for use on Heroku.

The original RealPython boilerplate lacks "separation of concerns" discussed in
the book of the same name. This may be because the separation of concerns
described in the text isn't completely successful, as the code in the original
views, models, and forms modules is tightly cross-dependent, which means the
modules can't be easily tested in isolation. Moreover the Blueprint examples in
the book have similar cross-dependencies.

In my own version of the boilerplate, I've isolated the forms and models from
the views, and the Blueprints from the main web application. Since concerns are
more-sucessfully separated, unit testing is easier, and my boilerplate should
make for more reliable web apps.
