import json
import os
from flask import Flask, render_template, request, url_for, redirect, send_from_directory, flash, current_app
from werkzeug.utils import secure_filename
import nltk
import re
from nltk.parse import (
    DependencyGraph,
    ProjectiveDependencyParser,
    NonprojectiveDependencyParser,
)





app = Flask(__name__, static_folder='s1245947/static/')

#A file in which site errors will be written, because the server has no visible error messages.
f1 = open('./siteerror.txt','w+')



app.debug = True

#Add remove punctuation function to dependency graph object
def remove_punct(self):
    print(self.nodes)
DependencyGraph.remove_punct = remove_punct

#Tokenizer Page - outputs sentence as tokens. Not Active
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


@app.route('/data/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename, as_attachment=True)


@app.route('/dependency', methods=['GET', 'POST'])
def dependency():
    return render_template('dependency.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
     return render_template('home.html')


@app.route('/projective_tree', methods=['GET', 'POST'])
def proj_tree():
    return render_template('projective_tree.html')

#Non Projective Dependecy Tree page. Not Active
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
        grammarPrint = ["\'taught\' -> \'play\' | \'man\'", "\'man\' -> \'the\'",
                        "\'play\' -> \'golf\' | \'dog\' | \'to\'", "\'dog\' -> \'his\'"]
        grammar = nltk.DependencyGrammar.fromstring("\n".join(grammarPrint))
        dp = nltk.NonprojectiveDependencyParser(grammar)
        g, = dp.parse(['the', 'man', 'taught', 'his', 'dog', 'to', 'play', 'golf'])
        for _, node in sorted(g.nodes.items()):
            if node['word'] is not None:
                nodes.append('{address} {word}: {d}'.format(d=node['deps'][''], **node))

        rules = grammarPrint
        results.append(g.tree())

    return render_template('non_projective_tree_version.html', errors=errors, results=results, rules=rules, nodes=nodes)

#Projective Dependecy Tree page. Not Active
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
        grammarPrint = ["\'fell\' -> \'price\' | \'stock\'", "\'price\' -> \'of\' \'the\'", "\'of\' -> \'stock\'",
                        "\'stock' -> 'the\'"]
        grammar = nltk.DependencyGrammar.fromstring("\n".join(grammarPrint))
        dp = nltk.ProjectiveDependencyParser(grammar)
        for t in sorted(dp.parse(['the', 'price', 'of', 'the', 'stock', 'fell'])):
            results.append(t)

        rules = grammarPrint

    return render_template('projective_tree_version.html', errors=errors, results=results, rules=rules, nodes=nodes)


@app.route('/dependency/dependency_graph', methods=['GET', 'POST'])
def dependency_graph():
    errors = []
    results = []
    sentence = ""
    rules = {}
    nodes = []
    grammar = ""
    tags = []
    words = []  #words extracted from the graph
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
        #folder for ntlk
        nltk.data.path.append('./nltk_data/')
        #code for TREE implementation, grammar rules to be printed
        grammarPrint = ["\'fell\' -> \'price\' | \'stock\'", "\'price\' -> \'of\' \'the\'", "\'of\' -> \'stock\'",
                        "\'stock' -> 'the\'"]
        #the grammar rules for nltk
        grammar_rules = nltk.DependencyGrammar.fromstring("\n".join(grammarPrint))
        dp = nltk.ProjectiveDependencyParser(grammar_rules)



        for t in sorted(dp.parse(['the', 'price', 'of', 'the', 'stock', 'fell'])):
            results.append(t)

        #rules = grammarPrint


    return render_template('dependency_graph.html', errors=errors, results=results, rules=rules,
                       nodes=nodes)  #CREDIT: http://code.runnable.com/UiPcaBXaxGNYAAAL/how-to-upload-a-file-to-the-server-in-flask-for-python
#FOR UPLOADING FILES

# This is the path to the upload directory
#app.config['UPLOAD_FOLDER'] = 'C:/dissertation/Dissertation/flask/uploads/'
app.config['UPLOAD_FOLDER'] = '/public/homepages/s1245947/data/'

# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'json'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=['GET', 'POST'])
def render_upload():
    return render_template('upload.html')


# Route that will process the file upload
@app.route('/uploaded', methods=['POST'])
def upload():
    #definitions
    errors = []
    messages = []  # within this block, current_app points to app.
    results = []
    sentence = ""
    rules = {}
    nodes = []
    grammar = ""
    tags = []
    words = []  #words extracted from the graph
    #json skeleton
    json_file = {}
    names = []
    links = []
    # Get the name of the uploaded file
    file = request.files['file']
    if request.files['file'].filename == '':
        #messages.append('No file was uploaded.')
        flash(u'You have not chosen a file to upload!', 'error')
        return render_template('upload.html')
    # Check if the file is one of the allowed types
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        text = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r')
        #errors.append(text)
        for line in text:
            grammar = grammar + line
        #Check if the file starts and ends with three "\"" and remove them from th  # within this block, current_app points to app.e front and back.
        if (grammar[0] == "\"" and grammar[1] == "\"" and grammar[2] == "\"" and grammar[-1] == "\"" and grammar[-2] == "\"" and grammar[-3] == "\""):
            grammar = grammar[3:-3]
        #extract the sentence from the ConLL file to remove punctuation

        for line in grammar.split('\n'):
            sentence += line.split(' ', 1)[0] + " "
        #remove trailing space character
        sentence.strip()
        #Tokenize the sentence and remove punctuation
        #tokens = nltk.word_tokenize(sentence)
        #no_punct_sent = nltk.Text(tokens)
        #nonPunctRegEx = re.compile('.*[A-Za-z].*')
        #nonPunctText = [w for w in no_punct_sent if nonPunctRegEx.match(w)]
        
        
        ##Try to parse the file passed by the upload page. If not possible raise an error
        f1.write(grammar)
        dg = DependencyGraph(grammar)
        try:
            dg = DependencyGraph(grammar)
            for node in dg.nodes:  #For each node in the graph aquire the needed information
                #skip root node
                if dg.nodes[node]["address"] == 0:
                    continue
                tags.append(dg.nodes[node]['tag'])  #tags
                words.append(dg.nodes[node]['word'])  #words
                #skip link for the root - verb
                if dg.nodes[node]["head"] == 0:
                    nodes.append({"name":dg.nodes[node]['word'], "group":1, "tag":dg.nodes[node]['tag'], "governor":"ROOT", "relation":dg.nodes[node]['rel']})
                    continue
                nodes.append({"name":dg.nodes[node]['word'], "group":1, "tag":dg.nodes[node]['tag'], "governor":dg.nodes[dg.nodes[node]['head']]['word'], "relation":dg.nodes[node]['rel']})
                links.append({"source":dg.nodes[node]["head"]-1, "target":dg.nodes[node]["address"]-1, "value":3})
        
                #fill the json skeleton parts - nodes and links with the information from the dependency graph
                # for word in words:
                #     nodes.append({"name":word, "group":1})
            json_file["nodes"] = nodes
            json_file["links"] = links
            json_file = json.dumps(json_file)
            text.close()
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
            return render_template('dependency_graph.html', json_file=json_file)
        except Exception as e:
                text.close()
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                f1.write(str(e))
                flash(u'Wrong file formatting! Pleace check the spacing between the rows of the ConLL grammar file.', 'error')
                return render_template('upload.html')

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/test')
def test():
    return render_template('test.html')


#Fix secret key error, for error alert message, when user tries to upload NO file
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
#Get passed the secret key error in Flask
if __name__ == "__main__":
    app.run()

