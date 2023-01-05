from flask import Flask, redirect, render_template, request, url_for, flash
from deta import Deta
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "hello world"
deta = Deta(os.environ.get("DETA_PROJECT_KEY"))

words = deta.Base("words")


@app.route("/")
def index():
    khorma_words = words.fetch().items
    khorma_words = sorted(khorma_words, key=lambda word: word["english"])
    return render_template("index.html", words=khorma_words)


@app.route("/add-word", methods=["GET", "POST"])
def add_word():
    if request.method == "POST":
        form = request.form
        english = form.get("english")
        khorma = form.get("khorma")
        apos = form.get("apos", False)
        apos_meaning = form.get("apos-meaning", False)
        if apos and apos_meaning:
            apos = (apos, apos_meaning)
        elif (apos and not apos_meaning) or (apos_meaning and not apos):
            flash("Error: Cannot enter only one of 'Apostrophe Form' or 'Apostrophe Meaning'")
            return redirect(url_for("add_word"))
        word = {
            "english": english,
            "khorma": khorma,
            "apos": apos if apos else "No Apostrophe Form",
        }
        words.insert(word)
        return redirect(url_for("index"))
    return render_template("add_word.html")

@app.route("/word/<id>")
def word(id):
    word = words.get(id)
    return render_template("word.html", word=word)

if __name__ == "__main__":
    is_repl = os.environ.get("REPL_SLUG", False)
    if is_repl:
        app.run(debug=True, host="0.0.0.0")
    else:
        app.run(debug=True)
