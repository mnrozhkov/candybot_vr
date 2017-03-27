#!/usr/bin/env python3

import sys
sys.path.insert(1,'/usr/local/lib/python3.5/dist-packages')


import cv2
import numpy
from typing import List, Dict


BASE_PATH = sys.path[0]
FACE_HARRCASCADE_FILE = BASE_PATH + '/haarcascades/haarcascade_frontalface_default.xml'
SMILE_HARRCASCADE_FILE = BASE_PATH + '/haarcascades/haarcascade_smile.xml'


def detect_faces(image: numpy.ndarray or None = None, min_neighbors=5) -> List[Dict[str,int]] or None:
    '''
    1. takes numpy.ndarray image
    2. searches faces regions on this image
    3. returns list dictionaries, which contain coordinates and sizes of faces regions
    '''

    if image is None:
        return None

    face_cascade = cv2.CascadeClassifier()
    if not face_cascade.load(self.FACE_HARRCASCADE_FILE):
        return None

    face_regions = list()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=min_neighbors)
    for (x,y,w,h) in faces:
        #detect face location
        face_regions.append({'x': x, 'y': y, 'w': w, 'h': h})

    return face_regions


def detect_smile(face_image: numpy.ndarray or None = None, min_neighbors=22) -> bool or None:
    '''
    1. takes numpy.ndarray - face image
    2. searches smile region on this image
    3. returns True if smile exists
    '''

    if image is None:
        return None

    smile_cascade = cv2.CascadeClassifier()
    if not face_cascade.load(self.SMILE_HARRCASCADE_FILE):
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    smiles = face_cascade.detectMultiScale(gray, scaleFactor=4, minNeighbors=min_neighbors, minSize=(25,25))
    if len(smiles) > 0:
        return True

    return False
