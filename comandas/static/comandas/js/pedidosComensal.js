document.addEventListener("DOMContentLoaded", () => {
    
    const pedidoList = document.getElementById("pedido-list");
    const navLinks = document.querySelectorAll("#pedidos-tabs .nav-link");

    
    function loadPedidos(status) {
        fetch(`/api/pedidos/?estado=${status}&comanda_id=${COMANDA_ID}`, {
            method: "GET",
            headers: {
                Authorization: `Bearer ${comensalToken}`,
            },
        })
            .then((response) => {
                if (!response.ok) throw new Error("Error al cargar pedidos");
                return response.json();
            })
            .then((pedidos) => renderPedidos(pedidos))
            .catch((error) => console.error("Error al cargar pedidos:", error));
    }

    function renderPedidos(pedidos) {
        pedidoList.innerHTML = "";
    
        pedidos.forEach((pedido) => {
            // Consultar los detalles del producto
            fetch(`/api/productos/${pedido.producto}/`, {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${comensalToken}`,
                },
            })
                .then((response) => {
                    if (!response.ok) throw new Error("Error al cargar detalles del producto");
                    return response.json();
                })
                .then((producto) => {
                    // Crear la card del pedido
                    const card = document.createElement("div");
                    card.className = "card";
                    card.style.borderColor = getStatusColor(pedido.estado);
    
                    card.innerHTML = `
                        <div class="card-header">
                            ${producto.nombre}
                            <i class="${getStatusIcon(pedido.estado)}"></i>
                        </div>
                        <div class="card-body">
                            <img src="${producto.imagen}" alt="Imagen del Producto" class="product-image">
                            <div class="product-quantity">Cantidad: ${pedido.cantidad}</div>
                        </div>
                    `;
                    pedidoList.appendChild(card);
                })
                .catch((error) => console.error("Error al cargar detalles del producto:", error));
        });
    }
    
    function getStatusColor(status) {
        return status === 0
            ? "#ebc244" // En preparación (info)
            : status === 2
            ? "#6c757d" // Preparado (primary)
            : "#00bf63"; // Entregado (success)
    }

    function getStatusIcon(status) {
        return status === 0
            ? "fa fa-clock"
            : status === 2
            ? "fa fa-check-circle"
            : "fa fa-hand-holding-heart";
    }

    navLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            event.preventDefault();
            navLinks.forEach((link) => link.classList.remove("active"));
            link.classList.add("active");
            loadPedidos(link.dataset.status);
        });
    });

    loadPedidos(0); // Cargar el primer estado por defecto
});
