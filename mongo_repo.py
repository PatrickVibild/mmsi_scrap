import pymongo

from mmsi_data import ShipData

client = pymongo.MongoClient("localhost", 27017)

mydb = client["ai-ships"]
mmsi = mydb["mmsi-meta"]


class AISMongo:
    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.mydb = self.client['ai-ships']
        self.mmsi_documents = self.mydb['mmsi-meta']

    def insert_mssi(self, data: ShipData):
        result = self.mmsi_documents.insert_one(data.to_dict())
        return result

    def exist_mmsi(self, mmsi):
        if self.mmsi_documents.count_documents({'mmsi': mmsi}, limit=1):
            return True
        return False

    def get_mmsi(self, mmsi):
        myquery = {"mmsi": mmsi}
        mydoc = self.mmsi_documents.find_one(myquery)
        mmsi = ShipData(mydoc['mmsi'], mydoc['generic_type'], mydoc['build_year'], mydoc['length'], mydoc['breath'],
                        mydoc['gross_tonnage'])
        return mmsi

    def __del__(self):
        self.client.close()
