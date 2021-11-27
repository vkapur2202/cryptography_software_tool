from flask import Flask, render_template, request, redirect, url_for
from md5 import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/md5', methods=['POST'])
def md5():
    f = request.files['md5file']
    steps = md5sum(f.read())
    return render_template('md5.html', value=steps)
    
if __name__ == '__main__':
   app.run(debug = True)