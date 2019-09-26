import uuid
import datetime
import requests

from flask import current_app
from google.cloud import bigquery

class UptimeAgent:
    def run(self):
        current_app.logger.info('[UptimeMonitor] running...')
        rows_to_insert = []

        payload = {'custom_uptime_ratios': '1', 'format': 'json', 'api_key': current_app.config['ALODOKTER_UPTIME_KEY']}
        response = requests.post('https://api.uptimerobot.com/v2/getmonitors', data=payload)
        uptime = float(response.json()['monitors'][0]['custom_uptime_ratio'])

        # channel: 1 = alodokter
        data = (uuid.uuid1().hex, 1, uptime, datetime.datetime.now())
        rows_to_insert.append(data)
        current_app.logger.info('[UptimeMonitor] '+ str(data))

        payload = {'custom_uptime_ratios': '1', 'format': 'json', 'api_key': current_app.config['ALOMEDIKA_UPTIME_KEY']}
        response = requests.post('https://api.uptimerobot.com/v2/getmonitors', data=payload)
        uptime = float(response.json()['monitors'][0]['custom_uptime_ratio'])

        # channel: 2 = alomedika
        data = (uuid.uuid1().hex, 2, uptime, datetime.datetime.now())
        rows_to_insert.append(data)
        current_app.logger.info('[UptimeMonitor] '+ str(data))

        client = bigquery.Client()
        dataset_id = 'alomonitoring'
        table_id = 'site_avalability_data'

        dataset_ref = client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)
        table = client.get_table(table_ref)

        return client.insert_rows(table, rows_to_insert)
        