function sendPointToServer(point) {
    fetch('/get_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ point: point }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('main-text').innerText = data.info;
    })
    .catch(error => console.error('Error:', error));
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
        const aOrder = parseInt(a.querySelector('.tile-order').value);
        const bOrder = parseInt(b.querySelector('.tile-order').value);
        return bOrder - aOrder;
    });
    const tileList = document.getElementById('tile-list');
    tiles.forEach(tile => tileList.appendChild(tile));
}

function updateTileName(input) {
    const tileNameSpan = input.previousElementSibling;
    tileNameSpan.innerText = input.value;
}
