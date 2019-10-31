import cv2
import os
import random
import requests
from gtts import gTTS
from playsound import playsound
from bs4 import BeautifulSoup

class Joker:
    """
    Joker is a class that tells "Yo Momma" jokes
    if there is a person standing in front of the
    (web) camera. All this is achieved by OpenCV
    for image recognition, gTTS for transforming
    text to sound, bs4 for scraping jokes online
    and finally playsound for actually playing the
    .mp3 (jokes) produced by gTTS.

    """

    jokes = list()

    def __init__(self):
        self.jokes = self._get_jokes()

    @classmethod
    def _get_jokes(cls) -> list:
        """
        Fetches list of jokes from the web.

        Returns:
        list: List of "Yo Momma" jokes.

        """
        response = requests.get('https://www.laughfactory.com/jokes/yo-momma-jokes')
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find_all('div', {'class': 'joke-text'})
        return [joke.find('p').text.strip() for joke in div]

    def tell_joke(self):
        """Picks a joke from list of jokes and tells it using gTTS and playsound."""
        tts = gTTS(text=random.choice(self.jokes), lang='en')
        tts.save('jokes/joke.mp3')
        playsound('jokes/joke.mp3')

    def take_picture(self) -> int:
        """
        Takes a picture via (web) camera.

        Returns:
        int: Number of recognized faces in the picture.
        0 - If no faces are recognized.
        -1 - If picture couldn't be taken properly.
        [1, inf] - If faces are captured.
        """
        cam = cv2.VideoCapture(0)
        picture_taken, image = cam.read()

        if picture_taken:
            return self._find_faces(image)

        return -1

    @classmethod
    def _find_faces(cls, image: object) -> int:
        """
        Uses OpenCV to recognize faces in the taken picture.

        Arguments:
        object: Previously taken image (or any image).

        Returns:
        int: Number of recognized faces in the picture.
        """
        casc_path = 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(casc_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        return len(faces)

