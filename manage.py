# -*- coding: utf-8 -*-
"""
This is the entry point of the Flask application.
"""

from flask_script import Manager

from app import LOGGER, create_app

# The logger should always be used instead of a print(). You need to import it from
# the app package. If you want to understand how to use it properly and why you
# should use it, check: http://bit.ly/2nqkupO
LOGGER.info('Server has started.')

# Creates the Flask application object that we use to initialize things in the app.
app = create_app()

# Initializes the Manager object, which allows us to run terminal commands on the
# Flask application while it's running (using Flask-Script).
manager = Manager(app)

# Starts the Flask app.
if __name__ == '__main__':
    manager.run()
