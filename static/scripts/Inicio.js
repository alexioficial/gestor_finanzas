async function LlenarDdlCategorias() {
    // Para ingresos
    const dataIngresos = await tools.PostBack('/LlenarDdlCategorias', {tipo: 'I'});
    if (dataIngresos.status == 1) {
        alert(dataIngresos.msj);
        return;
    }
    $('#categoria_ingreso').html(dataIngresos.html);

    // Para gastos
    const dataGastos = await tools.PostBack('/LlenarDdlCategorias', {tipo: 'G'});
    if (dataGastos.status == 1) {
        alert(dataGastos.msj);
        return;
    }
    $('#categoria_gasto').html(dataGastos.html);
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
    await CargarDatos();
    $('#monto_ingreso').val('');
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
    await CargarDatos();
    $('#monto_gasto').val('');
}

async function CargarDatos() {
    const resp = await tools.PostBack('/ObtenerDatosInicio', {});
    if (resp.status == 1) {
        alert(resp.msj);
        return;
    }
    $('#balance_total').html(resp.dtusuario.balance);
    $('#lista_de_transacciones').empty();
    resp.transacciones.forEach(transaccion => {
        $('#lista_de_transacciones').append(`
            <li class="list-group-item">
                ${transaccion.categoria.nombre}
                <span>
                    <i class="fas fa-${transaccion.tipo == 'I' ? 'plus' : 'minus'} text-${transaccion.tipo == 'I' ? 'success' : 'danger'} me-2"></i>
                    <span class="badge bg-${transaccion.tipo == 'I' ? 'success' : 'danger'}">${transaccion.monto}</span>
                </span>
            </li>
        `);
    });
}

$(() => {
    $('.9N_2D').mask('000,000,000.00', {reverse: true});
    LlenarDdlCategorias();
    CargarDatos();
    tools.Enter('#monto_ingreso', () => RegIngreso());
    tools.Enter('#monto_gasto', () => RegGasto());
    $('#btn_reg_ingreso').click(() => RegIngreso());
    $('#btn_reg_gasto').click(() => RegGasto());
});