# import main Flask class and request object
from flask import Flask, request
from generation_request import GenerationRequest
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--generator', type=str, required=True,
                    help="Generator. Either 'oobabooga', 'llama.cpp'")
args = parser.parse_args()
if args.generator == "oobabooga":
    from gen_oobabooga import OobaboogaGenerator
    gen = OobaboogaGenerator()
elif args.generator == "llama.cpp":
    from gen_llamacpp import LlamaCppGenerator
    gen = LlamaCppGenerator()
else:
    raise Exception(f"Unexpected parser {args.parser}")

app = Flask(__name__)


@app.route('/api/v1/model')
def model_name():
    # result = {'result': 'facebook/opt-125m'}
    # print("Model name quieried")
    result = {'result': 'hoperator/oobabooga'}
    return result
    # return 'JSON Object Example'


@app.route('/api/v1/generate', methods=['POST'])
def generate_text(*args, **kwargs):

    data = request.json

    new_request = GenerationRequest()
    new_request.prompt = data.get('prompt')
    new_request.max_new_length = data.get('max_length')
    new_request.max_context_length = data.get('max_context_length')
    new_request.repetition_penalty = data.get('rep_pen')
    new_request.repetition_penalty_slope = data.get('rep_pen_slope')
    new_request.repetition_penalty_range = data.get('rep_pen_range')
    new_request.temperature = data.get('temperature')
    new_request.top_p = data.get('top_p')
    new_request.top_k = data.get('top_k')
    new_request.top_a = data.get('top_a')
    new_request.tail_free_sampling = data.get('tfs')
    new_request.typical = data.get('typical')
    new_request.batch_count = data.get('n')
    response = gen.run(new_request)
    result = {'results': [{
        "text": response
    }]}

    return result


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    print('You want path: %s' % path)
    return 'You want path: %s' % path


if __name__ == '__main__':
    app.run(debug=True, port=11111)
