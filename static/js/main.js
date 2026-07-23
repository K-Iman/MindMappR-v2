document.addEventListener("DOMContentLoaded", () => {
    const themeToggle = document.getElementById("themeToggle");
    const themeToggleMobile = document.getElementById("themeToggleMobile");
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

    // Mobile theme toggle (mirrors desktop)
    if (themeToggleMobile) {
        themeToggleMobile.addEventListener("click", () => {
            let theme = document.documentElement.getAttribute("data-theme");
            let newTheme = theme === "dark" ? "light" : "dark";
            document.documentElement.setAttribute("data-theme", newTheme);
            localStorage.setItem("theme", newTheme);
            updateIcon(newTheme);
        });
    }

    function updateIcon(theme) {
        const sunIcon = `<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>`;
        const moonIcon = `<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>`;
        const icon = theme === "dark" ? sunIcon : moonIcon;
        if (themeToggle) themeToggle.innerHTML = icon;
        if (themeToggleMobile) themeToggleMobile.innerHTML = icon;
    }

    // ── Mobile Sidebar Toggle ──────────────────────────────────
    const hamburgerBtn = document.getElementById("hamburgerBtn");
    const mobileSidebar = document.getElementById("mobileSidebar");
    const sidebarOverlay = document.getElementById("sidebarOverlay");

    function openSidebar() {
        hamburgerBtn.classList.add("open");
        hamburgerBtn.setAttribute("aria-expanded", "true");
        mobileSidebar.classList.add("open");
        sidebarOverlay.style.display = "block";
        // Force reflow before adding active so opacity transition fires
        requestAnimationFrame(() => sidebarOverlay.classList.add("active"));
        document.body.style.overflow = "hidden";
    }

    function closeSidebar() {
        hamburgerBtn.classList.remove("open");
        hamburgerBtn.setAttribute("aria-expanded", "false");
        mobileSidebar.classList.remove("open");
        sidebarOverlay.classList.remove("active");
        document.body.style.overflow = "";
        // Hide overlay after transition
        setTimeout(() => { sidebarOverlay.style.display = "none"; }, 300);
    }

    if (hamburgerBtn) {
        hamburgerBtn.addEventListener("click", () => {
            if (mobileSidebar.classList.contains("open")) {
                closeSidebar();
            } else {
                openSidebar();
            }
        });
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener("click", closeSidebar);
    }

    // Close sidebar when any sidebar link is tapped
    if (mobileSidebar) {
        mobileSidebar.querySelectorAll(".sidebar-nav-link").forEach(link => {
            link.addEventListener("click", closeSidebar);
        });
    }
});

