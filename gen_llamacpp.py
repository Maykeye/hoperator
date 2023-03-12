#!/usr/bin/env python
from generation_request import GenerationRequest
from base_generator import BaseGenerator
import subprocess

CMD_APPN = ".appn$"
CMD_APP = ".app$"
CMD_DONE = ".done$"
CMD_GEN = ".gen$"


class LlamaCppGenerator(BaseGenerator):
    def __init__(self) -> None:
        super().__init__()

        self.cmd = "../llama.cpp/main -m ../llama.cpp/models/13B/ggml-model-q4_0.bin -t 16 -n 80"
        self.process = None

    def run_process(self):
        if self.process:
            return
        print("Starting the processs")
        self.process = subprocess.Popen(
            self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, text=True)
        print("Process is open")

    def run(self, request: GenerationRequest):
        self.run_process()

        # TODO: .topn$, etc

        # Input prompt
        prompt = request.prompt.replace("</s>", "")
        print(f"***: {prompt}")
        prompt_lines = prompt.splitlines(True)
        for i, line in enumerate(prompt_lines):
            if line.endswith("\n"):
                self.process.stdin.write(f"{CMD_APPN}{line}")
            else:
                self.process.stdin.write(f"{CMD_APP}{line}\n")
        self.process.stdin.write(f"{CMD_GEN}\n")
        self.process.stdin.flush()
        response = ""
        # text = "\n".join(prompt_lines) + "\n"
        # self.process.stdin.write(".echo$hello\n")

        while True:
            response_part = self.process.stdout.readline()
            response_part = response_part.rstrip("\n")
            print(f"<<< {response_part}")
            if response_part.startswith(CMD_APPN):
                response += response_part[len(CMD_APPN):]+"\n"
            elif response_part.startswith(CMD_APP):
                response += response_part[len(CMD_APP):]
            elif response_part.startswith(CMD_DONE):
                break
            else:
                print(f"ERROR: unexpected input {response_part}")
        print("***")
        print("Prompt:", prompt.replace('\n', '<NL>'))
        print("Response:", response.replace('\n', '<NL>'))

        return response[len(prompt):]


if __name__ == "__main__":
    gen = LlamaCppGenerator()
    req = GenerationRequest()
    req.prompt = "List of best cats names:\n10."
    print(gen.run(req))
