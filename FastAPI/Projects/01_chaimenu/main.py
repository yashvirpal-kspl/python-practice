from fastapi import FastAPI ,Query,HTTPException
from models import MenuItem,MenuResponse
from data import menu_items

app = FastAPI(
    title="Chai Point Menu API",
    description="Read only menu API for Kiosk display and Mobile App"
)

@app.get("/")
def root():
    return {"message":"Welcome to chai point menu API"}


#/menu -> path
#/menu?name="test" -> query parameter

@app.get("/menu",response_model=MenuResponse) # 2nd Parameter is dependency injection
def get_menu(category:str | None = Query(None,description="Filter by chai,beverage or desert")):
    if category:
        filtered = [item for item in menu_items if item["category"] == category.lower()]
        if not filtered:
            raise HTTPException(status_code=404,detail="no item found in category: {category}")
        return MenuResponse(count=len(filtered),items=filtered)
    return MenuResponse(count=len(menu_items),items=menu_items)
        
@app.get("/menu/{item_id}",response_model=MenuItem)
def get_item(item_id:int):
    for item in menu_items:
        if item["id"]  == item_id:
            return item
    raise HTTPException(status_code=404,detail="no item found id for: {item_id}")    
        