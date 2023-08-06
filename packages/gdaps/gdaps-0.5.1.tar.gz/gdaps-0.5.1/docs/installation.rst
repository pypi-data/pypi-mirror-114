Installation
============

Install GDAPS in your Python virtual environment. If you want to create plugins, install cookiecutter too.

.. code-block:: bash

    pip install gdaps cookiecutter


Create a Django application as usual: ``django-admin startproject myproject``.

First, set a variable named ``PROJECT_NAME``.

.. code-block:: python

    PROJECT_NAME = "myproject"

This is a (machine) name for your project. Django itself does not provide such a name. It will be used in various places. Must be a valid python identifier.

.. note::

    ``PROJECT_NAME`` is roughly what Django means with ``ROOT_URLCONF[0]``, but GDAPS requires it to be set explicitly.

Now add "gdaps" to the ``INSTALLED_APPS`` section, and add a special line below it:

.. code-block:: python

    from gdaps.pluginmanager import PluginManager

    INSTALLED_APPS = [
        # ... standard Django apps and GDAPS
        "gdaps",
    ]
    # The following line is important: It loads all plugins from setuptools
    # entry points and from the directory named 'myproject.plugins':
    INSTALLED_APPS += PluginManager.find_plugins(PROJECT_NAME + ".plugins")

You can use whatever you want for your plugin path, but we recommend that you use "**<PROJECT_NAME>.plugins**" here to make things easier. Basically, this is all you really need so far, for a minimal working GDAPS-enabled Django application. See :doc:`usage` for how to use GDAPS.

URL handling
------------
Now add the URL path for GDAPS, so it can add plugins' URLs automatically to the global urlpattern.

.. code-block:: python

    # urls.py
    from gdaps.pluginmanager import PluginManager

    urlpatterns = PluginManager.urlpatterns() + [
        # ... add your fixed URL patterns here, like "admin/", etc.
    ]

This way each plugin can have an `urlpatterns` variable in `urls.py`, and all are merged together. However, by now, the plugin order is not determined, so urlpatterns too are not in a deterministically determined order. This could lead to problems, depending on your application design, so keep that in mind when designing plugins.

Logging
-------
Django does not write loggings to the command line automatically. GDAPS uses various levels of logging. It is recommended that you create a LOGGING section in settings.py for GDAPS:

.. code-block:: python

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {"console": {"class": "logging.StreamHandler"}},
        "loggers": {
            "gdaps": {"handlers": ["console"], "level": "INFO", "propagate": True},
        },
    }

This will output all GDAPS log messages to the console.

Frontend support
----------------

If you want to add frontend support to your project, you need to add ``gdaps.frontend`` (before  ``gdaps``!), and ``webpack_loader`` to Django.

Frontend engines are packed in plugin eggs. You can easily install them using pip, e.g.

.. code-block:: bash

    pip install gdaps-frontend-vue

Then you have to tell Django which engine to use:

.. code-block:: python

    GDAPS = {
        "FRONTEND_ENGINE": "vue",
    }

Further configuration may be necessary depending on your frontend plugin.
Available plugins ATM:

* `Vue <https://gdaps-frontend-vue.readthedocs.io>`_
* PySide (currently only stub)

There are some keys in this section to configure:


``FRONTEND_DIR``
^^^^^^^^^^^^^^^^
This is the directory for the frontend, relative to DJANGO_ROOT.

Default: ``frontend``

``FRONTEND_ENGINE``
^^^^^^^^^^^^^^^^^^^
The engine which is used for setting up a frontend. ATM it can only be "vue". In future, maybe other engines are supported (Angular, React, etc.). PRs welcome.

``FRONTEND_PKG_MANAGER``
^^^^^^^^^^^^^^^^^^^^^^^^
This is the package manager used to init/install packages. It depends on your frontend which are available.

``PROJECT_TITLE``
^^^^^^^^^^^^^^^^^
A title for your project. If left empty, PROJECT_NAME is taken (without hyphens/underlines and capitalized).

Default: ``PROJECT_NAME``, without underlines and capitalized.

``ADMIN``
^^^^^^^^^
True if your app should add the GDAPS specific parts to the Django admin panel. You can e.g. see the installed plugins there.

Default: ``True``


Final step
----------
Now you can initialize the frontend with

.. code-block:: bash

    ./manage.py initfrontend

This creates a basic boilerplate frontend, depending on which engine is installed.
