#!/usr/bin/env python
from generation_request import GenerationRequest
'''
This is an example on how to use the API for oobabooga/text-generation-webui.
Make sure to start the web UI with the following flags:
python server.py --model MODEL --listen --no-stream
Optionally, you can also add the --share flag to generate a public gradio URL,
allowing you to use the API remotely.
'''
import requests
from base_generator import BaseGenerator


class OobaboogaGenerator(BaseGenerator):
    def __init__(self) -> None:
        super().__init__()

        # Server address
        self.server = "127.0.0.1"
        self.server_port = 7860

    def run(self, request: GenerationRequest):
        # Generation parameters
        # Reference: https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig
        params = {
            'max_new_tokens': request.max_new_length,
            'temperature': request.temperature,
            'top_p': request.top_p,
            'top_k': request.top_k,
            'typical_p': request.typical,
            'repetition_penalty': request.repetition_penalty,
            'do_sample': True,
            'min_length': 0,
            'no_repeat_ngram_size': 0,
            'num_beams': 1,
            'penalty_alpha': 0,
            'length_penalty': 1,
            'early_stopping': False,
        }

        # Input prompt
        prompt = request.prompt
        prompt = prompt.replace("</s>", "")
        print(f"***\n{prompt}\n\n")

        response = requests.post(f"http://{self.server}:{self.server_port}/run/textgen", json={
            "data": [
                prompt,
                params['max_new_tokens'],
                params['do_sample'],
                params['temperature'],
                params['top_p'],
                params['typical_p'],
                params['repetition_penalty'],
                params['top_k'],
                params['min_length'],
                params['no_repeat_ngram_size'],
                params['num_beams'],
                params['penalty_alpha'],
                params['length_penalty'],
                params['early_stopping'],
            ]
        }).json()

        reply = response["data"][0]
        return reply[len(prompt):]
