
const analyzeBtn = document.getElementById("analyzeBtn");

analyzeBtn.addEventListener("click", async function () {

    const filename = document.getElementById("filename").value.trim();
    const code = document.getElementById("code").value.trim();

    // Check user input
    if (filename === "" || code === "") {
        alert("Please enter filename and code!");
        return;
    }

    // Show loading message
    analyzeBtn.innerText = "Analyzing...";
    analyzeBtn.disabled = true;

    let reportSection = document.getElementById("report");

    // Create report section if it doesn't exist
    if (!reportSection) {
        reportSection = document.createElement("div");
        reportSection.id = "report";
        analyzeBtn.parentElement.appendChild(reportSection);
    }

    reportSection.innerHTML = "<h2>Reviewing your code...</h2>";

    try {

        // Send code to FastAPI backend
        const response = await fetch("http://127.0.0.1:8000/review", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                filename: filename,
                code: code
            })

        });

        const data = await response.json();

        // Check for backend errors
        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong!");
        }

        // Display actual AI report
        reportSection.innerHTML = `
            <h2>AI Review Report</h2>
            <p>${data.message}</p>
            <pre id="reportContent"></pre>
        `;

        document.getElementById("reportContent").textContent =
            JSON.stringify(data.report, null, 2);

    }

    catch (error) {

        reportSection.innerHTML = `
            <h2>Review Failed</h2>
            <p>${error.message}</p>
        `;

    }

    finally {

        analyzeBtn.innerText = "Analyze Code";
        analyzeBtn.disabled = false;

    }

});
