document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".filter-btn");
    const categories = document.querySelectorAll(".menu-category");

    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            // Remove active from all buttons
            buttons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            const filter = btn.getAttribute("data-filter");

            categories.forEach(cat => {
                if (filter === "all" || cat.getAttribute("data-category") === filter) {
                    cat.style.display = "block";
                } else {
                    cat.style.display = "none";
                }
            });
        });
    });
});
