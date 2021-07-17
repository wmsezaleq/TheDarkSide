function addRow(newIndex) {
    $("tbody").append(`
        <tr index="${newIndex}">
            <td>
                <div class="form-check form-switch">
                    <input  type="checkbox" index="${newIndex}" name="auto${newIndex}" class="form-check-input" checked>
                    <label for="auto" class="form-check-label">Au   to</label>
                </div>
            </td>
            <td>
                <input type="text" list="SKUs" index="${newIndex}" name="SKU${newIndex}" class="form-control input-sm" disabled>
            </td>
            <td>
                <input class="form-control" list="Descriptions" input-sm" index="${newIndex}" name="description${newIndex}" type="text" required>
            </td>
            <td><input class="form-control input-sm" index="${newIndex}" name="quantity${newIndex}" type="number" required></td>
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

function test_append(e, thisObj, type) {
    var code = e.keyCode || e.which;
    if (code == 9 && !e.shiftKey) {  // Si se presionó la tecla tab
        e.preventDefault();
        let newIndex = $("input[name*='quantity']").length
        if (thisObj.attr('index') == newIndex - 1 && (type == "button" || type == "primary")) { // En caso de que sea el último input change 
            addRow(newIndex);        // Añado una nueva row
            $(`input[name='auto${newIndex}']`).focus();
        }
        else {
            let myIndex = +thisObj.attr("index");
            if (type == "primary" || type == "button") {
                $(`input[name='auto${myIndex + 1}']`).focus();
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

function reloadFunctions() {
    // Cuando se presione una tecla en el input de CANTIDAD....
    $("input[name='quantity0'").keydown(function (e) {
        test_append(e, $(this), "primary");
    });
    // Cuando se presione una tecla en el input de CANTIDAD que no sea el primero...
    $("input[name!='quantity0'][name*='quantity']").keydown(function (e) {
        test_append(e, $(this), "secondary");
    });
    // Por cada botón, 
    $("button[id*='delete']").keydown(function (e) {
        test_append(e, $(this), "button");
    }).click(function () {
        deleteRow($(this).attr("index"))
    });
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    $("input[name*='auto']").change(function () {
        var SKUInputObj = $(`input[name='SKU${$(this).attr('index')}']`);
        if ($(this).is(":checked")) {
            SKUInputObj.prop("disabled", true);
            SKUInputObj.prop("required", false);

        }
        else {
            SKUInputObj.prop("disabled", false);
            SKUInputObj.prop("required", true);
        }
    });

    function SKUFunc(thisObj){
        let index = thisObj.attr("index");
        let descriptionObj = $(`input[name='description${index}']`);
        let div_warning = $(`div[class*='warning-feedback'][index='${index}']`);
        div_warning.hide();
        
        for (let SKU in SKU_list){
            if (thisObj.val() == SKU){
                descriptionObj.val(SKU_list[SKU]);
                return;
            }
        }
        div_warning.show();
    }
    $("input[name*='SKU'").keyup(function(){
        SKUFunc($(this));
    }).change(function(){
        SKUFunc($(this));
    });

    // Función que va detectando la completación de la descripción y así autocompletar el SKU
    function descriptionFunc(thisObj){
        let index = thisObj.attr("index");
        let SKUObj = $(`input[name='SKU${index}']`);
        let autoObj = $(`input[name='auto${index}']`);
        // let div_warning = $(`div[class*='warning-feedback'][index='${index}']`);
        // div_warning.hide();

        for (let SKU in SKU_list) {
            if (thisObj.val() == SKU_list[SKU]) {
                SKUObj.val(SKU);
                return;
            }
            else if (autoObj.is(":checked")){
                SKUObj.val("");
            }
        }
    }

    $("input[name*='description']").keyup(function () {
        descriptionFunc($(this));
    }).change(function(){
        descriptionFunc($(this));
    });
}
$(function () {
    // Click en el botón de agregar fila
    $("#newRow").click(function () {
        let length = $("input[name*='quantity']").length;
        let newIndex = length;
        addRow(newIndex);
    });
    reloadFunctions(); // Cargar todas las funciones básicas de los elementos
    
});