/* Notificaciones del sistema */

document.addEventListener('DOMContentLoaded', function() {
    const notifBell = document.getElementById('notifBell');
    const notifDropdown = document.getElementById('notifDropdown');
    const notifList = document.getElementById('notifList');
    const notifCount = document.getElementById('notifCount');

    // Solo ejecutar si existen los elementos de notificación
    if (!notifBell || !notifDropdown || !notifList || !notifCount) {
        return;
    }

    function cargarNotificaciones() {
        // Detectar dinámicamente la URL
        const urlPattern = '{% url "get_notificaciones_sin_leer" %}' || '/get_notificaciones_sin_leer/';
        
        fetch(urlPattern, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            // Actualizar contador
            if (data.total_sin_leer > 0) {
                notifCount.style.display = 'inline-block';
                notifCount.textContent = data.total_sin_leer;
            } else {
                notifCount.style.display = 'none';
            }

            // Actualizar lista de notificaciones
            notifList.innerHTML = '';
            if (data.notificaciones.length > 0) {
                data.notificaciones.forEach(notif => {
                    const div = document.createElement('div');
                    div.className = 'notif-item';
                    div.innerHTML = `
                        <div class="notif-item-title">${notif.titulo}</div>
                        <div class="notif-item-text">${notif.mensaje.substring(0, 60)}...</div>
                        <div class="notif-item-time"><i class="fas fa-clock"></i> ${notif.fecha}</div>
                    `;
                    notifList.appendChild(div);
                });
            } else {
                notifList.innerHTML = '<div style="padding: 20px; text-align: center; color: #999;">No hay notificaciones</div>';
            }
        })
        .catch(error => console.error('Error al cargar notificaciones:', error));
    }

    // Toggle del dropdown
    notifBell.addEventListener('click', (e) => {
        e.preventDefault();
        notifDropdown.style.display = notifDropdown.style.display === 'none' ? 'block' : 'none';
        if (notifDropdown.style.display === 'block') {
            cargarNotificaciones();
        }
    });

    // Cerrar dropdown al hacer clic fuera
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.notif-container')) {
            notifDropdown.style.display = 'none';
        }
    });

    // Cargar notificaciones cada 30 segundos
    setInterval(cargarNotificaciones, 30000);
    cargarNotificaciones();
});
