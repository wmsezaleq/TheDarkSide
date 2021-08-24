var wh = undefined;
const socketio = io();

$(function(){
    wh = new warehouse();
    let formLayout = $("form[name='generation']");
    let divLayout = $("div[name='layout']");
    if (modeData["mode"] == "edit"){
        formLayout.hide();
        divLayout.show();

        wh.create(modeData["h"],
                  modeData["w"],
                  modeData["lvl"],
                  modeData["name"]);
        for (let lvl in wh.dpos){
            for (let h in wh.dpos[lvl]){
                for(let w in wh.dpos[lvl][h]){
                    let mod = new module();
                    mod.type = modeData["dpos"][lvl][w][h];
                    wh.dpos[lvl][h][w] = mod;
                }
            }
        }
        wh.drawIn(divLayout);
    }
    $("button[id='generateLayout']").click(function(){
        if(formLayout.valid()){
            formLayout.hide();
            divLayout.show();
    
            let h = + $("input[id='alto']").val();
            let w = + $("input[id='ancho']").val();
            let lvl = + $("input[id='niveles']").val();
            let name = $("input[id='whname']").val();
            $("h1[name='whname']").text(name);
            wh.create(h, w, lvl, name);
            wh.drawIn(divLayout);
        }

    });


    $("button[id='insR']").click(function(){
        wh.insR();
    });
    $("button[id='insL']").click(function(){
        wh.insL();
    });
    $("button[id='delCol']").click(function(){
        wh.delCol();
    });
    $("button[name='confirmLayout']").click(function(){
        socketio.emit("confirmLayout", [userID, {
            "name" : wh.name,
            "h" : wh.h,
            "w" : wh.w,
            "lvl" : wh.lvl,
            "layout" : wh.dpos
        }]);
    });

});