from flask import Flask, render_template, request, redirect, url_for
from md5 import *
from vigenere_cipher import *
import DES
import rsa
import os

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
    f2 = request.files['vkfile']
    key = f2.read().decode('utf-8')
    string = f.read().decode('utf-8')
    
    rk = keygen(key, string)
    steps = encrypt(key, string)
    steps2 = decrypt(key, steps)

    # l.append(rk)
    return render_template('vigenere.html', value=[rk, steps, steps2])


@app.route('/des', methods=['POST'])
def des():
    f1 = request.files['desfile']
    f2 = request.files['deskey']
    steps = DES.des_msg(f1.read(), f2.read())
    return render_template('des.html', value=steps)


@app.route('/rsa', methods=['POST'])
def render_rsa():
    f = request.files["rsafile"]
    # f.save(os.path.join('tempFiles'), f.filename)
    # fullPath = 'tempFiles/' + file.filename
    steps = rsa.rsa(f)
    # steps[10].save("/rsa/" + steps[10])
    # os.remove(fullPath)
    return render_template('rsa.html', value=steps)

if __name__ == '__main__':
    app.run(debug=True)
