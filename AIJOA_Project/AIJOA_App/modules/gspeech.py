# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import division

import re
import sys

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue
from threading import Thread
import time

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True
        self.isPause = False

    def __enter__(self): # class가 시작될때 적용 되는 부분
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback): # class가 끝나면서 적용 되는 부분
        self._audio_stream.stop_stream()
        self._audio_stream.close()

        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def pause(self):
        if self.isPause == False:
            self.isPause = True

    def resume(self):
        if self.isPause == True:
            self.isPause = False

    def status(self):
        return self.isPause

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        if self.isPause == False:
            self._buff.put(in_data)
        # else
        return None, pyaudio.paContinue

    def generator(self):
        print("not self.closed: ", not self.closed)  # True
        print("self.closed: ", self.closed)          # False
        ## 여기에 if문으로 최초 음성인식 활성화부분이 들어가야 될꺼 같음
        # 음성이 들어오기 전까지 while문이 계속 실행되고 있는 상태로 보임
        # 무한 대기 같은 느낌적인 느낌
        while not self.closed:
            # 아래 class Gspeech에서 def run안에 with MicrophoneStream 부분이
            # 끝나야 closed가 True로 바뀌면서 not self.closed가 False가 되면서
            # while문이 종교가 되는데 현재 closed를 control하는 부분이
            # example.py에서 음성에 그만이 들어와서 '그만'이라는 text가 있어야
            # 전체 프로그램이 종료가 되는 상황으로 보임

            chunk = self._buff.get()
            if chunk is None:
                return

            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


# [END audio_stream]


class Gspeech(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.language_code = 'ko-KR'  # a BCP-47 language tag

        self._buff = queue.Queue()

        self.client = speech.SpeechClient()
        self.config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=self.language_code)
        self.streaming_config = types.StreamingRecognitionConfig(
            config=self.config,
            interim_results=True)

        self.mic = None
        self.status = True

        self.daemon = True
        # 자기자신의 쓰레드를 실행시킨다...그래서 자기자신의 쓰레드는 누구나?
        # 아마도 def run 함수가 실행 되는거 같다
        self.start()

    def __eixt__(self):
        self._buff.put(None)

    def run(self):
        with MicrophoneStream(RATE, CHUNK) as stream:
            self.mic = stream
            audio_generator = stream.generator()
            print("type(audio_generator): ", type(audio_generator))
            requests = (types.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)
            print("type(requests): ", type(requests))
            responses = self.client.streaming_recognize(
                self.streaming_config, requests)
            print("type(responses): ", type(responses))
            # for response in responses:
            #     print("response: ", response)

            # Now, put the transcription responses to use.
            self.listen_print_loop(responses, stream)
        self._buff.put(None)
        self.status = False

    def pauseMic(self):
        if self.mic is not None:
            self.mic.pause()

    def resumeMic(self):
        if self.mic is not None:
            self.mic.resume()

    # 인식된 Text 가져가기
    def getText(self, block=True):
        return self._buff.get(block=block)

    # 음성인식 처리 루틴
    def listen_print_loop(self, responses, mic):
        num_chars_printed = 0
        try:
            for response in responses:
                # response는 '그만'이라고 말하면 아래와 같이 나온다
                # response:
                # results {
                #     alternatives {transcript: "\352\267\270\353\247\214"}
                #     stability: 0.009999999776482582
                #     result_end_time {seconds: 5 nanos: 340000000}
                # }
                #
                # response:
                # results {
                #     alternatives {transcript: "\352\267\270\353\247\214"
                #                   confidence: 0.9236595630645752}
                #     is_final: true
                #     result_end_time {seconds: 5 nanos: 730000000}
                # }
                if not response.results:
                    # response.results가 False면(비어있으면) continue
                    continue

                # response.results가 True면(비어있지 않으면) 아래 코드 실행
                result = response.results[0]
                if not result.alternatives:
                    # result.alternatives가 False면(비어있으면) continue
                    continue

                # result.alternatives가 True면(비어있지 않으면) 아래 코드 실행
                transcript = result.alternatives[0].transcript # transcript: "\354\213\234\354\236\221"
                overwrite_chars = ' ' * (num_chars_printed - len(transcript))
                #
                if not result.is_final: # result.is_final이 False면
                    sys.stdout.write(transcript + overwrite_chars + '\r')
                    sys.stdout.flush()
                    # 추가 ### 화면에 인식 되는 동안 표시되는 부분.
                    num_chars_printed = len(transcript)
                else: # result.is_final이 True면
                    # 큐에 넣는다.
                    self._buff.put(transcript+overwrite_chars)
                    num_chars_printed = 0
        except:
            return
