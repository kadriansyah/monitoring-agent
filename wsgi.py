import logging
from logging.handlers import RotatingFileHandler
from monitor_endpoint import app

formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler = RotatingFileHandler('logs/flask.log', maxBytes=10000000, backupCount=1)
handler.setFormatter(formatter)
app.logger.setLevel(logging.INFO)
app.logger.addHandler(handler)

# testing using: uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
if __name__ == "__main__":
    app.run()