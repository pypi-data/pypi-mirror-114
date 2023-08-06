===========================
Flask Api Sign Verification
===========================

.. image:: https://readthedocs.org/projects/flask-api-sign/badge/?version=latest
   :target: https://flask-api-sign.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://github.com/juforg/flask-api-sign/actions/workflows/publish-to-pypi.yml/badge.svg
   :target: https://github.com/juforg/flask-api-sign/actions/workflows/publish-to-pypi.yml
   :alt: Publish Python 🐍 distributions 📦 to PyPI and TestPyPI

Features
--------
* Testing setup with ``unittest`` and ``python setup.py test`` or ``py.test``
* Command line interface using Click

Quickstart
----------

Install the latest Cookiecutter if you haven't installed it yet ::

    pip install -U flask-api-sign



Then::

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


Links
-----

-   Documentation: https://flask-api-sign.readthedocs.io/en/latest/index.html
-   Changes: https://flask-api-sign.readthedocs.io/en/latest/history.html
-   PyPI Releases: https://pypi.org/project/flask-api-sign/
-   Source Code: https://github.com/juforg/flask-api-sign/
-   Issue Tracker: https://github.com/juforg/flask-api-sign/issues/
