# main/views.py

import os
import tensorflow as tf
import numpy as np
import pandas as pd
from django.shortcuts import render,redirect
from django.conf import settings
from django.core.files.storage import default_storage
from .forms import ImageUploadForm, SymptomForm
from .models import UploadedImage

# Load the models and data
image_model = tf.keras.models.load_model("E:/CAPSTONE PROJECT/CAPSTONE/med_site/main/SkinNet.keras")
model = tf.keras.models.load_model('E:/CAPSTONE PROJECT/CAPSTONE/med_site/main/models.keras')
data_cat = ['Chickenpox', 'Cowpox', 'HFMD', 'Healthy', 'Measles', 'Monkeypox']
sorethroat_map = {'Yes': 1, 'No': 0}

def diagnosis(request):
    if request.method == 'POST' and 'image_upload' in request.POST:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            file_name = image.name
            file_path = os.path.join(settings.MEDIA_ROOT,'../media/media/temp/', file_name)

            with default_storage.open(file_path, 'wb') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            image_load = tf.keras.utils.load_img(file_path, target_size=(224, 224))
            img_arr = tf.keras.utils.img_to_array(image_load)
            img_bat = np.expand_dims(img_arr, axis=0)

            predict = image_model.predict(img_bat)
            score = tf.nn.softmax(predict)
            predicted_class = data_cat[np.argmax(score)]

            # Pass image URL to symptoms template
            image_url = file_path[len(settings.MEDIA_ROOT):]  # Relative path for HTML rendering

            if predicted_class == "Measles":
                symptom_form = SymptomForm()
                return render(request, 'main/symptoms.html', {
                    'predicted_class': predicted_class,
                    'score': np.max(score) * 100,
                    'form': symptom_form,
                    'image_url': image_url
                })
            else:
                return render(request, 'main/diagnosis_result.html', {
                    'predicted_class': "The skin is out of scope",
                    'score': "",
                    'image_url': image_url
                })

    else:
        form = ImageUploadForm()
    return render(request, 'main/diagnosis.html', {'form': form})

# main/views.py

def predict_diagnosis(request):
    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            incubation = form.cleaned_data['incubation']
            sorethroat = form.cleaned_data['sorethroat']
            temperature = form.cleaned_data['temperature']
            
            # Prepare input data
            input_data = pd.DataFrame({
                'incubation': [incubation],
                'sorethroat': [sorethroat_map[sorethroat]],
                'temperature': [temperature]
            })
            
            # Make prediction
            prediction = model.predict(input_data)
            predicted_class = "Measles" if prediction[0] > 0.5 else "German Measles"
            
            # Render template with prediction result
            return render(request, 'main/prediction_result.html', {
                'predicted_class': predicted_class
            })
    else:
        form = SymptomForm()
    return render(request, 'main/symptoms.html', {'form': form})

def home(request):
    return render(request, 'main/home.html')

def history(request):
    return render(request, 'main/history.html')

def symptoms(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to the predict_diagnosis view after successful form submission
            return redirect('predict_diagnosis')
    else:
        form = ImageUploadForm()
    return render(request, 'main/symptoms.html', {'form': form, 'uploaded': False})
