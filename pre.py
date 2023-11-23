import docx
import json

from helper import *
# Load the Word document
doc = docx.Document('./data/context.docx')

# Extract paragraphs
paragraphs = [para for para in doc.paragraphs if para.text.strip() != '']

db = MilvusHelper()
rows = [{'text': para, 'text_vector': db.get_embedding(para)} for para in paragraphs]

with open('./data/db.json','w') as file:
    file.writelines(json.dumps({'rows':rows}))


print(paragraphs)
