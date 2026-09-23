class BaseChai:
    def __init__(self,type_):
        self.type=type_
        
    def prepare(self):
        print(f"Preparing {self.type} chai ....")    
        
class MasalaChai(BaseChai):
    def add_spice(self):
        print(f"Added cardamon,ginger,clove")
        
class Chaishop:
    chai_cls=BaseChai   
    
    def __init__(self):
        self.chai=self.chai_cls("Regular")
        
    def serve(self):
        print(f"Serving {self.chai.type} chain in shop")    
        self.chai.prepare()
        
class Fancychaishop(Chaishop):
    chai_cls=MasalaChai        
  
shop=Chaishop()
fancy=Fancychaishop()    
shop.serve()
fancy.serve()
fancy.chai.add_spice()