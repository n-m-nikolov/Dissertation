from flask import Flask, render_template, request
import flask
import nltk
import requests

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    sentence = ""
    if request.method == "POST":
        # get sentence that the user has entered
        try:
            sentence = request.form['sentence']
        except BaseException as e:
            errors.append(
                "Unable to get Sentence. Please make sure it's valid and try again."
            )
            errors.append(e)
        if sentence:
            nltk.data.path.append('./nltk_data/')
            tokens = nltk.word_tokenize(sentence)
            text = nltk.Text(tokens)
            results = text
    return render_template('tokenize.html', errors=errors, results=results)


app.run()

