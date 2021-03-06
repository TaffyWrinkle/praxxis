"""
This training code is hosted on the server. it runs a nightly re-train of the
LSTM model.
"""
"""http://nmnode-0-svc:50070/webhdfs/v1/praxxis?op=LISTSTATUS"""
PRAXXIS_ROOT = "http://nmnode-0-svc:50070/webhdfs/v1/praxxis/"

import json
import requests
from datetime import date, timedelta


def train():
    """the app entry point"""
    sequences = get_sequences()
    model, converter = get_model()
    if model is None:
        write_model(model, converter)
    elif sequences == []:
        write_model(model, converter)
        # write model without training
    else:
        nightly_train(model, converter, sequences)

    return str(sequences)


def nightly_train(model, converter, sequences):
    """runs a nightly train on a preexisting model"""
    # train
    write_model(model, converter)


def create(model, converter, sequences):
    """creates a new model from data"""
    # create
    write_model(model, converter)


def write_model(model, converter):
    """writes back model and converter to HDFS"""
    pass
    # writes model back


def get_model():
    """fetches model and converter from HDFS"""
    # TODO: clean this the heck up
    # TODO: return none for model if doesn't exist
    from keras.models import load_model
    from sklearn.externals import joblib

    date_path = (date.today() - timedelta(days=1)).strftime('%Y/%m/%d/model/')

    global PRAXXIS_ROOT
    basepath = PRAXXIS_ROOT + date_path

    MODEL_NAME = "lstm_model.h5"
    CONVERTER_NAME = "convert.pkl"

    modelpath = basepath + MODEL_NAME
    converterpath = basepath + CONVERTER_NAME

    params = (
        ('op', 'OPEN'),
    )

    response1 = requests.get(modelpath, params=params)
    open("tempmodel.h5", 'wb').write(response1.content)
    model = load_model("tempmodel.h5")

    response2 = requests.get(converterpath, params=params)

    open("temppkl.pkl", 'wb').write(response2.content)
    converter = joblib.load("temppkl.pkl")

    import os
    os.remove("tempmodel.h5")
    os.remove("temppkl.pkl")
    return model, converter


def get_sequences():
    """collect the sequences for all users and all scenes"""

    date_path = (date.today() - timedelta(days=1)).strftime('%Y/%m/%d/ipynb')

    global PRAXXIS_ROOT
    basepath = PRAXXIS_ROOT + date_path

    params = (
        ('op', 'LISTSTATUS'),
    )

    response = requests.get(basepath, params=params)

    users = (response.json())['FileStatuses']['FileStatus']

    sequences = []
    for user in users:
        user_basepath = basepath + "/" + user['pathSuffix']
        response = requests.get(user_basepath, params=params)

        scenes = (response.json())['FileStatuses']['FileStatus']
        for scene in scenes:
            scene_basepath = user_basepath + "/" + scene['pathSuffix']
            response = requests.get(scene_basepath, params=params)
            files = (response.json())['FileStatuses']['FileStatus']
            sequence = []
            for f in files:
                fullname = f['pathSuffix']
                fullname.rstrip('.ipynb')
                # removes datetime info at start of string, and library name
                filename = ('-'.join(fullname.split('-')[3:]))
                filename = filename[0:len(filename) - 6]  # removes .ipynb
                sequence.append(filename)
            sequences.append(sequence)

    return sequences
