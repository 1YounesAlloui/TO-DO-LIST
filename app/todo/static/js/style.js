document.addEventListener('DOMContentLoaded', function() {
    const body = document.documentElement;
    const themeSwitcherBtn = document.getElementById('themeSwitcherBtn');
    const themePopover = document.getElementById('themePopover');
    const themeOptions = document.querySelectorAll('.theme-option');

    const savedTheme = localStorage.getItem('theme');
    const validThemes = ['theme-mountain-dawn', 'theme-ocean-horizon', 'theme-desert-canyon', 'theme-forest-sanctuary', 'theme-sunset-highlands'];
    
    if (savedTheme && validThemes.includes(savedTheme)) {
        body.className = savedTheme;
    } else {
        body.className = 'theme-mountain-dawn';
        localStorage.setItem('theme', 'theme-mountain-dawn');
    }

    // Toggle popover
    themeSwitcherBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        themePopover.style.display = themePopover.style.display === 'block' ? 'none' : 'block';
    });

    // Close popover when clicking outside
    document.addEventListener('click', function(e) {
        if (!themePopover.contains(e.target) && e.target !== themeSwitcherBtn) {
            themePopover.style.display = 'none';
        }
    });

    // Apply selected theme
    themeOptions.forEach(option => {
        option.addEventListener('click', function() {
            const theme = this.dataset.theme;
            body.className = theme;
            localStorage.setItem('theme', theme);
            themePopover.style.display = 'none';
        });
    });
});