from flask import Flask, render_template


app = Flask(__name__)


if __name__ == '__main__':
    from views import *

    app.run(debug=True)
