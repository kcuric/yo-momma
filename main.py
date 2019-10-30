import cv2
import os
import random
import time
import requests
from gtts import gTTS
from playsound import playsound
from bs4 import BeautifulSoup

class Joker:

    jokes = list()

    def __init__(self):
        self.jokes =  self.GetJokes()

    def GetJokes(self):
        self.response = requests.get('https://www.laughfactory.com/jokes/yo-momma-jokes')
        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        self.div = self.soup.find_all('div', {'class': 'joke-text'})
        return [joke.find('p').text.strip() for joke in self.div]

    def TellJoke(self):
        self.tts = gTTS(text=random.choice(self.jokes), lang='en')
        self.tts.save('jokes/joke.mp3')
        playsound('jokes/joke.mp3')

    def TakePicture(self):
        cam = cv2.VideoCapture(0)
        pictureTaken, image = cam.read()

        if pictureTaken:
            return self.FindFaces(image)
        else:
            return 0

    def FindFaces(self, image: object) -> int:
        self.imagePath = image
        self.cascPath = 'haarcascade_frontalface_default.xml'

        self.faceCascade = cv2.CascadeClassifier(self.cascPath)

        self.gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        self.faces = self.faceCascade.detectMultiScale(
            self.gray,
            scaleFactor = 1.1,
            minNeighbors = 5,
            minSize = (30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )
        return len(self.faces)

def Main():
    jk = Joker()

    while True:
        if jk.TakePicture():
            jk.TellJoke()
        time.sleep(2)

if __name__ == "__main__":
    Main()
