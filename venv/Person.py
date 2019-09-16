import os
from create_data import *
import face_recognition

class Person:
    def __init__(self, image, sound, display_name):
        self.image = image
        self.sound = sound
        self.display_name = display_name
        self.playing = 0
        img = face_recognition.load_image_file(image)
        self.face_encoding=face_recognition.face_encodings(img)[0]


    @staticmethod
    def getPeople():
        peopleToReturn = []
        people = DataHelper.select("select id, image, sound, display_name from People;")
        for person in people:
            image = Person.writeFile(person[0], person[1], 'image')
            sound = Person.writeFile(person[0], person[2], 'sound')
            peopleToReturn.append(Person(image, sound, person[3]))
        return peopleToReturn


    def getAttributeAsBinary(self, attr):
        with open(attr, 'rb') as file:
            bin = file.read()
        return bin

    @staticmethod
    def writeFile(identity, blob, attr):
        rootDir = './'+str(identity)
        path = (rootDir+'/'+attr)
        if not os.path.exists(rootDir):
            os.mkdir(rootDir)
        with open(path,'wb') as file:
            file.write(blob)
        return path

    def writePersonData(self):
        try:
            connection = DataHelper.get_connection()
            stat = 'insert into People(image,sound,display_name) values (%s,%s,%s);'
            image = self.getAttributeAsBinary(self.image)
            sound = self.getAttributeAsBinary(self.sound)
            tup = (image, sound, self.display_name)
            cur = connection.cursor()
            result = cur.execute(stat, tup)
            connection.commit()
        finally:
            if connection.is_connected():
                cur.close()
                connection.close()

    @staticmethod
    def generateCraig():
        a = Person(
            './img/zaza.jpg',
            '/home/craig/PycharmProjects/faceRecognition/venv/sound/Howsit.m4a',
            "Craig Goodspeed"
        )
        a.writePersonData()


