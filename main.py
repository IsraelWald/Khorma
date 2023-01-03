from flask import Flask, render_template, request
from deta import Deta
import os

app = Flask(__name__)
deta = Deta(os.environ.get("DETA_PROJECT_KEY"))

words = deta.Base("words")


@app.route("/")
def index():
    khorma_words = words.fetch().items
    return render_template("index.html", words=khorma_words)

@app.route("/add-word", methods=["GET", "POST"])
def add_word():
    if request.method == "POST":
        ...
    return render_template("add_word.html")

if __name__ == "__main__":
    is_repl = os.environ.get("REPL_SLUG", False)
    if is_repl:
        app.run(debug=True, host="0.0.0.0")
    else:
        app.run(debug=True)
