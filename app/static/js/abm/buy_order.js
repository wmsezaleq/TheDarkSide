var totalQ = 0;
var totalPrice = 0.0;


/*
    Función que va a agregar el HTML nuevo de la nueva fila
    asignándole nuevo index automáticamente y refrescando
    todas las funciones asociadas a los widgets
*/
function addRow(newIndex) {
    $("tbody").append(`
        <tr index="${newIndex}">
            <td>
                <div class="row">
                    <div class="col-10 form-group">
                        <input type="text" index="${newIndex}" list="SKUs" name="SKU${newIndex}" data-bs-toggle="tooltip" data-bs-placement="top" title="Saraza" class="form-control input-sm" required>
                    </div>
                    <div name="skuAdd${newIndex}" style="display: none" class="col-2 ps-2 pt-1">
                        <button data-bs-toggle="modal" data-bs-target="#newSKUModal" type="button" name="addSKU" style="cursor: pointer; background-color: transparent; border: none;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle" viewBox="0 0 16 16">
                                <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
                            </svg>
                        </button>
                    </div>
                </div>
            </td>
            <td>
                <div class="row">
                    <div class="col-11 form-group">
                        <input class="form-control input-sm" list="Descriptions" index="${newIndex}" name="description${newIndex}" type="text" required>
                    </div>
                    <div class="col-1 ps-2 pt-1" name = "descriptionAdd${newIndex}" style="display: none">
                        <button data-bs-toggle="modal" data-bs-target="#newSKUModal" type="button" name="addSKU" style="cursor: pointer; background-color: transparent; border: none;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle" viewBox="0 0 16 16">
                                <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
                            </svg>
                        </button>
                    </div>
                </div>
            </td>
            
            <td><input class="form-control input-sm" index="${newIndex}" name="quantity${newIndex}" type="number" required></td>
            <td><input class="form-control input-sm" index="${newIndex}" name="price${newIndex}" type="number" required></td>
                    <td>
                        <button type="button" id="delete${newIndex}" index="${newIndex}" style="background-color:transparent; border-color: transparent;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                                <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"/>
                            </svg>
                        </button>
                    </td>
        </tr>`);
    reloadFunctions();
}

function deleteRow(index) {
    $(`tr[index='${index}'`).remove();
}



/*
Función que va a verificar que se haya presionado TAB en los tachitos de basura o 
en último input (precio bruto) para crear automáticamente otra fila sin tener
que realizar el click en crear nueva fila, focuseando en el primer input de la misma

También va a chequear que se haya presionado espacio en los tachitos de basura 
para eliminarlos sin tener que realizar el click
*/

function test_append(e, thisObj, type) {
    var code = e.keyCode || e.which;
    if (code == 9 && !e.shiftKey) {  // Si se presionó la tecla tab
        e.preventDefault();
        let newIndex = $("input[name*='quantity']").length
        if (thisObj.attr('index') == newIndex - 1 && (type == "button" || type == "primary")) { // En caso de que sea el último input change 
            addRow(newIndex);        // Añado una nueva row
            $(`input[name='SKU${newIndex}']`).focus();
        }
        else {
            let myIndex = +thisObj.attr("index");
            if (type == "primary" || type == "button") {
                $(`input[name='SKU${myIndex + 1}']`).focus();
            }
            else if (type == "secondary") {
                $(`button[id='delete${myIndex}']`).focus();
            }
        }
    }
    else if (code == 32 && type == "button") { // En caso de tocar espacio y que sea el botón de eliminar
        let myIndex = thisObj.attr("index");
        deleteRow(myIndex);
    }
}


/*
    Función que va a actualizar el precio y la cantidad 
    recorriendo todos los quantity y price objetos del tipo input
    guardando la información también en las variables globales 
    totalQ y totalPrice
*/
function updatePrice(){
    totalQ = 0;
    // Recorro todos los elementos que sean del tipo quantity
    $("input[name*='quantity'").each(function(){
        totalQ += +$(this).val() // Sumo sus valores al total de cantidad
    });
    $(".q").text(totalQ)


    totalPrice = 0;
    // Para el precio recorro lo mismo y su respectiva cantidad para hacer la multiplicación
    $("input[name*='price'").each(function(){
        let index = $(this).attr("index");
        let qOfProduct = +$(`input[name='quantity${index}'`).val();
        let brutePrice = +$(this).val();
        totalPrice +=  (qOfProduct*brutePrice);
    });
    $(".price").text(totalPrice);
}

/* Función que va detectando el completado del SKU y así autocompletar la descripción
    En caso de que no se encuentre, salta un alerta con un botón para poder agregarlo
*/
function SKUFunc(thisObj){
    let index = thisObj.attr("index");
    let descriptionObj = $(`input[name='description${index}']`);
    let priceObj = $(`input[name='price${index}']`);
    let skuAddObj = $(`div[name='skuAdd${index}']`);
    let inputVal = thisObj.val();
    if (inputVal == ""){
        descriptionObj.val("");
        priceObj.val("");
        skuAddObj.hide();
        return;
    }
    
    let data = SKU_list[inputVal]; // Obtengo lo que esté almacenado en la key como SKU
    // En caso de que exista esta key dentro de la base de datos
    if (data != undefined){
        descriptionObj.val(data["Descripcion"]); 
        priceObj.val(data["Precio"]);
        skuAddObj.hide();
        return; 
    } 
    // En caso de que no, muestro el objeto para agregarlo dinámicamente
    skuAddObj.show();
    descriptionObj.val("");
    priceObj.val("");
    updatePrice();
}

// Función que va detectando la completación de la descripción y así autocompletar el SKU
function descriptionFunc(thisObj){
    let index = thisObj.attr("index");
    let SKUObj = $(`input[name='SKU${index}']`);
    let priceObj = $(`input[name='price${index}']`);
    let descriptionAddObj = $(`div[name='descriptionAdd${index}']`);

    let inputVal = thisObj.val();
    /*
        Forma neandertal de autocompletar recorriendo toda el diccionario
        de SKU buscando que la descripción escrita concuerde con la descripción
        de algún SKU almacenado en la base de datos
    */
    if (inputVal == "") {
        SKUObj.val("");
        priceObj.val("");
        descriptionAddObj.hide();
        return;

    }

    for (let SKU in SKU_list) {
        // En caso de que el SKU tenga la misma descripción que la escrita
        if (inputVal == SKU_list[SKU]["Descripcion"]) {
            // Autocomplteo todos los datos
            SKUObj.val(SKU);
            priceObj.val(SKU_list[SKU]["Precio"]);
            descriptionAddObj.hide();
            return;
        }
        // si está seteado para modo automático
        
    }
    
    descriptionAddObj.show();
    SKUObj.val("");
    priceObj.val("");
    updatePrice();

}


/*
Función que va a actualizar en caso de agregar o eliminar cualquier widget
con los eventos dinámicos
*/
function reloadFunctions() {

    // Funciones de bootstrap para actualizar todos los objetos que sean del tipo tooltip
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Cuando se escriba en la cantidad...
    $("input[name*='quantity'").change(function(){
        
        updatePrice();
    });

    // Cuando se escriba en el precio...
    $("input[name*='price'").change(function(){
        updatePrice();
    });

    // Cuando se presione una tecla en el input de CANTIDAD....
    $("input[name='price0'").keydown(function (e) {
        test_append(e, $(this), "primary");
    });

    // Cuando se presione una tecla en el input de CANTIDAD que no sea el primero...
    $("input[name!='price0'][name*='price']").keydown(function (e) {
        test_append(e, $(this), "secondary");
    });
    // Por cada botón que tenga delete y se presione una tecla...
    $("button[id*='delete']").keydown(function (e) {
        test_append(e, $(this), "button");
    })
    // En caso de que se clickee...
    .click(function () {
        let index = $(this).attr("index");
        deleteRow(index);
        updatePrice();

    });

    $("button[name='addSKU']").click(function(){
        $("#description").val("");
        $("#price").val("");
        $("#SKUID").val("").prop("disabled", true);
        $("#auto").prop("checked", true);
    });


    // Cada vez que se cambie el estado de auto a no auto en el botón...
    
    $("input[name*='description']").keyup(function () {
        descriptionFunc($(this));
    }).change(function(){
        descriptionFunc($(this));
    });

    $("input[name*='SKU'").keyup(function(){
        SKUFunc($(this));
    }).change(function(){
        SKUFunc($(this));
    });
}


$(function () {
    const socketio = io();
    socketio.on("updateListSKU", function(data){
        SKU_list = data;
        let datalistSKUObj = $("#SKUs");
        let datalistDescriptionObj = $("#Descriptions");
        datalistDescriptionObj.empty();
        datalistSKUObj.empty();
        for (let IDSKU in SKU_list){
            datalistSKUObj.append(`<option value='${IDSKU}'>`);
            datalistDescriptionObj.append(`<option value='${SKU_list[IDSKU]["Descripcion"]}'>`);
        }

    });
    // Click en el botón de agregar fila
    $("#newRow").click(function () {
        let length = $("input[name*='quantity']").length;
        let newIndex = length;
        addRow(newIndex);
    });

    // Click en el botón de generar automáticamente SKU
    $("#auto").change(function(){
        var status = $(this).is(":checked"); // Booleano
        $("#SKUID").prop("disabled", status);
    });
    
    // Click en el botón de guardar SKU
    $("#saveNewSKU").click(function(){
        let descripcion = $("#description").val();
        let price = +$("#price").val();
        socketio.emit("flash_newSKU", descripcion, price, userID);
        $("#newSKUModal").modal('toggle');
    });
    reloadFunctions(); // Cargar todas las funciones básicas de los elementos
    
});