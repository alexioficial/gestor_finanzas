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

function VerificarCampos() {
    var valor = $('#txt_nombre').val();
    if (valor.trim() === '') { // Verifica si está vacío o solo tiene espacios
        alert('Por favor, ingrese un nombre.');
        return false;
    }
    return true;
}

$('#addcategory').click(() => {
    VerificarCampos() ? RegCategoria() : null;
});

$(() => {
    BuscarCategorias();
})

$('#cleanButton').click(() => {
    LimpiarCampos();
});

$('#categorias').click((event) => {
    // Verifica que el elemento clicado sea un li
    if (event.target.tagName === 'LI') {
        alert('has seleccionado una li')
    }
});

// Categorias: funciona el check status, agregue: btn limpiar, verificacion de vacio, evento de seleccion a la lista