from helper import *
import docx
import json

db = MilvusHelper()
db.drop(COLLECTION_NAME)
try:
    db.create_collection(COLLECTION_NAME, PARAGRAPH_SCHEMA)
except:
    pass

with open('./data/db.json','r') as f:
    temp = f.readlines()
    temp = json.loads(temp[0])

    for row in temp['rows']:
        db.insert_text_data(COLLECTION_NAME,row)

