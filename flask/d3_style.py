from flask import Flask, render_template, request
import flask
import nltk
import requests
import re

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    sentence = ""
    nopunct = ""
    if request.method == "POST":
        # get sentence that the user has entered
        try:
            if 'sentence' in request.form.keys():
                sentence = request.form['sentence']
            if 'nopunct_tokenizer' in request.form.keys():
                nopunct = request.form['nopunct_tokenizer']
        except BaseException as e:
            errors.append(
                "Unable to get Sentence. Please make sure it's valid and try again."
            )
            errors.append(e)
           # check the form with: errors.append(request.form)
        if sentence:
            nltk.data.path.append('./nltk_data/')
            tokens = nltk.word_tokenize(sentence)
            text = nltk.Text(tokens)
            results = text
        if nopunct:
            nltk.data.path.append('./nltk_data/')
            tokens = nltk.word_tokenize(nopunct)
            text = nltk.Text(tokens)
            nonPunct = re.compile('.*[A-Za-z].*')
            nonPunctText = [w for w in text if nonPunct.match(w)]
            results = nonPunctText
    return render_template('tokenize.html', errors=errors, results=results)


app.run()

