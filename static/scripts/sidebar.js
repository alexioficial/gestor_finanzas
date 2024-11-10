async function Logout() {
    const data = await tools.PostBack('/Logout', {});
    if (data.status == 1) {
        alert(data.msj);
        return;
    }
    location.href = data.redireccion;
}

document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const menuClose = document.getElementById('menuClose');
    const sideMenu = document.getElementById('sideMenu');
    const themeSwitch = document.getElementById('themeSwitch');

    menuToggle.addEventListener('click', function() {
        sideMenu.classList.add('active');
    });

    menuClose.addEventListener('click', function() {
        sideMenu.classList.remove('active');
    });

    themeSwitch.addEventListener('change', function() {
        document.body.classList.toggle('dark-theme');
        localStorage.setItem('darkMode', this.checked);
    });

    // Set dark mode as default
    if (localStorage.getItem('darkMode') === null) {
        localStorage.setItem('darkMode', 'true');
    }

    // Check for saved theme preference or use default (dark mode)
    const savedDarkMode = localStorage.getItem('darkMode');
    if (savedDarkMode === 'true' || savedDarkMode === null) {
        document.body.classList.add('dark-theme');
        themeSwitch.checked = true;
    } else {
        document.body.classList.remove('dark-theme');
        themeSwitch.checked = false;
    }
});