document.addEventListener('DOMContentLoaded', function() {
    // Initialize Feather icons
    feather.replace();

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

    // Admin content editor
    const contentEditor = document.getElementById('content-editor');
    if (contentEditor) {
        // Simple WYSIWYG functionality
        const toolbar = document.createElement('div');
        toolbar.className = 'btn-toolbar mb-3';
        toolbar.innerHTML = `
            <div class="btn-group me-2">
                <button type="button" class="btn btn-sm btn-outline-secondary" data-command="bold">
                    <i data-feather="bold"></i>
                </button>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-command="italic">
                    <i data-feather="italic"></i>
                </button>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-command="underline">
                    <i data-feather="underline"></i>
                </button>
            </div>
        `;
        
        contentEditor.parentNode.insertBefore(toolbar, contentEditor);
        
        toolbar.querySelectorAll('[data-command]').forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const command = this.dataset.command;
                document.execCommand(command, false, null);
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
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);
        
        L.marker([lat, lng]).addTo(map);
    }
});
