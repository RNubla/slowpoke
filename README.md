## This is Slowpoke, a text to speech application based on tortoise

## Server To run the server, you will need the following

```
conda create --name tortoise python=3.9 numba inflect
conda activate tortoise
conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
conda install transformers=4.29.2
git clone https://github.com/neonbjb/tortoise-tts.git
cd tortoise-tts
python setup.py install

```

### To test if its running successfully

```
python tortoise/do_tts.py --text "I'm going to speak this" --voice random --preset fast

```
