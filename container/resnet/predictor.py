# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.

from __future__ import print_function

import os
import json
import sys
import signal
import traceback

import flask
from flask import Flask, render_template, request, Response, jsonify

from classify import classify
prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model')

model_paths = [ os.path.join(model_path, model) for model in os.listdir(model_path) ]
model_path = model_paths[-1]

CF = classify()
pretrained_model = CF.get_model(model_path)
# A singleton for holding the model. This simply loads the model and holds it.
# It has a predict function that does a prediction based on the model and the input data.


# The flask app for serving predictions
app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    health = pretrained_model is not None  # You can insert a health check here

    status = 200 if health else 404
    return flask.Response(response='\n', status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def transformation():
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    # data = None

    # # Convert from CSV to pandas
    # if flask.request.content_type == 'text/csv':
    #     data = flask.request.data.decode('utf-8')
    #     s = io.StringIO(data)
    #     data = pd.read_csv(s, header=None)
    # else:
    #     return flask.Response(response='This predictor only supports CSV data', status=415, mimetype='text/plain')

    # print('Invoked with {} records'.format(data.shape[0]))

    # # Do the prediction
    # predictions = ScoringService.predict(data)

    # # Convert from numpy back to CSV
    # out = io.StringIO()
    # pd.DataFrame({'results':predictions}).to_csv(out, header=False, index=False)
    # result = out.getvalue()

    ######################################################################################
    try:
        data = request.get_json()
        img = data['img']
    except Exception:
        return jsonify({'message': 'Content is not string type'}), 400
    category = CF.classfy(pretrained_model, img)
    result = {
        "category" : category
    }

    result = jsonify(result)
    return result
