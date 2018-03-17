#!/usr/bin/python
# Filename: text.py
from firebase import firebase
firebase = firebase.FirebaseApplication('https://lokalizacja-gps.firebaseio.com/Users58de49ab6bb5a502', None)

result = firebase.post('Users58de49ab6bb5a502',{'2018.03.17 at 16:30':'proba'})