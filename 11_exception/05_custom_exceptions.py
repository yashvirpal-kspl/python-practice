def brew_chai(flavor):
    if flavor not in ["masala","ginger","elaichi"]:
        raise ValueError("Unsupported Chai flavor")
    
    print(f"Brewing {flavor} chai")

brew_chai("ginger")        
brew_chai("mint")    
