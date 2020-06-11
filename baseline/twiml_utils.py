from twilio.twiml.voice_response import VoiceResponse, Start
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
import random

call_duration = 45

facts = ["Jeffrey Epstein didn't kill himself",
         "Banging your head against a wall for one hour burns 150 calories.",
         "According to Genesys 1:20-22, zealots should clame that the chicken came before the egg... Wut?"]


def generate_twiml():
    response = VoiceResponse()
    # inbound
    inbound = Start()
    inbound.stream(name='in Audio Stream', url="wss://" + os.environ["WSS_INBOUND"], track="inbound_track")
    response.append(inbound)
    # outbound
    # outbound = Start()
    # outbound.stream(name='out Audio Stream', url="wss://" + os.environ["WSS_PRIMARY_OUTBOUND"], track="outbound_track")
    # response.append(outbound)
    # response.dial("+33689101696")
    response.pause(length=call_duration)
    print(response)
    return str(response)
