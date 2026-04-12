document.addEventListener("DOMContentLoaded", () => {
    const themeToggle = document.getElementById("themeToggle");
    const currentTheme = localStorage.getItem("theme");

    // Initialize Theme Pipeline natively preventing JS flashes ideally handled efficiently via local variables.
    if (currentTheme) {
        document.documentElement.setAttribute("data-theme", currentTheme);
        updateIcon(currentTheme);
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.setAttribute("data-theme", "dark");
        updateIcon("dark");
    } else {
        // Default natively safely mapped.
        updateIcon("light");
    }

    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            let theme = document.documentElement.getAttribute("data-theme");
            let newTheme = theme === "dark" ? "light" : "dark";
            
            document.documentElement.setAttribute("data-theme", newTheme);
            localStorage.setItem("theme", newTheme);
            updateIcon(newTheme);
        });
    }

    function updateIcon(theme) {
        if (!themeToggle) return;
        // Clean linear moon and sun svg icons dynamically parsed depending on conditional loop output!
        const sunIcon = `<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>`;
        const moonIcon = `<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>`;
        themeToggle.innerHTML = theme === "dark" ? sunIcon : moonIcon;
    }

    // Mobile Navigation Toggle Logic
    const mobileMenuBtn = document.getElementById("mobileMenuBtn");
    const mobileCloseBtn = document.getElementById("mobileCloseBtn");
    const mobileSidebar = document.getElementById("mobileSidebar");
    const mobileOverlay = document.getElementById("mobileOverlay");
    const mobileLinks = document.querySelectorAll(".mobile-nav-link");

    function closeMobileMenu() {
        if (mobileSidebar) mobileSidebar.classList.remove("open");
        if (mobileOverlay) mobileOverlay.classList.remove("open");
    }

    function openMobileMenu() {
        if (mobileSidebar) mobileSidebar.classList.add("open");
        if (mobileOverlay) mobileOverlay.classList.add("open");
    }

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener("click", openMobileMenu);
    }
    if (mobileCloseBtn) {
        mobileCloseBtn.addEventListener("click", closeMobileMenu);
    }
    if (mobileOverlay) {
        mobileOverlay.addEventListener("click", closeMobileMenu);
    }
    mobileLinks.forEach(link => {
        link.addEventListener("click", closeMobileMenu);
    });
});
