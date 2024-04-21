document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const response = await fetch('/upload_resume', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        console.log('Response data:', data); // Add this line to see the response data
        displayResults(data);
    });

    function displayResults(data) {
        const atsScoreDiv = document.getElementById('ats_score');
        const keywordSuggestionsDiv = document.getElementById('keyword_suggestions');
        const percentageCircle = document.querySelector('.circle');
        const percentageText = document.querySelector('.percentage');

        if (data.ats_score !== null) {
            atsScoreDiv.innerHTML = `<h2>ATS Score: ${data.ats_score}</h2>`;
            // Update the percentage circle
            const percentage = Math.round(data.ats_score);
            percentageText.innerText = `${percentage}%`;
            const fillRotation = percentage / 100 * 180;
            const fixRotation = fillRotation * 2;
            percentageCircle.querySelector('.fill').style.transform = `rotate(${fillRotation}deg)`;
            percentageCircle.querySelector('.fill.fix').style.transform = `rotate(${fixRotation}deg)`;
        } else {
            atsScoreDiv.innerHTML = '';
        }
        if (data.keyword_suggestions !== null && data.keyword_suggestions.length > 0) {
            keywordSuggestionsDiv.innerHTML = `<h2>Keyword Suggestions:</h2><ul>${data.keyword_suggestions.map(kw => `<li>${kw}</li>`).join('')}</ul>`;
        } else {
            keywordSuggestionsDiv.innerHTML = '';
        }
    }
});
