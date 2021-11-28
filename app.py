from flask import Flask, render_template, request, redirect, url_for
from md5 import *
from vigenere_cipher import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/md5', methods=['POST'])
def md5():
    f = request.files['md5file']
    steps = md5sum(f.read())
    return render_template('md5.html', value=steps)

@app.route('/vigenere', methods=['POST'])
def vigenere():
    f = request.files['vfile']
    #f2 = request.files['vkfile']
    #repeated_key = keygen(f2.read(), f.read())
    steps = encrypt("YTWdw34@", f.read())
    steps2 = decrypt("YTWdw34@", f.read())

    #b_repeated_key = b_keygen(f2.read(), f.read())
    #b_steps = b_encrypt(f2.read(), f.read())
    #b_steps2 = b_decrypt(f2.read(), f.read())

    return render_template('vigenere.html', value=steps)
    
if __name__ == '__main__':
   app.run(debug = True)