# voicemail2text
voicemail transcription through stt because voicemails...


## how it works

for the PoC any unanswered call is forwarded to an auxiliary phone
when a call is detected the inbound track is sent through WSS to a buffer later on
sent to a STT API
after completion voicemail is forwarder under text form through SMS

## todo

- [x] baseline::purchase number
- [x] baseline::handle transcription
- [ ] baseline::forward voicemails
- [ ] baseline::expose service
- [ ] baseline::test
