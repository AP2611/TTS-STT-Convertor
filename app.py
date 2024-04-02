from flask import Flask, render_template, request, redirect, url_for
from gtts import gTTS
import os
import speech_recognition as sr
from io import BytesIO
import base64

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    text = request.form['text']


    tts = gTTS(text=text, lang='en')


    output_stream = BytesIO()
    tts.write_to_fp(output_stream)
    output_stream.seek(0)


    encoded_audio = base64.b64encode(output_stream.read()).decode('utf-8')

    return render_template('index.html', result='text_to_speech', audio=encoded_audio)


@app.route('/speech_to_text', methods=['POST'])
def speech_to_text():
    audio_file = request.files['audio']


    audio_stream = BytesIO(audio_file.read())

    
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_stream) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return render_template('index.html', result='speech_to_text', text=text)


if __name__ == '__main__':
    app.run(debug=True)




