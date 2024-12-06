document.addEventListener("DOMContentLoaded", () => {
    const categoryElements = document.querySelectorAll(".category-item");
    const productsContainer = document.querySelector(".products-list");

    // Inicializar lógica para productos ya cargados desde el template
    addQuantityLogic();
    addAddToCartLogic();

    // Inicializar el badge
    updateBadge();

    // Marcar la primera categoría como seleccionada
    categoryElements[0]?.classList.add("selected");

    categoryElements.forEach((category) => {
        category.addEventListener("click", () => {
            const categoryId = category.dataset.id;

            // Marcar categoría seleccionada
            categoryElements.forEach((item) => item.classList.remove("selected"));
            category.classList.add("selected");

            // Fetch productos desde la API
            fetch(`/api/productos/?categoria=${categoryId}`, {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${comensalToken}` // Usamos la variable comensalToken
                }
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error(`Error en la API: ${response.status}`);
                    }
                    return response.json();
                })
                .then((productos) => {
                    if (!Array.isArray(productos)) {
                        throw new Error("La respuesta no es una lista de productos válida.");
                    }
                    renderProducts(productos);
                })
                .catch((error) => console.error("Error al cargar productos:", error));
        });
    });

    function renderProducts(products) {
        productsContainer.innerHTML = "";
        products.forEach((product) => {
            const productCard = `
                <div class="product-card">
                    <img src="${product.imagen}" alt="${product.nombre}" class="product-image">
                    <div class="product-details">
                        <h5>${product.nombre}</h5>
                        <p>${product.descripcion}</p>
                        <p class="product-price" data-precio="${product.precio}"><strong>${product.precio_format}</strong></p> <!-- Aquí usamos precio_format -->
                        <div class="quantity-selector">
                            <button class="btn-quantity" data-action="decrease">-</button>
                            <span class="quantity">1</span>
                            <button class="btn-quantity" data-action="increase">+</button>
                        </div>
                        <button class="add-to-cart-btn" data-id="${product.id}">Agregar a Pedido</button>
                    </div>
                </div>`;
            productsContainer.innerHTML += productCard;
        });

        // Reaplicar lógica a los nuevos productos renderizados
        addQuantityLogic();
        addAddToCartLogic();
    }

    function addQuantityLogic() {
        const quantityButtons = document.querySelectorAll(".btn-quantity");

        quantityButtons.forEach((button) => {
            button.addEventListener("click", () => {
                const action = button.dataset.action;
                const quantityElement = button.parentNode.querySelector(".quantity");
                let quantity = parseInt(quantityElement.textContent);

                if (action === "increase") {
                    quantity++;
                } else if (action === "decrease" && quantity > 1) {
                    quantity--;
                }

                quantityElement.textContent = quantity;
            });
        });
    }

    function addAddToCartLogic() {
        const addToCartButtons = document.querySelectorAll(".add-to-cart-btn");

        addToCartButtons.forEach((button) => {
            button.addEventListener("click", () => {
                const productId = button.dataset.id;
                const quantity = parseInt(button.parentNode.querySelector(".quantity").textContent);
                const price = parseFloat(button.parentNode.querySelector(".product-price").dataset.precio);
                const total = quantity * price;

                fetch("/api/pedidos/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${comensalToken}` // Usamos la variable comensalToken
                    },
                    body: JSON.stringify({
                        producto: productId,
                        cantidad: quantity,
                        estado: 4,
                        comanda: COMANDA_ID,
                        total_pedido: total,
                        comensal: COMENSAL_ID // Agregar comensal desde el servidor
                    })
                })
                    .then((response) => {
                        if (!response.ok) throw new Error("Error al agregar pedido");
                        return response.json();
                    })
                    .then(() => updateBadge()) // Actualiza el badge desde la API después de agregar un pedido
                    .catch((error) => console.error("Error al registrar pedido:", error));
            });
        });
    }

    function updateBadge() {
        fetch(`/api/pedidos/?estado=4&comanda=${COMANDA_ID}`, {
            method: "GET",
            headers: {
                Authorization: `Bearer ${comensalToken}`
            }
        })
            .then((response) => {
                if (!response.ok) throw new Error("Error al consultar pedidos confirmados");
                return response.json();
            })
            .then((pedidos) => {
                const badge = document.getElementById("badge-confirmar");
                badge.textContent = pedidos.length;
                badge.style.display = pedidos.length > 0 ? "inline-block" : "none";
            })
            .catch((error) => console.error("Error al actualizar el badge:", error));
    }
});
