document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const sendButton = document.getElementById('send-button');

    // Generar un ID de sesión simple
    let sessionId = typeof crypto !== 'undefined' && crypto.randomUUID ? crypto.randomUUID() : Math.random().toString(36).substring(2);

    // Cargar documentos dinámicamente en la sidebar
    async function loadDocs() {
        const docsList = document.getElementById('docs-list');
        if (!docsList) return;
        
        try {
            const res = await fetch('/api/docs');
            const data = await res.json();
            
            docsList.innerHTML = '';
            if (data.docs && data.docs.length > 0) {
                data.docs.forEach(doc => {
                    const li = document.createElement('li');
                    const isCsv = doc.toLowerCase().endsWith('.csv');
                    const icon = isCsv ? '📊' : '📄';
                    li.innerHTML = `<span class="icon">${icon}</span> <span class="doc-name" title="${doc}">${doc}</span>`;
                    li.style.cursor = 'pointer';
                    li.addEventListener('click', () => openDocPreview(doc));
                    docsList.appendChild(li);
                });
            } else {
                docsList.innerHTML = '<li style="opacity: 0.5;">No hay documentos</li>';
            }
        } catch (error) {
            docsList.innerHTML = '<li style="opacity: 0.5; color: red;">Error al cargar</li>';
        }
    }
    
    loadDocs();

    // Función para manejar el envío del formulario
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = chatInput.value.trim();
        if (!message) return;

        // Añadir mensaje del usuario a la UI
        appendMessage('user', message);
        chatInput.value = '';
        
        // Mostrar indicador de carga
        const loadingId = appendMessage('bot', '<span class="loading-dots">Escribiendo...</span>', null, true);

        try {
            // Enviar solicitud a la API
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    message: message,
                    session_id: sessionId
                })
            });

            const data = await response.json();
            
            // Remover indicador de carga
            removeMessage(loadingId);

            if (response.ok) {
                appendMessage('bot', data.answer, data.sources);
            } else {
                appendMessage('system', 'Error: ' + (data.detail || 'Hubo un problema al procesar la solicitud.'));
            }
            
        } catch (error) {
            console.error('Error:', error);
            removeMessage(loadingId);
            appendMessage('system', 'Error de conexión. Asegúrate de que el servidor está corriendo.');
        }
    });

    // Permitir enviar con Enter (sin Shift)
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });

    // Lógica para el botón de limpiar chat
    const clearBtn = document.getElementById('clear-chat-btn');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            chatMessages.innerHTML = '';
            // Generar nuevo ID de sesión para empezar de cero
            sessionId = typeof crypto !== 'undefined' && crypto.randomUUID ? crypto.randomUUID() : Math.random().toString(36).substring(2);
            appendMessage('system', 'Historial borrado. Iniciando nueva sesión.');
        });
    }
    // Elementos del Modal
    const docModal = document.getElementById('doc-modal');
    const modalCloseBtn = document.getElementById('modal-close-btn');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');

    // Función para abrir la previsualización
    function openDocPreview(filename) {
        modalTitle.textContent = filename;
        modalBody.innerHTML = '<div class="csv-loading">Cargando...</div>';
        docModal.classList.remove('hidden');
        
        const fileUrl = `/docs_files/${filename}`;
        const ext = filename.toLowerCase().split('.').pop();
        
        if (ext === 'pdf') {
            modalBody.innerHTML = `<iframe src="${fileUrl}" width="100%" height="100%" style="border: none;"></iframe>`;
        } else if (ext === 'csv') {
            fetch(fileUrl)
                .then(res => res.text())
                .then(text => {
                    const rows = text.split('\n').filter(r => r.trim() !== '');
                    if (rows.length === 0) {
                        modalBody.innerHTML = '<div class="csv-error">El archivo CSV está vacío.</div>';
                        return;
                    }
                    
                    let html = '<div class="csv-table-wrapper"><table class="csv-preview-table">';
                    rows.forEach((row, index) => {
                        // Regex básico para separar por comas ignorando comas dentro de comillas
                        const cols = row.split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/);
                        
                        if (index === 0) {
                            html += '<tr>' + cols.map(c => `<th>${c.replace(/^"|"$/g, '').trim()}</th>`).join('') + '</tr>';
                        } else {
                            html += '<tr>' + cols.map(c => `<td>${c.replace(/^"|"$/g, '').trim()}</td>`).join('') + '</tr>';
                        }
                    });
                    html += '</table></div>';
                    modalBody.innerHTML = html;
                })
                .catch(err => {
                    modalBody.innerHTML = '<div class="csv-error">Error al cargar el archivo CSV.</div>';
                });
        } else {
             fetch(fileUrl)
                .then(res => res.text())
                .then(text => {
                     modalBody.innerHTML = `<pre style="padding: 20px; font-size: 14px; color: #333; white-space: pre-wrap;">${text}</pre>`;
                })
                .catch(err => {
                    modalBody.innerHTML = '<div class="csv-error">Error al cargar el archivo.</div>';
                });
        }
    }

    // Cerrar el modal al hacer clic en la X
    if (modalCloseBtn) {
        modalCloseBtn.addEventListener('click', () => {
            docModal.classList.add('hidden');
            setTimeout(() => { modalBody.innerHTML = ''; }, 300); // Limpiar contenido tras la animación
        });
    }

    // Cerrar el modal al hacer clic en el fondo oscurecido
    if (docModal) {
        docModal.addEventListener('click', (e) => {
            if (e.target === docModal) {
                docModal.classList.add('hidden');
                setTimeout(() => { modalBody.innerHTML = ''; }, 300);
            }
        });
    }

});

let messageCounter = 0;

function removeMessage(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}

function appendMessage(sender, text, sources = null, isRawHtml = false) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.id = 'msg-' + (messageCounter++);
    
    // Configurar avatar
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.innerHTML = sender === 'user' ? '🤔' : (sender === 'system' ? '⚠️' : '🙂');
    
    // Configurar contenido
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content markdown-body';
    
    // Si es bot y no es raw html (como los loading dots), parsear Markdown
    if (sender === 'bot' && !isRawHtml && window.marked && window.DOMPurify) {
        contentDiv.innerHTML = DOMPurify.sanitize(marked.parse(text));
    } else if (isRawHtml) {
        contentDiv.innerHTML = text;
    } else {
        contentDiv.textContent = text;
    }
    
    // Agregar fuentes si existen
    if (sources && sources.length > 0) {
        const sourcesContainer = document.createElement('div');
        sourcesContainer.className = 'sources-container';
        
        const sourcesTitle = document.createElement('div');
        sourcesTitle.className = 'sources-title';
        sourcesTitle.textContent = 'Fuentes consultadas:';
        sourcesContainer.appendChild(sourcesTitle);
        
        sources.forEach(source => {
            const badge = document.createElement('span');
            badge.className = 'source-badge';
            badge.textContent = source.source;
            badge.title = source.content_snippet; // Tooltip on hover
            sourcesContainer.appendChild(badge);
        });
        
        contentDiv.appendChild(sourcesContainer);
    }
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    
    // Auto-scroll al final
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return messageDiv.id;
}
