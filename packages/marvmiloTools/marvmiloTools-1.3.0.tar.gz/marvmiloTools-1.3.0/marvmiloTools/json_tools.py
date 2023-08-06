import json

from . import dictionary_tools

#load a json file to dict or object
def load(filename, object = True):
    with open(filename, "r") as rd:
        loaded = json.loads(rd.read())
    if object:
        return dictionary_tools.toObj(loaded)
    else:
        return loaded

#save json file from dictionary to file
def save(dictionary, filename):
    with open(filename, "w") as wd:
        if type(dictionary) == dictionary_tools.DictObject:
            wd.write(json.dumps(dictionary.toDict(), indent = 4))
        else:
            wd.write(json.dumps(dictionary, indent = 4))
