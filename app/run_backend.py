from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import dill
from time import strftime
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

handler = RotatingFileHandler(filename='logs/app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

model_path = "/my_app/notebooks/models/CatBoost_model.dill"
with open(model_path, 'rb') as f:
	model = dill.load(f)

@app.route("/", methods=["GET"])
def general():
	return """Welcome to fraudelent prediction process. Please use 'http://<address>/predict' to POST!!!"""

# функция POST запроса
@app.route("/predict", methods=["POST"])
def predict():

    data = {"success": False}
    dt = strftime("[%Y-%b-%d %H:%M:%S]")

    gender, relevent_experience, enrolled_university, education_level, major_discipline = "", "", "", "", ""
    experience, company_size, company_type, last_new_job = "", "", "", ""
    
    request_json = request.get_json()

    if request_json["gender"]:
        gender = request_json['gender']

    if request_json["relevent_experience"]:
        relevent_experience = request_json['relevent_experience']

    if request_json["enrolled_university"]:
        enrolled_university = request_json['enrolled_university']

    if request_json["education_level"]:
        education_level = request_json['education_level']

    if request_json["major_discipline"]:
        major_discipline = request_json['major_discipline']

    if request_json["experience"]:
        experience = request_json['experience']

    if request_json["company_size"]:
        company_size = request_json['company_size']

    if request_json["company_type"]:
        company_type = request_json['company_type']

    if request_json["last_new_job"]:
        last_new_job = request_json['last_new_job']

    logger.info(f'{dt} Data: gender={gender}, \
                             relevent_experience={relevent_experience}, \
                             enrolled_university={enrolled_university}, \
                             education_level={education_level}, \
                             major_discipline={major_discipline}, \
                             experience={experience}, \
                             company_size={company_size}, \
                             company_type={company_type}, \
                             last_new_job={last_new_job}')
    try:
        preds = model.predict_proba([[gender, relevent_experience, enrolled_university, education_level, major_discipline, \
                                      experience, company_size, company_type, last_new_job]])   

    except AttributeError as e:
        logger.warning(f'{dt} Exception: {str(e)}')
        data['predictions'] = str(e)
        data['success'] = False
        return jsonify(data)

    data["predictions"] = preds[:, 1][0]
    data["success"] = True

    return jsonify(data)