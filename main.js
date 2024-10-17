document.addEventListener('DOMContentLoaded', (event) => {
    // Populate filter options
    fetch('/api/filter_options')
        .then(response => response.json())
        .then(data => {
            for (const [key, values] of Object.entries(data)) {
                const select = document.getElementById(key);
                if (select) {
                    values.forEach(value => {
                        const option = document.createElement('option');
                        option.value = value;
                        option.textContent = value;
                        select.appendChild(option);
                    });
                }
            }
        });

    // Handle filter form submission
    document.getElementById('filter-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const searchParams = new URLSearchParams(formData);
        fetchAndRenderData(searchParams);
    });

    // Initial data fetch
    fetchAndRenderData(new URLSearchParams());
});

function fetchAndRenderData(searchParams) {
    fetch('/api/data?${searchParams.toString()}')
        .then(response => response.json())
        .then(data => {
            Plotly.newPlot('intensity-likelihood-chart', data.intensity_likelihood.data, data.intensity_likelihood.layout);
            Plotly.newPlot('relevance-year-chart', data.relevance_year.data, data.relevance_year.layout);
            Plotly.newPlot('topics-chart', data.topics.data, data.topics.layout);
            Plotly.newPlot('region-chart', data.region.data, data.region.layout);
            renderDataTable(data.data_table);
        });
}

function renderDataTable(data) {
    const table = document.createElement('table');
    table.className = 'table table-striped';
    
    // Create table header
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    Object.keys(data[0]).forEach(key => {
        const th = document.createElement('th');
        th.textContent = key;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Create table body
    const tbody = document.createElement('tbody');
    data.forEach(row => {
        const tr = document.createElement('tr');
        Object.values(row).forEach(value => {
            const td = document.createElement('td');
            td.textContent = value;
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
    table.appendChild(tbody);

    // Replace the existing table
    const tableContainer = document.getElementById('data-table');
    tableContainer.innerHTML = '';
    tableContainer.appendChild(table);
}