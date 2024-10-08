async function Logout() {
    const data = await tools.PostBack('/Logout', {});
    if (data.status == 1) {
        alert(data.msj);
        return;
    }
    location.href = data.redireccion;
}