from flask import Blueprint, request
from flask.helpers import url_for
from flask_login import current_user, login_required
from flask.templating import render_template
from werkzeug.utils import redirect
from app.models import User, Deposit, Position
from app import db
import barcode
from io import BytesIO
from barcode.writer import ImageWriter
import base64

abm_deposit = Blueprint("abm_deposit", __name__)

@abm_deposit.route("/abm/deposit")
@login_required
def index():
    userID = User.get_id(current_user)
    depositos = Deposit.query.filter_by(userID=userID).all()
    depositos_dict = {}
    posDict = {}
    for depo in depositos:
        depositos_dict[depo.name] = {"total" : 0, "productos" : 0, "id" : depo.ID}
        posDict[depo.ID] = []
        posiciones = Position.query.filter_by(userID=userID, depositID=depo.ID).all()

        for pos in posiciones:
            for producto in pos.products:
                depositos_dict[depo.name]["productos"] += pos.products[producto]
            if pos.type:
                depositos_dict[depo.name]["total"] += 1
                posDict[depo.ID].append(f"{pos.w}-{pos.h}-{pos.floor}")

    return render_template("logged/abm/deposit/index.html", name=current_user.name,
                                                            depositos=depositos_dict,
                                                            posiciones=posDict,
                                                            userID=userID)
@abm_deposit.route("/abm/deposit/edit?deposit=<whname>")
@login_required
def edit(whname):
    userID = User.get_id(current_user)
    wh = Deposit.query.filter_by(userID=userID, name=whname).first()
    data = {"mode" : "edit", 
            "h" : wh.h,
            "w" : wh.w,
            "lvl" : wh.lvl,
            "name" : wh.name,
            "dpos" : {}}
    dpos = {}
    for row in Position.query.filter_by(userID=userID,
                                          depositID=wh.ID).all():
        row : Position
        if row.floor not in dpos:
            dpos[row.floor] = {row.h : {row.w : row.type}}
        elif row.h not in dpos[row.floor]:
            dpos[row.floor][row.h] = {row.w : row.type}
        else:
            dpos[row.floor][row.h][row.w] = row.type

    data["dpos"] = dpos
    return render_template("logged/abm/deposit/new.html",
                            userID=userID,
                            name=current_user.name,
                            mode=data)
        

@abm_deposit.route("/abm/deposit/new")
@login_required
def new():
    userID = User.get_id(current_user)
    return render_template("logged/abm/deposit/new.html", userID=userID,  mode={"mode" : "new"}, name=current_user.name)

@abm_deposit.route("/abm/deposit/print", methods=["POST"])
@login_required
def post_printing():
    userID = User.get_id(current_user)
    posiciones = request.form.get("posSelected").split(";;;")
    barcodes = []
    depositID = request.form.get("depositID")
    depoObj = Deposit.query.filter_by(userID=userID, ID=depositID).first()
    posiciones.sort()
    for pos in posiciones:
        if pos:
            data = f"{depoObj.name}-{pos}"
            img = barcode.get("code128", data, writer=ImageWriter()).render()
            bytearr = BytesIO()
            img.save(bytearr, format="PNG")
            bytearr = bytearr.getvalue()
            barcodes.append(base64.b64encode(bytearr))
    
    
    return render_template("logged/abm/deposit/printpos.html", barcodes=barcodes, name=current_user.name)
