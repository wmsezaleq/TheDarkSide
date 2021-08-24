const types={
    MODULE: 1,
    CORRIDOR: 0
};

class module{
    constructor(){
        this.type = types.MODULE;
    }

    changeType(){
        this.type = !this.type; 
    }

    html(){
        return `<button class='${this.getClass()}'>${this.getText()}</button>`;
    }

    getClass(){
        if (this.type){
            return "btn btn-primary";
        }
        return "btn btn-secondary"
    }

    getText(){
        if (this.type){
            return "Módulo";
        }
        return "Pasillo";
    }
}