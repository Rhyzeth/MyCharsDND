let currentPage = 1;
let totalPages = 1;
let currentPoint = '';

function fetchData() {
    const searchQuery = document.getElementById('search-input').value;

    // Reset the page if search query is different
    if (currentPoint !== searchQuery) {
        currentPoint = searchQuery;
        currentPage = 1; // Reset to first page on new search
    }

    fetch('/get_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            point: currentPoint,
            page: currentPage,
            search: searchQuery
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.results) {
            updateDisplay(data.results);
            totalPages = data.total_pages;
            updatePaginationInfo();
        } else {
            document.getElementById('main-text').innerText = data.error;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('main-text').innerText = 'An error occurred. Please try again.';
    });
}

function sendTableToServer(table_name) {
    fetch('/get_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ table_name: table_name }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.info) {
            displayData(data.info);
        } else {
            document.getElementById('main-text').innerText = data.error;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('main-text').innerText = 'An error occurred. Please try again.';
    });
}

function displayData(data) {
    const mainText = document.getElementById('main-text');
    mainText.innerHTML = ''; // Clear previous content

    const fragment = document.createDocumentFragment(); // Create a fragment for performance

    data.forEach((row, index) => {
        const rowElement = document.createElement('div');
        rowElement.classList.add('data-row');
        rowElement.innerText = `Row ${index + 1}: ${JSON.stringify(row)}`;
        fragment.appendChild(rowElement); // Append to the fragment
    });

    mainText.appendChild(fragment); // Append the fragment to the DOM
}

function updatePaginationInfo() {
    document.getElementById('page-info').textContent = `Page ${currentPage} of ${totalPages}`;
}

function nextPage() {
    if (currentPage < totalPages) {
        currentPage++;
        fetchData().catch(() => {
            currentPage--; // Revert to the previous page if fetch fails
        });
    }
}

function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        fetchData().catch(() => {
            currentPage++; // Revert to the next page if fetch fails
        });
    }
}

function updateMainContent(content) {
    document.getElementById('main-text').innerText = content;
}

function toggleLeftPanel() {
    const panel = document.querySelector('.left-panel');
    panel.classList.toggle('collapsed');
}

function toggleRightPanel() {
    const panel = document.querySelector('.right-panel');
    const isCollapsed = panel.classList.toggle('collapsed');
    
    document.querySelectorAll('.tile-order, .tile-name-input').forEach(input => {
        input.disabled = isCollapsed;
    });

    document.querySelectorAll('.tile-name').forEach(nameElement => {
        const input = nameElement.nextElementSibling;
        nameElement.innerText = isCollapsed ? input.value.charAt(0) : input.value;
    });
}

function reorderTiles() {
    const tiles = Array.from(document.querySelectorAll('#tile-list li'));
    tiles.sort((a, b) => {
        const aOrder = parseInt(a.querySelector('.tile-order').value) || 0; // Default to 0 if invalid
        const bOrder = parseInt(b.querySelector('.tile-order').value) || 0; // Default to 0 if invalid
        return bOrder - aOrder;
    });
    const tileList = document.getElementById('tile-list');
    tiles.forEach(tile => tileList.appendChild(tile));
}

function updateTileName(input) {
    const tileNameSpan = input.previousElementSibling;
    const panel = document.querySelector('.right-panel');
    const isCollapsed = panel.classList.contains('collapsed');

    tileNameSpan.innerText = isCollapsed ? input.value.charAt(0) : input.value;
}
