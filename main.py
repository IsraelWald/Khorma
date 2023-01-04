from flask import Flask, redirect, render_template, request, url_for
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
        form = request.form
        english = form.get("english")
        khorma = form.get("khorma")
        apos = form.get("apos", False)
        word = {
            "english": english,
            "khorma": khorma,
            "apos": apos if apos else "No Apostrophe Form",
        }
        words.insert(word)
        return redirect(url_for("index"))
    return render_template("add_word.html")

if __name__ == "__main__":
    is_repl = os.environ.get("REPL_SLUG", False)
    if is_repl:
        app.run(debug=True, host="0.0.0.0")
    else:
        app.run(debug=True)
