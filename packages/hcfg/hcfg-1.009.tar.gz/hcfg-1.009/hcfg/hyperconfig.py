from os import system
from hcfg.exceptions import *

class hcfg():


    def __init__(self) -> None:
        pass
    

    @staticmethod
    def readFile(fileName):
        buffer = {}
        if not fileName.endswith(".hcfg"):
            raise hypFileError("[Errno 0] This is a not .hcfg file.")
            return
            

        if not (open(fileName,"r")):
            raise hypFileError("[Errno 1] File does not exist.")
            return

        with open(fileName,"r") as file:
            i = 0
            for line in file:
                i += 1
                object = line.split(":")
                if len(object) <= 1:
                    raise hypSyntaxError(f"[Errno 2] Syntax error [Line:{i}].")
                    return
                name = object[0].strip(" ")
                value = hcfg.assignValue(object[1])
                buffer[name] = value
            return buffer

    @staticmethod
    def saveFile(filename,object):
        if not filename.endswith(".hcfg"):
            raise hypFileError("[Errno 0] This is a not .hcfg file.")
            return
        with open(filename, "w") as file:
            for i in object:
                string = f"{i} : {object[i]}\n"
                file.writelines(string)
                
            
        
        

    @staticmethod
    def assignValue(value):
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

                