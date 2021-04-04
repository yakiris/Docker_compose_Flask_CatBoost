from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import SelectField, StringField #, TextField, IntegerField
from wtforms.validators import DataRequired
import urllib.request
import json

app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess')

class ClientDataForm(FlaskForm):

    gender = SelectField("Gender: ", choices=[
                        ("Female", "Female"),
                        ("Male", "Male")]) 

    enrolled_university = SelectField("Enrolled university: ", choices=[
                                    ("no_enrollment", "no_enrollment"),
                                    ("Part time course", "Part time course"),
    	                            ("Full time course", "Full time course")]) 

    education_level = SelectField("Education level: ", choices=[
                                 ("Primary School", "Primary School"),
                                 ("High School", "High School"), 
    	                         ("Graduate", "Graduate"), 
                                 ("Masters", "Masters"), 
                                 ("Phd", "Phd")])

    major_discipline = SelectField("Major discipline: ", choices=[
    	                          ("No Major", "No Major"), 
                                  ("Humanities", "Humanities"), 
                                  ("Arts", "Arts"),
                                  ("Business Degree", "Business Degree"),
                                  ("STEM", "STEM"),
                                  ("Other", "Other")])

    relevent_experience = SelectField("Relevent experience: ", choices=[
                                     ("No relevent experience", "No relevent experience"),
    	                             ("Has relevent experience", "Has relevent experience")]) 

    experience = SelectField("Experience: ", choices=[
    	                    ("<2", "<2"), 
                            ("2-5", "2-5"), 
                            ("5-8", "5-8"), 
                            ("8-15", "8-15"), 
    	                    (">15", ">15")])   
   
    company_size= SelectField("Company size: ", choices=[
    	                    ("<100", "<100"), 
                            ("100-1000", "100-1000"), 
                            ("1000-10000", "1000-10000"), 
    	                    (">10000", ">10000")])

    company_type = SelectField("Company type: ", choices=[
    	                      ("Pvt Ltd", "Pvt Ltd"),
                              ("Early Stage Startup", "Early Stage Startup"),
                              ("Funded Startup", "Funded Startup"),
    	                      ("NGO", "NGO"),
                              ("Public Sector", "Public Sector"),
                              ("Other", "Other")])

    last_new_job = SelectField("Last new job: ", choices=[
    	                      ("never", "never"), 
                              ("1-4", "1-4"), 
    	                      (">4", ">4")])

def get_prediction(gender, relevent_experience, enrolled_university, education_level, major_discipline, experience, company_size, company_type, last_new_job):
    body = {
        'gender': gender,
        'relevent_experience': relevent_experience,
        'enrolled_university': enrolled_university,
        'education_level': education_level,
        'major_discipline': major_discipline,
        'experience': experience,
        'company_size': company_size,
        'company_type': company_type,
        'last_new_job': last_new_job
        }

    myurl = "http://10.5.0.5:8180/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(req, jsondataasbytes)
    return json.loads(response.read())['predictions']

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/predicted/<response>')
def predicted(response):
    response = json.loads(response)
    return render_template('predicted.html', response=response)

@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    form = ClientDataForm()
    data = dict()
    if request.method == 'POST':
        data['gender'] = request.form.get('gender')
        data['relevent_experience'] = request.form.get('relevent_experience')
        data['enrolled_university'] = request.form.get('enrolled_university')
        data['education_level'] = request.form.get('education_level')
        data['major_discipline'] = request.form.get('major_discipline')
        data['experience'] = request.form.get('experience')
        data['company_size'] = request.form.get('company_size')
        data['company_type'] = request.form.get('company_type')
        data['last_new_job'] = request.form.get('last_new_job')
        try:
            response = str(get_prediction(data['gender'],
                                          data['relevent_experience'],
                                          data['enrolled_university'],
                                          data['education_level'],
                                          data['major_discipline'],
                                          data['experience'],
                                          data['company_size'],
                                          data['company_type'],
                                          data['last_new_job']))
                           
            # print(response)
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
            # print(response)
        return redirect(url_for('predicted', response=response))
    return render_template('form.html', form=form)