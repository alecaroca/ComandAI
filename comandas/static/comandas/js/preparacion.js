// Función para calcular el tiempo transcurrido desde un inicio dado
function calcularTiempoDesdeInicio(horaInicio) {
    if (!horaInicio) return "00:00";
    const inicio = new Date(horaInicio);
    if (isNaN(inicio)) return "00:00";

    const ahora = new Date();
    const diferencia = Math.floor((ahora - inicio) / 1000);

    const minutos = Math.floor(diferencia / 60);
    const segundos = diferencia % 60;

    return `${String(minutos).padStart(2, '0')}:${String(segundos).padStart(2, '0')}`;
}

// Función para actualizar el tiempo transcurrido de las comandas y pedidos
function iniciarActualizacionTiempos() {
    setInterval(() => {
        document.querySelectorAll(".tiempo-transcurrido").forEach(element => {
            const horaInicio = element.getAttribute("data-inicio");
            if (horaInicio) {
                const tiempoFormateado = calcularTiempoDesdeInicio(horaInicio);
                element.querySelector(".tiempo-global-text").textContent = `${tiempoFormateado} min/seg.`;
            }
        });

        document.querySelectorAll(".tiempo-restante").forEach(element => {
            const horaInicio = element.getAttribute("data-inicio");
            if (horaInicio) {
                const tiempoFormateado = calcularTiempoDesdeInicio(horaInicio);
                element.querySelector(".tiempo-pedido-text").textContent = `${tiempoFormateado} min/seg.`;
            }
        });
    }, 1000);
}

// Función para actualizar las comandas y su estado actual
function actualizarComandas() {
    fetch('/preparacion/actualizar/', { method: "GET" })
        .then(response => response.json())
        .then(data => {
            const filaComandas = document.querySelector(".fila-comandas");
            filaComandas.innerHTML = "";

            data.comandas.forEach(comanda => {
                if (comanda.pedidos.length === 0) return;

                const pedidosSeleccionados = comanda.pedidos.filter(p => p.estado === 3).length;
                const totalPedidos = comanda.pedidos.length;

                const card = `
                <div class="col-12 col-md-4 col-lg-3">
                    <div class="tarjeta-comanda card shadow-sm h-100" data-id="${comanda.id}">
                        <div class="encabezado-comanda card-header">
                            <h5 class="titulo-comanda mb-0 d-flex justify-content-between align-items-center">
                                Comanda #${comanda.id}
                                <span class="tiempo-transcurrido" data-inicio="${comanda.tiempo_inicio}">
                                    <i class="bi bi-stopwatch"></i> 
                                    <span class="tiempo-global-text">${calcularTiempoDesdeInicio(comanda.tiempo_inicio)} min/seg.</span>
                                </span>
                            </h5>
                        </div>
                        <div class="cuerpo-comanda card-body">
                            <div class="row mb-2">
                                <div class="col-4">
                                    <p class="mesa-detalle">
                                        <strong>Mesa:</strong> ${comanda.mesa}
                                    </p>
                                </div>
                                <div class="col-8 text-end">
                                    <p class="progreso-pedidos">
                                        ${pedidosSeleccionados} de ${totalPedidos} seleccionados
                                    </p>
                                </div>
                            </div>
                            <ul class="lista-pedidos">
                                ${comanda.pedidos.map(pedido => `
                                <li class="item-pedido p-3 ${pedido.estado === 3 ? 'seleccionado' : 'border-start border-success'}" data-id="${pedido.id}">
                                    <div class="d-flex align-items-center mb-2">
                                        <div class="cantidad-producto-circle">${pedido.cantidad}</div>
                                        <div class="texto-producto">
                                            <h6 class="nombre-producto ${pedido.estado === 3 ? "text-decoration-line-through" : ""}">${pedido.producto}</h6>
                                        </div>
                                        <div class="ms-auto columna-checkbox">
                                            <input type="checkbox" class="checkbox-pedido form-check-input" 
                                                ${pedido.estado === 3 ? "checked" : ""} data-id="${pedido.id}">
                                        </div>
                                    </div>
                                    <div class="d-flex justify-content-start tiempos-pedido">
                                        <p class="tiempo-estimado mb-0 me-3">
                                            <strong>Tiempo estimado:</strong> ${pedido.tiempo_estimado || "-"} min
                                        </p>
                                        <p class="tiempo-restante mb-0 ${pedido.tiempo_excedido ? "tiempo-excedido" : ""}" data-inicio="${pedido.hora_ini}">
                                            <strong>Tiempo transcurrido:</strong> <span class="tiempo-pedido-text">${calcularTiempoDesdeInicio(pedido.hora_ini)} min/seg.</span>
                                        </p>
                                    </div>
                                    <p class="notas-pedido mt-2">
                                        <strong>Nota:</strong> ${pedido.notas || "Sin notas"}
                                    </p>
                                </li>`).join("")}
                            </ul>
                            <button class="btn-comanda-lista btn w-100" data-id="${comanda.id}" ${pedidosSeleccionados === 0 ? "disabled" : ""}>
                                Marcar como preparados
                            </button>
                        </div>
                    </div>
                </div>`;
                filaComandas.insertAdjacentHTML("beforeend", card);
            });

            agregarEventosCheckboxes();
            agregarEventosBotones();
        })
        .catch(error => console.error("Error al actualizar comandas:", error));
}

// Función para cambiar el estilo de un pedido según su estado
function actualizarEstiloPedido(itemPedido, estado) {
    if (estado === 3) {
        itemPedido.classList.add("seleccionado");
        itemPedido.classList.remove("border-start");
    } else {
        itemPedido.classList.remove("seleccionado");
        itemPedido.classList.add("border-start");
    }
}

// Función para mantener el estado del botón al actualizar comandas
function actualizarBotones() {
    document.querySelectorAll(".tarjeta-comanda").forEach(comanda => {
        const boton = comanda.querySelector(".btn-comanda-lista");
        const seleccionados = Array.from(comanda.querySelectorAll(".checkbox-pedido")).filter(cb => cb.checked).length;
        boton.disabled = seleccionados === 0;
    });
}

// Función para manejar eventos en cuadros y checkboxes
function agregarEventosCheckboxes() {
    document.querySelectorAll(".item-pedido").forEach(item => {
        item.addEventListener("click", function (e) {
            if (!e.target.classList.contains("checkbox-pedido")) {
                const checkbox = this.querySelector(".checkbox-pedido");
                checkbox.checked = !checkbox.checked;
                checkbox.dispatchEvent(new Event("change"));
            }
        });
    });

    document.querySelectorAll(".checkbox-pedido").forEach(checkbox => {
        checkbox.addEventListener("change", function () {
            const pedidoId = this.dataset.id;
            const nuevoEstado = this.checked ? 3 : 0;

            actualizarEstiloPedido(this.closest(".item-pedido"), nuevoEstado);

            fetch(`/preparacion/actualizar-estado-pedido/${pedidoId}/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ estado: nuevoEstado }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const comandaId = this.closest(".tarjeta-comanda").dataset.id;
                        actualizarConteoSeleccionados(comandaId);
                        actualizarBotones();
                    }
                });
        });
    });
}

// Función para los botones de marcar como preparados
function agregarEventosBotones() {
    document.querySelectorAll(".btn-comanda-lista").forEach(boton => {
        boton.addEventListener("click", function () {
            const comandaId = this.dataset.id;
            Swal.fire({
                title: "¿Estás seguro?",
                text: "Esto marcará como preparados los pedidos seleccionados.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#00bf63",
                cancelButtonColor: "#d33",
                confirmButtonText: "Sí, marcar",
                cancelButtonText: "Cancelar",
            }).then(result => {
                if (result.isConfirmed) {
                    fetch(`/preparacion/marcar-comanda-preparada/${comandaId}/`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                actualizarComandas();
                            }
                        });
                }
            });
        });
    });
}

// Inicialización al cargar la página
document.addEventListener("DOMContentLoaded", () => {
    actualizarComandas();
    iniciarActualizacionTiempos();
    setInterval(actualizarComandas, 1000); // Actualización periódica
});
