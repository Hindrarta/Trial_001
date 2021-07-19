from pymongo import MongoClient 
import logging
import logging.config
import datetime
import os
import time
from bson.objectid import ObjectId
import uuid

from passlib.hash import pbkdf2_sha256

import json
from dotenv import load_dotenv
load_dotenv()

from bson import json_util
import re

class backendDatabase(object):
    def __init__(self):
        try:
            # DB SETUP
            self.host = os.getenv("MONGODB_HOST")
            self.port = int(os.getenv("MONGODB_PORT"))
            self.credential = os.getenv("MONGODB_CREDENTIAL")
            self.username,self.password = self.credential.split(":")
            self.db_client = MongoClient(self.host, self.port, uuidRepresentation="standard",
                                                username=self.username, password=self.password)
            self.db = self.db_client["qv"]
            self.col = self.db["Persons"]
            # self.newid = '938452559'
            self.newid = '36345363457'

        except:
            print("Exception occurred", exc_info=True)
            self.initialize = False

    def getData(self,rfid_id=None):
        result = self.col.find({})
        #TODO: change to non regex and create column in dashboard for only rfidID
        if rfid_id != None:
            rgx = re.compile(f'{int(rfid_id)}*', re.IGNORECASE)  # compile the regex
            result = self.col.find({'identifier_number':rgx})
        return list(result)

    def getDataRFID(self, rfid_id=None):
        rgx = re.compile(f'{int(self.newid)}', re.IGNORECASE)  # compile the regex
        result = self.col.find({'identifier_number':rgx})
        # print(type(result))
        r = list(result)
        if(len(r) > 0):
            rfid_data = r[0]
            curr_rfid_id = rfid_data["identifier_number"]
            curr_secondary_id = rfid_data["secondary_id"]

            print(f'X - {rfid_data["name"]} - {rfid_data["person_id"]} ')

            rgx = re.compile(f'{int(curr_secondary_id)}', re.IGNORECASE)  # compile the regex
            result = self.col.find({'secondary_id':rgx})
            secondary_id_data = list(result)
            if(len(secondary_id_data)):
                for i in r2:
                    print(f'A - {i["name"]} - {i["person_id"]}')
            else:
                pass
        else:
            print("RFID not Found")



    def verifyRFID(self):
        rfid_id = self.newid
        try:
            result = self.col.find({})
            list_result = list(result)
            #print(list_result)
            print('-----------------------------------------------------------------------------')
            if len(list_result) == 0:
                # self.client.set('rfid_verified',False)
                self.rfid_data_checked = True
                return False,self.rfid_data_checked,"RFID"
            else:
                # self.client.set('rfid_verified',True)
                uuid_list = []
                for x in list_result:
                    identifier_number = x["identifier_number"]
                    try:
                        curr_secondary_id = x["secondary_id"]
                    except Exception as e:
                        curr_secondary_id = None
                        pass

                    curr_rfid_id = identifier_number
                    # print("ID in database: {} , ID Detected in card: {} ".format(curr_rfid_id,rfid_id))

                    try:
                        isinstance(int(curr_rfid_id),int)
                    except:
                        continue
                    if int(curr_rfid_id) == int(rfid_id):
                        # self.client.set('curr_person_id',[uuid.UUID(str(x["person_id"]))])
                        print(f'X - {x["name"]} - {x["person_id"]} - {[uuid.UUID(str(x["person_id"]))]}')
                        # Not using unit id grouping
                        if curr_secondary_id == None:
                            uuid_list.append(uuid.UUID(str(x["person_id"])))
                            break
                        else:
                            curr_unit_id = curr_secondary_id

                            for a in list_result:
                                id_number = a["identifier_number"]
                                new_unit_id = a["secondary_id"]
                                try:
                                    new_unit_id = a["secondary_id"]
                                except Exception as e:
                                    new_unit_id = None
                                    pass
                                if new_unit_id == curr_unit_id:
                                    uuid_list.append(uuid.UUID(str(a["person_id"])))
                                    print(f'A - {a["name"]} - {a["person_id"]}')
                            break
                print(len(uuid_list))
                print(uuid_list)
                print("*****************************************************************************")

                if len(uuid_list) == 0:
                    # self.client.set('rfid_verified',False)
                    self.rfid_data_checked = True
                    return False,self.rfid_data_checked,"RFID"
                else:
                    # set value to redis for AI
                    # person_uuid = uuid.UUID(str(result["person_id"]))
                    # self.client.set('rfid_verified',True)
                    # self.client.set('person_uuid',uuid_list)
                    self.rfid_data_checked = True
                    return True,self.rfid_data_checked,None
        except Exception as e:
            print(f"Error on RFID reader, reason : {str(e)}")
            return False,True,"Systems"


if __name__ == "__main__":
    db = backendDatabase()
    start_t = time.time()
    db.getDataRFID()
    # db.verifyRFID()
    end_t = time.time()
    elapsed_t = end_t - start_t
    print(f'Time Elapsed : {elapsed_t}')


