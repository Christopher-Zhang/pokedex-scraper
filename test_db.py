import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017")

mydb = myclient["test"]
mycol = mydb["pokemon"]

query1 = {'name': 'Bulbasaur'}
query2 = {'number': 4}
query3 = {'stats.special defense': 80}
query4 = {"stats.attack": {"$gt":50}}
query5 = {"name": "list"}

doc1 = mycol.find(query1)
doc2 = mycol.find(query2)
doc3 = mycol.find(query3)
doc4 = mycol.find(query4)
doc5 = mycol.find(query5)

def print_doc(doc):
    for x in doc:
        print(x)
print("doc 1: ")
print_doc(doc1)
print("doc 2: ")
print_doc(doc2)
print("doc 3: ")
print_doc(doc3)
print("doc 4: ")
print_doc(doc4)
print("doc 5: ")
print_doc(doc5)