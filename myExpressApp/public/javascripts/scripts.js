// Detect the current template from the data-template attribute in the body tag
const currentTemplate = document.body.getAttribute("data-template");

// Main function to initialize the appropriate content updates based on the template
function initContentUpdates() {
    switch (currentTemplate) {
        case "home":
            setInterval(updateHomeContent, 5000);
            break;
        case "news":
            setInterval(updateNewsContent, 5000);
            break;
        // Add cases for other templates as needed
        default:
            console.warn("No specific content updates for this template.");
            break;
    }
}

// Home content update function (e.g., updating team data, scores, and box names)
async function updateHomeContent() {
    try {
        const response = await fetch('/api/getAllContent');
        const data = await response.json();

        if (data && data.team1 && data.team2 && data.boxNames) {
            updateTeamContent(data.team1, "team1-name", "team1-score", "team1-text-area");
            updateTeamContent(data.team2, "team2-name", "team2-score", "team2-text-area");

            updateBoxName(data.boxNames[0], "box1");
            updateBoxName(data.boxNames[1], "box2");
            updateBoxName(data.boxNames[2], "box3");
            updateBoxName(data.boxNames[3], "box4");
        }
    } catch (error) {
        console.error("Error fetching home content:", error);
    }
}

// News content update function (e.g., updating side-text and news areas)
async function updateNewsContent() {
    try {
        const response = await fetch('/api/getNewsContent');
        const data = await response.json();

        if (data && data.leftText && data.news && data.rightText) {
            updateSideText(data.leftText, "side-text-left");
            updateNewsArea(data.news);
            updateSideText(data.rightText, "side-text-right");
        }
    } catch (error) {
        console.error("Error fetching news content:", error);
    }
}

// Function to update team content (used in Home template)
function updateTeamContent(teamData, nameId, scoreId, textAreaId) {
    document.getElementById(nameId).textContent = teamData.name;
    document.getElementById(scoreId).textContent = teamData.score;
    document.getElementById(textAreaId).textContent = teamData.textArea;
}

// Function to update selectable box names (used in Home template)
function updateBoxName(boxName, boxId) {
    document.getElementById(boxId).textContent = boxName;
}

// Function to update side-text content (used in News template)
function updateSideText(content, elementId) {
    document.getElementById(elementId).innerHTML = content;
}

// Function to update news area content (used in News template)
function updateNewsArea(content) {
    document.getElementById("news-area").innerHTML = content;
}

// Initialize content updates when the page loads
document.addEventListener("DOMContentLoaded", initContentUpdates);

function toggleTeams() {
    const afcTeams = document.getElementById("afc-teams");
    const nfcTeams = document.getElementById("nfc-teams");
    const toggleButton = document.getElementById("toggle-button");

    if (afcTeams.style.display === "none") {
        afcTeams.style.display = "block";
        nfcTeams.style.display = "none";
        toggleButton.innerText = "AFC";
    } else {
        afcTeams.style.display = "none";
        nfcTeams.style.display = "block";
        toggleButton.innerText = "NFC";
    }
}

// update team names
function updateTeamNames(team1Name, team2Name) {
    document.getElementById("team1-name").textContent = team1Name;
    document.getElementById("team2-name").textContent = team2Name;
}

// update team scores
function updateTeamScores(team1Score, team2Score) {
    document.getElementById("team1-score").textContent = team1Score;
    document.getElementById("team2-score").textContent = team2Score;
}

// update text area
function updateTextArea(content) {
    // If you want to update the text inside divs, you can use innerHTML
    document.getElementById("team1-text-area").innerHTML = content;
    document.getElementById("team2-text-area").innerHTML = content;
}

updateTeamNames("Buffalo Bills", "Kansas City Chiefs");
updateTeamScores(34, 21);
updateTextArea("This is a game summary or other adjustable information.");
