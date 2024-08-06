import bottle
import json
import os
import pdfplumber
import utils

@bottle.route('/healthz/readiness')
def readiness():
    return 'OK'

@bottle.route('/parse', method='POST')
def parse():
    try:
        with pdfplumber.open(bottle.request.body) as pdf:
            bottle.response.content_type = 'text/html'
            bottle.response.headers['Access-Control-Allow-Origin'] = '*'
            return utils.to_markdown(pdf)
    except Exception as e:
        bottle.response.status = 400
        return str(e)

bottle.run(host='0.0.0.0', port=os.getenv('PORT', 8080))