async function BuscarCategorias() {
    const data = await tools.PostBack('/BuscarCategorias', {});
    if (data.status == 1) {
        alert(data.msj);
        return;
    }
    $('#categorias').html(data.html);
}

async function RegCategoria() {
    const datos = {
        txt_nombre: $('#txt_nombre').val(),
        chk_status: $('#chk_status').prop('checked')
    }
    const data = await tools.PostBack('/RegCategoria', datos);
    if (data.status == 1) {
        alert(data.msj);
        return;
    }
    BuscarCategorias();
    LimpiarCampos();
}

async function LimpiarCampos() {
    $('#txt_nombre').val('');
}

async function LlenarCampos(nombre) {
    const datos = {nombre : nombre}
    const data = await tools.PostBack('/BuscarCategoriaPorNombre', datos);
    if (data.status == 1) {
        alert(data.msj);
        return;
    }
    $('#txt_nombre').val(data.nombre);
    $('#chk_status').prop('checked', data.status);
    ModifyButton();
}



function VerificarCampos() {
    var valor = $('#txt_nombre').val();
    if (valor.trim() === '') { // Verifica si está vacío o solo tiene espacios
        alert('Por favor, ingrese un nombre.');
        return false;
    }
    return true;
}

function ModifyButton() {
    $("#addcategory").addClass("d-none");
    $('#editcategory').removeClass("d-none");
}

function AddButton() {
    $("#addcategory").removeClass("d-none");
    $('#editcategory').addClass("d-none");
}


$('#addcategory').click(() => {
    VerificarCampos() ? RegCategoria() : null;
});

$(() => {
    BuscarCategorias();
})

$('#cleanButton').click(() => {
    LimpiarCampos();
    AddButton();
});


$('#categorias').on('click', 'li', async function () {
    const nombreCategoria = $(this).clone().children().remove().end().text().trim();
    LlenarCampos(nombreCategoria);
});

