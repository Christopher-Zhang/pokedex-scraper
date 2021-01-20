import pymongo
from scraper import scrape_pokemon


scraped_data = scrape_pokemon(10)

pokemon_data = scraped_data[0]
pokemon_list = scraped_data[1]

myclient = pymongo.MongoClient("mongodb://localhost:27017")

mydb = myclient["test"]
mycol = mydb["pokemon"]
# mycol.insert_many(pokemon_data)
pokemon_list_obj = {
    "name": "list",
    "list": pokemon_list,
}
mycol.insert_one(pokemon_list_obj)
print("done")
