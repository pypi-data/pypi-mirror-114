from os import system
from exceptions import *

class hcfg():


    def __init__(self) -> None:
        pass
    

    @staticmethod
    def readFile(fileName):
        buffer = {}
        if not fileName.endswith(".hcfg"):
            raise Exception("[Errno 0] This is a not .hcfg file.")
            

        if(open(fileName,"r")):
            raise Exception("[Errno 1] File does not exist.")

        with open(fileName,"r") as file:
            i = 0
            for line in file:
                try:
                    i += 1
                    object = line.split(":")
                    name = object[0].strip(" ")
                    value = hcfg.tryValue(object[1])
                    buffer[name] = value
                except hypSyntaxError:
                    raise hypSyntaxError(f"[Errno 2] Syntax error [Line:{i}].")
            return buffer

    @staticmethod
    def tryValue(value):
        try:
            val = int(value)
            return val
        except:
            None
        try:
            val = str(value).strip().strip('"')
            return val
        except:
            None
        try:
            val = bool(value)
            return val
        except:
            None    

                