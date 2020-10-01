import base64
import json
import os
from flask import Flask, request
from flask_sockets import Sockets
from google.cloud.speech import enums, types

from bridge import SpeechBridge
from utils import generate_twiml, send_sms
from dotenv import load_dotenv
load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./voicemailtt-baseline.json"

HTTP_SERVER_PORT = int(os.environ["PORT"])
RATE = 8000


app = Flask(__name__)
app.secret_key = 'secret_app'
sockets = Sockets(app)


@app.after_request
def after_request_func(response):
    global caller
    global twilio_number
    caller = request.values.get('From')
    twilio_number = request.values.get('To')
    print(f"call emmitted from {caller}")
    print(f"call received at {twilio_number}")
    return response


# expose twiml for call handling through webhook
@app.route('/twiml', methods=['POST', 'GET'])
def return_twiml_primary():
    print("webhook detected inbound call")
    print("generating twiml instructions")
    xml = generate_twiml()
    return xml


# expose twiml for call handling through webhook
@app.route('/healthcheck', methods=['POST', 'GET'])
def test():
    return {"status": "pass"}


config = types.RecognitionConfig(
    # source : https://support.twilio.com/hc/en-us/articles/223180588-Best-Practices-for-Audio-Recordings
    # tldr >> 8-bit PCM mono uLaw @ 8Khz sample rate
    encoding=enums.RecognitionConfig.AudioEncoding.MULAW,
    sample_rate_hertz=RATE,
    # use_enhanced=True, ## enhanced model are not yet available in french
    # model="phone_call", ## not available in french
    language_code='fr-FR')

streaming_config = types.StreamingRecognitionConfig(
    config=config,
    interim_results=True)



import time

@sockets.route('/stream')
def transcribe_inbound(ws):
    print("WS connection opened")
    print("Connection accepted")
    # instancie speech_Bridge
    bridge = SpeechBridge(streaming_config)
    print("transcoder instanciation done")
    while not ws.closed:
        message = ws.receive()
        if message is None:
            bridge.shutdown()
            print("message is None")
            break
        data = json.loads(message)
        if data["event"] == "start":
            print(f"Media WS: Received event '{data['event']}': {message}")
            continue
        if data["event"] == "media":
            media = data["media"]
            chunk = base64.b64decode(media["payload"])
            bridge.fill_buffer(chunk)
        if data["event"] == "stop":
            print(f"Media WS: Received event 'stop': {message}")
            bridge.shutdown()
            time.sleep(15)
            break

    print("send SMS")
    print(bridge.transcript)
    send_sms(bridge.transcript, os.environ["MY_NUMBER"])
    print("Stopping...")


if __name__ == '__main__':
    # need a wsgi server that handles websocket // nb http & ws share same port
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    # for docker use 0.0.0.0
    server = pywsgi.WSGIServer(('', HTTP_SERVER_PORT), app, handler_class=WebSocketHandler)
    print("Server listening on: http://localhost:" + str(HTTP_SERVER_PORT))
    server.serve_forever()
