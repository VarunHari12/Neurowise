import tensorflow as tf
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

test_img = "C:\\Users\\varun\\Brain_Tumor_Classification\\Brain-Tumor-Classification\\images (3).jpeg"
image = cv.imread(test_img)
image = cv.resize(image, (32,32))
image = image / 255.0

model = tf.keras.models.load_model("C:\\Users\\varun\\Brain_Tumor_Classification\\Brain-Tumor-Classification\\Brain_Scan_Model.keras")
print(1)
prediction = model.predict(np.expand_dims(image, axis = 0))
print(2)
class_names = ["glioma", "meningioma", "notumor", "pituitary"]
predicted_class_index = np.argmax(prediction)
predicted_class_prob = prediction[0, predicted_class_index]
predicted_class_name = class_names[predicted_class_index]
print(3)
print("Predicted classification: ", predicted_class_name)
print("Predicted probability: ", predicted_class_prob)

