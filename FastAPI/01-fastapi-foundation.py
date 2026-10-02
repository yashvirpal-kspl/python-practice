from fastapi import FastAPI
from fastapi import Request
import uvicorn

app = FastAPI(
    title="Swiggy Order Service",
    description=(
        "Internal API for managing orders"
        "Handle creation ,tracking of delivery system"
    ),
    version="1.2.1",
    docs_url="/docs",
    redoc_url="/redocs",
    openapi_url="/openapi.json"
)

@app.get("/")
def read_root():
    """ Root Endpoint - Health check"""
    # FastAPI convert this dict to json 
    return {"message":"Welcome to swiggy order service","status":"healthy"}

@app.get("/about")
def about():
    """Return API Metadata"""
    return {
        "service":"order-service",
        "team":"backend plateform",
        "region":"ap-south-1",
        "version":"1.2.1"
    }
    
@app.get("/orders")
def list_orders():
    """ List resent orders """    
    return {
        "order":[
            {"id":1,"item":"Butter Chicken","status":"delivered"},
            {"id":2,"item":"Masala Dosa","status":"preparing"},
            {"id":3,"item":"Paneer Tikka","status":"delivered"},
        ]
    }
@app.get("/orders/status")
def order_status():
    """ Get Order Status """    
    return {
        "total_today":2_340_23,
        "top_city":"Noida"
    }
    
@app.get("/debug/request-info")
async def request_info(request:Request):
    """ Inspect the raw request object"""
    return {
        "method":request.method,
        "url":str(request.url),
        "headers":dict(request.headers),
        "path_params":request.path_params,
        "query_params":dict(request.query_params)
    }
    
@app.get(
    "/orders/active",
    summary="Get Active Orders",
    description=(
        "Return all orders that are currently being prepared"
        "or are out for delivery"
    ),
    tags=['orders'],
    response_description="List of active order",
    deprecated=False,
)

def get_active_order():
    """This doc string also apears in docs"""
    return {
        "active_orders":[
            {"id":1,"item":"Masala Dosa","status":"out_for_delivery"},
        ]
    }
    
@app.get("/restaurants",tags=["Restaurants"])
def list_restro():
    """Another Description for another endpoint"""    
    return {
        "restaurants":[
            {"test":"test"}
        ]
    }