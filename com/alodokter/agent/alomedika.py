import uuid
import datetime
import requests

from flask import current_app
from pymongo import MongoClient
from google.cloud import bigquery

class AlomedikaAgent:
    def run(self):
        current_app.logger.info('[AlomedikaMonitor] running...')
        client = MongoClient(current_app.config['URI_ALOMEDIKA'])
        db = client.alomedika

        rows_to_insert = []
        # artikel
        for post in db.core_posts.aggregate([{'$match': {"post_type": 'post', "post_status": 'publish'}}, {'$sample': {'size': 5} }]):
            data_permalink = [data for data in post['core_post_meta'] if data['meta_key'] == 'custom_permalink']
            if len(data_permalink) > 0:
                permalink = data_permalink[0]['meta_value']
                url = 'https://www.alomedika.com/'+ permalink
            else:
                url = 'https://www.alomedika.com/'+ post['post_name']

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
                data = (uuid.uuid1().hex, 2, 1, u''+ url, score, rtime, datetime.datetime.now())
                rows_to_insert.append(data)
                current_app.logger.info('[AlomedikaMonitor] '+ str(data))
        
        # penyakit a-z
        for post in db.core_posts.aggregate([{'$match': {"post_parent_id": 76, "post_status": 'publish'}}, {'$sample': {'size': 5} }]):
            data_permalink = [data for data in post['core_post_meta'] if data['meta_key'] == 'custom_permalink']
            if len(data_permalink) > 0:
                permalink = data_permalink[0]['meta_value']
                url = 'https://www.alomedika.com/'+ permalink
            else:
                url = 'https://www.alomedika.com/'+ post['post_name']

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
                data = (uuid.uuid1().hex, 2, 2, u''+ url, score, rtime, datetime.datetime.now())
                rows_to_insert.append(data)
                current_app.logger.info('[AlomedikaMonitor] '+ str(data))
        
        # obat
        for post in db.core_posts.aggregate([{'$match': {"post_parent_id": 150, "post_status": 'publish'}}, {'$sample': {'size': 5} }]):
            data_permalink = [data for data in post['core_post_meta'] if data['meta_key'] == 'custom_permalink']
            if len(data_permalink) > 0:
                permalink = data_permalink[0]['meta_value']
                url = 'https://www.alomedika.com/'+ permalink
            else:
                url = 'https://www.alomedika.com/'+ post['post_name']

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
                data = (uuid.uuid1().hex, 2, 3, u''+ url, score, rtime, datetime.datetime.now())
                rows_to_insert.append(data)
                current_app.logger.info('[AlomedikaMonitor] '+ str(data))

        # tindakan medis
        for post in db.core_posts.aggregate([{'$match': {"post_parent_id": 586059, "post_status": 'publish'}}, {'$sample': {'size': 5} }]):
            data_permalink = [data for data in post['core_post_meta'] if data['meta_key'] == 'custom_permalink']
            if len(data_permalink) > 0:
                permalink = data_permalink[0]['meta_value']
                url = 'https://www.alomedika.com/'+ permalink
            else:
                url = 'https://www.alomedika.com/'+ post['post_name']

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
                data = (uuid.uuid1().hex, 2, 4, u''+ url, score, rtime, datetime.datetime.now())
                rows_to_insert.append(data)
                current_app.logger.info('[AlomedikaMonitor] '+ str(data))

        client = bigquery.Client()
        dataset_id = 'alomonitoring'
        table_id = 'page_speed_data'

        dataset_ref = client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)
        table = client.get_table(table_ref)

        return client.insert_rows(table, rows_to_insert)
        