document.addEventListener("DOMContentLoaded", () => {
    const pedidoList = document.getElementById("pedido-list");
    const confirmarBtn = document.getElementById("confirmar-pedido-btn");

    function loadPedidos() {
        fetch(`/api/pedidos/?estado=4&comanda_id=${COMANDA_ID}`, {
            method: "GET",
            headers: {
                Authorization: `Bearer ${comensalToken}`,
            },
        })
            .then((response) => {
                if (!response.ok) throw new Error("Error al cargar pedidos");
                return response.json();
            })
            .then((pedidos) => {
                renderPedidos(pedidos);
                updateBadge(COMANDA_ID, comensalToken);
            })
            .catch((error) => console.error("Error al cargar pedidos:", error));
    }

    function renderPedidos(pedidos) {
        pedidoList.innerHTML = "";
        pedidos.forEach((pedido) => {
            const card = document.createElement("div");
            card.className = "card mb-3";
            card.dataset.id = pedido.id;

            card.innerHTML = `
                <div class="card-header d-flex justify-content-between align-items-center bg-light">
                    <span>${pedido.producto_nombre}</span>
                    <span class="badge bg-warning text-dark">Por Confirmar</span>
                </div>
                <div class="card-body d-flex">
                    <div class="flex-column-left">
                        <div><strong>Cantidad:</strong> ${pedido.cantidad}</div>
                        <div><strong>Total:</strong> ${pedido.total_pedido_format}</div>
                    </div>
                    <div class="flex-column-right">
                        <button class="btn-remove btn  " title="Eliminar">
                            <i class="fa fa-trash"></i> Eliminar
                        </button>
                    </div>
                </div>
            `;
            pedidoList.appendChild(card);
        });

        // Agregar eventos para los botones de eliminar
        document.querySelectorAll(".btn-remove").forEach((btn) =>
            btn.addEventListener("click", removePedido)
        );
    }

    function removePedido(event) {
        const id = event.target.closest(".card").dataset.id;
        fetch(`/api/pedidos/${id}/`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${comensalToken}`,
            },
        })
            .then((response) => {
                if (!response.ok) throw new Error("Error al eliminar pedido");
                loadPedidos();
            })
            .catch((error) => console.error("Error al eliminar pedido:", error));
    }

    confirmarBtn.addEventListener("click", () => {
        Swal.fire({
            title: "Confirmar Pedido",
            text: "¿Estás seguro de enviar el pedido a preparación?",
            icon: "question",
            showCancelButton: true,
            confirmButtonText: "Sí, confirmar",
            cancelButtonText: "Cancelar",
        }).then((result) => {
            if (result.isConfirmed) {
                fetch(`/api/pedidos/confirmar/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${comensalToken}`,
                    },
                    body: JSON.stringify({
                        comanda: COMANDA_ID,
                        estado_nuevo: 0, // Estado preparación
                    }),
                })
                    .then((response) => {
                        if (!response.ok) throw new Error("Error al confirmar pedidos");
                        return response.json();
                    })
                    .then(() => {
                        Swal.fire(
                            "¡Pedido Confirmado!",
                            "Tu pedido fue enviado a preparación.",
                            "success"
                        );
                        loadPedidos();
                    })
                    .catch((error) => console.error("Error al confirmar pedidos:", error));
            }
        });
    });

    loadPedidos();
});
