from fastapi import APIRouter

from app import contracts

router = APIRouter()


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/hotels/{hotel_id}")
async def read_item(hotel_id: int):
    return {"hotel_id": hotel_id}


@router.get("/users/")
async def read_user(user_id: str, name: str | None = None):
    if name:
        return {"item_id": user_id, "name": name}
    return {"item_id": user_id}


@router.get("/users/{user_id}/bookings/{item_id}")
async def read_user_item(  
    user_id: int, item_id: int, q: str | None = None, short: bool = False
):
    item = {"booking_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@router.post("/hotels/")
async def create_item(item: contracts.Hotel):
    item_dict = item.dict()

    if item.city == "Moscow":
        item_dict.update({"description": item.description + " in the capital of Russian Federation"})
    return item_dict
