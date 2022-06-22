from flask import Flask, render_template
import datetime
app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def hello():
	return render_template('index.html', utc_dt=datetime.datetime.utcnow())

@app.route('/about/')
def about():
	return '<h3>This is a flask web application.</h3>'

if __name__ == '__main__':
	app.run(host='localhost', port=8000, debug=True)
