=====
Usage
=====

To use Flask Api Sign in a project::

    import flask_api_sign

------------------------------
Configuring flask-api-sign
------------------------------
**flask-api-sign** is configured through the standard Flask config API. These are the available
options (each is explained later in the documentation):

* **SIGN_LOCATION** : default **query_string**

* **SIGN_TIMESTAMP_EXPIRATION** : default **30**

verification is managed through a ``ApiSignManager`` instance::

    from flask import Flask
    from flask_api_sign import ApiSignManager

    app = Flask(__name__)
    api_sign_mgr = ApiSignManager(app)

In this case all verification using the configuration values of the application that
was passed to the ``ApiSignManager`` class constructor.

Alternatively you can set up your ``ApiSignManager`` instance later at configuration time, using the
**init_app** method::

    from flask import Flask
    api_sign_mgr = ApiSignManager()
    app = Flask(__name__)
    api_sign_mgr.init_app(app)

In this case verification will use the configuration values from Flask's ``current_app``
context global. This is useful if you have multiple applications running in the same
process but with different configuration options.


::::::::::::::::::::::::::::
Flask Api Sign Verification
::::::::::::::::::::::::::::
To generate a serial number first create a ``ApiSignManager`` instance::

    from flask import Flask
    from flask_api_sign import ApiSignManager
    from flask_api_sign import verify_sign

    app = Flask(__name__)

    api_sign_mgr = ApiSignManager()
    api_sign_mgr.init_app(app)
    @app.route("/")
    @verify_sign
    def index():
        pass
