from flask import Flask, views
import flask

app = Flask(__name__)
app.debug = True


class View(flask.views.MethodView) :
    def get(self):
        return flask.render_template('index.html')

class Random(flask.views.MethodView):
    def get(self):
        return flask.render_template('random.html')


app.add_url_rule('/', view_func=View.as_view('main'))
app.add_url_rule('/random', view_func=Random.as_view('random'))
# @app.route('/index')
# def hello_world():
#     return flask.render_template('index.html')



app.run()
