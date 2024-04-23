import os
import random
import time
from pydub import AudioSegment
from PIL import Image, ImageTk
import requests
from io import BytesIO
import tkinter as tk
import requests

def extract_sample(audio_file):
    song = AudioSegment.from_file(audio_file)
    middle_point = len(song) // 2
    five_seconds = 5 * 1000  # 5 seconds in milliseconds
    start_point = max(0, middle_point - (five_seconds // 2))
    end_point = min(len(song), middle_point + (five_seconds // 2))
    sample = song[start_point:end_point]
    return sample

def retrieve_photo(song_title):
    access_key = 'OHkbvR3W7gAt6YysSTWRsFhYPgfkMWAYX-mkPoInSsk'
    url = 'https://api.unsplash.com/search/photos'
    
    params = {
        'query': song_title,
        'client_id': access_key
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:

        data = response.json()
        
        if data['results']:
            photo_url = data['results'][0]['urls']['regular']
            return photo_url
        else:
            return "No photo found"
    else:
        return "Error fetching photo"

photo_url = retrieve_photo("How Far I'll Go")
print(photo_url)


def main():
    song_file = 'C:\Users\plami\Downloads\soongaws.mp3'  
    photo_title = "How Far I'll Go" 

    sample = extract_sample(song_file)

    photo = retrieve_photo(photo_title)

    root = tk.Tk()
    root.title("Song Photo App")

    image_data = requests.get(photo)
    photo_image = Image.open(BytesIO(image_data.content))
    photo_image = ImageTk.PhotoImage(photo_image)
    
    label = tk.Label(root, image=photo_image)
    label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()