class ListOfLists: 
    def __init__(self,args):
        self.lists = []
        for arg in args:
            self.lists += [arg]
            assert(type(arg) == list)

    def __len__(self):
        return sum(len(L) for L in self.lists)

    def __iter__(self):
        for L in self.lists:
            yield from L 
        
    
    def __getitem__(self, key):
        if (type(key) == int):
            for L in self.lists:
                if key < len(L):
                    return L[key]
                key -= len(L)
            raise Exception("Index out of bounds")
        else:
            raise Exception("Index must be integer")
        
    def __setitem__(self, key, value):
        raise Exception("ListOfLists Class does not modify original lists!")       


    