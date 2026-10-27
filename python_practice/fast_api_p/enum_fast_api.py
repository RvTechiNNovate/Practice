from enum import Enum,unique
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app= FastAPI()

# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
# @unique
# class ModelName(str,Enum):
#     gpt1 = "alexnet"
#     gpt2 = "resnet"
#     gpt3 = "lenet"
#     # gpt4= "alexnet"

# @app.get("/get_req")
# def get_req(model_name:ModelName):
#     print(model_name)
#     print(model_name==ModelName.gpt1)
#     print(model_name==ModelName.gpt2)
#     print("----------------------------------")
#     print(ModelName["gpt1"])
#     print(ModelName.gpt1.name)
#     print(ModelName.gpt1.value)

#     return {"response":"hi there this is the response : "+ model_name}

# @app.get("/items")
# def get_items(skip:int=0,limit:int=2):
#     return fake_items_db[skip:skip+limit]




class OrderStatus(Enum):
    PENDING="pending"
    SHIPPED="shipped"
    DELIVERED="delivered"


class OrderInputPayload(BaseModel):
    order_id:int
    order_status: Optional[OrderStatus]=Field(
        default=OrderStatus.PENDING,
        examples=["pending","delivered","shipped"]
        )


@app.post("/post_order")
def post_order(order:OrderInputPayload):
    print(order.order_id)
    print(order.order_status)
    return {
        "order_id":order.order_id,
        "status":order.order_status
        }

enabled_payment_methods="STRIPE,PAYPAL".split(",")

PaymentProvider=Enum(
    "PaymentProvider", 
    {method.strip(): method.strip().lower() for method in enabled_payment_methods}
)


# Usage
print(PaymentProvider.STRIPE)        # PaymentProvider.STRIPE
print(PaymentProvider.STRIPE.value)  # "stripe"

# class UserRole(Enum):
#     ADMIN="admin"
#     EDITOR="editor"
#     VIEWER="viewer"

#     @property
#     def permissions(self):
#         if self==UserRole.ADMIN:
#             return ["create","edit","delete"]
#         if self==UserRole.EDITOR:
#             return ["edit"]
#         return []

#     def can_delete(dd):
#         return "delete" in dd.permissions

# current_user = UserRole.ADMIN
# print(current_user.permissions)  # ['edit']
# print(current_user.can_delete()) # False


# if __name__=="__main__":
#     import uvicorn
#     uvicorn.run(app,host="localhost",port=9000)
