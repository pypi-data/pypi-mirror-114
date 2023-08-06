# Firebase and Cloud Firestore Extractor

The project extracts data from **cloud firestore** among other things and do **CRUD** operations for backend purpose.

## Motivation
The motivation behind it came from the purpose and realisation to **help** others understand it in a much better.
**In other words,** to push others and become a better version of ourselves.

## Tech/framework used
Ex. -

<b>Built with</b>
- [idle-python3](http://echorand.me/site/notes/articles/idle/article.html)

## Features
My project stands out because I built it **by tapping into my subconsious mind and dreams** and put a gamble on it or say **faith** on it.
As they say,**your faith alone will guide you**.[song-ref](https://www.youtube.com/watch?v=-YDSaI0f5aU)
And then by following my own instinct without following guidelines(like PEP8) and using fancy editors like **pycharm,android-studio,visual studio code** in the beginning.

## Code Example
It is nothing special, but if you are favoring python3 to write it.
Make sure to pay attention to small things like while making a function say extractdatabaseRef using credentials:-

```python3
def extractDatabase(cred):
    app=firebase_admin.initialize_app(cred)
    db=firestore.client()
    delete_app(app)
    return db
database_1=extractDatabase(cred_1)
```

Create a **delete_app(app)** instance of it as well to recreate say database_i=extractDatabase(cred_i)
where i=[1,2,3,4,5,6,7,8.....10^6)
using the same function.

## Installation
To install firebase_admin API and any other module for a specific version of python,say,3.6
python3.6 -m pip install **moduleName**,
where,
#### moduleName=firebase_admin,google-cloud-python.
