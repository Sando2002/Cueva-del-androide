/* Funciones de pago - Verificación automática */

function iniciarVerificacionPago(urlVerificar, urlRedirect) {
    let verificarInterval;
    let intentos = 0;
    const maxIntentos = 30; // 60 segundos de verificación máximo
    
    function verificarPago() {
        intentos++;
        
        fetch(urlVerificar)
            .then(response => response.json())
            .then(data => {
                console.log("Verificación de pago:", data);
                
                if (data.status === 'success' && data.estado === 'aprobado') {
                    // Pago confirmado, detener el polling
                    clearInterval(verificarInterval);
                    
                    // Redirigir a mis pedidos después de 1 segundo
                    setTimeout(() => {
                        window.location.href = urlRedirect;
                    }, 1000);
                } else if (data.status === 'pending') {
                    // Aún en proceso, seguir verificando
                    console.log("Pago en proceso...");
                } else if (intentos >= maxIntentos) {
                    // Dejar de intentar después de 60 segundos
                    clearInterval(verificarInterval);
                    console.log("Se alcanzó el máximo de intentos de verificación");
                }
            })
            .catch(error => {
                console.error("Error al verificar pago:", error);
                if (intentos >= maxIntentos) {
                    clearInterval(verificarInterval);
                }
            });
    }
    
    // Iniciar verificación automática después de 2 segundos de carga
    verificarInterval = setInterval(verificarPago, 2000);
    
    // Hacer una verificación inmediata
    verificarPago();
}
