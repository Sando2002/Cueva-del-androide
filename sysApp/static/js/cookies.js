/**
 * Cookie Banner Script
 * Maneja la visualización y aceptación de cookies
 * Cumplimiento: Ley 19.628 y directiva de cookies
 */

document.addEventListener('DOMContentLoaded', function() {
  const cookieBanner = document.getElementById('cookieBanner');
  const acceptBtn = document.getElementById('acceptCookies');
  const declineBtn = document.getElementById('declineCookies');
  
  // Cookie names
  const COOKIE_CONSENT_NAME = 'cueva_cookie_consent';
  const COOKIE_CONSENT_TIMEOUT = 365 * 24 * 60 * 60 * 1000; // 1 año

  /**
   * Verifica si el usuario ya ha aceptado/rechazado cookies
   */
  function hasCookieConsent() {
    const consent = localStorage.getItem(COOKIE_CONSENT_NAME);
    return consent !== null;
  }

  /**
   * Muestra el banner si no hay consentimiento previo
   */
  function showBannerIfNeeded() {
    if (!hasCookieConsent()) {
      // Pequeño delay para asegurar que el DOM esté listo
      setTimeout(() => {
        if (cookieBanner) {
          cookieBanner.classList.add('show');
        }
      }, 500);
    } else {
      // Ocultar banner si ya tiene consentimiento
      if (cookieBanner) {
        cookieBanner.classList.add('hide');
      }
    }
  }

  /**
   * Guarda el consentimiento de cookies
   */
  function saveCookieConsent(accepted) {
    const consentData = {
      accepted: accepted,
      date: new Date().toISOString(),
      version: '1.0'
    };
    
    localStorage.setItem(COOKIE_CONSENT_NAME, JSON.stringify(consentData));
    
    // Log para auditoría
    if (window.gtag) {
      gtag('consent', 'update', {
        'analytics_storage': accepted ? 'granted' : 'denied',
        'ad_storage': accepted ? 'granted' : 'denied',
        'wait_for_update': 500
      });
    }
    
    hideBanner();
  }

  /**
   * Oculta el banner con animación
   */
  function hideBanner() {
    if (cookieBanner) {
      cookieBanner.classList.remove('show');
      cookieBanner.classList.add('hide');
    }
  }

  /**
   * Event listeners
   */
  if (acceptBtn) {
    acceptBtn.addEventListener('click', function() {
      saveCookieConsent(true);
      
      // Aquí puedes agregar Google Analytics, Hotjar, etc.
      // Solo si el usuario aceptó
      if (window.gtag) {
        gtag('event', 'page_view');
      }
    });
  }

  if (declineBtn) {
    declineBtn.addEventListener('click', function() {
      saveCookieConsent(false);
    });
  }

  /**
   * Inicialización
   */
  showBannerIfNeeded();

  /**
   * Exposición pública para limpiar cookies (admin tools)
   */
  window.clearCookieConsent = function() {
    localStorage.removeItem(COOKIE_CONSENT_NAME);
    showBannerIfNeeded();
  };
});

/**
 * Helper: Obtener consentimiento de cookies
 * Uso: getCookieConsent()
 * Retorna: {accepted: boolean, date: string, version: string} | null
 */
function getCookieConsent() {
  const consent = localStorage.getItem('cueva_cookie_consent');
  return consent ? JSON.parse(consent) : null;
}

/**
 * Helper: Verificar si cookies fueron aceptadas
 * Uso: isCookiesAccepted()
 * Retorna: boolean
 */
function isCookiesAccepted() {
  const consent = getCookieConsent();
  return consent ? consent.accepted : false;
}
