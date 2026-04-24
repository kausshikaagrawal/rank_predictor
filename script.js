document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictor-form');
    const resultsSection = document.getElementById('results-section');
    const rankRangeDisplay = document.getElementById('predicted-rank-range');
    const campusesWrapper = document.getElementById('campuses-wrapper');
    const predictBtn = form.querySelector('.btn-predict');

    let predictorData = null;

    // Fetch cutoff data from JSON
    fetch('data.json')
        .then(response => response.json())
        .then(data => {
            predictorData = data;
        })
        .catch(error => {
            console.error('Error loading data:', error);
            campusesWrapper.innerHTML = '<p class="no-branches">Error loading historical data. Please check data.json.</p>';
        });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!predictorData) {
            alert("Cutoff data is still loading or failed to load.");
            return;
        }

        const userName = document.getElementById('user-name').value;
        const userEmail = document.getElementById('user-email').value;
        const metScore = parseFloat(document.getElementById('met-score').value);
        let boardPercentage = parseFloat(document.getElementById('board-percentage').value);
        
        if (isNaN(boardPercentage)) {
            // Default assumption if not provided
            boardPercentage = 85.0; 
        }

        // UI Loading state
        predictBtn.textContent = 'Predicting with AI...';
        predictBtn.disabled = true;

        try {
            // Call the ML API endpoint
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: userName,
                    email: userEmail,
                    met_score: metScore,
                    board_percentage: boardPercentage
                })
            });

            if (!response.ok) {
                throw new Error('API request failed');
            }

            const result = await response.json();
            
            if (result.error) {
                throw new Error(result.error);
            }

            const predictedRank = result.predicted_rank;

            // Display Rank
            rankRangeDisplay.textContent = `~${predictedRank.toLocaleString()}`;
            
            // Render eligible branches based on the precise numeric rank
            renderEligibleBranches(predictedRank, predictorData.cutoffs);
            
            // Show results
            resultsSection.classList.remove('hidden');
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

        } catch (error) {
            console.error('Prediction error:', error);
            alert("Error running the prediction model. Is the API running?");
        } finally {
            predictBtn.textContent = 'Predict My Rank & Branches';
            predictBtn.disabled = false;
        }
    });

    function renderEligibleBranches(numericRank, campuses) {
        campusesWrapper.innerHTML = ''; // Clear previous results

        campuses.forEach(campusData => {
            const campusDiv = document.createElement('div');
            campusDiv.classList.add('campus-group');

            const title = document.createElement('h4');
            title.classList.add('campus-title');
            title.textContent = campusData.campus;
            campusDiv.appendChild(title);

            // Filter branches where the student's rank is LESS THAN OR EQUAL TO the closing rank
            const eligibleBranches = campusData.branches.filter(b => numericRank <= b.closing_rank);

            if (eligibleBranches.length > 0) {
                const ul = document.createElement('ul');
                ul.classList.add('branch-list');
                
                eligibleBranches.forEach(branch => {
                    const li = document.createElement('li');
                    li.classList.add('branch-item');
                    li.innerHTML = `
                        <span class="branch-name">${branch.name}</span>
                        <span class="branch-cutoff">Closing Rank: ~${branch.closing_rank.toLocaleString()}</span>
                    `;
                    ul.appendChild(li);
                });
                
                campusDiv.appendChild(ul);
            } else {
                const noBranchMsg = document.createElement('p');
                noBranchMsg.classList.add('no-branches');
                noBranchMsg.textContent = "No branches likely available based on historical cutoffs.";
                campusDiv.appendChild(noBranchMsg);
            }

            campusesWrapper.appendChild(campusDiv);
        });
    }
});

