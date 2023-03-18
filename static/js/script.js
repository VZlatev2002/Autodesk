function scrapeComments() {
  // Get the link entered by the user
  const linkInput = document.getElementById("link");
  const link = linkInput.value.trim();

  // Send an HTTP request to the server to scrape the comments
  fetch("/scrape", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ link })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.text();
  })
  .then(csvData => {
    const tableContainer = document.getElementById("table-container");

    // Create Tabulator table with parsed data
    const table = new Tabulator(tableContainer, {
      data: csvData,
      layout: "fitColumns",
      responsiveLayout: "collapse",
      tooltips: true,
      addRowPos: "bottom",
      pagination: "local",
      paginationSize: 10,
      movableColumns: true,
      resizableRows: true,
      columns: [
        { title: "ID", field: "ID", width: 50 },
        { title: "User Name", field: "User Name", sorter: "string" },
        { title: "Comment", field: "Comment", sorter: "string" }
      ]
    });

    // Display the table
    tableContainer.style.display = "block";
  })
  .catch(error => {
    console.error("Error: ", error);
  });
}