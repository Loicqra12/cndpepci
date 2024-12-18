document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Directory search form handling
    const directorySearchForm = document.getElementById('directory-search-form');
    if (directorySearchForm) {
        directorySearchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const searchQuery = document.getElementById('search').value;
            const region = document.getElementById('region').value;
            
            let url = '/directory?';
            if (searchQuery) url += `search=${encodeURIComponent(searchQuery)}&`;
            if (region) url += `region=${encodeURIComponent(region)}`;
            
            window.location.href = url;
        });
    }

    // Contact form validation
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            if (!contactForm.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            contactForm.classList.add('was-validated');
        });
    }

    // Initialize modals
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modalEl => {
        new bootstrap.Modal(modalEl);
    });

    // Admin content editor
    const contentEditor = document.getElementById('content-editor');
    if (contentEditor) {
        // Simple WYSIWYG functionality
        const toolbar = document.createElement('div');
        toolbar.className = 'btn-toolbar mb-3';
        toolbar.innerHTML = `
            <div class="btn-group me-2">
                <button type="button" class="btn btn-sm btn-outline-secondary" data-command="bold">
                    <i class="bi bi-type-bold"></i>
                </button>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-command="italic">
                    <i class="bi bi-type-italic"></i>
                </button>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-command="underline">
                    <i class="bi bi-type-underline"></i>
                </button>
            </div>
            <div class="btn-group me-2">
                <button type="button" class="btn btn-sm btn-outline-secondary" data-command="justifyLeft">
                    <i class="bi bi-text-left"></i>
                </button>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-command="justifyCenter">
                    <i class="bi bi-text-center"></i>
                </button>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-command="justifyRight">
                    <i class="bi bi-text-right"></i>
                </button>
            </div>
        `;

        contentEditor.parentNode.insertBefore(toolbar, contentEditor);

        // Handle toolbar button clicks
        toolbar.querySelectorAll('[data-command]').forEach(button => {
            button.addEventListener('click', function() {
                const command = this.dataset.command;
                document.execCommand(command, false, null);
                contentEditor.focus();
            });
        });
    }

    // Handle member location map if present
    const memberMap = document.getElementById('member-map');
    if (memberMap) {
        const lat = memberMap.dataset.lat;
        const lng = memberMap.dataset.lng;
        
        // Initialize map (assuming using Leaflet.js)
        const map = L.map('member-map').setView([lat, lng], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: ' OpenStreetMap contributors'
        }).addTo(map);
        
        L.marker([lat, lng]).addTo(map);
    }
});
