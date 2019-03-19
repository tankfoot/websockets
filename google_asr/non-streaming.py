from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


def speech_api_buffer(buffer):

    client = speech.SpeechClient()

    audio = types.RecognitionAudio(content=b''.join(buffer))

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')

    responses = client.recognize(config, audio)

    return responses


def print_response_buffer(r):
    for result in r.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
        return result.alternatives[0].transcript
