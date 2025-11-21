//---------------------------------------------------------------------
// MODE SOMBRE / CLAIR
//---------------------------------------------------------------------
window.toggleDarkMode = () => {
    const body = document.body;
    body.classList.toggle("dark-mode");

    const mode = body.classList.contains("dark-mode") ? "dark" : "light";
    localStorage.setItem("theme", mode);
};

window.initTheme = () => {
    const saved = localStorage.getItem("theme");
    if (saved === "dark") {
        document.body.classList.add("dark-mode");
    }
};


//---------------------------------------------------------------------
// GRAPH SIMPLE (line)
//---------------------------------------------------------------------
window.creerGraphique = (canvasId, labels, valeurs, label) => {
    const ctx = document.getElementById(canvasId);

    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: valeurs,
                borderWidth: 2,
                borderColor: getComputedStyle(document.body).getPropertyValue("--chart-primary"),
                backgroundColor: getComputedStyle(document.body).getPropertyValue("--chart-primary-bg"),
                tension: 0.3,
                pointRadius: 3
            }]
        },
        options: {
            responsive: true,
            animation: {
                duration: 800,
                easing: "easeOutQuint"
            }
        }
    });
};


//---------------------------------------------------------------------
// GRAPH COMBINÉ TEMP + HUM
//---------------------------------------------------------------------
window.creerGraphiqueCombine = (canvasId, labels, temp, hum) => {
    const ctx = document.getElementById(canvasId);

    new Chart(ctx, {
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Température (°C)",
                    type: "line",
                    data: temp,
                    borderColor: "rgb(255, 80, 80)",
                    backgroundColor: "rgba(255, 80, 80, 0.25)",
                    tension: 0.3,
                    borderWidth: 2
                },
                {
                    label: "Humidité (%)",
                    type: "line",
                    data: hum,
                    borderColor: "rgb(80, 80, 255)",
                    backgroundColor: "rgba(80, 80, 255, 0.25)",
                    tension: 0.3,
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            animation: {
                duration: 900,
                easing: "easeOutCubic"
            }
        }
    });
};


//---------------------------------------------------------------------
// GRAPH RADAR (VENT DIRECTION)
//---------------------------------------------------------------------
window.creerGraphiqueRadar = (canvasId, labels, valeurs) => {
    const ctx = document.getElementById(canvasId);

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: "Direction du vent",
                data: valeurs,
                borderColor: "rgba(255, 206, 86, 1)",
                backgroundColor: "rgba(255, 206, 86, 0.2)",
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            animation: {
                duration: 1000,
                easing: "easeOutCubic"
            }
        }
    });
};


//---------------------------------------------------------------------
// EXPORT PDF
//---------------------------------------------------------------------
window.exportPDF = async () => {
    const { jsPDF } = window.jspdf;

    const pdf = new jsPDF("p", "mm", "a4");

    const charts = document.querySelectorAll("canvas");
    let y = 10;

    for (let canvas of charts) {
        const img = canvas.toDataURL("image/png");

        pdf.addImage(img, "PNG", 10, y, 180, 90);
        y += 95;

        if (y > 260) {
            pdf.addPage();
            y = 10;
        }
    }

    pdf.save("dashboard_meteo.pdf");
};

//---------------------------------------------------------------------
// PIE CHART (ticket résolus / non résolus)
//---------------------------------------------------------------------
window.renderPie = (resolus, nonRes) => {
    const canvas = document.getElementById('chartRes');

    if (!canvas) {
        console.error("Canvas 'chartRes' non trouvé dans le DOM.");
        return;
    }

    // OBLIGATOIRE POUR CHART.JS 4
    Chart.register(
        Chart.ArcElement,
        Chart.Legend,
        Chart.Tooltip
    );

    new Chart(canvas, {
        type: 'pie',
        data: {
            labels: ['Résolus', 'Non résolus'],
            datasets: [{
                data: [resolus, nonRes],
                backgroundColor: ['#28a745', '#dc3545'],
                hoverOffset: 4
            }]
        }
    });
};

