document.addEventListener("DOMContentLoaded", () => {
    const { jsPDF } = window.jspdf;

    const downloadBtn = document.getElementById("downloadPdf");

    downloadBtn.addEventListener("click", () => {
        const doc = new jsPDF({ unit: "pt", format: "a4" });

        const pageWidth = doc.internal.pageSize.getWidth();
        const leftMargin = 40;
        const rightMargin = 40;
        const columnGap = 30;
        const columnWidth = (pageWidth - leftMargin - rightMargin - columnGap) / 2;

        const totalMenuWidth = columnWidth * 2 + columnGap;
        const menuStartX = (pageWidth - totalMenuWidth) / 2;

        let yPos = 60;
        let contentStartY = 60; //added
        let currentColumn = 0;

        // Draw logo at top if available
        const logo = new Image();
        logo.src = '../static/images/logo.png'; // Make sure path is correct
        logo.onload = () => {
            doc.addImage(logo, "PNG", pageWidth / 2 - 60, 10, 120, 120); // center top
            contentStartY = 10 + 80 + 30 //added
            yPos+= contentStartY;
            drawMenu();
        };
        logo.onerror = () => drawMenu();

        function drawMenu() {
            // Title
            doc.setFontSize(22);
            doc.setTextColor(150, 60, 0); // warm brown
            doc.text("Menu", pageWidth / 2, yPos, { align: "center" });

            const titleWidth = doc.getTextWidth("Menu");
            doc.setDrawColor(150, 60, 0);
            doc.setLineWidth(1);
            doc.line(
                pageWidth / 2 - titleWidth / 2,
                yPos + 4,
                pageWidth / 2 + titleWidth / 2,
                yPos + 4
            );

            yPos += 30;

            doc.setFontSize(12);
            doc.setTextColor(150, 60, 0); // warm brown

            const categories = document.querySelectorAll(".menu-category");

            categories.forEach(cat => {
                if (cat.style.display === "none") return;

                const categoryTitle = cat.querySelector("h2").textContent;
                doc.setFontSize(18);
                doc.setTextColor(150, 60, 0);
                doc.text(categoryTitle, leftMargin + currentColumn * (columnWidth + columnGap), yPos);
                yPos += 20;
                doc.setFontSize(14);
                doc.setTextColor(150, 60, 0);

                const items = cat.querySelectorAll(".menu-item");
                items.forEach(item => {
                    const name = item.querySelector(".item-name").textContent;
                    const price = item.querySelector(".item-price").textContent;

                    // Fit in column, create dots
                    const line = name + " " + ".".repeat(60 - name.length) + " " + price;
                    doc.text(line, leftMargin + currentColumn * (columnWidth + columnGap), yPos);
                    yPos += 18;

                    if (yPos > 750) {
                        if (currentColumn === 0) {
                            // Move to second column
                            currentColumn = 1;
                            yPos = contentStartY; //changed
                        } else {
                            doc.addPage();
                            currentColumn = 0;
                            yPos = contentStartY; // changed
                        }
                    }
                });

                yPos += 20; // space between categories
            });

            doc.save("Gregorys_Bistro_Menu.pdf");
        }
    });
});
