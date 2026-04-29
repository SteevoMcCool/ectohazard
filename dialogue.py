from gamepaths import *
class Dialogue:
    
    class Node:
        def __init__(self,id,msg,optTxt,optRes):
            self.id = id 
            self.msg = msg
            self.optTxt = optTxt
            self.optRes = optRes
            def __str__(self):
                return self.msg + " "+str(len(self.optTxt))
                

    def __init__(self,dfilename):
        self.nodes:dict[int,Dialogue.Node] = {}

        sf = None 
        with open(getFile("_",dfilename,"dialogue")) as df:
            for line in df:
                if len(line := line.strip()) < 3:
                    continue
                if (line[0:3] == "opt"):
                    if not sf:
                        raise ValueError("Malformed file: got 'opt' before node id")
                    tokens = line.split('"')
                    sf.optTxt += [tokens[1]]
                    sf.optRes += [int(tokens[2].strip())]
                else:
                    if sf: self.nodes[sf.id] = sf 
                    tokens = line.split('"')
                    id = int(tokens[0].strip())
                    sf = Dialogue.Node(id,tokens[1].replace("\\n","\n"),[],[])
        if sf: self.nodes[sf.id] = sf 
    def next(self,currentState:int,optionId:int):
        if (optionId == -1): return -1
        node = self.nodes[currentState]
        return node.optRes[optionId]

    def options(self,currentState:int):
        return self.nodes[currentState].optTxt
    def text(self,currentState:int):
        return self.nodes[currentState].msg

    def __str__(self):
        return "\n".join(str(node) for node in self.nodes)