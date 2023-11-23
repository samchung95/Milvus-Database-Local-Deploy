from helper import *
from pprint import pprint
db = MilvusHelper()

pprint(db.search(COLLECTION_NAME,"gateway logic",20))

# print()