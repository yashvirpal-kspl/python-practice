class A:
    label = "A: base class"
    
class B(A):
    label="B: Masala blend"    

class C(A):
    label="C: Herbal blen"   
    
#class D(B,C):  #Fisrt Class called label (B in this )
class D(C,B):  #Fisrt Class called label (C in this )
    pass

cup=D()
print(cup.label)    
print(D.__mro__) 