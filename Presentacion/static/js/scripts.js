// scripts.js - Menú Hamburguesa (3 Pestañas), Chatbot, Datos de Pago Simulados y Configuración AJAX

// 1. ABRIR Y CERRAR MENÚ HAMBURGUESA
function toggleHamburgerMenu() {
    const sidebar = document.getElementById('hamburger-sidebar');
    const backdrop = document.getElementById('hamburger-backdrop');
    if (!sidebar || !backdrop) return;

    if (sidebar.style.right === '0px') {
        sidebar.style.right = '-420px';
        backdrop.style.display = 'none';
    } else {
        sidebar.style.right = '0px';
        backdrop.style.display = 'block';
        cargarDatosLive();
        cargarDatosPerfilConfig();
    }
}

// 2. CAMBIO DE PESTAÑAS EN EL HAMBURGUESA (NOTIFICACIONES | PEDIDOS | CONFIGURACIÓN)
function switchTab(tabName) {
    const tabNotif = document.getElementById('tab-btn-notif');
    const tabPedidos = document.getElementById('tab-btn-pedidos');
    const tabConfig = document.getElementById('tab-btn-config');

    const contentNotif = document.getElementById('content-notificaciones');
    const contentPedidos = document.getElementById('content-pedidos');
    const contentConfig = document.getElementById('content-configuracion');

    if (!tabNotif || !tabPedidos || !tabConfig || !contentNotif || !contentPedidos || !contentConfig) return;

    // Reset de estilos
    [tabNotif, tabPedidos, tabConfig].forEach(btn => {
        btn.style.color = '#888';
        btn.style.borderBottom = '3px solid transparent';
    });
    [contentNotif, contentPedidos, contentConfig].forEach(c => c.style.display = 'none');

    if (tabName === 'notificaciones') {
        tabNotif.style.color = '#A35D49';
        tabNotif.style.borderBottom = '3px solid #A35D49';
        contentNotif.style.display = 'block';
    } else if (tabName === 'pedidos') {
        tabPedidos.style.color = '#A35D49';
        tabPedidos.style.borderBottom = '3px solid #A35D49';
        contentPedidos.style.display = 'block';
    } else if (tabName === 'configuracion') {
        tabConfig.style.color = '#A35D49';
        tabConfig.style.borderBottom = '3px solid #A35D49';
        contentConfig.style.display = 'block';
        cargarDatosPerfilConfig();
    }
}

// 3. TOGGLE DE INPUTS SIMULADOS DE PAGO EN CARRITO
function togglePagoInputs(valor) {
    const boxTarjeta = document.getElementById('box-pago-tarjeta');
    const boxPaypal = document.getElementById('box-pago-paypal');
    const boxTransf = document.getElementById('box-pago-transferencia');
    const boxEfectivo = document.getElementById('box-pago-efectivo');

    if (!boxTarjeta) return;

    boxTarjeta.style.display = 'none';
    boxPaypal.style.display = 'none';
    boxTransf.style.display = 'none';
    boxEfectivo.style.display = 'none';

    // Desactivar campos required cuando no están visibles
    document.querySelectorAll('#box-pago-tarjeta input').forEach(i => i.required = false);
    document.querySelectorAll('#box-pago-paypal input').forEach(i => i.required = false);

    if (valor === 'TARJETA') {
        boxTarjeta.style.display = 'flex';
        document.querySelectorAll('#box-pago-tarjeta input').forEach(i => i.required = true);
    } else if (valor === 'PAYPAL') {
        boxPaypal.style.display = 'flex';
        document.getElementById('paypal_acc').required = true;
    } else if (valor === 'TRANSFERENCIA') {
        boxTransf.style.display = 'block';
    } else if (valor === 'EFECTIVO') {
        boxEfectivo.style.display = 'block';
    }
}

// 4. TOGGLE EN PANEL DE CONFIGURACIÓN DE PAGO
function toggleConfigPagoInputs() {
    const metodo = document.getElementById('cfg-metodo-pref').value;
    const boxT = document.getElementById('cfg-box-tarjeta');
    const boxP = document.getElementById('cfg-box-paypal');
    if (!boxT || !boxP) return;

    if (metodo === 'TARJETA') {
        boxT.style.display = 'block';
        boxP.style.display = 'none';
    } else {
        boxT.style.display = 'none';
        boxP.style.display = 'block';
    }
}

// 5. CARGAR DATOS EN PANEL DE CONFIGURACIÓN VIA AJAX
function cargarDatosPerfilConfig() {
    fetch('/api/configuracion/')
        .then(res => res.json())
        .then(data => {
            if (data.ok) {
                const elNombre = document.getElementById('cfg-nombre');
                const elApellido = document.getElementById('cfg-apellido');
                const elEmail = document.getElementById('cfg-email');
                const elTel = document.getElementById('cfg-telefono');
                const elDir = document.getElementById('cfg-direccion');

                if (elNombre) elNombre.value = data.nombre || '';
                if (elApellido) elApellido.value = data.apellido || '';
                if (elEmail) elEmail.value = data.email || '';
                if (elTel) elTel.value = data.telefono || '';
                if (elDir) elDir.value = data.direccion || '';

                if (data.metodo_guardado && data.metodo_guardado.metodo) {
                    const selPref = document.getElementById('cfg-metodo-pref');
                    if (selPref) {
                        selPref.value = data.metodo_guardado.metodo;
                        toggleConfigPagoInputs();
                    }
                    if (data.metodo_guardado.num_tarjeta) {
                        const inputTarj = document.getElementById('cfg-num-tarjeta');
                        if (inputTarj) inputTarj.value = '**** **** **** ' + data.metodo_guardado.num_tarjeta;
                    }
                    if (data.metodo_guardado.paypal_email) {
                        const inputPay = document.getElementById('cfg-paypal-email');
                        if (inputPay) inputPay.value = data.metodo_guardado.paypal_email;
                    }
                }
            }
        })
        .catch(err => console.error("Error cargando perfil:", err));
}

// 6. GUARDAR PERFIL (DATOS PERSONALES)
function guardarPerfil(e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append('accion', 'perfil');
    formData.append('nombre', document.getElementById('cfg-nombre').value);
    formData.append('apellido', document.getElementById('cfg-apellido').value);
    formData.append('email', document.getElementById('cfg-email').value);
    formData.append('telefono', document.getElementById('cfg-telefono').value);
    formData.append('direccion', document.getElementById('cfg-direccion').value);

    fetch('/api/configuracion/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            alert(data.mensaje);
            if (data.ok) cargarDatosPerfilConfig();
        });
}

// 7. GUARDAR MÉTODO DE PAGO PREDETERMINADO
function guardarMetodoPagoPref(e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append('accion', 'metodo_pago');
    formData.append('metodo_pago_pref', document.getElementById('cfg-metodo-pref').value);
    formData.append('num_tarjeta', document.getElementById('cfg-num-tarjeta').value);
    formData.append('paypal_email', document.getElementById('cfg-paypal-email').value);

    fetch('/api/configuracion/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            alert(data.mensaje);
        });
}

// 8. GUARDAR CAMBIO DE CONTRASEÑA
function guardarPassword(e) {
    e.preventDefault();
    const passActual = document.getElementById('cfg-pass-actual').value;
    const passNuevo = document.getElementById('cfg-pass-nuevo').value;

    const formData = new FormData();
    formData.append('accion', 'password');
    formData.append('pass_actual', passActual);
    formData.append('pass_nuevo', passNuevo);

    fetch('/api/configuracion/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            alert(data.mensaje);
            if (data.ok) {
                document.getElementById('cfg-pass-actual').value = '';
                document.getElementById('cfg-pass-nuevo').value = '';
            }
        });
}

// OBTENER CSRF TOKEN DE LAS COOKIES
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// 9. ACORDEÓN DE MIS PEDIDOS
function togglePedidoAccordion(pedidoId) {
    const detailDiv = document.getElementById(`pedido-detail-${pedidoId}`);
    const iconSpan = document.getElementById(`pedido-icon-${pedidoId}`);
    if (!detailDiv) return;

    if (detailDiv.style.display === 'block') {
        detailDiv.style.display = 'none';
        if (iconSpan) iconSpan.innerText = 'expand_more';
    } else {
        detailDiv.style.display = 'block';
        if (iconSpan) iconSpan.innerText = 'expand_less';
    }
}

// 10. AUTO-ACTUALIZACIÓN EN VIVO (LIVE POLLING)
function cargarDatosLive() {
    fetch('/api/mis-pedidos/')
        .then(response => response.json())
        .then(data => {
            renderNotificaciones(data.notificaciones);
            renderPedidosAcordeon(data.pedidos);
        })
        .catch(err => console.error("Error consultando API Live Pedidos:", err));
}

function renderNotificaciones(notificaciones) {
    const container = document.getElementById('lista-notificaciones');
    const navBadge = document.getElementById('badge-notif-nav');
    if (!container) return;

    if (!notificaciones || notificaciones.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #888; margin-top: 30px;">No tienes notificaciones recientes.</p>';
        if (navBadge) navBadge.style.display = 'none';
        return;
    }

    if (navBadge) {
        navBadge.style.display = 'flex';
        navBadge.innerText = notificaciones.length;
    }

    let html = '';
    notificaciones.forEach(n => {
        html += `
        <div style="background: #FFFDF9; border-left: 4px solid #A35D49; border-radius: 8px; padding: 12px 15px; margin-bottom: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <b style="color: #3E211D; font-size: 0.95rem;">${n.titulo}</b>
                <span style="font-size: 0.75rem; color: #888;">${n.fecha}</span>
            </div>
            <p style="font-size: 0.85rem; color: #555; margin: 0;">${n.mensaje}</p>
        </div>`;
    });
    container.innerHTML = html;
}

function renderPedidosAcordeon(pedidos) {
    const container = document.getElementById('lista-pedidos-acordeon');
    if (!container) return;

    if (!pedidos || pedidos.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #888; margin-top: 30px;">No has realizado pedidos aún.</p>';
        return;
    }

    let html = '';
    pedidos.forEach(p => {
        let badgeColor = '#e67e22';
        if (p.estado === 'EN_PROCESO') badgeColor = '#3498db';
        if (p.estado === 'ENTREGADO') badgeColor = '#27ae60';
        if (p.estado === 'FALLIDO') badgeColor = '#e74c3c';

        let itemsHtml = '';
        p.detalles.forEach(d => {
            itemsHtml += `
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; padding: 4px 0; border-bottom: 1px dashed #eee;">
                <span>${d.cantidad}x ${d.producto}</span>
                <b>S/ ${d.subtotal.toFixed(2)}</b>
            </div>`;
        });

        html += `
        <div style="background: white; border: 1px solid #ddd; border-radius: 12px; margin-bottom: 15px; overflow: hidden; box-shadow: 0 3px 8px rgba(0,0,0,0.04);">
            <div onclick="togglePedidoAccordion(${p.id})" style="padding: 15px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; background: #FFFDF9;">
                <div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <b style="color: #3E211D; font-size: 1.05rem;">Pedido #${p.id}</b>
                        <span style="background: ${badgeColor}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; font-weight: bold;">${p.estado_display}</span>
                    </div>
                    <p style="font-size: 0.8rem; color: #888; margin: 4px 0 0 0;">${p.fecha} • S/ ${p.total.toFixed(2)}</p>
                </div>
                <span class="material-symbols-outlined" id="pedido-icon-${p.id}" style="color: #A35D49;">expand_more</span>
            </div>

            <div id="pedido-detail-${p.id}" style="display: none; padding: 15px; background: white; border-top: 1px solid #eee;">
                <p style="font-size: 0.85rem; color: #4A2825; margin-bottom: 8px;"><b>⏱ Tiempo Estimado:</b> ${p.tiempo_estimado}</p>
                <p style="font-size: 0.85rem; color: #4A2825; margin-bottom: 8px;"><b> Entrega:</b> ${p.metodo_entrega}</p>
                <p style="font-size: 0.85rem; color: #4A2825; margin-bottom: 12px;"><b> Pago:</b> ${p.metodo_pago}</p>
                
                <b style="font-size: 0.85rem; color: #3E211D; display: block; margin-bottom: 6px;">Productos Comprados:</b>
                ${itemsHtml}

                <a href="/repetir-pedido/${p.id}/" class="btn-primary" style="margin-top: 15px; padding: 10px; font-size: 0.85rem; border-radius: 8px; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 6px; font-weight: bold; background-color: #A35D49;">
                    <span class="material-symbols-outlined" style="font-size: 18px;">autorenew</span> 🔄 Repetir este Pedido
                </a>
            </div>
        </div>`;
    });

    container.innerHTML = html;
}

// 11. CHATBOT FLOTANTE
function toggleChat() {
    const body = document.getElementById('chat-body');
    if (body) {
        body.style.display = body.style.display === 'none' ? 'block' : 'none';
    }
}

function enviarMensaje() {
    const input = document.getElementById('chat-input');
    const messages = document.getElementById('chat-messages');
    if (!input || !messages) return;

    const userText = input.value;
    if (userText.trim() === '') return;

    messages.innerHTML += `<p style="text-align: right; color: blue;"><b>Tú:</b> ${userText}</p>`;
    input.value = '';
    messages.scrollTop = messages.scrollHeight;

    fetch(`/api/chat/?mensaje=${encodeURIComponent(userText)}`)
        .then(response => response.json())
        .then(data => {
            messages.innerHTML += `<p style="text-align: left; color: #333;"><b>Bot:</b> ${data.respuesta}</p>`;
            messages.scrollTop = messages.scrollHeight;
        })
        .catch(error => console.error('Error:', error));
}

// INICIALIZACIÓN
document.addEventListener("DOMContentLoaded", function () {
    const chatInput = document.getElementById("chat-input");
    if (chatInput) {
        chatInput.addEventListener("keypress", function (event) {
            if (event.key === "Enter") {
                event.preventDefault();
                enviarMensaje();
            }
        });
    }

    cargarDatosLive();
    setInterval(cargarDatosLive, 5000);
});
