from flask import Blueprint, url_for, redirect, render_template, request
from flask_login import current_user
from app.models import User, Providers
from app import db
abm_providers = Blueprint("abm_providers", __name__)

@abm_providers.route("/abm/providers", methods=["GET", "POST"])
def index():
    userID = User.get_id(current_user)
    data = None
    if request.method == "GET":
        data = Providers.query.filter_by(userID=userID).order_by(Providers.IDProvider.asc()).all()
    else:
        type = Providers.__dict__[request.form.get("type")]
        data = Providers.query.filter(Providers.userID==userID, 
                                      type.contains(request.form.get("search"))
                                      ).order_by(Providers.IDProvider.asc()).all()
    return render_template("logged/abm/providers/index.html", data=data, name=current_user.name, userID=userID)


@abm_providers.route("/abm/providers/newprovider", methods=["POST"])
def post_provider():
    userID = User.get_id(current_user)
    IDProvider = int(request.form.get("IDProvider"))
    if IDProvider >= 0: # En caso de que sea un cambio
        editProvider = Providers.query.filter_by(userID=userID, IDProvider=IDProvider)
        editProvider.update(request.form.to_dict())
    else: # En caso de que sea un nuevo proveedor
        data = request.form.to_dict()
        data["IDProvider"] = Providers.query.filter_by(userID=userID).order_by(Providers.IDProvider.desc()).count()+1
        data["userID"] = userID
        newProvider = Providers(**data)
        db.session.add(newProvider)
    db.session.commit()
    return redirect(request.referrer)