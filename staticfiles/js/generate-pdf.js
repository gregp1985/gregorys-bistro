document.addEventListener('DOMContentLoaded', () => {
    const { jsPDF } = window.jspdf;

    const downloadBtn = document.getElementById('downloadPdf');

    downloadBtn.addEventListener('click', () => {
        const doc = new jsPDF({ unit: 'pt', format: 'a4' });

        const pageWidth = doc.internal.pageSize.getWidth();
        const pageHeight = doc.internal.pageSize.getHeight();

        // Page Background
        const drawBackground = () => {
            doc.setFillColor(179, 141, 60); 
            doc.rect(0, 0, pageWidth, pageHeight, 'F');
        };

        // Page Border
        const drawPageBorder = () => {
            const inset = 20; // distance from page edge

            doc.setDrawColor(90, 62, 43);
            doc.setLineWidth(1.2);

            doc.roundedRect(
                inset,
                inset,
                pageWidth - inset * 2,
                pageHeight - inset * 2,
                8,
                8
            );
        };

        drawBackground();
        drawPageBorder();

        const contentWidth = 360;
        const contentX = (pageWidth - contentWidth) / 2;

        let yPos = 60;
        let contentStartY = 60;

        // Draw logo at top
        const logo = new Image();
        logo.src = '../static/images/logo.png';
        logo.onload = () => {
            doc.addImage(logo, 'PNG', pageWidth / 2 - 60, 10, 120, 120); // center top
            contentStartY = 10 + 120 + 30;
            yPos = contentStartY;

            drawMenu();
        };
        logo.onerror = () => drawMenu();

        function drawMenu() {
            // Title
            doc.setFontSize(22);
            doc.setTextColor(150, 60, 0); // warm brown
            doc.text('Menu', pageWidth / 2, yPos, { align: 'center' });

            const titleWidth = doc.getTextWidth('Menu');
            doc.setDrawColor(90, 62, 43);
            doc.setLineWidth(1);
            doc.line(
                pageWidth / 2 - titleWidth / 2,
                yPos + 4,
                pageWidth / 2 + titleWidth / 2,
                yPos + 4
            );

            yPos += 40;

            doc.setFontSize(12);
            doc.setTextColor(150, 60, 0); // warm brown

            const categories = document.querySelectorAll('.menu-category');

            categories.forEach(cat => {
                if (cat.style.display === 'none') return;

                const categoryTitle = cat.querySelector('h2').textContent;
                // Category Title
                doc.setFontSize(18);
                doc.setTextColor(150, 60, 0);
                doc.text(
                    categoryTitle,
                    contentX + contentWidth / 2,
                    yPos,
                    { align: 'center' }
                );

                yPos += 10;

                // Divider Line
                doc.setDrawColor(90, 62, 43);
                doc.setLineWidth(0.6);
                doc.line(
                    contentX,
                    yPos,
                    contentX + contentWidth,
                    yPos
                );

                yPos += 14;

                // Items
                doc.setFontSize(14);
                doc.setTextColor(120, 80, 40);

                const items = cat.querySelectorAll('.menu-item');
                
                items.forEach(item => {
                    const name = item.querySelector('.item-name').textContent;
                    const price = item.querySelector('.item-price').textContent;
 
                    doc.text(name, contentX + contentWidth / 2, yPos, { align:'center'});
                    doc.text(
                        price,
                        contentX + contentWidth,
                        yPos,
                        { align: 'right' }
                    );

                    yPos += 18;
                    
                    // Column / page break
                    if (yPos > 750) {
                        doc.addPage();
                        drawBackground();
                        drawPageBorder();
                        yPos = contentStartY;
                    }
                });

                yPos += 24; // space between categories
            });

            doc.save('Gregorys_Bistro_Menu.pdf');
        }
    });
});
