from twilio.twiml.voice_response import VoiceResponse, Start
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
import random

call_duration = 45

def generate_twiml():
    response = VoiceResponse()
    # inbound
    inbound = Start()
    inbound.stream(name='in Audio Stream', url="wss://" + os.environ["WSS_URL"], track="inbound_track")
    response.append(inbound)
    response.pause(length=call_duration)
    print(response)
    return str(response)
