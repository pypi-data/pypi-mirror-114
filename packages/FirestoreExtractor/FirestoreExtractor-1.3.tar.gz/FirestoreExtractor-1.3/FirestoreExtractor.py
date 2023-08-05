import firebase_admin
from firebase_admin import *
from firebase_admin import firestore
import json

from firebase_admin import credentials
from firebase_admin import db

from datetime import datetime
import datetime


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

def lengthOfCollection(collection):
    length=0
    for docs in collection:
        length+=1
    return length

def MiBToBytes_Conversion(mib):
    One_mib_in_bytes=1049000.0
    converted_bytes=mib*One_mib_in_bytes
    return converted_bytes

def BytesToMiB_Conversion(mib_bytes):
    One_mib_in_bytes=1049000.0
    converted_mib=mib_bytes/One_mib_in_bytes
    return converted_mib

def utf8len(s):
    return 1+len(s.encode('utf-8'))

def SizeAccordingToType(types,size=0):#right now accounts for int,str,bool,list,map,null,datetime,timestamp
    if type(types)==datetime.datetime:
        size=8
    elif type(types)==None:
        size=1
    if type(types)==int or type(types)==float:
        size=8
    elif type(types)==str:
        size=utf8len(types)
    elif type(types) in [True,False]:
        size=1
    elif type(types)==dict:
        for key,value in types.items():
            size+=(SizeAccordingToType(value)+SizeAccordingToType(key))
    elif type(types)==list:
        for t in types:
            size+=SizeAccordingToType(t)#recursive so need to set maximum recursive depth
    return size

