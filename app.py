#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import random

from flask import Flask
from flask import request
from flask import make_response

CREDENTIALS = ("rose", "anna")

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])

def webhook():
    req = request.get_json(silent=True, force=True)

    username = request.authorization.get("username")
    password = request.authorization.get("password")

    print("Request:")
    print(json.dumps(req, indent=4))

    if (username, password) == CREDENTIALS:
        print("Authentication successful")
        res = processRequest(req)
    else:
        print("Failed to authenticate")
        res = {}

    res = json.dumps(res, indent=4)
    r = make_response(res)

    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "chooseSome":
        return {}

    result = req.get("result")

    data = result.get("parameters")

    res = makeWebhookResult(data)

    return res


def makeWebhookResult(data):
    names = data.get("names")

    if names is None:
        return {}

    k = random.randint(1, max(1,len(names)-1))
    chosen_ones = random.sample(names, k)

    if len(chosen_ones) == 1:
        speech = "I choose " + chosen_ones[0]
    else:
        speech = "I choose " + ", ".join(chosen_ones[:-1]) + " and " + chosen_ones[-1]

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "rose-pick-some-webhook"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
