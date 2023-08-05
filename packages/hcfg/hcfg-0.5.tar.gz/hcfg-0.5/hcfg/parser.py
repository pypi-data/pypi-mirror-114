from os import system


class hcfg():


    def __init__(self) -> None:
        pass
    
    def readFile(self,fileName):
        buffer = {}
        if not fileName.endswith(".hcfg"):
            raise Exception("[Errno 0] This is a not .hcfg file.")
            

        with open(fileName,"r") as file:
            i = 0
            for line in file:
                try:
                    i += 1
                    object = line.split(":")
                    name = object[0].strip(" ")
                    value = self.tryValue(object[1])
                    buffer[name] = value
                except:
                    raise Exception(f"[Errno 1] Syntax error [Line:{i}].")
            return buffer

    
    def tryValue(self,value):
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

                