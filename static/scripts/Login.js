async function Login() {
    const username = $('#txt_username').val();
    const password = $('#txt_password').val();
    const datos = {
        username: username,
        password: password
    }
    const data = await tools.PostBack('/Login', datos);
    if (data.status == 1) {
        alert(data.msj);
        return;
    }
    location.href = data.redireccion;
}

$('#btnLogin').click(() => {
    Login();
});

$('#txt_username, #txt_password').keyup(e => {
    if (e.key === "Enter" || e.keyCode === 13) {
        Login();
    }
});