from app.auth import login
from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import current_user, login_required
from app import db
from app.models import Position, SKU, User, IMG, Deposit

putaway = Blueprint("putaway", __name__)


@putaway.route("/inbound/putaway", methods=["POST", "GET"])
@login_required
def index():
    userID = User.get_id(current_user)
    if request.method == "GET":
        WH = Deposit.query.filter_by(userID=userID).all()
        if WH:
            query = SKU.query.filter_by(userID=userID).all()
            return render_template("logged/inbound/putaway/index.html", 
                                    name=current_user.name,
                                    WH=WH,
                                    SKUData=query,
                                    SKUDataDict = SKU.getDict(SKU, query))
        else:
            return render_template("logged/inbound/putaway/nowarehouse.html")
            
    print(request.form.get("SKU"))
    SKUID = request.form.get("SKU")
    skuObj = SKU.query.filter_by(userID=userID, SKUID=SKUID).first()
    if skuObj:
        return redirect(
                        url_for("putaway.sku",
                                sku=SKUID))
    else:
        flash("skuBad")
        return redirect(url_for("putaway.index"))



@putaway.route("/putaway?sku=<sku>", methods=["GET", "POST"])
@login_required
def sku(sku):
    userID = User.get_id(current_user)
    if request.method == "GET":
        return render_template("logged/inbound/putaway/sku.html", 
                                sku=SKU.query.filter_by(userID=userID, SKUID=sku).first(),
                                img=IMG.query.filter_by(userID=userID, SKU=sku).first(),
                                name=current_user.name)
    else:
        posicion = request.form.get("posicion")
        try:
            wh, w, h, floor = posicion.split("-")
        except ValueError:
            flash("positionBad")
            print("NO")
            return redirect(url_for("putaway.sku", sku=sku, wh=wh))
        posObj = Position.query.filter_by(
            userID=userID,
            depositID=Deposit.query.filter_by(userID=userID, name=wh).first().ID,
            floor=floor,
            w=w,
            h=h
        ).first() #type: Position
        if posObj and posObj.type:
            cantidad = int(request.form.get("cantidad"))
            dictObj = dict(posObj.products) # type: dict
            if sku in dictObj:
                dictObj[sku] += cantidad
            else:
                dictObj[sku] = cantidad
            posObj.products = dictObj
            db.session.commit()
            print("SI")

            return redirect(url_for("putaway.index"))
        else:
            flash("positionBad")
            print("NO")
            return redirect(url_for("putaway.sku", sku=sku, wh=wh))
