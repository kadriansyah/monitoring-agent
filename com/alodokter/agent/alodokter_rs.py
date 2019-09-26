import uuid
import datetime
import requests

from flask import current_app
from pymongo import MongoClient
from google.cloud import bigquery

class AlodokterRSAgent:
    def run(self):
        current_app.logger.info('[AlodokterRSMonitor] running...')
        client = MongoClient(current_app.config['URI_ALODOKTER_RS'])
        db = client.alodokter_rs

        rows_to_insert = []
        for hospital in db.hospitals.aggregate([{'$match': {"status": 'publish'}}, {'$sample': {'size': 5} }]):
            url = 'https://www.alodokter.com/cari-rumah-sakit/'+ hospital['permalink']
            r = requests.get('https://www.googleapis.com/pagespeedonline/v4/runPagespeed?url='+ url +'&strategy=mobile&key='+ current_app.config['PAGE_SPEED_KEY'])
            if r.status_code == 200 and r.json()['responseCode'] == 200:
                score = int(r.json()['ruleGroups']['SPEED']['score'])
                rtime = 0.0
                if r.json()['formattedResults']['ruleResults']['MainResourceServerResponseTime']['summary']['args'][0]['type'] == 'DURATION':
                    rtime = float(r.json()['formattedResults']['ruleResults']['MainResourceServerResponseTime']['summary']['args'][0]['value'].split()[0])

                # channel: 1 = alodokter-web
                # channel: 2 = alomedika-web
                # type: 1 = artikel
                # type: 2 = penyakit a-z
                # type: 3 = obat
                # type: 4 = topik (alodokter) / tindakan medis (alomedika)
                # type: 5 = hospitals
                # type: 6 = doctors
                data = (uuid.uuid1().hex, 1, 5, u''+ url, score, rtime, datetime.datetime.now())
                rows_to_insert.append(data)
                current_app.logger.info('[AlodokterRSMonitor] '+ str(data))
        
        for doctor in db.doctors.aggregate([{'$match': {'publish': True}}, {'$sample': {'size': 5} }]):
            url = 'https://www.alodokter.com/cari-dokter/'+ doctor['permalink']
            r = requests.get('https://www.googleapis.com/pagespeedonline/v4/runPagespeed?url='+ url +'&strategy=mobile&key='+ current_app.config['PAGE_SPEED_KEY'])
            if r.status_code == 200 and r.json()['responseCode'] == 200:
                score = int(r.json()['ruleGroups']['SPEED']['score'])
                rtime = 0.0
                if r.json()['formattedResults']['ruleResults']['MainResourceServerResponseTime']['summary']['args'][0]['type'] == 'DURATION':
                    rtime = float(r.json()['formattedResults']['ruleResults']['MainResourceServerResponseTime']['summary']['args'][0]['value'].split()[0])

                # channel: 1 = alodokter-web
                # channel: 2 = alomedika-web
                # type: 1 = artikel
                # type: 2 = penyakit a-z
                # type: 3 = obat
                # type: 4 = topik (alodokter) / tindakan medis (alomedika)
                # type: 5 = hospitals
                # type: 6 = doctors
                data = (uuid.uuid1().hex, 1, 6, u''+ url, score, rtime, datetime.datetime.now())
                rows_to_insert.append(data)
                current_app.logger.info('[AlodokterRSMonitor] '+ str(data))

        client = bigquery.Client()
        dataset_id = 'alomonitoring'
        table_id = 'page_speed_data'

        dataset_ref = client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)
        table = client.get_table(table_ref)

        return client.insert_rows(table, rows_to_insert)
        