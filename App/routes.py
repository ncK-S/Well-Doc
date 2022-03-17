from werkzeug.utils import redirect
from app import app
from app import db
from app.models import Caregiver, Patient, Medication, Vaccine_dose
from flask import json, render_template, request, session, url_for, jsonify, flash



@app.route('/')
def index():
    if 'caregiver' in session.keys():
        return redirect(url_for('patients'))
    else:
        return render_template('main.html')

@app.route('/register-caregiver', methods=['POST'])
def register_caregiver():
    form = request.form
    caregiver = Caregiver(
        name=form['name'],
        email=form['email-address'],
        phone_number=form['phone-number'])
    Caregiver.set_password(form['password'])
    db.session.add(caregiver)
    db.session.commit()
    return render_template('patients.html')

@app.route('/validate-caregiver', methods=['POST'])
def validate_caregiver():
    if request.method == "POST":
        email_address = request.get_json()['email']
        caregiver = Caregiver.query.filter_by(email=email_address).first()
        if caregiver:
            return jsonify({'user_exists': 'true'})
        else:
            return jsonify({'user_exists': 'false'})

@app.route('/validate-password', methods=['POST'])
def validate_password():
    if request.method == "POST":
        email_address = request.get_json()['email']
        password = request.get_json()['password']
        userFound = 'false'
        passwordCorrect = 'false'
        caregiver = Caregiver.query.filter_by(email=email_address).first()
        if caregiver:
            userFound = 'true'
            if caregiver.check_password(password):
                passwordCorrect = 'true'
        
        return jsonify({'user_exists': userFound, 'passwordCorrect': passwordCorrect})
        
@app.route('/login-caregiver', methods=['POST'])
def login_caregiver():
    form = request.form
    caregiver = caregiver.query.filter_by(email=form['email-address']).first()

    if caregiver and caregiver.check_password(form['password']):
        return redirect(url_for('patients'))
    else:
        flash("Password was incorrect or user doesn't exist.")
        return redirect(url_for('patients.html'))

@app.route('/logout-caregiver', methods=['POST', 'GET'])
def logout_caregiver():
    session.pop('caregiver', None)
    return redirect(url_for('main.html'))


@app.route('/patient', methods=['POST', 'GET'])
def patient():
    caregiver = None
    if session['caregiver']:
        caregiver = session['caregiver']
        patient = Caregiver.query.filter_by(patient_id=patient)
        return render_template('patient.html', patient=patient)
    return render_template('patient.html')



