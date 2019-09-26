import os
import traceback

from flask import current_app
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from com.alodokter.agent.uptime import UptimeAgent
from com.alodokter.agent.alodokter_rs import AlodokterRSAgent
from com.alodokter.agent.alodokter import AlodokterAgent
from com.alodokter.agent.alomedika import AlomedikaAgent
from com.alodokter.agent.android import AndroidAgent

app = Flask(__name__)
app.config.from_pyfile('settings/settings.cfg')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = current_app.config['GOOGLE_APPLICATION_CREDENTIALS']
api = Api(app)

uptime_agent = UptimeAgent()
alodokter_rs_agent = AlodokterRSAgent()
alodokter_agent = AlodokterAgent()
alomedika_agent = AlomedikaAgent()
android_agent = AndroidAgent()

class UptimeMonitor(Resource):
    def get(self):
        try:
            # app.logger.info(request.headers)
            if 'Auth-Unique-Token' not in request.headers.keys() or current_app.config['AUTH_UNIQUE_TOKEN'] != request.headers['Auth-Unique-Token']:
                return 'INVALID TOKEN', 404

            errors = uptime_agent.run()
            app.logger.info('[UptimeMonitor] '+ str(errors))

            data = {}
            data['status'] = 'success'
            data['errors'] = errors
            return make_response(jsonify(data=data), 200)

        except:
            app.logger.info(traceback.format_exc())
            return make_response(jsonify(data='None'), 200)

class AlodokterRSMonitor(Resource):
    def get(self):
        try:
            # app.logger.info(request.headers)
            if 'Auth-Unique-Token' not in request.headers.keys() or current_app.config['AUTH_UNIQUE_TOKEN'] != request.headers['Auth-Unique-Token']:
                return 'INVALID TOKEN', 404

            errors = alodokter_rs_agent.run()
            app.logger.info('[AlodokterRSMonitor] '+ str(errors))

            data = {}
            data['status'] = 'success'
            data['errors'] = errors
            return make_response(jsonify(data=data), 200)

        except:
            app.logger.info(traceback.format_exc())
            return make_response(jsonify(data='None'), 200)

class AlodokterMonitor(Resource):
    def get(self):
        try:
            # app.logger.info(request.headers)
            if 'Auth-Unique-Token' not in request.headers.keys() or current_app.config['AUTH_UNIQUE_TOKEN'] != request.headers['Auth-Unique-Token']:
                return 'INVALID TOKEN', 404

            errors = alodokter_agent.run()
            app.logger.info('[AlodokterMonitor] '+ str(errors))

            data = {}
            data['status'] = 'success'
            data['errors'] = errors
            return make_response(jsonify(data=data), 200)

        except:
            app.logger.info(traceback.format_exc())
            return make_response(jsonify(data='None'), 200)

class AlomedikaMonitor(Resource):
    def get(self):
        try:
            # app.logger.info(request.headers)
            if 'Auth-Unique-Token' not in request.headers.keys() or current_app.config['AUTH_UNIQUE_TOKEN'] != request.headers['Auth-Unique-Token']:
                return 'INVALID TOKEN', 404

            errors = alomedika_agent.run()
            app.logger.info('[AlomedikaMonitor] '+ str(errors))

            data = {}
            data['status'] = 'success'
            data['errors'] = errors
            return make_response(jsonify(data=data), 200)

        except:
            app.logger.info(traceback.format_exc())
            return make_response(jsonify(data='None'), 200)

class AlomobileMonitor(Resource):
    def get(self):
        try:
            # app.logger.info(request.headers)
            if 'Auth-Unique-Token' not in request.headers.keys() or current_app.config['AUTH_UNIQUE_TOKEN'] != request.headers['Auth-Unique-Token']:
                return 'INVALID TOKEN', 404

            errors = android_agent.run()
            app.logger.info('[AndroidMonitor] '+ str(errors))

            data = {}
            data['status'] = 'success'
            data['errors'] = errors
            return make_response(jsonify(data=data), 200)

        except:
            app.logger.info(traceback.format_exc())
            return make_response(jsonify(data='None'), 200)

api.add_resource(UptimeMonitor, '/monitoring-agent/uptime')
api.add_resource(AlodokterRSMonitor, '/monitoring-agent/alodokter_rs')
api.add_resource(AlodokterMonitor, '/monitoring-agent/alodokter')
api.add_resource(AlomedikaMonitor, '/monitoring-agent/alomedika')
api.add_resource(AlomobileMonitor, '/monitoring-agent/alomobile')

# # for development only
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=9090)
