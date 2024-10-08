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
        txt_nombre: $('#txt_nombre').val()
    }
    const data = await tools.PostBack('/RegCategoria', datos);
    if (data.status == 1) {
        alert(data.msj);
        return;
    }
    BuscarCategorias();
}

$('#addcategory').click(() => {
    RegCategoria();
});

$(() => {
    BuscarCategorias();
})