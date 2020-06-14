from twilio.twiml.voice_response import VoiceResponse, Start
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os

call_duration = 20


def generate_twiml():
    response = VoiceResponse()
    # inbound
    inbound = Start()
    inbound.stream(name='in Audio Stream', url="wss://" + os.environ["WSS_URL"], track="inbound_track")
    response.append(inbound)
    response.pause(length=call_duration)
    print(response)
    return str(response)


def send_sms(content, to, from_=os.environ["VM_NUMBER"]):
    client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])
    try:
        client.messages.create(
            body=content,
            from_=from_,
            to=to
        )
    except TwilioRestException as exception:
        # Check for invalid mobile number error from Twilio
        if exception.code == 21614:
            print("No Way Jose")
