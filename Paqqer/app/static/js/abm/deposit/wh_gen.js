class warehouse{
    constructor(){
        this.name = "";
        this.h = 0;
        this.w = 0;
        this.lvl = 0;
        this.qpos = 0; // Cantidad de posiciones
        this.dpos = []; // Array que almacena las posiciones
    }

    create(h, w, lvl, name){
        this.name = name;
        this.h = h;
        this.w = w;
        this.lvl = lvl;

        this._createGrid();
    }

    /*
    Función que va a crear el array
    del objeto de posiciones segun la grilla creada
    por el usuario
    */
    _createGrid(){
        this.dpos = [];
        for (let lvl=0; lvl<=this.lvl; lvl++){
            let floor = [];
            for (let h=0; h<this.h; h++){
                let calle = [];
                for (let w=0; w<this.w; w++){
                    calle.push(new module());
                }
                floor.push(calle);
            }
            this.dpos.push(floor);
        }
    }

    _setSelect(){
        let selectObj = $("select[id='floor']");
        selectObj.empty();
        for (let lvl=0; lvl<=this.lvl; lvl++){
            let option = new Option(lvl, lvl);
            selectObj.append(option);
        }
    }

    drawIn(obj){
        this._setSelect();
        this._board = obj;
        let thead = "<tr><th>Calles</th>";
        for (let i=0; i<this.dpos[0][0].length; i++){
            thead += `
            <th col="${i}">
                <button id="configuration" class="btn btn-secondary">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-gear" viewBox="0 0 16 16">
                        <path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492zM5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0z"/>
                        <path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52l-.094-.319zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115l.094-.319z"/>
                    </svg>
                </button>
            </th>`
        }
        let html = "";
        for (let h in this.dpos[0]){
            html += `<tr><th>${h}</th>`;
            for (let w in this.dpos[0][h]){
                html += `
                    <td w="${h}" h="${w}"> ${this.dpos[0][h][w].html()}</td>                    
                `;
            }
            html += "</tr>";
        }
        $("table > thead").append(thead);
        $("table > tbody").append(html);
        this._refreshEvents();
    }

    _insertCol(mode){
        this.w++;
        for (floor in this.dpos){
            for (h in this.dpos[floor]){
                if (mode){ // en caso de la izquierda
                    this.dpos[floor][h][this.selectedCol-1];
                }
                else{
                    this.dpos[floor][h][this.selectedCol+1];

                } 
            }
        }

    }

    insR(){
        this._insertCol(1);
    }

    insL(){
        this._insertCol(0)
    }

    delCol(){

    }


    _refreshEvents(){
        let dpos = this.dpos;
        $("td > button").click(function(){
            let tdObj = $(this).parent();
            let h = + tdObj.attr("h");
            let w = + tdObj.attr("w");
            for (let floor in dpos){
                $(this).removeClass(dpos[floor][w][h].getClass());
                dpos[floor][w][h].changeType();
                $(this).addClass(dpos[floor][w][h].getClass());
                $(this).text(dpos[floor][w][h].getText());
            }
        });
        let obj = this;
        $("button[id='configuration']").click(function(){
            $("#modal").modal("toggle");
        });
    }

};