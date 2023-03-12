Hoperator:

Hoperator is a primitive server which emulates enough of Kobold API
to connect Kobold Client(UI1) to Oobabooga.

Usage:

1) Start Oobabooga in no-stream mode
```console
$ cd text-generation-webui
$ python server.py --model llama-13b --load-in-4bit --no-stream
```
NOTE: --no-stream is important. Hoperator relies on it.

2) Start Hoperator 
```console
$ cd hoperator
# One of:
$ python kai_listener.py --generator oobabooga
$ python kai_listener.py --generator llama.cpp
```

3) Start kobold AI client 
```console
$ cd KoboldAI-Client
$ ./play.sh 
```
Select AI/Online Services/KoboldAI enter `http://localhost:11111` as API server

NOTE: "http://" is important. "localhost:11111" will not work.

4) Enjoy 

CAVEATS(aka WORKSFORME/WONTFIX):

* API introduces the model as `hoperator/oobabooga`. Kobold has no idea what tokenizer to use and use something default.
* Not all parameters are passed from the KAI to Oobabooga
* If Oobabooga runs out of memory or encounter any other error, it will not be reported to Kobold. Change settings and restart KAI client. 
* There is no way to change ports for hoperator or Oobabooga other than through editing the source code.

