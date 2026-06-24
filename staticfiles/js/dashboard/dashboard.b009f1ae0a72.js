// ── Dashboard UI Interactions ──────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    // Note Modal Logic
    const noteModal = document.getElementById('noteModal');
    const viewNoteBtns = document.querySelectorAll('.view-note-btn');
    const closeBtns = document.querySelectorAll('.close, .toggle-btn');
    const modalContent = document.getElementById('modalNoteContent');

    if (noteModal) {
        viewNoteBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const row = btn.closest('tr');
                const noteText = row.querySelector('.note-cell')?.title || "No detailed note available.";
                modalContent.textContent = noteText;
                noteModal.style.display = 'flex';
                // Trigger transition reflow
                setTimeout(() => noteModal.classList.add('show'), 10);
            });
        });

        closeBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                noteModal.classList.remove('show');
                setTimeout(() => {
                    noteModal.style.display = 'none';
                }, 250); // Matches transition duration
            });
        });

        window.addEventListener('click', (e) => {
            if (e.target === noteModal) {
                noteModal.classList.remove('show');
                setTimeout(() => {
                    noteModal.style.display = 'none';
                }, 250);
            }
        });
    }

    // Dashboard Summary Counts (Restore functionality)
    const servicesCountEl = document.getElementById('services-count');
    const todayCountEl = document.getElementById('today-count');
    
    // In a real app, these would come from the backend. 
    // Here we'll do a quick count of rows if on the relevant page or use placeholders.
    if (servicesCountEl) {
        // Mock count for visual completeness if not provided by template context
        if (servicesCountEl.textContent === '...') {
            servicesCountEl.textContent = '8'; 
        }
    }
    if (todayCountEl) {
        const rows = document.querySelectorAll('.admin-table tbody tr:not(.empty-state)');
        if (todayCountEl.textContent === '...') {
            todayCountEl.textContent = rows.length > 0 ? rows.length.toString() : '0';
        }
    }

    // Table row highlight
    document.querySelectorAll('.admin-table tbody tr').forEach(row => {
        row.addEventListener('click', (e) => {
            if (e.target.closest('button, a, form')) return;
            
            document.querySelectorAll('.admin-table tbody tr').forEach(r =>
                r.style.background = ''
            );
            row.style.background = 'var(--accent-pale)';
        });
    });

    // Reveal animations
    const revealEls = document.querySelectorAll('.stat-card, .table-card, .card');
    const obs = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                obs.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    revealEls.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        obs.observe(el);
    });
});

// ── Prevent double-submit on forms ──────────────────────────────
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', () => {
        const btn = form.querySelector('button[type="submit"]');
        if (btn && !btn.classList.contains('no-disable')) {
            setTimeout(() => {
                btn.disabled = true;
                btn.innerHTML = '<span class="spinner"></span> Processing...';
            }, 0);
        }
    });
});
