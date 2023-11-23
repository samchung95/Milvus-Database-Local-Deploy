from pymilvus import Collection, connections, FieldSchema, CollectionSchema, DataType, utility
from FlagEmbedding import FlagModel

id = FieldSchema(
  name="sentenceId",
  dtype=DataType.INT64,
  is_primary=True,
  auto_id=True
)
text = FieldSchema(
  name="text",
  dtype=DataType.VARCHAR,
  max_length=9999
)
text_vector = FieldSchema(
  name="text_vector",
  dtype=DataType.FLOAT_VECTOR,
  dim=1024
)
PARAGRAPH_SCHEMA = CollectionSchema(
  fields=[id, text, text_vector],
  description="Paragraph table",
  enable_dynamic_field=True
)
COLLECTION_NAME = "paragraphs"

# collection = Collection(
#     name=collection_name,
#     schema=schema,
#     using='default',
#     shards_num=2
#     )

class MilvusHelper:
    def __init__(self, host='localhost', port='19530'):
        self.model = FlagModel('BAAI/bge-large-en-v1.5', use_fp16=True)
        connections.connect(host=host, port=port)

    def create_collection(self, collection_name, schema):
        if utility.has_collection(collection_name):
            print(f"Collection {collection_name} already exists.")
            return
        # collection_schema = CollectionSchema(fields, description="Collection for vectors")
        collection = Collection(name=collection_name, schema=schema)

        # # Define index type and parameters (example: IVF_FLAT)
        index_params = {
            "metric_type": "L2",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 1024}
        }
        collection.create_index("text_vector", index_params=index_params, index_name="text_idx")
        collection.load()
        
        print(f"Collection {collection_name} is created.")

    def get_embedding(self, data):
        embedding = self.model.encode([data])[0]
        return embedding.tolist()

    def insert_text_data(self, collection_name, text_data):
        if isinstance(text_data,dict):
            collection = Collection(name=collection_name)
            ids = collection.insert(text_data)
            collection.load()
        else:
            embeddings = self.model.encode([text_data])
            collection = Collection(name=collection_name)
            ids = collection.insert({"text":text_data,"text_vector": embeddings[0]})
            collection.load()
        return ids
    
    
    def bulk_insert(self, collection_name, filepath):
        task_id = utility.do_bulk_insert(
            collection_name=collection_name,
            files=[filepath]
        )
        collection = Collection(name=collection_name)
        collection.load()

    def search(self, collection_name, query_text, top_k):
        query_embedding = self.model.encode([query_text])[0]
        collection = Collection(name=collection_name)
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        collection.load()
        results = collection.search([query_embedding], anns_field="text_vector", param=search_params, limit=top_k, expr=None)
        response = []
        for hits in results:
            ids = hits.ids
            res = collection.query(
                expr=f"sentenceId in {ids}", 
                output_fields=["text","sentenceId"],
                consistency_level="Strong"
                )
            res = sorted(res,key = lambda k:k['sentenceId'])
            response.append(res)
        return [res['text'] for res in response[0]]
    
    def drop(self,collection):
        utility.drop_collection(collection)
