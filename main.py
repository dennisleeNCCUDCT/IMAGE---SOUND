import base64
import json
from PIL import Image
import io
from scipy.io.wavfile import write
import numpy as np
#step1
def image_to_json(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    image_json = {
        "image_data": encoded_string
    }

    with open('image.json', 'w') as json_file:
        json.dump(image_json, json_file)

image_to_json('path_to_your_image.jpg')

#step2
def json_to_mp3(json_path):
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        image_data = base64.b64decode(data['image_data'])
    
    image = Image.open(io.BytesIO(image_data))
    image_array = np.array(image)
    average_color = np.mean(image_array, axis=(0, 1))

    # Create a simple wave based on the average color
    samplerate = 44100
    duration = 1  # in seconds
    frequency = np.mean(average_color)  # A simple example to convert average color to a frequency
    t = np.linspace(0, duration, int(samplerate * duration))
    audio = 0.5 * np.sin(2 * np.pi * frequency * t)

    write('output.mp3', samplerate, audio.astype(np.float32))

json_to_mp3('image.json')