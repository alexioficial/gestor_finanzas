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
        idcategoria: $('#idcategoria').val(),
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

async function EliminarCategoria() {
    const datos = {
        idcategoria: $('#idcategoria').val()
    }
    const data = await tools.PostBack('/EliminarCategoria', datos);
    if (data.status == 1) {
        alert(data.msj);
        return;
    }
    BuscarCategorias();
    LimpiarCampos();
}

async function LimpiarCampos() {
    $('#txt_nombre').val('');
    $('#idcategoria').val('');
}

function CamposRequeridos() {
    var valor = $('#txt_nombre').val();
    return !(valor.trim() === '');
}

function LlenarCampos(categoria) {
    $('#idcategoria').val(categoria.idcategoria);
    $('#txt_nombre').val(categoria.nombre);
    $('#chk_status').prop('checked', categoria.status);
}

$(() => {
    BuscarCategorias();
    $('#btn_guardar').click(() => {
        CamposRequeridos() ? RegCategoria() : null;
    });
    $('#btn_limpiar_categoria').click(() => {
        LimpiarCampos();
    });
    $('#btn_eliminar').click(() => {
        EliminarCategoria();
    });
});