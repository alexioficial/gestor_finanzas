async function LlenarDdlCategorias() {
    const data = await tools.PostBack('/LlenarDdlCategorias', {});
    if (data.status == 1) {
        alert(data.msj);
        return;
    }
    $('#categoria_ingreso').html(data.html);
    $('#categoria_gasto').html(data.html);
}

async function RegIngreso() {
    const datos = {
        idcategoria: $('#categoria_ingreso').val(),
        monto: $('#monto_ingreso').val()
    }
    const data = await tools.PostBack('/RegIngreso', datos);
    if (data.status == 1) {
        alert(data.msj);
        return;
    }
    // BuscarIngresos();
}

async function RegGasto() {
    const datos = {
        idcategoria: $('#categoria_gasto').val(),
        monto: $('#monto_gasto').val()
    }
    const data = await tools.PostBack('/RegGasto', datos);
    if (data.status == 1) {
        alert(data.msj);
        return;
    }
    // BuscarGastos();
}

$(() => {
    $('.9N_2D').mask('000,000,000.00', {reverse: true});
    LlenarDdlCategorias();
    tools.Enter('#monto_ingreso', () => RegIngreso());
    tools.Enter('#monto_gasto', () => RegGasto());
    $('#btn_reg_ingreso').click(() => RegIngreso());
    $('#btn_reg_gasto').click(() => RegGasto());
});