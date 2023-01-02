from flask import Flask, render_template
from deta import Deta
import os

app = Flask(__name__)
deta = Deta(os.environ.get("DETA_PROJECT_KEY"))

words = deta.Base("words")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    is_repl = os.environ.get("REPL_SLUG", False)
    if is_repl:
        app.run(debug=True, host="0.0.0.0")
    else:
        app.run(debug=True)
