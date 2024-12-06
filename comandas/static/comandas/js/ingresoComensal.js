// Archivo: ingresoComensal.js

document.addEventListener("DOMContentLoaded", () => {
    // Obtener elementos del DOM
    const form = document.getElementById("form-ingreso");
    const checkbox = document.getElementById("terminos");
    const btnVerMenu = document.getElementById("btn-ver-menu");

    // Verificar que el modal exista antes de inicializarlo
    const modalElement = document.getElementById("loadingModal");
    if (!modalElement) {
        console.error("[DEBUG] No se encontró el modal con ID #loadingModal");
        return;
    }
    const modalSpinner = new bootstrap.Modal(modalElement);

    // Habilitar o deshabilitar el botón según el estado del checkbox
    checkbox.addEventListener("change", () => {
        btnVerMenu.disabled = !checkbox.checked; // Habilitar si el checkbox está marcado
    });

    // Manejo del envío del formulario
    form.addEventListener("submit", (event) => {
        event.preventDefault(); // Prevenir el comportamiento predeterminado del formulario

        // Mostrar el modal de carga
        modalSpinner.show();

        // Deshabilitar el botón para evitar múltiples envíos
        btnVerMenu.disabled = true;

        // Construir los datos del formulario
        const formData = new FormData(form);

        // Enviar los datos al servidor
        fetch(form.action, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": formData.get("csrfmiddlewaretoken"), // CSRF para Django
            },
        })
            .then((response) => {
                if (!response.ok) {
                    console.error("[DEBUG] Error en respuesta del servidor:", response.status);
                    throw response.json();
                }
                return response.json();
            })
            .then((data) => {
                console.log("[DEBUG] Respuesta del servidor:", data);
                if (data.success) {
                    if (data.solicitud_id) {
                        // Iniciar polling para verificar el estado de la solicitud
                        verificarEstadoSolicitud(data.solicitud_id, formData);
                    } else {
                        modalSpinner.hide();
                        Swal.fire(
                            "Info",
                            "Otra solicitud está en proceso. Esperando aprobación.",
                            "info"
                        );
                    }
                } else {
                    modalSpinner.hide();
                    Swal.fire("Error", data.message, "error");
                    btnVerMenu.disabled = false; // Rehabilitar el botón
                }
            })
            .catch((error) => {
                console.error("[DEBUG] Error en la solicitud:", error);
                modalSpinner.hide();
                Swal.fire("Error", "Error inesperado. Intenta nuevamente.", "error");
                btnVerMenu.disabled = false; // Rehabilitar el botón
            });
    });

    // Función para verificar el estado de la solicitud periódicamente
    function verificarEstadoSolicitud(solicitudId, formData) {
        console.log(`[DEBUG] Iniciando verificación de estado para la solicitud ID: ${solicitudId}`);
        const url = `/consultar_estado_solicitud/${solicitudId}/`;

        const interval = setInterval(() => {
            fetch(url)
                .then((response) => response.json())
                .then((data) => {
                    console.log("[DEBUG] Estado de la solicitud:", data);
                    if (data.success) {
                        if (data.estado === 1) {
                            clearInterval(interval);
                            modalSpinner.hide();
                            Swal.fire("¡Éxito!", "Solicitud aprobada. Redirigiendo al menú...", "success").then(() => {
                                window.location.href = data.redirect_url || "/comensal/menu/";
                            });
                        } else if (data.estado === 2) {
                            clearInterval(interval);
                            modalSpinner.hide();
                            Swal.fire("Rechazado", "Tu solicitud fue rechazada. Intenta nuevamente.", "error");
                            btnVerMenu.disabled = false; // Rehabilitar el botón
                        }
                    } else {
                        console.error("[DEBUG] Error en respuesta del servidor durante el polling:", data);
                        clearInterval(interval);
                        Swal.fire("Error", data.message, "error");
                        btnVerMenu.disabled = false; // Rehabilitar el botón
                    }
                })
                .catch((error) => {
                    console.error("[DEBUG] Error al verificar estado:", error);
                    clearInterval(interval);
                    modalSpinner.hide();
                    Swal.fire("Error", "Error al consultar el estado de la solicitud.", "error");
                });
        }, 3000); // Consultar cada 3 segundos
    }
});
