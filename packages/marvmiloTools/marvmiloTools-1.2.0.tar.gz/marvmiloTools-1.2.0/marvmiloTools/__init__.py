import json
import os
import datetime as dt
import copy

#load other scripts
from . import dash_tools as dash

#convert dictionary to object
def Dicts2Obj(instance):
    class DictObject():
        def __init__(self, instance):
            if not isinstance(instance, dict):
                raise TypeError("No dictionary")
            else:
                self._current = 0
                for key in instance:
                    if isinstance(instance[key], dict):
                        self.__dict__[key] = DictObject(instance[key])
                    else:
                        self.__dict__[key] = Dicts2Obj(instance[key])
        
        def __str__(self):
            return str({k:(v.__str__() if isinstance(v, DictObject) else v) for k,v in self.__dict__.items() if not k.startswith("_")})
        __repr__ = __str__
        def __iter__(self):
            return self
        def __next__(self):
            try:
                val = [key for key in list(self.__dict__.keys()) if not key.startswith("_")][self._current]
                self._current += 1
                return val
            except IndexError:
                raise StopIteration
        def __len__(self):
            return(len(self.__dict__)-1)
        def __getitem__(self, item):
            return self.__dict__[item]
        def __setitem__(self, item, value):
            self.__dict__[item] = value
        def __delitem__(self, item):
            del self.__dict__[item]
        
        def get(self, item):
            return self.__dict__[item]
        def keys(self):
            return {k:v for k,v in self.__dict__.items() if not k.startswith("_")}.keys()
        def values(self):
            return {k:v for k,v in self.__dict__.items() if not k.startswith("_")}.values()
        def items(self):
            return {k:v for k,v in self.__dict__.items() if not k.startswith("_")}.items()
        def update(self, dictionary):
            self.__dict__.update(dictionary)
        def pop(self, item):
            self.__dict__.pop(item)
        def popitem(self):
            self.__dict__.popitem()
        def clear(self):
            self.__dict__.clear()
        def copy(self):
            return self.__dict__.copy()
        
    if isinstance(instance, dict):
        return DictObject(instance)
    
    elif isinstance(instance, str):
        return instance
    
    else: 
        try:
            for i, item in enumerate(instance):
                if isinstance(item, dict):
                    instance[i] = DictObject(item)
                else:
                    instance[i] = Dicts2Obj(item)
            return instance
        except TypeError:
            return instance

#load a json file to dict or object
def loadJson(filename, object = True):
    with open(filename, "r") as rd:
        loaded = json.loads(rd.read())
    if object:
        return Dicts2Obj(loaded)
    else:
        return loaded

#print command with Script name in front
class ScriptPrint:
    def __init__(self, name, block = False):
        self.name = name
        self.block = block
    def print(self, msg):
        if not self.block:
            print(f"[{self.name}]: {msg}")
            
#Timer for Script runtimes
class Timer:
    def __init__(self):
        self.startpoint = None
        self.lapstartpoint = None
        self.runtime = dt.timedelta(seconds = 0)
        self.lapruntime = dt.timedelta(seconds = 0)
        self.laps = []
    def start(self):
        if not self.startpoint:
            self.startpoint = dt.datetime.now()
            self.lapstartpoint = dt.datetime.now()
        else:
            raise Exception("Timer already running")
    def pause(self):
        if self.startpoint:
            now = dt.datetime.now()
            self.runtime += now - self.startpoint
            self.lapruntime += now - self.lapstartpoint
            self.startpoint = None
            self.lapstartpoint = None
            return self.runtime
        else:
            raise Exception("Timer not running")
    def set_lap(self):
        if self.lapstartpoint:
            now = dt.datetime.now()
            self.laps.append(self.lapruntime + now - self.lapstartpoint)
            self.lapstartpoint = now
            self.lapruntime = dt.timedelta(seconds = 0)
            return self.laps[-1]
        else:
            self.laps.append(self.lapruntime)
            self.lapruntime = dt.timedelta(seconds = 0)
            return self.laps[-1]
    def get_runtime(self):
        if self.startpoint:
            return self.runtime + dt.datetime.now() - self.startpoint
        else:
            return self.runtime
    def get_laps(self):
        return self.laps
    def get_lap_runtime(self):
        if self.lapstartpoint:
            return self.lapruntime + dt.datetime.now() - self.lapstartpoint
        else:
            return self.lapruntime
    def reset(self):
        self.__init__()
timer = Timer()                    