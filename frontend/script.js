const analyzeBtn = document.getElementById("analyzeBtn");

// Prevent HTML from being interpreted as actual HTML
function escapeHTML(value) {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Convert long AI text into readable paragraphs
function formatParagraphs(value) {

    if (!value) {
        return "<p>None reported.</p>";
    }

    let text = String(value);

    // Remove code blocks from suggestions
    text = text.replace(/```[\s\S]*?```/g, "");

    const paragraphs = text
        .split(/\n+/)
        .map(line => line.trim())
        .filter(line => line.length > 0);

    return paragraphs.map(line => {

        line = escapeHTML(line);

        // Remove Markdown heading symbols
        line = line.replace(/^#{1,6}\s*/, "");

        // Remove bullet and numbering symbols
        line = line.replace(/^[-*]\s*/, "");
        line = line.replace(/^\d+\.\s*/, "");

        // Format bold and italic text
        line = line.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
        line = line.replace(/\*(.*?)\*/g, "<em>$1</em>");

        return `<p>${line}</p>`;

    }).join("");
}

// Create a report section
function createSection(title, content) {

    return `
        <div class="report-card">
            <h3>${title}</h3>
            ${content}
        </div>
    `;
}

// Display bugs and logical errors
function renderFindings(items) {

    if (!Array.isArray(items) || items.length === 0) {
        return "<p>No issues found.</p>";
    }

    return items.map(item => {

        if (typeof item === "string") {
            return `<div class="finding-item">
                ${formatParagraphs(item)}
            </div>`;
        }

        return `
            <div class="finding-item">
                <p><strong>Line:</strong> ${escapeHTML(item.line ?? "Not specified")}</p>
                ${formatParagraphs(item.description ?? "No description available.")}
            </div>
        `;

    }).join("");
}

// Analyze button
analyzeBtn.addEventListener("click", async function () {

    const filename = document.getElementById("filename").value.trim();
    const code = document.getElementById("code").value.trim();

    if (filename === "" || code === "") {
        alert("Please enter filename and code!");
        return;
    }

    analyzeBtn.innerText = "Analyzing...";
    analyzeBtn.disabled = true;

    let reportSection = document.getElementById("report");

    if (!reportSection) {
        reportSection = document.createElement("div");
        reportSection.id = "report";
        analyzeBtn.parentElement.appendChild(reportSection);
    }

    reportSection.innerHTML = "<h2>Reviewing your code...</h2>";

    try {

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

        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong!");
        }

        // Read the actual backend response structure
        const report = data.report;

        const file = report["FILE DETAILS"] || {};
        const overall = report["OVERALL RESULT"] || {};
        const syntax = report["SYNTAX ANALYSIS"] || {};
        const security = report["SECURITY ANALYSIS"] || {};
        const quality = report["CODE QUALITY"] || {};
        const ai = report["AI ANALYSIS"] || {};

        let html = `
            <div class="report-heading">
                <h2>AI Code Review Report</h2>
                <p>${escapeHTML(data.message)}</p>
            </div>
        `;

        // File details
        html += createSection("FILE DETAILS", `
            <p><strong>Filename:</strong> ${escapeHTML(file["Filename"] ?? "Not available")}</p>
            <p><strong>Language:</strong> ${escapeHTML(file["Language"] ?? "Not available")}</p>
        `);

        // Overall result
        html += createSection("OVERALL RESULT", `
            <div class="score-display">
                <span class="score-number">${escapeHTML(overall["Score"] ?? "N/A")}</span>
                <span class="score-rating">${escapeHTML(overall["Rating"] ?? "Not available")}</span>
            </div>
        `);

        // Syntax analysis
        html += createSection("SYNTAX ANALYSIS", `
            <p><strong>Status:</strong> ${escapeHTML(syntax["Status"] ?? "Not checked")}</p>
            ${formatParagraphs(syntax["Message"] ?? "No syntax information available.")}
        `);

        // Security analysis
        html += createSection("SECURITY ANALYSIS", `
            <p><strong>Total Issues:</strong> ${escapeHTML(security["Total Issues"] ?? 0)}</p>
            ${renderFindings(security["Findings"])}
        `);

        // Code quality
        html += createSection("CODE QUALITY", `
            <p><strong>Total Issues:</strong> ${escapeHTML(quality["Total Issues"] ?? 0)}</p>
            ${renderFindings(quality["Findings"])}
        `);

        // AI analysis status
        html += createSection("AI ANALYSIS", `
            <p><strong>Status:</strong> ${escapeHTML(ai["Status"] ?? "Unavailable")}</p>
            <p><strong>Detected Language:</strong> ${escapeHTML(ai["Detected Language"] ?? "Unknown")}</p>
            ${ai["Error Message"] ? formatParagraphs(ai["Error Message"]) : ""}
        `);

        // Bugs
        html += createSection("BUGS DETECTED",
            renderFindings(ai["Bugs"])
        );

        // Logical errors
        html += createSection("LOGICAL ERRORS",
            renderFindings(ai["Logical Errors"])
        );

        // AI security review
        html += createSection("AI SECURITY REVIEW",
            renderFindings(ai["Security Issues"])
        );

        // Code explanation
        html += createSection("CODE EXPLANATION",
            formatParagraphs(ai["Code Explanation"])
        );

        // Suggestions
        html += createSection("SUGGESTIONS",
            formatParagraphs(
                Array.isArray(ai["Suggestions"])
                    ? ai["Suggestions"].join("\n")
                    : ai["Suggestions"]
            )
        );

        // Corrected code
        const correctedCode = ai["Corrected Code"];

        html += createSection("CORRECTED CODE",
            correctedCode
                ? `<pre class="corrected-code"><code>${escapeHTML(correctedCode)}</code></pre>`
                : "<p>No corrected code provided.</p>"
        );

        reportSection.innerHTML = html;

    }

    catch (error) {

        reportSection.innerHTML = `
            <h2>Review Failed</h2>
            <p>${escapeHTML(error.message)}</p>
        `;

    }

    finally {

        analyzeBtn.innerText = "Analyze Code";
        analyzeBtn.disabled = false;

    }

});