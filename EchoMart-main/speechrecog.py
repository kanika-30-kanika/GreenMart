import speech_recognition as sr
import whisper 
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
import pickle
model = whisper.load_model("small.en")
model.cuda(0)
def pickler(name,obj):
    file = open(name+".pickle","wb")
    pickle.dump(obj=obj,file=file)
    file.close()

def depickle(fname):
    file = open(fname+".pickle","rb")
    pickle_obj = pickle.load(file)
    file.close()
    return pickle_obj

def stt():
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            aud = r.listen(source)
        newf = open("tmp.wav","wb")
        newf.write(aud.get_wav_data())
        newf.close()
        print("Thinking")
        #time.sleep(2)
        res = model.transcribe("tmp.wav")
        if "Stop" in res['text']:
            print("Stopping")
            break
        print(res['text'])

def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        aud = r.listen(source)
    newf = open("tmp.wav","wb")
    newf.write(aud.get_wav_data())
    newf.close()
    print("Thinking")
    #time.sleep(2)
    res = model.transcribe("tmp.wav")
    return res['text']


def speech_to_text_always():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        #r.listen_in_background(source)
        print("Speak Now")
        aud = r.listen(source)
    newf = open("tmp.wav","wb")
    newf.write(aud.get_wav_data())
    newf.close()
    print("Thinking")
    #time.sleep(2)
    res = model.transcribe("tmp.wav")
    return res['text']


def getTags(text):
    wnl = WordNetLemmatizer()
    arr = pos_tag([i.lower() for i in word_tokenize(text)])
    wordlist = []
    for i in arr:
        if i[1][0]=='N':
            wordlist.append(wnl.lemmatize(i[0],pos=i[1].lower()[0]))
        else:
            wordlist.append(i[0])
    tags = depickle('total_tags')
    return [i for i in wordlist if i in tags]

#res = model.transcribe("D:\\ITProject\\tmp.wav")
#print(res)
