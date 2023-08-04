#! /usr/bin/env python3

import base64
import datetime
import requests
import sys
import json
import base64
import datetime
import hashlib
import hmac
import random
import urllib.parse
import psycopg2
from psycopg2 import sql

# Param de connexion : 
API_KEY = ''
id_client = ''
API_URL = 'https:///api/forms/?'



# local
dbhost = "localhost"
dbport = "5432"
dbuser = "postgres"
dbpwd = "postgres"
dbname = "postgres"
schema_name = ""
table_name = ""
# log file
logfile_location = "C://import_publik.log" # le chemin du fichier pour les log

conn = None
data_to_insert = None

def log_message(message):
	log_ts = datetime.datetime.now().replace(microsecond=0).isoformat() + " || "
	message = log_ts + message.encode('ascii', 'ignore').decode('ascii')
	print (message + "<br>")


credentials = ('%s:%s' % (id_client, API_KEY))
encoded_credentials = base64.b64encode(credentials.encode('ascii'))
print (encoded_credentials.decode("ascii"))
params = {"format": "json"} 
headers = {'Authorization': 'Basic %s' % encoded_credentials.decode("ascii"),
	   "Accept": "application/json"}
response = requests.get(API_URL, headers=headers, params=params).json()

try:
    # Connexion à la BDD : 
    conn = psycopg2.connect(dbname=dbname, port=dbport, user=dbuser, host=dbhost, password=dbpwd)
    if conn is None:
        log_message('Connexion à la base PostgreSQL échouée')
    cur = conn.cursor()
        #Insertion du formulaire dans la base de données
    for item in response["data"]:
        cur.execute("""
            INSERT INTO 
            test.newtable (nom, description, formulaire_json)
            VALUES (%s, %s, %s)
            ON CONFLICT (formulaire_json)
            DO UPDATE set nom=EXCLUDED.nom, description=EXCLUDED.description
            """, ( item["name"], item["title"], item["url"],))
        print("record insert or update pour :", item["url"])
    conn.commit()
    cur.close()
    log_message("Record INSERT OK")
finally:
    if conn is not None:
        conn.close() 
        sys.exit()
log_message("Fin du traitement")