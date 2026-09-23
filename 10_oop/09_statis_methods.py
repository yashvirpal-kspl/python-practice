class ChaiUtils:
    @staticmethod      #Decorator
    def  clean_ingredients(text):
        return [item.strip() for item in text.split(",")]


raw ="Water ,milk  ,ginger,  honey "
# obj=ChaiUtils()    Without static Decorator
# obj.clean_ingredients(raw)

cleaned=ChaiUtils.clean_ingredients(raw)
print(cleaned)

