# voicemail2text
voicemail transcription because... well voicemails


## how it works

for the PoC any unanswered call is forwarded to an auxiliary phone
when a call is detected the inbound track is sent through WSS to a buffer later on
sent to a STT API
after completion voicemail is forwarded under text form through SMS

## todo

- [x] baseline::purchase number
- [x] baseline::handle transcription
- [ ] baseline::add sms capability
- [ ] baseline::forward voicemails
- [ ] baseline::expose service
- [ ] baseline::test
