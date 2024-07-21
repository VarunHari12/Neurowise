from flask import Flask, request, jsonify
import tensorflow as tf
import cv2 as cv
import numpy as np
from flask_cors import CORS, cross_origin
import requests




app = Flask(__name__)
cors = CORS(app, resources={r"/predict": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type' 

model = tf.keras.models.load_model("./Brain_Scan_Model.keras")

def preprocess_image(image_path): # preprocess 
    image = cv.imread(image_path)
    image = cv.resize(image, (32, 32))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image

@app.route('/predict', methods=['POST'])
def predict(): # API endpoint to predict the tumor classification
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        file_path = "temp_image.jpg"
        file.save(file_path)
        
        image = preprocess_image(file_path)
        
        predictions = model.predict(image)
        class_idx = np.argmax(predictions, axis=1)[0]
    
        
        classification = "noTumor"
        
        if class_idx == 0:
            classification = "Glioma"
        elif class_idx == 1:
            classification = "Meningioma"
        elif class_idx == 3:
            classification = "Pituitary"
            
        if (classification != "noTumor"):
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            payload = {
                "model": "gpt-4",
                "messages": [
                    {"role": "user", "content": f"Make a general treatment plan for a patient with a {classification} tumor. Also suggest further tests other than an MRI that can be run to confirm the diagnosis."}
                ],
                "max_tokens": 500
            }
            
            response = requests.post(api_endpoint, headers=headers, json=payload)
            if (response.status_code==200): 
                generated_text = response.json()
                return jsonify({'classification': classification,
                                'treatment plan': generated_text["choices"][0]["message"]["content"]})
                
        else:
            return jsonify({'classification': "No Tumor",
                            'treatment plan': "You are Cancer Free!"})

if __name__ == '__main__':
    app.run(debug=True)
