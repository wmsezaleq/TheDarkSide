from datetime import datetime
from app import io, db
from app.models import BuyOrder, SKU, Providers
from flask import request

@io.on("flash_newSKU")
def flask_newSKU(description, precio, userID):
    cliente = request.sid
    ID = SKU.query.filter_by(userID=userID).count()
    SKUID = hex(ID).split("x")[1].zfill(10)
    sku = SKU(
        ID=ID,
        SKUID=SKUID,
        userID=userID,
        description=description,
        price=int(precio),
        image=""
    )
    db.session.add(sku)
    db.session.commit()

    io.emit("updateListSKU", SKU.getDict(SKU, userID), room=cliente)


@io.on("filterBuyOrders")
def filterBuyOrders(data):
    fromDate = datetime.date(datetime.strptime(data["fromDate"], "%Y-%m-%d"))
    toDate = datetime.date(datetime.strptime(data["toDate"], "%Y-%m-%d"))
    type = data["type"]
    text = data["text"]
    userID = data["userID"]
    orders = {}

    if text == "": # Solo veo la fecha:
        orders = BuyOrder.getDict(BuyOrder, data=BuyOrder.query.filter_by(userID=userID), 
                                            fromDate=fromDate, 
                                            toDate=toDate)
    else:
        if type=="Provider":
            type = "IDProvider"
            try:
                text = Providers.query.filter(Providers.userID==userID, Providers.name.contains(text)).first().IDProvider
            except AttributeError:
                IDProvider = -1
        orders = BuyOrder.getDict(BuyOrder, data=BuyOrder.query.filter_by(**{type : text}, userID=userID),
                                            fromDate=fromDate,
                                            toDate=toDate)

    io.emit("BuyOrderFilteredData", orders, room=request.sid)

        
