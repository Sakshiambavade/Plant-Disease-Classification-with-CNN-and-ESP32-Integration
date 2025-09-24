import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

# Load trained model
MODEL_PATH = "model/plant_model.h5"
model = load_model(MODEL_PATH)

# Class labels (change according to your dataset)
CLASS_NAMES = ["Healthy", "Bacterial Spot", "Early Blight", "Late Blight", "Leaf Mold"]

st.title("🌱 Plant Disease Detection")
st.write("Upload a plant leaf image to predict its health.")

# File uploader
uploaded_file = st.file_uploader("Choose a leaf image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Leaf", use_column_width=True)

    # Preprocess the image
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    # Predict
    prediction = model.predict(img_array)
    class_idx = np.argmax(prediction)
    confidence = np.max(prediction) * 100

    st.success(f"Prediction: **{CLASS_NAMES[class_idx]}** ({confidence:.2f}% confidence)")
