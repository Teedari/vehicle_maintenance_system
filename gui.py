#gui.py

from flaskwebgui import FlaskUI
from app.wsgi import application

ui = FlaskUI(application, start_server='django')
ui.run()

