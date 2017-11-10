from flask import Flask
import controllers_devices

app = Flask(__name__)
app.register_blueprint(controllers_devices.blue_print)
app.secret_key = 'T\x94 \x03\xd9\x896fF\xcc(\\b4B\x1b\xa2\x92g\xd8\x06\xdc\x1d$'


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=False)
