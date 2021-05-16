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
import numpy as np

prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model')

main_model_path = os.path.join(model_path, 'main_model.h5')
sub_model_chair_path = os.path.join(model_path, 'sub_model_chair.h5')
sub_model_bed_path = os.path.join(model_path, 'sub_model_bed.h5')

CF = classify()
main_model = CF.get_model(main_model_path)
sub_model_chair = CF.get_model(sub_model_chair_path)
sub_model_bed = CF.get_model(sub_model_bed_path)

# A singleton for holding the model. This simply loads the model and holds it.
# It has a predict function that does a prediction based on the model and the input data.


# The flask app for serving predictions
app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    health = main_model is not None  # You can insert a health check here

    status = 200 if health else 404
    return flask.Response(response='\n', status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def transformation():
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    try:
        data = request.get_json()
        img = data['img']
        img = np.array(img)
    except Exception:
        return jsonify({'message': 'Content is not string type'}), 400
    
    category1, category2, category3, category4 = CF.main_classify(img, main_model)

    if category1[0] == '의자':
        standard = CF.sub_classify(img, CF.chair_subclass, sub_model_chair)
    elif category1[0] == '침대':
        standard = CF.sub_classify(img, CF.bed_subclass, sub_model_bed)
    else :
        standard = ''

    result = {
        "category" : [category1, category2, category3, category4],
        "standard" : standard
    }

    result = jsonify(result)
    return result
