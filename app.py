from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from pymongo import MongoClient
import base64
import os
import re
import math
import uuid
import pickle
import numpy as np
import cv2
import pytesseract
from tensorflow.keras.models import load_model
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
client = MongoClient("mongodb://localhost:27017/")
db = client["user_db"]
users = db["users"]

def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def extract_details(text):
    parts = re.split(r"Medicine names:", text, flags=re.IGNORECASE)
    truncated_text = parts[0]
    medicines = parts[1].strip() if len(parts) > 1 else ""

    details = {
        "name": re.search(r"Name:\s*(.+)", truncated_text),
        "age": re.search(r"Age:\s*(.+)", truncated_text),
        "medical_facility": re.search(r"Medical Facility:\s*(.+)", truncated_text),
        "date": re.search(r"Date:\s*(.+)", truncated_text),
        "sex": re.search(r"Sex:\s*(.+)", truncated_text),
        "contact": re.search(r"Contact:\s*(.+)", truncated_text),
        "weight": re.search(r"Weight:\s*(.+)", truncated_text),
        "doctor_reg": re.search(r"Doctor’s Registration Number:\s*(.+)", truncated_text)
    }

    extracted_details = {
        key: (match.group(1).strip() if match and match.group(1).strip().lower() != "not specified" else "")
        for key, match in details.items()
    }

    extracted_details["medicine_names"] = [med.strip() for med in medicines.split(",")] if medicines else []

    return extracted_details

def load_models():
    with open('models/logistic_model.pkl', 'rb') as f:
        logistic_model = pickle.load(f)

    with open('models/random_forest_model.pkl', 'rb') as f:
        random_forest_model = pickle.load(f)

    with open('models/svm_model.pkl', 'rb') as f:
        svm_model = pickle.load(f)

    prescription_classification_model = load_model('models/prescription_classification_model.h5')

    with open('models/tfidf_vectorizer.pkl', 'rb') as f:
        tfidf_vectorizer = pickle.load(f)

    return logistic_model, random_forest_model, svm_model, prescription_classification_model, tfidf_vectorizer

def process_image(image_path):
    logistic_model, random_forest_model, svm_model, prescription_classification_model, tfidf_vectorizer = load_models()
    
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    extracted_text = pytesseract.image_to_string(gray_image).strip()

    details = extract_details(extracted_text)

    text_vectorized = tfidf_vectorizer.transform([extracted_text])
    logistic_prediction = logistic_model.predict(text_vectorized)
    random_forest_prediction = random_forest_model.predict(text_vectorized)
    svm_prediction = svm_model.predict(text_vectorized)
    
    prescription_input = preprocess_for_prescription_model(extracted_text)
    prescription_prediction = prescription_classification_model.predict(np.array([prescription_input]))

    return {
        'extracted_text': extracted_text,
        'details': details,
        'logistic_prediction': logistic_prediction.tolist(),
        'random_forest_prediction': random_forest_prediction.tolist(),
        'svm_prediction': svm_prediction.tolist(),
        'prescription_prediction': prescription_prediction.tolist()
    }

def extract_details_from_text(extracted_text):
    lines = extracted_text.split("\n")
    details = {}

    for line in lines:
        if "Name:" in line:
            details['Name'] = line.split("Name:")[1].strip()
        elif "Age:" in line:
            details['Age'] = line.split("Age:")[1].strip()
        elif "Medical Facility:" in line:
            details['Medical Facility'] = line.split("Medical Facility:")[1].strip()
        elif "Date:" in line:
            details['Date'] = line.split("Date:")[1].strip()
        elif "Sex:" in line:
            details['Sex'] = line.split("Sex:")[1].strip()
        elif "Contact:" in line:
            details['Contact'] = line.split("Contact:")[1].strip()
        elif "Weight:" in line:
            details['Weight'] = line.split("Weight:")[1].strip()
        elif "Doctor’s Registration Number:" in line:
            details['Doctor’s Registration Number'] = line.split("Doctor’s Registration Number:")[1].strip()
        elif "Medicine:" in line:
            details['Medicine'] = line.split("Medicine:")[1].strip()
    
    for key in ['Name', 'Age', 'Medical Facility', 'Date', 'Sex', 'Contact', 'Weight', 'Doctor’s Registration Number', 'Medicine']:
        details.setdefault(key, 'Not specified')

    return details


def fetch_medicine_info(medicine_name):
    extracted_text = """
    Name: John Doe
    Age: 30
    Medical Facility: City Hospital
    Date: 2025-02-25
    Sex: Male
    Contact: 1234567890
    Weight: 70 kg
    Doctor’s Registration Number: DR12345
    Medicine: Aspirin, Ibuprofen
    """
    
    details = extract_details_from_text(extracted_text)

    medicines = details['Medicine'].split(", ")
    medicine_info_list = {}

    for medicine in medicines:
        medicine_info_list[medicine] = {
            'description': f'Simulated description for {medicine}',
            'storage_info': 'Room temperature',
            'warnings': f'Simulated warnings for {medicine}',
            'before_after_meals': 'After meals',
            'dosage_strength': '500 mg',
            'frequency': 'Once daily',
            'duration': 'As needed'
        }

    return {
        'patient_details': details,
        'medicine_info': medicine_info_list
    }


def predict_tablet(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    results = model(image)

    detected_items = results.pandas().xyxy[0]

    if detected_items.empty:
        return {"tablet": "No Tablet detected", "confidence": 0}

    tablet_info = detected_items.iloc[0]
    tablet_name = tablet_info['name']
    confidence = float(tablet_info['confidence']) * 100

    return {"tablet": tablet_name, "confidence": confidence}

@app.route('/trend')
def trend():
    df = pd.read_csv('drug_frequencies.csv')
    
    fig = px.bar(
        df,
        x='Drug',
        y='Frequency',
        title='Drug Frequencies',
        labels={'Frequency': 'Frequency', 'Drug': 'Drug'},
        color='Frequency', 
        color_continuous_scale=px.colors.sequential.Viridis  # Color scale
    )
    
    # Update layout for better aesthetics
    fig.update_layout(
        title=dict(
            text='Drug Frequencies',
            font=dict(size=24, color='darkblue'),
            x=0.5,  # Center title
        ),
        xaxis_title='Drug',
        yaxis_title='Frequency',
        font=dict(size=16),  # Font size for axis labels
        paper_bgcolor='lightgray',  # Background color
        plot_bgcolor='white',  # Plot area background color
        showlegend=False,  # Hide legend if not needed
        xaxis=dict(showgrid=True, gridcolor='lightgray'),  # X-axis grid
        yaxis=dict(showgrid=True, gridcolor='lightgray'),  # Y-axis grid
        margin=dict(l=40, r=40, t=40, b=40)  # Margins
    )
    
    # Generate the HTML representation of the plot
    graph_html = pio.to_html(fig, full_html=False)

    return render_template("trend.html", graph=graph_html)


@app.route('/home')
def home():
    return render_template("home.html")

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "login":
            email = request.form["email"]
            password = request.form["password"]
            return redirect(url_for('home'))
        elif action == "signup":
            name = request.form["name"]
            email = request.form["email"]
            password = request.form["password"]
            return redirect(url_for('home'))
    
    return render_template("index.html")

@app.route('/tablet')
def tablet_page():
    return render_template('tablet.html')

@app.route("/predict_tablet", methods=["POST"])
def predict_tablet():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    
    if image.filename == "":
        return jsonify({"error": "No selected image"}), 400

    filename = f"{uuid.uuid4().hex}_{image.filename}"
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    image.save(image_path)

    prediction = predict_tablet(image_path)
    print(f"Image saved at: {image_path}")

    return jsonify({
        "image_url": url_for('static', filename=f"uploads/{filename}"),
        "tablet": prediction["tablet"],
        "confidence": prediction["confidence"]
    })


@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    
    if image.filename == "":
        return jsonify({"error": "No selected image"}), 400

    image_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
    image.save(image_path)
    
    extracted_data = process_image(image_path)
    extracted_data["image_url"] = url_for('static', filename=f"uploads/{image.filename}")
    return jsonify(extracted_data)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

main_location = {"name": "New Delhi (Main Location)", "lat": 28.6339, "lng": 77.2195}

pharmacies = [
    {"name": "Apollo Pharmacy", "lat": 28.6201, "lng": 77.2150},
    {"name": "MedPlus Pharmacy", "lat": 28.6215, "lng": 77.2255},
    {"name": "Guardian Pharmacy", "lat": 28.6223, "lng": 77.2102},
    {"name": "Fortis HealthWorld", "lat": 28.6237, "lng": 77.2055},
    {"name": "Wellness Forever", "lat": 28.6245, "lng": 77.2300},
    {"name": "Sanjivani Pharmacy", "lat": 28.6250, "lng": 77.2020},
    {"name": "Medcity Pharmacy", "lat": 28.6267, "lng": 77.2170},
    {"name": "Cure & Care Pharmacy", "lat": 28.6279, "lng": 77.2215},
    {"name": "Health Plus Pharmacy", "lat": 28.6290, "lng": 77.2060},
    {"name": "Lifeline Pharmacy", "lat": 28.6305, "lng": 77.2123},
    {"name": "Aster Pharmacy", "lat": 28.6312, "lng": 77.2280},
    {"name": "Green Cross Pharmacy", "lat": 28.6320, "lng": 77.2075},
    {"name": "Urban Medicos", "lat": 28.6337, "lng": 77.2235},
    {"name": "Max Pharmacy", "lat": 28.6349, "lng": 77.2158},
    {"name": "Global Health Pharmacy", "lat": 28.6358, "lng": 77.2005},
    {"name": "Reliable Pharmacy", "lat": 28.6370, "lng": 77.2207},
    {"name": "Sun Pharma Store", "lat": 28.6385, "lng": 77.2250},
    {"name": "Healthy Life Pharmacy", "lat": 28.6398, "lng": 77.2080},
    {"name": "Om Sai Pharmacy", "lat": 28.6409, "lng": 77.2195},
    {"name": "SureCare Pharmacy", "lat": 28.6423, "lng": 77.2050}
]

@app.route("/list")
def list_page():
    lat = request.args.get("lat", type=float)
    lng = request.args.get("lng", type=float)

    print(f"Received lat: {lat}, lng: {lng}")

    if lat is None or lng is None:
        return "Latitude and longitude must be provided!", 400

    main_location = {"name": "Searched Location", "lat": lat, "lng": lng}
    print(main_location)

    for pharmacy in pharmacies:
        if pharmacy.get("lat") is None or pharmacy.get("lng") is None:
            print(f"Missing coordinates for pharmacy: {pharmacy}")
            continue
        pharmacy["distance"] = haversine(
            main_location["lat"], main_location["lng"],
            pharmacy["lat"], pharmacy["lng"]
        )
    
    sorted_pharmacies = sorted(pharmacies, key=lambda x: x.get("distance", float('inf')))
    print(sorted_pharmacies)
    return render_template("list.html", pharmacies=sorted_pharmacies[1:])

@app.route('/map')
def maps():
    return render_template("map.html")

@app.route("/get_medicine_info", methods=["POST"])
def get_medicine_info():
    data = request.json
    medicine_name = data.get("medicine_name")

    if not medicine_name:
        return jsonify({"error": "No medicine name provided"}), 400

    medicine_info = fetch_medicine_info(medicine_name)
    print({"medicine_name": medicine_name, "info": medicine_info})
    return jsonify({"medicine_name": medicine_name, "info": medicine_info})

if __name__ == "__main__":
    app.run(debug=True)
