from django.shortcuts import redirect
from django.http import HttpResponse
from rest_framework import views, status
from rest_framework.response import Response
from .forms import FileUploadForm
import pytesseract
from PIL import Image
import pyttsx3
import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
import os
from django.conf import settings


nlp = spacy.load("en_core_web_sm")
vectorizer = TfidfVectorizer()


dictionary_en_pl = {}
dictionary_file_path = os.path.join(settings.BASE_DIR, 'app', 'templates', 'dictionary', 'dictionary_en_pl.txt')
with open(dictionary_file_path, 'r') as f:  
    for line in f:
        key, value = line.strip().split(':')
        dictionary_en_pl[key.strip()] = value.strip()

def vectorize():
    X = vectorizer.fit_transform(list(dictionary_en_pl.keys()))
    return np.array(X.todense().copy())

word_vectors = vectorize()

def calculate_similarity(word_to_translate, candidate_vector):
    word_to_translate_vector = np.array(vectorizer.transform([word_to_translate]).todense().copy())[0,:]
    similarity = np.dot(word_to_translate_vector, candidate_vector.T) / (np.linalg.norm(word_to_translate_vector) * np.linalg.norm(candidate_vector))
    return similarity

def translate_word(word):
    translated_word = word.lower()
    highest_similarity = -1
    best_match = translated_word  

    for candidate, candidate_vector in zip(dictionary_en_pl.keys(), word_vectors):
        similarity = calculate_similarity(word.lower(), candidate_vector)
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = dictionary_en_pl[candidate]

    return best_match

def translate_text(text):
    doc = nlp(text)
    lemmatized_words = [token.lemma_ for token in doc]
    translated_text = ' '.join(translate_word(word) for word in lemmatized_words)
    return translated_text.replace(' ,', ',').replace(' .', '.')

def text_to_speech(text, language):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    voices = engine.getProperty('voices')
    engine.setProperty("voice", voices[language].id)
    engine.say(text)
    engine.runAndWait()

def get_text_from_image(file):
    img = Image.open(file)
    text = pytesseract.image_to_string(img)
    return text.replace('\n', ' ')

class UploadFileAPI(views.APIView):
    def post(self, request, *args, **kwargs):
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            text = get_text_from_image(uploaded_file)
            translated_text = translate_text(text)
            # Optionally speak text (disabled by default for web services)
            # text_to_speech(text, 1)  # English
            text_to_speech(translated_text, 0)  # Polish
            return Response({'original': text, 'translated': translated_text}, status=status.HTTP_200_OK)
        else:
            return Response({'error': "Invalid form"}, status=status.HTTP_400_BAD_REQUEST)
