from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing import image

# Load the trained model
model = load_model('predictor.h5')

# Class label mapping
label = {0: "Messi", 1: "Ronaldo"}

# Ask user for the test image path
img_path = input("Enter the path to the test image: ")

# Load and preprocess the image
img = image.load_img(img_path, target_size=(256, 256))
img_array = image.img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Predict
predictions = model.predict(img_array)[0]  # Single prediction vector
predicted_class = np.argmax(predictions)

# Print results
print(f"\nImage: {img_path}")
for i, prob in enumerate(predictions):
    print(f"{label[i]}: {prob * 100:.2f}%")
print(f"Predicted class: {label[predicted_class]}")
