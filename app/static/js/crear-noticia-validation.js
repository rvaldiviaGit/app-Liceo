// Constantes para validación
const TITULO_MIN_LENGTH = 5;
const TITULO_MAX_LENGTH = 100;
const CONTENIDO_MIN_LENGTH = 50;
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif'];
const ALLOWED_FILE_TYPES = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
];

class FormValidator {
    constructor(formId) {
        this.form = document.getElementById(formId);
        this.errors = new Map();
        
        // Inicializar validación
        this.initializeValidation();
    }

    initializeValidation() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));

        // Validación en tiempo real
        this.form.querySelector('#titulo').addEventListener('input', (e) => this.validateTitulo(e.target.value));
        this.form.querySelector('#categoria').addEventListener('change', (e) => this.validateCategoria(e.target.value));
        this.form.querySelector('#contenido').addEventListener('input', (e) => this.validateContenido(e.target.value));
        this.form.querySelector('#imagen').addEventListener('change', (e) => this.validateImagen(e.target.files[0]));
        this.form.querySelector('#archivos').addEventListener('change', (e) => this.validateArchivos(e.target.files));
    }

    // ... (métodos de validación anteriores se mantienen igual) ...

    async submitForm() {
        try {
            const formData = new FormData(this.form);
            const response = await fetch(window.location.pathname, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'  // Importante para el CSRF token
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Error al crear la noticia');
            }

            const result = await response.json();
            if (result.success) {
                window.location.href = result.redirect;
            } else {
                throw new Error(result.message);
            }
        } catch (error) {
            alert('Error: ' + error.message);
        }
    }
}

// Inicializar el validador cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new FormValidator('crear-noticia-form');
});