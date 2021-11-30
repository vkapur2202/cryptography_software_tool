from flask import Flask, render_template, request, redirect, url_for
from md5 import *
from vigenere_cipher import *
import DES

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
    #repeated_key = keygen("YTWdw", f.read())
    # step1 = encrypt("YTWdw", f.read())
    # steps2 = decrypt("YTWdw", step1)
    # steps = "The decrypted message is " + steps2
    # b_repeated_key = b_keygen(f2.read(), f.read())
    # b_steps = b_encrypt(f2.read(), f.read())
    # b_steps2 = b_decrypt(f2.read(), f.read())
    # f = request.files.getlist("vfile[]")
    # for files in request.files.getlist("vfile[]"):
    #     if files.filename == "test1":
    #         f = files
    #     else:
    #         f2 = files
    #rk = keygen(f2.read().decode('utf-8'), f.read().decode('utf-8'))
    steps = encrypt(f2.read().decode('utf-8'), f.read().decode('utf-8'))
    steps2 = decrypt("UTIWG", steps)
    return render_template('vigenere.html', value=steps2)


@app.route('/des', methods=['POST'])
def des():
    f = request.files.getlist("desfile[]")
    steps = DES.des_msg(f[0].read(), f[1].read())
    return render_template('des.html', value=steps)

@app.route('/rsa', methods=['POST'])
def rsa():
    f = request.files["rsafile"]
    steps = rsa.rsa(f)
    return render_template('rsa.html', value=steps)

if __name__ == '__main__':
    app.run(debug=True)
