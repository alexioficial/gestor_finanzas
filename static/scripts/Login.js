$('#btnLogin').click(async () => {
    const data = await tools.PostBack('/Login', {'hola': 'mundo'});
    if (data.status == 1) {
        alert(data.msj);
        return;
    }
    console.log(data);
});