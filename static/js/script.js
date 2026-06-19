// API বেস URL
const API_BASE = window.location.origin;

// পেজ লোড হলে চালান
document.addEventListener('DOMContentLoaded', function() {
    loadGuides();
    checkServerStatus();
});

// প্লেয়ার খোঁজার ফাংশন
function searchPlayer() {
    const uid = document.getElementById('playerUid').value.trim();
    
    // ভ্যালিডেশন
    if (!uid) {
        showError('দয়া করে প্লেয়ার ইউআইডি দিন');
        return;
    }
    
    if (!/^\d+$/.test(uid)) {
        showError('ইউআইডি শুধুমাত্র সংখ্যা হতে পারে');
        return;
    }
    
    // লোডিং স্পিনার দেখান
    showLoading(true);
    hideError();
    hidePlayerInfo();
    
    // API কল করুন
    fetch(`${API_BASE}/api/player/${uid}`)
        .then(response => response.json())
        .then(data => {
            showLoading(false);
            
            if (data.success) {
                displayPlayerInfo(data.data);
                showPlayerInfo();
            } else {
                showError(data.error || 'প্লেয়ার খুঁজে পাওয়া যায়নি');
            }
        })
        .catch(error => {
            showLoading(false);
            showError('অনুরোধ প্রক্রিয়াকরণে ত্রুটি: ' + error.message);
            console.error('Error:', error);
        });
}

// প্লেয়ার তথ্য প্রদর্শন
function displayPlayerInfo(data) {
    // বেসিক ইনফো
    document.getElementById('playerName').textContent = data.name || 'অজানা প্লেয়ার';
    document.getElementById('playerUidDisplay').textContent = `ইউআইডি: ${data.uid || 'N/A'}`;
    
    // স্ট্যাটাস
    const statusElement = document.getElementById('playerStatus');
    if (data.status && data.status.toLowerCase() === 'অনলাইন') {
        statusElement.textContent = '🟢 অনলাইন';
        statusElement.className = 'status-badge online';
    } else {
        statusElement.textContent = '⚫ অফলাইন';
        statusElement.className = 'status-badge offline';
    }
    
    // এভাটার
    const avatarElement = document.getElementById('playerAvatar');
    avatarElement.src = data.avatar_url || 'https://via.placeholder.com/150';
    avatarElement.onerror = function() {
        this.src = 'https://via.placeholder.com/150';
    };
    
    // স্ট্যাটস
    document.getElementById('playerLevel').textContent = data.level || 'N/A';
    document.getElementById('playerRank').textContent = data.rank || 'N/A';
    document.getElementById('playerRankPoints').textContent = formatNumber(data.rank_points || 0);
    document.getElementById('playerMatches').textContent = formatNumber(data.matches || 0);
    
    // বিস্তারিত স্ট্যাটস
    document.getElementById('playerWins').textContent = formatNumber(data.wins || 0);
    document.getElementById('playerWinRate').textContent = (data.win_rate || 0).toFixed(2) + '%';
    document.getElementById('playerKills').textContent = formatNumber(data.kills || 0);
    document.getElementById('playerDeaths').textContent = formatNumber(data.deaths || 0);
    document.getElementById('playerKDRatio').textContent = (data.kd_ratio || 0).toFixed(2);
    document.getElementById('playerHeadshots').textContent = formatNumber(data.headshots || 0);
}

// সংখ্যা ফরম্যাটিং ফাংশন
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// গাইড লোড করুন
function loadGuides() {
    fetch(`${API_BASE}/api/guides`)
        .then(response => response.json())
        .then(data => {
            if (data.success && data.data) {
                displayGuides(data.data);
            }
        })
        .catch(error => console.error('Guides load error:', error));
}

// গাইড প্রদর্শন
function displayGuides(guides) {
    const guidesList = document.getElementById('guidesList');
    guidesList.innerHTML = '';
    
    guides.forEach(guide => {
        const guideCard = document.createElement('div');
        guideCard.className = 'guide-card';
        guideCard.innerHTML = `
            <h4>${guide.title}</h4>
            <p>${guide.description}</p>
            <span class="guide-category">${guide.category}</span>
        `;
        guidesList.appendChild(guideCard);
    });
}

// সার্ভার স্ট্যাটাস চেক করুন
function checkServerStatus() {
    fetch(`${API_BASE}/api/status`)
        .then(response => response.json())
        .then(data => {
            const serverStatusBadge = document.getElementById('serverStatus');
            const apiStatusBadge = document.getElementById('apiStatus');
            
            if (serverStatusBadge && data.status === 'চলমান') {
                serverStatusBadge.textContent = '🟢 চলমান';
                serverStatusBadge.className = 'status-badge online';
            }
            
            if (apiStatusBadge) {
                if (data.api_status === 'সংযুক্ত') {
                    apiStatusBadge.textContent = '🟢 সংযুক্ত';
                    apiStatusBadge.className = 'status-badge online';
                } else {
                    apiStatusBadge.textContent = '🟡 ' + data.api_status;
                    apiStatusBadge.className = 'status-badge warning';
                }
            }
        })
        .catch(error => {
            console.error('Status check error:', error);
            const serverStatusBadge = document.getElementById('serverStatus');
            if (serverStatusBadge) {
                serverStatusBadge.textContent = '⚫ অফলাইন';
                serverStatusBadge.className = 'status-badge offline';
            }
        });
}

// UI হেল্পার ফাংশন
function showLoading(show) {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.style.display = show ? 'block' : 'none';
    }
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    if (errorDiv) {
        errorDiv.textContent = '❌ ' + message;
        errorDiv.style.display = 'block';
    }
}

function hideError() {
    const errorDiv = document.getElementById('errorMessage');
    if (errorDiv) {
        errorDiv.style.display = 'none';
    }
}

function showPlayerInfo() {
    const playerInfo = document.getElementById('playerInfo');
    if (playerInfo) {
        playerInfo.style.display = 'block';
        // মসৃণভাবে স্ক্রোল করুন
        playerInfo.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function hidePlayerInfo() {
    const playerInfo = document.getElementById('playerInfo');
    if (playerInfo) {
        playerInfo.style.display = 'none';
    }
}

// এন্টার কী দিয়ে সার্চ করার সুবিধা
document.addEventListener('DOMContentLoaded', function() {
    const playerUidInput = document.getElementById('playerUid');
    if (playerUidInput) {
        playerUidInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                searchPlayer();
            }
        });
    }
});
