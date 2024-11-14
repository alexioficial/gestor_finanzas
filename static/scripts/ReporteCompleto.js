async function LlenarDdlCategorias() {
    const data = await tools.PostBack('/LlenarDdlCategorias', {tipo: 'T'});
    if (data.status == 1) {
        alert(data.msj);
        return;
    }
    $('#ddl_categoria').html('<option value="0">Todas</option>' + data.html);
}

async function LlenarDdlBilleteras() {
    const resp = await tools.PostBack('/LlenarDdlBilleteras', {});
    if (resp.status == 1) {
        alert(resp.msj);
        return;
    }
    $('#ddl_billetera').html('<option value="0">Todas</option>' + resp.html);
}

async function ProcesarReporte() {
    const datos = {
        idcategoria: $('#ddl_categoria').val(),
        idbilletera: $('#ddl_billetera').val(),
        tipo: $('#ddl_tipo').val(),
        fecha_inicial: $('#txt_fechainicial').val(),
        fecha_final: $('#txt_fechafinal').val(),
        organizar: $('#ddl_organizar').val()
    }

    const resp = await tools.PostBack('/ProcesarReporteCompleto', datos);
    if (resp.status == 1) {
        alert(resp.msj);
        return;
    }

    // Mostrar resultados
    $('#resultados').show();

    console.log(JSON.stringify(resp.data));

    // Mostrar totales
    // let htmlTotales = '';
    // resp.data.totales.forEach(total => {
    //     const tipo = total._id === 'I' ? 'Ingresos' : 'Gastos';
    //     const clase = total._id === 'I' ? 'text-success' : 'text-danger';
    //     htmlTotales += `<p>${tipo}: <span class="${clase}">$${total.total.toFixed(2)}</span></p>`;
    // });
    // $('#totales_container').html(htmlTotales);

    // // Mostrar totales por categoría
    // let htmlTotalesCat = '';
    // resp.data.total_por_categoria.forEach(cat => {
    //     const tipo = cat._id.tipo === 'I' ? 'Ingreso' : 'Gasto';
    //     const clase = cat._id.tipo === 'I' ? 'text-success' : 'text-danger';
    //     htmlTotalesCat += `<p>${cat._id.categoria} (${tipo}): <span class="${clase}">$${cat.total.toFixed(2)}</span></p>`;
    // });
    // $('#totales_categoria_container').html(htmlTotalesCat);
}

$(() => {
    // Inicializar máscaras para fechas
    $('#txt_fechainicial, #txt_fechafinal').mask('00/00/0000');
    
    // Cargar datos iniciales
    LlenarDdlCategorias();
    LlenarDdlBilleteras();
    
    // Evento click del botón procesar
    $('#btn_procesar').click(() => ProcesarReporte());
});
