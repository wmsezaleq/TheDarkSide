from datetime import datetime
from app import io, db
from app.models import BuyOrder, SKU, Providers, IMG, Deposit, Position
from flask import request, url_for, redirect


# SKU
@io.on("flash_newSKU")
def flask_newSKU(description, precio, userID):
    cliente = request.sid
    data = SKU.query.filter_by(userID=userID)
    ID = data.count()
    SKUID = SKU.getSKU(SKU, ID)
    sku = SKU(
        INTSKU=ID,
        SKUID=SKUID,
        userID=userID,
        description=description,
        price=int(precio),
    )
    db.session.add(sku)
    db.session.commit()

    io.emit("updateListSKU", SKU.getDict(SKU, data.all()), room=cliente)



# BuyOrders 
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


# SKU 
@io.on("productDelete")
def productDelete(SKUID, userID):
    for row in BuyOrder.query.filter_by(userID=userID).all():
        if SKUID in row.SKU:
            io.emit("productDeleteAsk")
            return
    productDeleteConfirm(SKUID, userID)
    

@io.on("productDeleteConfirm")
def productDeleteConfirm(SKUID, userID):
    for row in BuyOrder.query.filter_by(userID=userID).all():
        if SKUID in row.SKU:
            db.session.delete(row)
    SKU.query.filter_by(userID=userID, SKUID=SKUID).delete()
    try:
        IMG.query.filter_by(userID=userID, SKUID=SKUID).delete()
    except:
        pass
    db.session.commit()
    io.emit("refreshPage", room=request.sid)

# Providers
@io.on("deleteProvider")
def providerDelete(IDProvider, userID):
    Providers.query.filter_by(IDProvider=IDProvider, userID=userID).delete()
    db.session.commit()
    io.emit("refreshPage", room=request.sid)




@io.on("confirmLayout")
def confirmLayout(data):
        
    userID, whObj = data
    whQuery = Deposit.query.filter_by(userID=userID, name=whObj["name"]).first()
    if whQuery: # En caso de que sea en modo edición
        whQuery.h = whObj["h"]
        whQuery.w = whObj["w"]
        whQuery.lvl = whObj["lvl"]
        layout = whObj["layout"]
        for floor, dummy in enumerate(layout):
            for w, dummy in enumerate(layout[floor]):
                for h, dummy in enumerate(layout[floor][w]):
                    posObj = Position.query.filter_by(userID=userID,
                                             depositID=whQuery.ID,
                                             w=w,
                                             h=h,
                                             floor=floor).first()
                    posObj.type = dummy["type"]

    else:
        depoObj = Deposit(
            userID=userID,
            h=whObj["h"],
            w=whObj["w"],
            lvl=whObj["lvl"],
            name=whObj["name"]
        )
        db.session.add(depoObj)
        depositID = len(Deposit.query.all())+1

        layout = whObj["layout"]
        for floor, dummy in enumerate(layout):
            for w, dummy in enumerate(layout[floor]):
                for h, dummy in enumerate(layout[floor][w]):
                    posObj = Position(
                        userID=userID,
                        depositID=depositID,
                        w=w,
                        h=h,
                        floor=floor,
                        type=dummy["type"],
                        products={}
                    )
                    db.session.add(posObj)

    db.session.commit()
    io.emit("layout_getBack", room=request.sid)


@io.on("delete_deposit")
def delete_deposit(data):
    userID = data["userID"]
    depositID = data["depositID"]
    depoObj = Deposit.query.filter_by(ID=depositID, userID=userID).first()
    posiObj = Position.query.filter_by(userID=userID, depositID=depositID).all()
    db.session.delete(depoObj)
    for posi in posiObj:
        db.session.delete(posi)
    db.session.commit()
    io.emit("refreshPage", room=request.sid)
    return redirect(url_for("abm_deposit.index"))