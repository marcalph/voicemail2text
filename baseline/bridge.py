import queue
from threading import Thread
from google.cloud import speech
from google.cloud.speech import types
import logging


logger = logging.getLogger('step')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s \n %(message)s", "%Y-%m-%d %H:%M")
ch.setFormatter(formatter)
logger.addHandler(ch)


class SpeechBridge:
    def __init__(self, streaming_config, number):
        self.buff = queue.Queue()
        self.ended = False
        self.number = number
        self.streaming_config = streaming_config
        self.client = speech.SpeechClient()
        self.start()

    def start(self):
        Thread(target=self.process).start()

    def shutdown(self):
        self.ended = True

    def fill_buffer(self, data):
        self.buff.put(types.StreamingRecognizeRequest(audio_content=bytes(data)))

    def stream_generator(self):
        while not self.ended:
            chunk = self.buff.get()
            yield chunk

    def process(self):
        responses = self.client.streaming_recognize(
            self.streaming_config,
            self.stream_generator()
        )
        self.handle_response_loop(responses)

    def handle_response_loop(self, responses):
        """Iterates through gcp server responses and prints them.
        """
        num_chars_printed = 0
        for response in responses:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript
            overwrite_chars = ' ' * (num_chars_printed - len(transcript))
            logger.info("hellow bitches")
            if not result.is_final:
                print(transcript)
                # sys.stdout.write(transcript + overwrite_chars + '\r')
                # sys.stdout.flush()
                num_chars_printed = len(transcript)
            else:
                print(transcript + overwrite_chars)
                num_chars_printed = 0
            if self.ended:
                break
