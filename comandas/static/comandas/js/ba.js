const nav = document.querySelector("#nav");
const abrir = document.querySelector("#abrir");
const cerrar = document.querySelector("#cerrar");

abrir.addEventListener("click", () => {
    nav.classList.add("visible");
})

cerrar.addEventListener("click", () => {
    nav.classList.remove("visible");
})

function adjustQuantity(button, change) {
    const input = button.parentElement.querySelector('input[type="text"]');
    const currentValue = parseInt(input.value) || 1;
    const newValue = Math.max(1, currentValue + change); // Evita valores menores a 1
    input.value = newValue;
}

function leerSolicitudes(){

    fetch(`/api/solicitudes/`, {
        method: "GET",
        
    })
        .then((response) => {
            if (!response.ok) throw new Error("Error al cargar pedidos");
            return response.json();
        })
        .then((response) => {
            // Actualiza solicitudes
            const nSolicitudes2 = document.querySelectorAll("#nSolicitudes")[0];
            console.log(nSolicitudes2);
            console.log(response.length);
            nSolicitudes2.textContent =response.length;
            
        })
        .catch((error) => console.error("Error al cargar pedidos:", error));

       

}

setInterval(leerSolicitudes, 3000);

document.addEventListener("DOMContentLoaded", () => {
leerSolicitudes();

});

