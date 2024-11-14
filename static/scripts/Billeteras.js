async function BuscarBilleteras() {
    const data = await tools.PostBack('/BuscarBilleteras', {});
    if (data.status == 1) {
        alert(data.msj);
        return;
    }
    $('#billeteras').html(data.html);
}

async function RegBilletera() {
    const datos = {
        idbilletera: $('#idbilletera').val(),
        txt_nombre: $('#txt_nombre').val(),
        chk_status: $('#chk_status').prop('checked')
    }
    const data = await tools.PostBack('/RegBilletera', datos);
    if (data.status == 1) {
        alert(data.msj);
        return;
    }
    BuscarBilleteras();
    LimpiarCampos();
}

async function EliminarBilletera() {
    const datos = {
        idbilletera: $('#idbilletera').val()
    }
    const data = await tools.PostBack('/EliminarBilletera', datos);
    if (data.status == 1) {
        alert(data.msj);
        return;
    }
    BuscarBilleteras();
    LimpiarCampos();
}

async function LimpiarCampos() {
    $('#txt_nombre').val('');
    $('#idbilletera').val('');
}

function CamposRequeridos() {
    var valor = $('#txt_nombre').val();
    return !(valor.trim() === '');
}

function LlenarCampos(billetera) {
    $('#idbilletera').val(billetera.idbilletera);
    $('#txt_nombre').val(billetera.nombre);
    $('#chk_status').prop('checked', billetera.status);
}

$(() => {
    BuscarBilleteras();
    $('#btn_guardar').click(() => {
        CamposRequeridos() ? RegBilletera() : null;
    });
    $('#btn_limpiar_billetera').click(() => {
        LimpiarCampos();
    });
    $('#btn_eliminar').click(() => {
        EliminarBilletera();
    });
});