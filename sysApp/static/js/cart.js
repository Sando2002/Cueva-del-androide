/* Funcionalidades del carrito */

// Función para actualizar el contador del carrito dinámicamente
function actualizarCarrito() {
    // Detectar dinámicamente la URL
    const urlPattern = '{% url "get_carrito_count" %}' || '/get_carrito_count/';
    
    fetch(urlPattern, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        const cartBadge = document.querySelector('.cart-badge');
        if (cartBadge) {
            cartBadge.textContent = data.total;
        }
    })
    .catch(error => console.error('Error al actualizar carrito:', error));
}

// Escuchar eventos personalizados cuando el carrito cambia
document.addEventListener('carritoActualizado', actualizarCarrito);

// Si hay cambios en el formulario de actualización de cantidad, actualizar el contador después de 500ms
document.addEventListener('DOMContentLoaded', function() {
    const formsCarrito = document.querySelectorAll('form[action*="actualizar_cantidad"]');
    formsCarrito.forEach(form => {
        form.addEventListener('submit', () => {
            setTimeout(actualizarCarrito, 500);
        });
    });
});

// Función para toggle de detalles en pedidos
function toggleDetalles(pedidoId) {
    const itemsDiv = document.getElementById('items-' + pedidoId);
    const textSpan = document.getElementById('text-' + pedidoId);
    if (itemsDiv.style.display === 'none') {
        itemsDiv.style.display = 'block';
        textSpan.textContent = 'Ocultar';
    } else {
        itemsDiv.style.display = 'none';
        textSpan.textContent = 'Ver';
    }
}
