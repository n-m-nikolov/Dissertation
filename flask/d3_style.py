from flask import Flask, render_template, request
import flask
import nltk
import requests
import re

app = Flask(__name__)
app.debug = True


@app.route('/tokenizer', methods=['GET', 'POST'])
def tokenizer():
    errors = []
    results = {}
    punct_results = {}
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
            punct_results = nonPunctText
    return render_template('tokenize.html', errors=errors, results=results, punct_results=punct_results)

@app.route('/dependency', methods=['GET', 'POST'])
def dependency():
    return render_template('dependency.html')

#TO DO: Create separate pages for selecting a grammar and for parsing with the selected grammar

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/dependency/non_projective', methods=['GET', 'POST'])
def non_projective():
    errors = []
    results = []
    sentence = ""
    rules = {}
    nodes = []
    if request.method == "POST":
        # get sentence that the user has entered
        try:
            if 'sentence' in request.form.keys():
                sentence = request.form['sentence']
        except BaseException as e:
            errors.append(
                "Unable to get Sentence. Please make sure it's valid and try again."
            )
            errors.append(e)
           # check the form with: errors.append(request.form)

        nltk.data.path.append('./nltk_data/')
        grammarPrint = ["\'taught\' -> \'play\' | \'man\'", "\'man\' -> \'the\'", "\'play\' -> \'golf\' | \'dog\' | \'to\'", "\'dog\' -> \'his\'"  ]
        grammar = nltk.DependencyGrammar.fromstring("\n".join(grammarPrint))
        dp = nltk.NonprojectiveDependencyParser(grammar)
        g, = dp.parse(['the', 'man', 'taught', 'his', 'dog', 'to', 'play', 'golf'])
        for _, node in sorted(g.nodes.items()):
            if node['word'] is not None:
                nodes.append('{address} {word}: {d}'.format(d=node['deps'][''], **node))

        rules = grammarPrint
        results.append(g.tree())

    return render_template('non_projective.html', errors=errors, results=results, rules=rules, nodes = nodes)

@app.route('/dependency/projective', methods=['GET', 'POST'])
def projective():
    errors = []
    results = []
    sentence = ""
    rules = {}
    nodes = []
    if request.method == "POST":
        # get sentence that the user has entered
        try:
            if 'sentence' in request.form.keys():
                sentence = request.form['sentence']
        except BaseException as e:
            errors.append(
                "Unable to get Sentence. Please make sure it's valid and try again."
            )
            errors.append(e)
           # check the form with: errors.append(request.form)

        nltk.data.path.append('./nltk_data/')
        grammarPrint = ["\'fell\' -> \'price\' | \'stock\'", "\'price\' -> \'of\' \'the\'", "\'of\' -> \'stock\'", "\'stock' -> 'the\'" ]
        grammar = nltk.DependencyGrammar.fromstring("\n".join(grammarPrint))
        dp = nltk.ProjectiveDependencyParser(grammar)
        for t in sorted(dp.parse(['the', 'price', 'of', 'the', 'stock', 'fell'])):
             results.append(t)

        rules = grammarPrint


    return render_template('projective.html', errors=errors, results=results, rules=rules, nodes = nodes)

app.run()

