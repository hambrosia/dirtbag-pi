"""DirtBag Pi is a network-connected garden and plant monitor.
This module prepopulates the Postgres database with a reading and prerenders the html for the graph.
It starts the scheduler to update the database and graph at a specified interval.
It begins serving the graph with Flask.
 """
import flask

import startup

# Create first reading, prerender html, start scheduler
startup.on_startup()

# API setup
app = flask.Flask(__name__)
app.config["DEBUG"] = True


# Main endpoint
@app.route('/', methods=['GET'])
def home() -> None:
    """Start serving the graph with Flask"""
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5000, host='0.0.0.0')
