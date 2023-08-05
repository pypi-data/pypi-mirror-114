import firebase_admin
from firebase_admin import *
from firebase_admin import firestore
import json

from firebase_admin import credentials
from firebase_admin import db


def  extractFromFirebase(certificate_json_file_path,firebase_url):
    cred = credentials.Certificate(certificate_json_file_path)
    app=firebase_admin.initialize_app(cred,{'databaseURL':firebase_url})
    ref=db.reference()
    mydict=ref.get()
    delete_app(app)
    return mydict


def extractFromFirstProjectOfFirebase(certificate_json_file_path):
    cred = credentials.Certificate(certificate_json_file_path)
    app=firebase_admin.initialize_app(cred)
    db=firestore.client()
    delete_app(app)
    return db


def CollectionExtractor(collection):
    array=[]
    for document in collection:
        array.append([document.id,document.to_dict()])
    return array


def CollectionReferenceExtractor(reference):
    docs=reference.get()
    array=[]
    for doc in docs:
        array.append([doc.id,doc.to_dict()])
    return array
