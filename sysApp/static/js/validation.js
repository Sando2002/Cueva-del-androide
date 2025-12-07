/* Validación de formularios */

function validarFormulario(form) {
    // Obtener el valor del campo precio y stock
    var precio = parseFloat(form.precio.value);
    var stock = parseFloat(form.stock.value);

    // Verificar si el precio o stock son negativos
    if (isNaN(precio) || precio < 0) {
        alert('El precio no puede ser negativo.');
        return false; // Evitar el envío del formulario
    }

    if (isNaN(stock) || stock < 0) {
        alert('El stock no puede ser negativo.');
        return false; // Evitar el envío del formulario
    }

    // Si ambos valores son válidos, se permite el envío del formulario
    return true;
}
