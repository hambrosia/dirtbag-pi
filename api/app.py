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
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5000, host='0.0.0.0')
