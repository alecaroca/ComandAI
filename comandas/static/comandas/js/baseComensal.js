document.addEventListener("DOMContentLoaded", () => {
    const footerLinks = document.querySelectorAll(".footer-nav a");

    footerLinks.forEach((link) => {
        link.addEventListener("click", () => {
            footerLinks.forEach((el) => el.classList.remove("selected"));
            link.classList.add("selected");
        });
    });

    // Actualizar el badge al cargar la página
    if (typeof COMANDA_ID !== "undefined" && typeof comensalToken !== "undefined") {
        updateBadge(COMANDA_ID, comensalToken);
    }
});

function updateBadge(comandaId, comensalToken) {
    fetch(`/api/pedidos/?estado=4&comanda_id=${comandaId}`, {
        method: "GET",
        headers: {
            Authorization: `Bearer ${comensalToken}`,
        },
    })
        .then((response) => {
            if (!response.ok) throw new Error("Error al consultar pedidos confirmados");
            return response.json();
        })
        .then((pedidos) => {
            const badge = document.getElementById("badge-confirmar");
            if (badge) {
                badge.textContent = pedidos.length;
                badge.style.display = pedidos.length > 0 ? "inline-block" : "none";
            }
        })
        .catch((error) => console.error("Error al actualizar el badge:", error));
}
