class Chai:
    def __init__(self,type_,strength):
        self.type=type_
        self.strength=strength
    
    
# class GingerChai(Chai):
#     def __init__(self, type_, strength,spice_leve):
#         self.type=type_
#         self.strength=strength
#         self.spice_leve=spice_leve

# class GingerChai(Chai):
#     def __init__(self, type_, strength,spice_lavel):
#         Chai.__init__(type_, strength)
#         self.spice_lavel=spice_lavel
        
class GingerChai(Chai):
    def __init__(self, type_, strength,spice_lavel):
        super().__init__(type_, strength)
        self.spice_lavel=spice_lavel      