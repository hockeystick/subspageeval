// Main application JavaScript

let currentAnalysis = null;
let comparisonData = null;

// Single page analysis
document.getElementById('singleAnalysisForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const publisherName = document.getElementById('publisherName').value;
    const url = document.getElementById('subscriptionUrl').value;
    const language = document.getElementById('languageSelect').value;
    
    await analyzeSinglePage(publisherName, url, language);
});

async function analyzeSinglePage(publisherName, url, language = 'auto') {
    showLoading('Analyzing with Claude AI...');
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                publisher_name: publisherName,
                url: url,
                language: language
            })
        });
        
        if (!response.ok) {
            throw new Error('Analysis failed');
        }
        
        const data = await response.json();
        currentAnalysis = data;
        displaySingleResults(data);
        
    } catch (error) {
        alert('Error analyzing page: ' + error.message);
    } finally {
        hideLoading();
    }
}

function displaySingleResults(data) {
    // Show results section
    document.getElementById('resultsSection').classList.remove('d-none');
    document.getElementById('singleResults').classList.remove('d-none');
    document.getElementById('comparisonResults').classList.add('d-none');
    
    // Update basic info
    document.getElementById('resultPublisherName').textContent = data.publisher_name || 'Unknown Publisher';
    document.getElementById('sophisticationScore').textContent = data.sophistication_score || '0';
    document.getElementById('totalWords').textContent = data.total_words || '0';
    
    // Update language information
    document.getElementById('detectedLanguage').textContent = (data.detected_language || 'en').toUpperCase();
    document.getElementById('languageName').textContent = data.language_name || 'English';
    
    // Update primary strategy
    const strategy = data.primary_strategy || determinePrimaryStrategy(data);
    document.getElementById('primaryStrategy').textContent = formatStrategy(strategy);
    
    // Update charts
    updateMotivationChart(data);
    updateBehavioralChart(data);
    updateEmotionalChart(data);
    
    // Update detailed scores
    updateMotivationScores(data);
    updateBehavioralScores(data);
    updateEmotionalScores(data);
    
    // Update cultural insights
    updateCulturalElements(data);
    updateKeyInsights(data);
    
    // Show screenshot if available
    if (data.screenshot) {
        document.getElementById('pageScreenshot').src = 'data:image/png;base64,' + data.screenshot;
        document.getElementById('screenshotSection').style.display = 'block';
    } else {
        document.getElementById('screenshotSection').style.display = 'none';
    }
}

function determinePrimaryStrategy(data) {
    const motivation = data.motivation_framework || {};
    const supportRatio = motivation.support_ratio || 0;
    const missionDensity = motivation.mission_density || 0;
    const featureDensity = motivation.feature_density || 0;
    
    if (supportRatio > 0.6 && missionDensity > 0.01) {
        return 'Mission-Driven';
    } else if (featureDensity > 0.02) {
        return 'Feature-Focused';
    } else if (supportRatio > 0.4) {
        return 'Hybrid Approach';
    } else {
        return 'Transactional';
    }
}

function updateMotivationChart(data) {
    const ctx = document.getElementById('motivationChart').getContext('2d');
    const motivation = data.motivation_framework?.counts || {};
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(motivation).map(k => k.charAt(0).toUpperCase() + k.slice(1)),
            datasets: [{
                data: Object.values(motivation),
                backgroundColor: [
                    '#0d6efd',
                    '#6610f2',
                    '#6f42c1',
                    '#d63384',
                    '#dc3545',
                    '#fd7e14'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Motivation Framework Distribution'
                }
            }
        }
    });
}

function formatStrategy(strategy) {
    return strategy.replace(/[-_]/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

function updateBehavioralChart(data) {
    const ctx = document.getElementById('behavioralChart').getContext('2d');
    const behavioral = data.behavioral_triggers || {};
    
    const labels = ['Scarcity', 'Social Proof', 'Loss Aversion', 'Reciprocity', 'Authority'];
    const values = [
        (behavioral.scarcity_score || 0) * 100,
        (behavioral.social_proof_score || 0) * 100,
        (behavioral.loss_aversion_score || 0) * 100,
        (behavioral.reciprocity_score || 0) * 100,
        (behavioral.authority_score || 0) * 100
    ];
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Score',
                data: values,
                backgroundColor: '#0d6efd'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 10
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Behavioral Triggers Analysis'
                }
            }
        }
    });
}

function updateEmotionalChart(data) {
    const ctx = document.getElementById('emotionalChart').getContext('2d');
    const emotional = data.emotional_appeals || {};
    
    const labels = ['Fear', 'Hope', 'Belonging', 'Status'];
    const values = [
        (emotional.fear_score || 0) * 100,
        (emotional.hope_score || 0) * 100,
        (emotional.belonging_score || 0) * 100,
        (emotional.status_score || 0) * 100
    ];
    
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Emotional Appeals',
                data: values,
                backgroundColor: 'rgba(220, 53, 69, 0.2)',
                borderColor: '#dc3545',
                pointBackgroundColor: '#dc3545'
            }]
        },
        options: {
            responsive: true,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 10
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Emotional Appeals Analysis'
                }
            }
        }
    });
}

function updateMotivationScores(data) {
    const motivation = data.motivation_framework || {};
    const tbody = document.getElementById('motivationScores');
    tbody.innerHTML = '';
    
    const scores = [
        { name: 'Support Ratio', value: motivation.support_ratio || 0, format: 'ratio' },
        { name: 'Mission Density', value: motivation.mission_density || 0, format: 'density' },
        { name: 'Feature Density', value: motivation.feature_density || 0, format: 'density' },
        { name: 'Identity Score', value: motivation.identity_score || 0, format: 'density' },
        { name: 'Community Score', value: motivation.community_score || 0, format: 'density' }
    ];
    
    scores.forEach(score => {
        const row = tbody.insertRow();
        row.innerHTML = `
            <td>${score.name}</td>
            <td>${formatScore(score.value, score.format)}</td>
        `;
    });
}

function updateBehavioralScores(data) {
    const behavioral = data.behavioral_triggers || {};
    const habit = data.habit_formation || {};
    const tbody = document.getElementById('behavioralScores');
    tbody.innerHTML = '';
    
    const scores = [
        { name: 'Scarcity', value: behavioral.scarcity_score || 0 },
        { name: 'Social Proof', value: behavioral.social_proof_score || 0 },
        { name: 'Loss Aversion', value: behavioral.loss_aversion_score || 0 },
        { name: 'Reciprocity', value: behavioral.reciprocity_score || 0 },
        { name: 'Temporal Anchors', value: habit.temporal_score || 0 },
        { name: 'Convenience', value: habit.convenience_score || 0 }
    ];
    
    scores.forEach(score => {
        const row = tbody.insertRow();
        const badge = getScoreBadge(score.value);
        row.innerHTML = `
            <td>${score.name}</td>
            <td><span class="score-badge ${badge.class}">${badge.text}</span></td>
        `;
    });
}

function formatScore(value, format) {
    if (format === 'ratio') {
        return `${(value * 100).toFixed(1)}%`;
    } else if (format === 'density') {
        return (value * 1000).toFixed(2);
    }
    return value.toFixed(4);
}

function getScoreBadge(value) {
    const normalized = value * 100;
    if (normalized > 5) {
        return { class: 'score-high', text: 'High' };
    } else if (normalized > 2) {
        return { class: 'score-medium', text: 'Medium' };
    } else {
        return { class: 'score-low', text: 'Low' };
    }
}

// Comparison functions
function addComparisonRow() {
    const container = document.getElementById('comparisonInputs');
    const newRow = document.createElement('div');
    newRow.className = 'comparison-row mb-2';
    
    // Get language options from the existing select
    const languageSelect = document.getElementById('defaultLanguageSelect');
    let languageOptions = '<option value="">Use default</option>';
    
    for (let i = 1; i < languageSelect.options.length; i++) {
        const option = languageSelect.options[i];
        languageOptions += `<option value="${option.value}">${option.text}</option>`;
    }
    
    newRow.innerHTML = `
        <div class="row">
            <div class="col-md-3">
                <input type="text" class="form-control publisher-name-compare" 
                       placeholder="Publisher Name">
            </div>
            <div class="col-md-5">
                <input type="url" class="form-control url-compare" 
                       placeholder="https://example.com/subscribe">
            </div>
            <div class="col-md-2">
                <select class="form-select language-compare">
                    ${languageOptions}
                </select>
            </div>
            <div class="col-md-2">
                <button class="btn btn-danger btn-sm remove-row w-100" onclick="removeRow(this)">
                    <i class="bi bi-trash"></i> Remove
                </button>
            </div>
        </div>
    `;
    container.appendChild(newRow);
}

function removeRow(button) {
    const row = button.closest('.comparison-row');
    if (document.querySelectorAll('.comparison-row').length > 1) {
        row.remove();
    }
}

async function comparePublishers() {
    const rows = document.querySelectorAll('.comparison-row');
    const urls = [];
    const defaultLanguage = document.getElementById('defaultLanguageSelect').value;
    
    rows.forEach(row => {
        const name = row.querySelector('.publisher-name-compare').value;
        const url = row.querySelector('.url-compare').value;
        const language = row.querySelector('.language-compare').value || defaultLanguage;
        
        if (name && url) {
            urls.push({ 
                publisher_name: name, 
                url: url,
                language: language
            });
        }
    });
    
    if (urls.length < 2) {
        alert('Please enter at least 2 publishers to compare');
        return;
    }
    
    showLoading('Comparing publishers with Claude AI...');
    
    try {
        const response = await fetch('/compare', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                urls: urls,
                default_language: defaultLanguage
            })
        });
        
        if (!response.ok) {
            throw new Error('Comparison failed');
        }
        
        const data = await response.json();
        comparisonData = data;
        displayComparisonResults(data);
        
    } catch (error) {
        alert('Error comparing publishers: ' + error.message);
    } finally {
        hideLoading();
    }
}

function displayComparisonResults(data) {
    document.getElementById('resultsSection').classList.remove('d-none');
    document.getElementById('singleResults').classList.add('d-none');
    document.getElementById('comparisonResults').classList.remove('d-none');
    
    const content = document.getElementById('comparisonContent');
    content.innerHTML = `
        <div class="row mb-4">
            <div class="col-md-12">
                <h5>Summary Statistics</h5>
                <p>Analyzed ${data.summary_stats.total_publishers} publishers</p>
                <p>Average Sophistication Score: <strong>${data.summary_stats.avg_sophistication}</strong></p>
                <p>Most Sophisticated: <strong>${data.summary_stats.most_sophisticated}</strong></p>
                <p>Most Mission-Driven: <strong>${data.summary_stats.most_mission_driven}</strong></p>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <canvas id="comparisonChart"></canvas>
            </div>
        </div>
    `;
    
    // Create comparison chart
    const ctx = document.getElementById('comparisonChart').getContext('2d');
    const publishers = data.publishers.map(p => p.publisher_name);
    const scores = data.publishers.map(p => p.sophistication_score || 0);
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: publishers,
            datasets: [{
                label: 'Sophistication Score',
                data: scores,
                backgroundColor: '#0d6efd'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 10
                }
            }
        }
    });
}

function updateEmotionalScores(data) {
    const emotional = data.emotional_appeals || {};
    const tbody = document.getElementById('emotionalScores');
    tbody.innerHTML = '';
    
    const scores = [
        { name: 'Fear Appeals', value: emotional.fear_score || 0, format: 'density' },
        { name: 'Hope Appeals', value: emotional.hope_score || 0, format: 'density' },
        { name: 'Belonging Appeals', value: emotional.belonging_score || 0, format: 'density' },
        { name: 'Status Appeals', value: emotional.status_score || 0, format: 'density' }
    ];
    
    scores.forEach(score => {
        const row = tbody.insertRow();
        row.innerHTML = `
            <td>${score.name}</td>
            <td>${formatScore(score.value, score.format)}</td>
        `;
    });
}

function updateCulturalElements(data) {
    const cultural = data.cultural_adaptations || {};
    const container = document.getElementById('culturalElements');
    
    let html = '';
    
    if (cultural.communication_style) {
        html += `<p><strong>Communication Style:</strong> ${cultural.communication_style}</p>`;
    }
    
    if (cultural.cultural_elements && cultural.cultural_elements.length > 0) {
        html += '<p><strong>Cultural Elements:</strong></p><ul>';
        cultural.cultural_elements.forEach(element => {
            html += `<li>${element}</li>`;
        });
        html += '</ul>';
    }
    
    if (cultural.local_references && cultural.local_references.length > 0) {
        html += '<p><strong>Local References:</strong></p><ul>';
        cultural.local_references.forEach(ref => {
            html += `<li>${ref}</li>`;
        });
        html += '</ul>';
    }
    
    if (cultural.trust_building && cultural.trust_building.length > 0) {
        html += '<p><strong>Trust Building:</strong></p><ul>';
        cultural.trust_building.forEach(trust => {
            html += `<li>${trust}</li>`;
        });
        html += '</ul>';
    }
    
    container.innerHTML = html || '<p class="text-muted">No cultural adaptations detected</p>';
}

function updateKeyInsights(data) {
    const insights = data.key_insights || [];
    const container = document.getElementById('keyInsights');
    
    if (insights.length > 0) {
        let html = '<ul>';
        insights.forEach(insight => {
            html += `<li>${insight}</li>`;
        });
        html += '</ul>';
        container.innerHTML = html;
    } else {
        container.innerHTML = '<p class="text-muted">No key insights available</p>';
    }
}

// Updated utility functions
function showLoading(message = 'Loading...') {
    const overlay = document.getElementById('loadingOverlay');
    const loadingText = overlay.querySelector('p');
    if (loadingText) {
        loadingText.textContent = message;
    }
    overlay.classList.remove('d-none');
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.add('d-none');
}

async function exportData(format) {
    window.location.href = `/export/${format}`;
}