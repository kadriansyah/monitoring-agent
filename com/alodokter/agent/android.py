import uuid
import datetime
import requests

from flask import current_app
from google.cloud import bigquery

class AndroidAgent:
    def run(self):
        current_app.logger.info('[AndroidMonitor] running...')

        headers = {'Authorization': current_app.config['ANDROID_TOKEN']}
        alodokter_urls = [
            "https://android.alodokter.com/api/v180/alodokter/infos/56e26dad150cd40d17000064.json",
            "https://android.alodokter.com/api/v180/alodokter/doctors.json",
            "https://android.alodokter.com/api/v180/questions/get_by_user_interest/56e26dad150cd40d17000064.json",
            "https://android.alodokter.com/api/v180/alodokter/hospital/list_doctor_by_hospital.json?id=5b7b744dd76c7d6ad687f671&page=1",
            "https://android.alodokter.com/api/v180/alodokter/doctors/get_time_slot/5a4af163a1faf339a3b73639.json"
        ]

        alomedika_urls = [
            "https://android.alodokter.com/api/v180/questions/list_of_unanswered_questions_with_time_slot/58342051edaba803d2000260.json",
            "https://android.alodokter.com/api/v180/alomedika/doctors/review/58342051edaba803d2000260.json",
            "https://android.alodokter.com/api/v180/alomedika/forums/threads.json",
            "https://android.alodokter.com/api/v180/questions/list_of_picked_up_by_doctor/58342051edaba803d2000260.json",
            "https://android.alodokter.com/api/v180/alomedika/doctors/list_bookings/58342051edaba803d2000260.json"
        ]

        rows_to_insert = []

        for i in range(5):
            r = requests.get(alodokter_urls[i], headers=headers)
            if r.status_code == 200:
                rtime = requests.get(alodokter_urls[i], headers=headers).elapsed.total_seconds()

                # channel: 1 = alodokter-web
                # channel: 2 = alomedika-web
                # channel: 3 = android-backend
                # type: 1 = artikel (alodokter & alomedika) / API (android alodokter)
                # type: 2 = penyakit a-z / API (android alomedika)
                # type: 3 = obat
                # type: 4 = topik (alodokter) / tindakan medis (alomedika)
                # type: 5 = hospitals
                # type: 6 = doctors
                data = (uuid.uuid1().hex, 3, 1, u''+ alodokter_urls[i], 0, rtime, datetime.datetime.now())
                rows_to_insert.append(data)
                current_app.logger.info('[AndroidMonitor] '+ str(data))
        
        for i in range(5):
            r = requests.get(alomedika_urls[i], headers=headers)
            if r.status_code == 200:
                rtime = requests.get(alomedika_urls[i], headers=headers).elapsed.total_seconds()

                # channel: 1 = alodokter-web
                # channel: 2 = alomedika-web
                # channel: 3 = android-backend
                # type: 1 = artikel (alodokter & alomedika) / API (android alodokter)
                # type: 2 = penyakit a-z / API (android alomedika)
                # type: 3 = obat
                # type: 4 = topik (alodokter) / tindakan medis (alomedika)
                # type: 5 = hospitals
                # type: 6 = doctors
                data = (uuid.uuid1().hex, 3, 2, u''+ alomedika_urls[i], 0, rtime, datetime.datetime.now())
                rows_to_insert.append(data)
                current_app.logger.info('[AndroidMonitor] '+ str(data))

        client = bigquery.Client()
        dataset_id = 'alomonitoring'
        table_id = 'page_speed_data'

        dataset_ref = client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)
        table = client.get_table(table_ref)

        return client.insert_rows(table, rows_to_insert)
        