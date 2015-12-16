import json
import os
from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from werkzeug.utils import secure_filename
import flask
import nltk
import requests
import re
from nltk.grammar import DependencyGrammar
from nltk.parse import (
                        DependencyGraph,
                        ProjectiveDependencyParser,
                        NonprojectiveDependencyParser,
                        )


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

@app.route('/projective_tree', methods=['GET', 'POST'])
def proj_tree():
    return render_template('projective_tree.html')


@app.route('/dependency/non_projective_tree_version', methods=['GET', 'POST'])
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

    return render_template('non_projective_tree_version.html', errors=errors, results=results, rules=rules, nodes = nodes)

@app.route('/dependency/projective_tree_version', methods=['GET', 'POST'])
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


    return render_template('projective_tree_version.html', errors=errors, results=results, rules=rules, nodes = nodes)

@app.route('/dependency/projective_graph', methods=['GET', 'POST'])
def projective_graph():
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
        conll = send_from_directory(app.config['UPLOAD_FOLDER'], 'treebank_data.txt')

        text = open(app.config['UPLOAD_FOLDER']+'treebank_data.txt', 'r')
        #errors.append(text)
        for line in text:
            print(line.strip())
        text.close()

        for t in sorted(dp.parse(['the', 'price', 'of', 'the', 'stock', 'fell'])):
             results.append(t)

        rules = grammarPrint


    return render_template('projective_graph.html', errors=errors, results=results, rules=rules, nodes = nodes)
#CREDIT: http://code.runnable.com/UiPcaBXaxGNYAAAL/how-to-upload-a-file-to-the-server-in-flask-for-python
#FOR UPLOADING FILES

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'C:/dissertation/Dissertation/flask/uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'json'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET', 'POST'])
def render_upload():
    return render_template('upload.html')

# Route that will process the file upload
@app.route('/uploaded', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return redirect(url_for('uploaded_file',
                                filename=filename))

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
app.run()
url_for('static', filename='projective_tree.json')
url_for('static', filename='non_projective_tree.json')
