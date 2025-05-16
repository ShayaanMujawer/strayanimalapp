document.addEventListener("DOMContentLoaded", function () {
    fetchReports();
    
    document.getElementById("submitReport").addEventListener("click", submitReport);
    document.getElementById("refreshReports").addEventListener("click", fetchReports);
});

function fetchReports() {
    fetch('/reports')
    .then(response => response.json())
    .then(data => {
        if (!Array.isArray(data)) {
            console.error("Unexpected response:", data);
            return;
        }
        const reportsContainer = document.getElementById("reportsContainer");
        reportsContainer.innerHTML = ""; // Clear previous reports
        data.forEach(report => {
            const reportDiv = document.createElement("div");
            reportDiv.className = "report-box"; // Add class for styling
            reportDiv.innerHTML = `
                <p>Description: ${report.description}</p>
                <p>Location: ${report.location}</p>
                ${report.image ? `<img src="${report.image}" alt="Report Image" style="max-width: 100%;">` : ''}
            `;
            reportsContainer.appendChild(reportDiv);
        });
    })
    .catch(error => console.error("Error fetching reports:", error));
}

function submitReport() {
    const description = document.getElementById("description").value;
    const location = document.getElementById("location").value;
    const formData = new FormData();
    formData.append("image", document.getElementById("image").files[0]); // Append the image file
    formData.append("description", description);
    formData.append("location", location);
    
    fetch("/submit", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(() => fetchReports())
    .catch(error => console.error("Error submitting report:", error));
}

function updateReport(id) {
    fetch(`/update_report/${id}`, {
        method: "POST",
        body: new FormData()
    })
    .then(response => response.json())
    .then(() => fetchReports())
    .catch(error => console.error("Error updating report:", error));
}

function deleteReport(id) {
    fetch(`/delete_report/${id}`, {
        method: "DELETE"
    })
    .then(response => response.json())
    .then(() => fetchReports())
    .catch(error => console.error("Error deleting report:", error));
}
