const tools = {
    PostBack: async (ruta, datos) => {
        return new Promise((resolve, reject) => {
            $.ajax({
                type: "POST",
                url: ruta,
                data: JSON.stringify(datos),
                contentType: "application/json",
                dataType: "json",
                success: resp => {
                    resolve(resp);
                },
                error: (xhr, status, error) => {
                    reject(error);
                }
            });
        });
    },
    Enter: (selector, callback) => {
        $(selector).on('keypress', (e) => {
            if (e.which == 13) callback();
        });
    }
};