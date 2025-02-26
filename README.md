# PharmX: Handwritten Prescription Assistant

## Table of Contents

- [Introduction](#introduction)
- [Problem Statement](#problem-statement)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)

- [How It Works](#how-it-works)
- [Impact](#impact)
- [Feasibility](#feasibility)
- [Use of AI](#use-of-ai)
- [Alternatives Considered](#alternatives-considered)
- [Future Enhancements](#future-enhancements)
- [License](#license)
- [Contributing](#contributing)

## Introduction

**PharmX** is an innovative application designed to automatically capture and interpret handwritten prescriptions, particularly those in illegible cursive. The application aims to enhance medication management for pharmacists and patients by reducing misreading and medication dispensing errors, thereby improving health safety. By combining advanced AI techniques with traditional pharmacy practices, PharmX streamlines the process of interpreting prescriptions and ensures patient safety.

## Problem Statement

PharmX addresses the challenge of interpreting handwritten prescriptions, which are often illegible and difficult to read. According to research, approximately 98% of doctors write in cursive, leading to significant issues in the pharmacy industry, including:

- **Misreading of prescriptions**, which can result in incorrect medication dispensing.
- **Medication dispensing errors** that can lead to severe health hazards.
- **Inefficiencies** in the pharmacy workflow due to the time spent deciphering handwritten notes.

By leveraging technology, PharmX aims to ensure accurate recognition of patient information, doctor details, and prescribed medications, ultimately enhancing the safety and efficiency of medication management.

## Features

- **Handwriting Recognition**: Utilizes advanced OCR techniques to accurately capture patient information, doctor details, and medication prescriptions from handwritten notes.
- **Doctor Credential Verification**: Confirms the legitimacy of doctors through their registration numbers, ensuring patient safety by preventing prescriptions from unlicensed practitioners.
- **Medicine Demand Forecasting**: Analyzes historical prescription data to predict patterns in medicine demand, aiding pharmacies in inventory management and stock preparation.
- **Pharmacy Locator**: Assists patients in finding the nearest pharmacies that have their prescribed medications in stock, improving access to necessary treatments.
- **Multilingual Support**: Incorporates OCR technology that supports multiple languages, enhancing accessibility for diverse populations.
- **Graphical Representation**: Displays graphs and charts of medicine requirements based on patient orders, providing pharmacies with valuable insights into inventory needs.

## Technologies Used

- **Deep Learning**: 
  - **CRNN (Convolutional Recurrent Neural Network)** for handwriting recognition, achieving an accuracy of 78% in deciphering cursive writing.
- **Machine Learning**: 
  - **Logistic Regression, SVM (Support Vector Machine), and Random Forest** algorithms to predict medicine names based on extracted text and symptoms.
- **OCR Technology**: 
  - **Tesseract OCR** for extracting text from images of handwritten prescriptions.
- **Frontend Development**: 
  - **HTML, CSS, JavaScript**, and **Leaflet** for mapping features to locate pharmacies.
- **Backend Development**: 
  - **Flask** framework for server-side logic and handling requests.
- **Database Management**: 
  - [Specify your database technology here, e.g., SQLite, PostgreSQL] for storing patient and prescription data.
- **Data Annotation**: 
  - Utilizes **Roboflow API** for efficient labeling and preparation of training datasets.

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:

   git clone https://github.com/DiptiAgarwal2004/pharmx.git

   ## Access Models  

[Click here to access the models](https://drive.google.com/drive/folders/1uljdaxVn9Hy881mMIdjXxa2LF5wM7rgA)  

2. Navigate to the project directory:
   
   cd pharmx
   
4.  Create a virtual environment (optional but recommended):
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`

5. Install the required dependencies:

    pip install -r requirements.txt

### Usage Run the Flask server:
   python app.py

## Accessing the Application

Access the application in your web browser at [http://localhost:5000](http://localhost:5000).

Follow the prompts to log in or sign up as a user, where you can upload a prescription image for analysis. Use the available features to verify doctor credentials, predict medication based on symptoms and prescriptions, and locate nearby pharmacies.

## How It Works

PharmX employs a multi-step approach to interpret handwritten prescriptions:

1. **Image Upload**: Users upload an image of a handwritten prescription.
2. **Text Extraction**: The application uses Tesseract OCR to extract text from the uploaded image.
3. **Data Processing**: The extracted text is processed using regular expressions to identify and categorize key parameters such as patient name, dosage, and medication.
4. **Prediction Models**: The processed data is fed into machine learning models (Logistic Regression, SVM, and Random Forest) to predict the actual names of medicines based on visible text and symptoms.
5. **Doctor Verification**: The doctor’s registration number is checked against a database to ensure legitimacy.
6. **Medicine Demand Forecasting**: The application analyzes historical data to predict future demand for medications.
7. **Pharmacy Locator**: Users can find the nearest pharmacies with stock available, using Leaflet to display maps and calculate distances.

## Impact

The proposed project addresses a significant societal challenge by improving the accuracy and efficiency of interpreting handwritten prescriptions. By utilizing advanced AI techniques, PharmX reduces the risk of medication errors and enhances patient safety. The application is grounded in research and data, ensuring its relevance and effectiveness in real-world scenarios. The expected outcomes include safer medication management, reduced error rates in pharmacies, and improved access to necessary medicines for patients.

## Feasibility

PharmX has a well-developed plan for execution, including:

- **Access to Meaningful Datasets**: Utilizes diverse datasets for training the handwriting recognition model.
- **Technical Expertise**: The project is supported by knowledge of AI and machine learning, ensuring the implementation is robust.
- **Partnerships**: Collaborations with healthcare professionals and domain experts are established to facilitate successful deployment and validation of the application.

## Use of AI

PharmX effectively applies AI technology to tackle the issue of handwriting recognition in prescriptions. The integration of CRNN for text recognition, combined with machine learning algorithms for medicine prediction, enhances the application’s accuracy. By employing these advanced technologies, PharmX not only streamlines the pharmacy workflow but also significantly improves patient safety.

## Alternatives Considered

Several design ideas were considered but ultimately set aside, including:

- Solely relying on traditional methods of interpreting prescriptions without integrating AI, which would not adequately address the issue of illegible handwriting.
- Developing separate applications for different functionalities, which would complicate user experience. The current integrated approach provides a seamless user interface and improves efficiency.

## Future Enhancements

- **User Feedback System**: Integration of a feedback mechanism to continuously improve the model’s accuracy based on real user experiences.
- **Mobile Application Development**: Creating a mobile app version to provide easier access and usability for patients and pharmacists.
- **Dataset Expansion**: Continuously updating the dataset with more diverse handwriting samples and multilingual support to enhance the model’s capability.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for discussion. For significant changes, please open an issue first to discuss what you would like to change.

