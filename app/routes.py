from app import app
from flask import render_template, request, jsonify
import requests
import os
import json


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/add_card', methods=['POST'])
def add_card():
    response = requests.post("https://tntnp9pg8q3.sandbox.verygoodproxy.com/post",
                             {'card_number': request.form['card_number'],
                              'exp_date': request.form['exp_date'],
                              'cvv': request.form['cvv']})
    data = response.content.decode('utf-8').replace("'", '"')
    content = json.loads(data)['form']
    return render_template('cards.html', content=content)


@app.route("/forward", methods=['POST'])
def forward():
    content = {'card_number': request.form['card_number'],
               'exp_date': request.form['exp_date'],
               'cvv': request.form['cvv']}

    os.environ['HTTPS_PROXY'] = 'https://USbJhTGe5opEtjnn5NuWDynU:3d3e1bf3-e9f5-4e73-9e6d-590c482a606c@tntnp9pg8q3.SANDBOX.verygoodproxy.com:8080'
    response = requests.post('https://echo.apps.verygood.systems/post',
                        json=content,
                        verify=os.path.abspath('app/cert.pem'))

    data = response.content.decode('utf-8').replace("'", '"')
    content = json.loads(json.loads(data)['data'])
    return render_template('forward.html', content=content)
