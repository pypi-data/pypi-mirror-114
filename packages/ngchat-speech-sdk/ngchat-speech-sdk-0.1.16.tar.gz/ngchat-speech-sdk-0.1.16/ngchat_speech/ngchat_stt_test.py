
import speech as speechsdk
import ngchat_speech.audio as audio
import asyncio
import threading
import sys
import time

# change this to `False` to use synchronized continuous recognition
USE_CONTINUOUS_ASYNC = True

def rate_limited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rate_limited_function(*args,**kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rate_limited_function
    return decorate


global speech_recognizer
if __name__=="__main__":
    # this is an example to show how to use the SDK

    @rate_limited(50)
    def write_frame(stream, frame_data):
        stream.write(frame_data)
    
    def send_data_to_ws(stream):
        count = 0
        with open("longjoke.wav", "rb") as wav:
            while True:
                frame = 656
                frame_data = wav.read(frame)
                count += 1
                if count == 1:
                    print('count 1 time: ' + str(time.time()))
                if count == 224:
                    print('count 224 time: ' + str(time.time()))
                if len(frame_data) == 0:
                    print("load file completed")
                    print('load completed time: ' + str(time.time()))
                    break
                write_frame(stream,frame_data)
            global speech_recognizer
            if USE_CONTINUOUS_ASYNC is True:
                speech_recognizer.stop_continuous_recognition_async()
            else:
                speech_recognizer.stop_continuous_recognition()

    try:
        speech_config = speechsdk.SpeechConfig(
            account_id="speechdemo",
            password="12345678",
            speech_recognition_language='zh-TW',
            speech_recognition_punctuation=True
        )
        audio_format = audio.AudioStreamFormat()
        audio_stream = audio.PushAudioInputStream(audio_format)
        audio_config = audio.AudioConfig(stream=audio_stream)
        print(f"format: {audio_config.stream.stream_format.content_type}")
        global speech_recognizer
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config
        )

        speech_recognizer.recognizing.connect(
            lambda evt: print(f"{str(time.time())} Recognizing: {evt.result.text}"))
        speech_recognizer.recognized.connect(
            lambda evt: print(f'{str(time.time())} Recognized: {evt.result.text}'))
        speech_recognizer.canceled.connect(
            lambda evt: print(f'Canceled: {evt}'))
        speech_recognizer.session_started.connect(
            lambda evt: print(f'Session_started: {evt}'))
        speech_recognizer.session_stopped.connect(
            lambda evt: print(f'Session_stopped: {evt}'))

        t = threading.Thread(
            target=send_data_to_ws,
            args=(audio_stream,)
        )
        t.daemon = True
        t.start()
        if USE_CONTINUOUS_ASYNC is True:
            speech_recognizer.start_continuous_recognition_async()
            time.sleep(10)
        else:
            speech_recognizer.start_continuous_recognition()

    except KeyboardInterrupt:
        print("Caught keyboard interrupt. Canceling tasks...")
        if USE_CONTINUOUS_ASYNC is True:
            speech_recognizer.stop_continuous_recognition_async()
        else:
            speech_recognizer.stop_continuous_recognition()
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        print("stop main")
        sys.exit()

