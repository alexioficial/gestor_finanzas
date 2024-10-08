async function BuscarCategorias() {
    datos = {}
    const data = tools.PostBack('/BuscarCategorias', datos);
    if (data.status == 1) {
        alert(data.msj);
        return;
    }
    $('#categorias').html(data.html);
}

async function RegCategoria() {
    datos = {}
    const data = tools.PostBack('/RegCategoria', datos);
    if (data.status == 1) {
        alert(data.msj);
        return;
    }
    BuscarCategorias();
}

$(() => {
    BuscarCategorias();
})