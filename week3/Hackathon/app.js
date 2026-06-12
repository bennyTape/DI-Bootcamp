/* ═══════════════════════════════════════════════════════════
   CinéMatch — Application Logic
   Pure JS, zero dependencies
   ═══════════════════════════════════════════════════════════ */

// ══════════════════════════════════════
// CONSTANTS & DATA
// ══════════════════════════════════════

const GENRES = [
    'Action', 'Comédie', 'Drame', 'Science-Fiction',
    'Horreur', 'Animation', 'Thriller', 'Romance'
];

const GENRE_COLORS = {
    'Action':          '#8dd3c7',
    'Comédie':         '#ffffb3',
    'Drame':           '#bebada',
    'Science-Fiction': '#fb8072',
    'Horreur':         '#80b1d3',
    'Animation':       '#fdb462',
    'Thriller':        '#b3de69',
    'Romance':         '#fccde5'
};

const CATALOG = [
    { id: 1,  title: 'Inception',                genre: 'Science-Fiction', director: 'Christopher Nolan',  avgRating: 4.5 },
    { id: 2,  title: 'The Dark Knight',           genre: 'Action',         director: 'Christopher Nolan',  avgRating: 4.7 },
    { id: 3,  title: 'Parasite',                  genre: 'Thriller',       director: 'Bong Joon-ho',       avgRating: 4.6 },
    { id: 4,  title: 'La La Land',                genre: 'Romance',        director: 'Damien Chazelle',    avgRating: 4.2 },
    { id: 5,  title: 'Get Out',                   genre: 'Horreur',        director: 'Jordan Peele',       avgRating: 4.3 },
    { id: 6,  title: 'Spider-Verse',              genre: 'Animation',      director: 'Peter Ramsey',       avgRating: 4.8 },
    { id: 7,  title: 'Grand Budapest Hotel',      genre: 'Comédie',        director: 'Wes Anderson',       avgRating: 4.1 },
    { id: 8,  title: 'Interstellar',              genre: 'Science-Fiction', director: 'Christopher Nolan',  avgRating: 4.4 },
    { id: 9,  title: 'Whiplash',                  genre: 'Drame',          director: 'Damien Chazelle',    avgRating: 4.5 },
    { id: 10, title: 'Mad Max: Fury Road',        genre: 'Action',         director: 'George Miller',      avgRating: 4.3 },
    { id: 11, title: 'Hereditary',                genre: 'Horreur',        director: 'Ari Aster',          avgRating: 4.0 },
    { id: 12, title: 'Your Name',                 genre: 'Animation',      director: 'Makoto Shinkai',     avgRating: 4.6 },
    { id: 13, title: 'Knives Out',                genre: 'Comédie',        director: 'Rian Johnson',       avgRating: 4.0 },
    { id: 14, title: 'Arrival',                   genre: 'Science-Fiction', director: 'Denis Villeneuve',   avgRating: 4.3 },
    { id: 15, title: 'Moonlight',                 genre: 'Drame',          director: 'Barry Jenkins',      avgRating: 4.4 },
    { id: 16, title: 'Gone Girl',                 genre: 'Thriller',       director: 'David Fincher',      avgRating: 4.2 },
    { id: 17, title: 'Coco',                      genre: 'Animation',      director: 'Lee Unkrich',        avgRating: 4.7 },
    { id: 18, title: 'Eternal Sunshine',          genre: 'Romance',        director: 'Michel Gondry',      avgRating: 4.3 }
];

const LOADING_MESSAGES = [
    'Analyse en cours…',
    'Calcul des préférences…',
    'Recherche de profils similaires…',
    'Application du clustering K-Means…',
    'Génération des recommandations…'
];

// ══════════════════════════════════════
// STATE
// ══════════════════════════════════════

let currentUser = null;
let selectedGenres = new Set();
let allUsers = []; // All users from utilisateurs.json
let vizUserName = null; // Name of the user shown in visualisation.png
let selectedRatings = {}; // filmId -> chosen star rating (pending confirmation)

// ══════════════════════════════════════
// API FUNCTIONS
// ══════════════════════════════════════

async function loadUsersFromAPI() {
    try {
        const response = await fetch('/api/users');
        allUsers = await response.json();
        console.log('Loaded users from API:', allUsers.length);
    } catch (error) {
        console.error('Error loading users:', error);
        allUsers = [];
    }
}

async function saveUserToAPI(user) {
    try {
        // Convert to utilisateurs.json format
        const userJson = {
            name: user.name,
            age: user.age,
            preferences: user.preferredGenres,
            watch_history: user.history.map(h => {
                let dateStr = '';
                if (h.date) {
                    if (h.date instanceof Date) {
                        dateStr = h.date.toISOString().split('T')[0];
                    } else {
                        dateStr = String(h.date).split('T')[0];
                    }
                } else {
                    dateStr = new Date().toISOString().split('T')[0];
                }
                return {
                    movie: h.film.title,
                    genre: h.film.genre,
                    director: h.film.director,
                    rating: h.rating,
                    date: dateStr
                };
            })
        };

        // Check if user already exists
        const existingIndex = allUsers.findIndex(u => (u.name || `Utilisateur ${u.id}`).toLowerCase() === user.name.toLowerCase());
        if (existingIndex !== -1) {
            // Update existing user
            const response = await fetch(`/api/users/${user.name}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userJson)
            });
            allUsers[existingIndex] = userJson;
        } else {
            // Create new user
            const response = await fetch('/api/users', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userJson)
            });
            allUsers.push(userJson);
        }
        console.log('User saved to API:', user.name);
    } catch (error) {
        console.error('Error saving user:', error);
    }
}

// ══════════════════════════════════════
// MATPLOTLIB VISUALISATION
// ══════════════════════════════════════

/**
 * Calls the server to regenerate visualisation.png via Python/Matplotlib,
 * then refreshes the <img> on the page (original file, no copy).
 */
async function generateMatplotlibViz(userName) {
    const container  = document.getElementById('matplotlib-container');
    const loading    = document.getElementById('matplotlib-loading');
    const imgWrap    = document.getElementById('matplotlib-img-wrap');
    const img        = document.getElementById('matplotlib-img');
    const subtitle   = document.getElementById('matplotlib-subtitle');

    // Show section & spinner
    container.classList.remove('hidden');
    loading.classList.remove('hidden');
    imgWrap.style.opacity = '0.3';

    try {
        const response = await fetch('/api/generate-viz', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: userName })
        });

        if (response.ok) {
            // Cache-bust so browser always reloads the file
            const ts = Date.now();
            img.src = `/visualisation.png?t=${ts}`;
            img.onload = () => {
                imgWrap.style.opacity = '1';
                loading.classList.add('hidden');
            };
            img.onerror = () => {
                loading.classList.add('hidden');
                imgWrap.style.opacity = '1';
            };
            subtitle.textContent = `Historique de visionnage \u2014 ${userName}`;
            vizUserName = userName;

            // Scroll into view
            container.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
            const err = await response.json();
            console.error('Viz generation error:', err);
            loading.classList.add('hidden');
            imgWrap.style.opacity = '1';
        }
    } catch (error) {
        console.error('Failed to generate visualization:', error);
        loading.classList.add('hidden');
        imgWrap.style.opacity = '1';
    }
}

// ══════════════════════════════════════
// UTILITY FUNCTIONS
// ══════════════════════════════════════

/** Box-Muller transform for normal distribution */
function normalRandom(mean, stddev) {
    let u1 = Math.random();
    let u2 = Math.random();
    // Avoid log(0)
    while (u1 === 0) u1 = Math.random();
    const z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
    return mean + z * stddev;
}

function clamp(val, min, max) {
    return Math.min(max, Math.max(min, val));
}

function shuffle(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

function roundTo(val, decimals) {
    const f = Math.pow(10, decimals);
    return Math.round(val * f) / f;
}

/** Format date as DD/MM */
function formatDate(d) {
    return `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}`;
}

// ══════════════════════════════════════
// DATA GENERATION
// ══════════════════════════════════════

/**
 * Generate a simulated watch history for a user.
 * - 5 to 7 films from the catalog
 * - Ratings follow N(4, 0.7) for preferred genres, N(2.5, 0.8) for others
 * - ~25% missing (null), ~20% outlier (outside 1-5)
 * - Dates spread over 30 days
 */
function generateWatchHistory(preferredGenres) {
    const count = 5 + Math.floor(Math.random() * 3); // 5, 6, or 7
    const films = shuffle(CATALOG).slice(0, count);
    const now = new Date();

    // Generate base ratings
    const history = films.map(film => {
        const isPreferred = preferredGenres.includes(film.genre);
        const mean = isPreferred ? 4 : 2.5;
        const stddev = isPreferred ? 0.7 : 0.8;
        let rating = roundTo(normalRandom(mean, stddev), 1);
        rating = clamp(rating, 1, 5); // Valid rating

        // Random date in last 30 days
        const daysAgo = Math.floor(Math.random() * 30);
        const date = new Date(now);
        date.setDate(date.getDate() - daysAgo);
        date.setHours(Math.floor(Math.random() * 14) + 8); // 8am-10pm

        return {
            film,
            rating,
            date,
            isMissing: false,
            isOutlier: false
        };
    });

    // Shuffle indices for injection
    const indices = shuffle([...Array(count).keys()]);

    // Inject ~25% missing values
    const missingCount = Math.max(1, Math.round(count * 0.25));
    for (let i = 0; i < missingCount; i++) {
        history[indices[i]].rating = null;
        history[indices[i]].isMissing = true;
    }

    // Inject ~20% outliers (on non-missing entries)
    const outlierCount = Math.max(1, Math.round(count * 0.2));
    let injected = 0;
    for (let i = missingCount; i < indices.length && injected < outlierCount; i++) {
        const idx = indices[i];
        // Generate outlier outside [1, 5]
        if (Math.random() > 0.5) {
            history[idx].rating = roundTo(5 + Math.random() * 3 + 0.5, 1); // 5.5 – 8.5
        } else {
            history[idx].rating = roundTo(-Math.random() * 2, 1); // -2.0 – 0.0
        }
        history[idx].isOutlier = true;
        injected++;
    }

    // Sort by date
    history.sort((a, b) => a.date - b.date);
    return history;
}

/** Generate a comparison user with random preferences */
function generateComparisonUser(id) {
    const numPreferred = 2 + Math.floor(Math.random() * 3); // 2–4
    const preferredGenres = shuffle([...GENRES]).slice(0, numPreferred);
    const history = generateWatchHistory(preferredGenres);
    return {
        id,
        name: `Utilisateur ${id}`,
        preferredGenres,
        history
    };
}

// ══════════════════════════════════════
// ALGORITHMS
// ══════════════════════════════════════

/** Build a genre→average-rating vector from a user's history (only valid ratings) */
function getGenreRatingVector(history) {
    const buckets = {};
    GENRES.forEach(g => buckets[g] = []);

    history.forEach(entry => {
        if (entry.rating !== null && !entry.isOutlier) {
            buckets[entry.film.genre].push(entry.rating);
        }
    });

    return GENRES.map(g => {
        const vals = buckets[g];
        if (vals.length === 0) return 0;
        return vals.reduce((a, b) => a + b, 0) / vals.length;
    });
}

/** Pearson correlation coefficient between two equal-length vectors */
function pearsonCorrelation(x, y) {
    const n = x.length;
    if (n === 0) return 0;

    const meanX = x.reduce((a, b) => a + b, 0) / n;
    const meanY = y.reduce((a, b) => a + b, 0) / n;

    let num = 0, denX = 0, denY = 0;
    for (let i = 0; i < n; i++) {
        const dx = x[i] - meanX;
        const dy = y[i] - meanY;
        num += dx * dy;
        denX += dx * dx;
        denY += dy * dy;
    }

    const den = Math.sqrt(denX * denY);
    return den === 0 ? 0 : num / den;
}

/** Simple K-Means clustering */
function kMeans(vectors, k, maxIter = 30) {
    const n = vectors.length;
    const dims = vectors[0].length;

    // Init centroids from random data points
    let centroids = shuffle([...Array(n).keys()])
        .slice(0, Math.min(k, n))
        .map(i => [...vectors[i]]);

    let assignments = new Array(n).fill(0);

    for (let iter = 0; iter < maxIter; iter++) {
        // Assign each point to nearest centroid
        const newAssignments = vectors.map(v => {
            let minDist = Infinity, minIdx = 0;
            centroids.forEach((c, ci) => {
                const dist = v.reduce((sum, val, d) => sum + (val - c[d]) ** 2, 0);
                if (dist < minDist) { minDist = dist; minIdx = ci; }
            });
            return minIdx;
        });

        // Check convergence
        if (newAssignments.every((a, i) => a === assignments[i])) break;
        assignments = newAssignments;

        // Recompute centroids
        centroids = centroids.map((_, ci) => {
            const members = vectors.filter((_, i) => assignments[i] === ci);
            if (members.length === 0) return centroids[ci];
            return Array(dims).fill(0).map((_, d) =>
                members.reduce((sum, v) => sum + v[d], 0) / members.length
            );
        });
    }

    return assignments;
}

// ══════════════════════════════════════
// RECOMMENDATION ENGINES
// ══════════════════════════════════════

function recommendByPreferences(user) {
    const watchedIds = new Set(user.history.map(h => h.film.id));
    return CATALOG
        .filter(f => !watchedIds.has(f.id) && user.preferredGenres.includes(f.genre))
        .sort((a, b) => b.avgRating - a.avgRating);
}

function recommendBySimilarity(user, compUsers) {
    const userVec = getGenreRatingVector(user.history);
    let bestCorr = -Infinity, bestUser = null;

    compUsers.forEach(cu => {
        const cuVec = getGenreRatingVector(cu.history);
        const corr = pearsonCorrelation(userVec, cuVec);
        if (corr > bestCorr) { bestCorr = corr; bestUser = cu; }
    });

    if (!bestUser) return { user: null, correlation: 0, films: [] };

    const watchedIds = new Set(user.history.map(h => h.film.id));
    const goodFilms = bestUser.history
        .filter(h => h.rating !== null && !h.isOutlier && h.rating >= 3.5 && !watchedIds.has(h.film.id))
        .map(h => h.film);

    return { user: bestUser, correlation: bestCorr, films: goodFilms };
}

function recommendByCluster(user, compUsers) {
    const allUsers = [user, ...compUsers];
    const vectors = allUsers.map(u => getGenreRatingVector(u.history));
    const assignments = kMeans(vectors, 3);

    const userCluster = assignments[0];
    const clusterMembers = allUsers.filter((_, i) => i !== 0 && assignments[i] === userCluster);
    const watchedIds = new Set(user.history.map(h => h.film.id));

    const filmScores = {};
    clusterMembers.forEach(member => {
        member.history.forEach(h => {
            if (h.rating !== null && !h.isOutlier && h.rating >= 3.5 && !watchedIds.has(h.film.id)) {
                if (!filmScores[h.film.id]) {
                    filmScores[h.film.id] = { film: h.film, total: 0, count: 0 };
                }
                filmScores[h.film.id].total += h.rating;
                filmScores[h.film.id].count++;
            }
        });
    });

    const films = Object.values(filmScores)
        .sort((a, b) => (b.total / b.count) - (a.total / a.count))
        .map(f => f.film);

    return { clusterSize: clusterMembers.length, films };
}

// ══════════════════════════════════════
// RENDERING HELPERS
// ══════════════════════════════════════

function renderStars(rating) {
    if (rating === null) {
        return '<span class="rating-missing">—</span>';
    }
    const isOutlier = rating < 1 || rating > 5;
    if (isOutlier) {
        return `<span class="rating-outlier">${rating.toFixed(1)} ⚠</span>`;
    }
    let html = '<span class="stars">';
    for (let i = 1; i <= 5; i++) {
        if (i <= Math.floor(rating)) {
            html += '<span class="star filled">★</span>';
        } else if (i - 0.5 <= rating) {
            html += '<span class="star half">★</span>';
        } else {
            html += '<span class="star empty">☆</span>';
        }
    }
    html += ` <span class="rating-value">${rating.toFixed(1)}</span></span>`;
    return html;
}

function renderGenreBadge(genre) {
    const color = GENRE_COLORS[genre] || '#888';
    return `<span class="genre-badge" style="--badge-color: ${color}">${genre}</span>`;
}

function renderFilmCard(film, rating, options = {}) {
    const { showAvg = false, isOutlier = false, isMissing = false } = options;
    const displayRating = showAvg ? film.avgRating : rating;
    const extraClass = isOutlier ? ' outlier-card' : isMissing ? ' missing-card' : '';

    return `
        <div class="film-card${extraClass}">
            ${renderGenreBadge(film.genre)}
            <div class="film-info">
                <span class="film-title">${film.title}</span>
                <span class="film-director">${film.director}</span>
            </div>
            <div class="film-rating">${renderStars(displayRating)}</div>
        </div>
    `;
}

// ══════════════════════════════════════
// DONUT CHART (SVG)
// ══════════════════════════════════════

function renderDonutChart(history) {
    // Count genres (only valid genres)
    const genreCounts = {};
    history.forEach(h => {
        if (h.film.genre && GENRES.includes(h.film.genre)) {
            genreCounts[h.film.genre] = (genreCounts[h.film.genre] || 0) + 1;
        }
    });

    const total = Object.values(genreCounts).reduce((a, b) => a + b, 0);
    
    if (total === 0) {
        document.getElementById('donut-chart').innerHTML = '<p class="no-data">Aucun genre valide</p>';
        return;
    }

    const cx = 100, cy = 100, r = 72;
    const circumference = 2 * Math.PI * r; // ~452.39

    let segments = '';
    let cumulativeOffset = 0;
    let startAngle = 140; // matplotlib startangle=140

    Object.entries(genreCounts).forEach(([genre, count], idx) => {
        const percentage = count / total;
        const segmentLength = percentage * circumference;
        const color = GENRE_COLORS[genre] || '#888';
        const percentageText = Math.round(percentage * 100) + '%';

        segments += `
            <circle
                cx="${cx}" cy="${cy}" r="${r}"
                fill="none"
                stroke="${color}"
                stroke-width="28"
                stroke-dasharray="0 ${circumference}"
                data-target-dash="${segmentLength} ${circumference - segmentLength}"
                stroke-dashoffset="${-cumulativeOffset}"
                transform="rotate(-${startAngle} ${cx} ${cy})"
                class="donut-segment"
                data-delay="${idx * 150}"
                stroke-linecap="butt"
            />
        `;
        cumulativeOffset += segmentLength;
    });

    const svg = `
        <div class="donut-wrapper">
            <svg viewBox="0 0 200 200" class="donut-svg">
                ${segments}
                <text x="${cx}" y="${cy - 6}" text-anchor="middle" class="donut-total">${total}</text>
                <text x="${cx}" y="${cy + 16}" text-anchor="middle" class="donut-label">films</text>
            </svg>
            <div class="donut-legend">
                ${Object.entries(genreCounts).map(([genre, count]) => {
                    const percentage = Math.round((count / total) * 100);
                    return `
                    <div class="legend-item">
                        <span class="legend-dot" style="background: ${GENRE_COLORS[genre] || '#888'}"></span>
                        <span class="legend-label">${genre}</span>
                        <span class="legend-count">${percentage}%</span>
                    </div>
                `}).join('')}
            </div>
        </div>
    `;

    document.getElementById('donut-chart').innerHTML = svg;

    // Animate segments in
    requestAnimationFrame(() => {
        document.querySelectorAll('.donut-segment').forEach(el => {
            const delay = parseInt(el.getAttribute('data-delay'), 10);
            const targetDash = el.getAttribute('data-target-dash');
            setTimeout(() => {
                el.style.strokeDasharray = targetDash;
            }, delay + 50);
        });
    });
}

// ══════════════════════════════════════
// LINE CHART (SVG)
// ══════════════════════════════════════

function renderLineChart(history) {
    const sorted = [...history].sort((a, b) => a.date - b.date);

    const width = 460, height = 260;
    const pad = { top: 24, right: 24, bottom: 48, left: 38 };
    const chartW = width - pad.left - pad.right;
    const chartH = height - pad.top - pad.bottom;

    const dates = sorted.map(h => h.date.getTime());
    const minDate = Math.min(...dates);
    const maxDate = Math.max(...dates);
    const dateRange = maxDate - minDate || 1;

    const xScale = t => pad.left + ((t - minDate) / dateRange) * chartW;
    const yScale = r => pad.top + chartH - ((r - 0) / 5.5) * chartH;

    let svg = `<svg viewBox="0 0 ${width} ${height}" class="line-svg">`;

    // Y-axis grid & labels (0–5.5 to match matplotlib)
    for (let i = 0; i <= 5; i++) {
        const y = yScale(i);
        svg += `<line x1="${pad.left}" y1="${y}" x2="${width - pad.right}" y2="${y}" class="grid-line" style="opacity: 0.3"/>`;
        svg += `<text x="${pad.left - 8}" y="${y + 4}" text-anchor="end" class="axis-label">${i}</text>`;
    }

    // Separate valid and invalid points
    const validPoints = sorted.filter(h => h.rating !== null && !h.isOutlier);
    const invalidPoints = sorted.filter(h => h.isMissing || h.isOutlier);

    // Draw line connecting valid points with matplotlib color #4C72B0
    if (validPoints.length > 1) {
        const pts = validPoints.map(h => `${xScale(h.date.getTime())},${yScale(h.rating)}`).join(' ');
        svg += `<polyline points="${pts}" class="data-line" style="stroke: #4C72B0; stroke-width: 2; fill: none;"/>`;
    }

    // Draw valid data points with matplotlib style
    validPoints.forEach(h => {
        const x = xScale(h.date.getTime());
        const y = yScale(h.rating);
        svg += `<circle cx="${x}" cy="${y}" r="7" class="data-point" style="fill: #4C72B0;"
                    data-title="${h.film.title}" data-rating="${h.rating.toFixed(1)}" data-date="${formatDate(h.date)}"/>`;
    });

    // Add annotations for movie titles (matplotlib style: rotation=15, fontsize=7)
    validPoints.forEach(h => {
        const x = xScale(h.date.getTime());
        const y = yScale(h.rating);
        svg += `<text x="${x}" y="${y - 12}" text-anchor="middle" class="annotation" style="font-size: 7px; fill: #333;">${h.film.title}</text>`;
    });

    // Draw invalid markers (✕ on x-axis)
    invalidPoints.forEach(h => {
        const x = xScale(h.date.getTime());
        const y = pad.top + chartH + 18;
        svg += `<text x="${x}" y="${y}" text-anchor="middle" class="invalid-marker">✕</text>`;
    });

    // X-axis date labels (spread a few, rotated 30 degrees like matplotlib)
    const labelIndices = [0];
    if (sorted.length > 2) labelIndices.push(Math.floor(sorted.length / 2));
    if (sorted.length > 1) labelIndices.push(sorted.length - 1);
    const seen = new Set();
    labelIndices.forEach(i => {
        const h = sorted[i];
        const x = xScale(h.date.getTime());
        const label = formatDate(h.date);
        if (!seen.has(label)) {
            svg += `<text x="${x}" y="${height - 6}" text-anchor="middle" class="axis-label" transform="rotate(30, ${x}, ${height - 6})">${label}</text>`;
            seen.add(label);
        }
    });

    svg += '</svg>';

    // Tooltip element
    svg += '<div id="line-tooltip" class="chart-tooltip hidden"></div>';

    const container = document.getElementById('line-chart');
    container.innerHTML = svg;

    // Interactive point click handlers
    container.querySelectorAll('.data-point').forEach(point => {
        point.addEventListener('click', function () {
            const svgEl = this.closest('svg');
            const rect = svgEl.getBoundingClientRect();
            const vbWidth = 460, vbHeight = 260;

            const cx = parseFloat(this.getAttribute('cx'));
            const cy = parseFloat(this.getAttribute('cy'));

            const xPx = (cx / vbWidth) * rect.width;
            const yPx = (cy / vbHeight) * rect.height;

            const tooltip = document.getElementById('line-tooltip');
            const title = this.getAttribute('data-title');
            const rating = this.getAttribute('data-rating');
            const date = this.getAttribute('data-date');

            tooltip.textContent = `${title} — ${rating}★ (${date})`;
            tooltip.style.left = xPx + 'px';
            tooltip.style.top = (yPx - 38) + 'px';
            tooltip.classList.remove('hidden');

            clearTimeout(tooltip._hideTimer);
            tooltip._hideTimer = setTimeout(() => tooltip.classList.add('hidden'), 2800);
        });
    });
}

// ══════════════════════════════════════
// UI: GENRE TOGGLES
// ══════════════════════════════════════

function renderGenreToggles() {
    const container = document.getElementById('genre-toggles');
    container.innerHTML = GENRES.map(genre => {
        const color = GENRE_COLORS[genre];
        return `
            <button type="button" class="genre-toggle" data-genre="${genre}" style="--badge-color: ${color}">
                <span class="toggle-dot"></span>
                ${genre}
            </button>
        `;
    }).join('');

    container.addEventListener('click', e => {
        const btn = e.target.closest('.genre-toggle');
        if (!btn) return;
        const genre = btn.dataset.genre;
        if (selectedGenres.has(genre)) {
            selectedGenres.delete(genre);
            btn.classList.remove('active');
        } else {
            selectedGenres.add(genre);
            btn.classList.add('active');
        }
    });
}

// ══════════════════════════════════════
// UI: PROFILE CARD
// ══════════════════════════════════════

function renderProfile(user) {
    const card = document.getElementById('profile-card');
    const initial = user.name.charAt(0).toUpperCase();
    const hasHistory = user.history.length > 0;

    let filmsHTML;
    if (hasHistory) {
        filmsHTML = user.history.map(h =>
            renderFilmCard(h.film, h.rating, { isOutlier: h.isOutlier, isMissing: h.isMissing })
        ).join('');
    } else {
        filmsHTML = '<div class="history-empty">Aucun film visionné — explorez le catalogue ci-dessous !</div>';
    }

    const countLabel = hasHistory
        ? ` (${user.history.length} film${user.history.length > 1 ? 's' : ''})`
        : '';

    card.innerHTML = `
        <div class="profile-header">
            <div class="profile-avatar">${initial}</div>
            <div>
                <div class="profile-name">${user.name}</div>
                <div class="profile-meta">${user.age} ans</div>
                <div class="profile-genres">
                    ${user.preferredGenres.map(g => renderGenreBadge(g)).join('')}
                </div>
            </div>
        </div>
        <div class="profile-section-label">Historique de visionnage${countLabel}</div>
        <div class="film-list">${filmsHTML}</div>
    `;

    card.classList.remove('hidden');

    // Show reco trigger only when history exists
    if (hasHistory) {
        document.getElementById('reco-trigger').classList.remove('hidden');
    } else {
        document.getElementById('reco-trigger').classList.add('hidden');
    }
    document.getElementById('reco-results').classList.add('hidden');
    document.getElementById('loading-indicator').classList.add('hidden');
}

// ══════════════════════════════════════
// UI: CATALOG & WATCH
// ══════════════════════════════════════

function renderCatalog() {
    const section = document.getElementById('catalog-section');
    const grid = document.getElementById('catalog-grid');
    const watchedIds = new Set(currentUser.history.map(h => h.film.id));

    let html = '';
    currentUser.preferredGenres.forEach(genre => {
        // Find films in this genre
        const genreFilms = CATALOG.filter(f => f.genre === genre);
        if (genreFilms.length === 0) return;

        // Sort by average rating descending, then take top 3
        const topFilms = [...genreFilms]
            .sort((a, b) => b.avgRating - a.avgRating)
            .slice(0, 3);

        html += `
            <div class="genre-section">
                <h4 class="genre-section-title" style="color: ${GENRE_COLORS[genre]}">${genre}</h4>
                <div class="catalog-grid">
                    ${topFilms.map(film => {
                        const isWatched = watchedIds.has(film.id);
                        return `
                            <div class="catalog-card${isWatched ? ' watched' : ''}" data-film-id="${film.id}">
                                <div class="catalog-card-top">
                                    ${renderGenreBadge(film.genre)}
                                    <div class="film-info">
                                        <span class="film-title">${film.title}</span>
                                        <span class="film-director">${film.director}</span>
                                    </div>
                                </div>
                                <div class="catalog-card-bottom">
                                    <div class="catalog-avg">
                                        <span class="star filled">★</span> ${film.avgRating.toFixed(1)} moyenne
                                    </div>
                                    <button class="btn-watch${isWatched ? ' watched' : ''}"
                                            onclick="handleWatchFilm(${film.id})"
                                            ${isWatched ? 'disabled' : ''}>
                                        ${isWatched ? '✓ Vu' : '▶ Regarder'}
                                    </button>
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        `;
    });

    grid.innerHTML = html;
    section.classList.remove('hidden');
}

/** Show inline star-rating form when user clicks "Regarder" */
function handleWatchFilm(filmId) {
    if (!currentUser) return;
    if (currentUser.history.some(h => h.film.id === filmId)) return;

    const card = document.querySelector(`[data-film-id="${filmId}"]`);
    if (!card) return;

    const bottom = card.querySelector('.catalog-card-bottom');
    bottom.innerHTML = `
        <div class="rating-form" id="rating-form-${filmId}">
            <div class="star-selector" id="stars-${filmId}">
                ${[1,2,3,4,5].map(i =>
                    `<span class="rate-star" data-value="${i}" onclick="selectStar(${filmId}, ${i})">&#9733;</span>`
                ).join('')}
            </div>
            <div class="rating-note">Votre note sur 5</div>
            <div class="rating-actions">
                <button class="btn-confirm-rating" id="btn-confirm-${filmId}" onclick="submitRating(${filmId})" disabled>
                    ✓ Confirmer
                </button>
                <button class="btn-cancel-rating" onclick="cancelRating(${filmId})">
                    × Annuler
                </button>
            </div>
        </div>
    `;
}

/** Highlight stars up to the selected value */
function selectStar(filmId, value) {
    selectedRatings[filmId] = value;
    const container = document.getElementById(`stars-${filmId}`);
    if (!container) return;
    container.querySelectorAll('.rate-star').forEach((star, i) => {
        if (i < value) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
    const btn = document.getElementById(`btn-confirm-${filmId}`);
    if (btn) btn.disabled = false;
}

/** Confirm the chosen rating and add film to history */
async function submitRating(filmId) {
    const rating = selectedRatings[filmId];
    if (rating === undefined) return;

    const film = CATALOG.find(f => f.id === filmId);
    if (!film) return;

    // Add to history with the user's exact rating (valid, no anomaly)
    currentUser.history.push({
        film,
        rating,        // user's chosen value 1–5
        date: new Date(),
        isMissing: false,
        isOutlier: false
    });
    currentUser.history.sort((a, b) => a.date - b.date);

    delete selectedRatings[filmId];

    // Save & refresh
    await saveUserToAPI(currentUser);
    renderProfile(currentUser);
    renderCatalog();

    // Refresh matplotlib visualisation with new rating data
    generateMatplotlibViz(currentUser.name);

    document.getElementById('profile-card').scrollIntoView({ behavior: 'smooth', block: 'center' });
}

/** Cancel the rating form and restore the Watch button */
function cancelRating(filmId) {
    delete selectedRatings[filmId];
    renderCatalog();
}

// ══════════════════════════════════════
// UI: RECOMMENDATIONS
// ══════════════════════════════════════

function renderRecommendations(prefRecos, simResult, clusterResult, inspiringMsg) {
    const container = document.getElementById('reco-results');

    let html = '';

    // Block 1: By Preferences
    html += `
        <div class="reco-block">
            
        </div>
    `;

    // Block 3: By Cluster (K-Means)
    html += `
        <div class="reco-block">
            <div class="reco-block-header">
                <div class="reco-block-icon cluster">🧩</div>
                <div>
                  
                    <div class="reco-block-subtitle">${clusterResult.clusterSize} utilisateur(s) similaire à vous</div>
                </div>
            </div>
            <div class="reco-film-list">
                ${clusterResult.films.length > 0
                    ? clusterResult.films.map(f => renderFilmCard(f, f.avgRating)).join('')
                    : '<div class="reco-empty">Aucune recommandation depuis votre cluster.</div>'
                }
            </div>
        </div>
    `;

    // Inspiring message
    if (inspiringMsg) {
        html += `
            <div class="inspiring-message">
                ✨ Puisque vous avez aimé <strong>${inspiringMsg.lastFilm}</strong>, vous pourriez apprécier <strong>${inspiringMsg.recommendation}</strong>.
            </div>
        `;
    }

    container.innerHTML = html;
    container.classList.remove('hidden');
}

// ══════════════════════════════════════
// UI: LOADING ANIMATION
// ══════════════════════════════════════

function showLoading() {
    return new Promise(resolve => {
        const indicator = document.getElementById('loading-indicator');
        const textEl = document.getElementById('loading-text');
        const trigger = document.getElementById('reco-trigger');
        const results = document.getElementById('reco-results');

        trigger.classList.add('hidden');
        results.classList.add('hidden');
        indicator.classList.remove('hidden');

        let msgIndex = 0;
        const interval = setInterval(() => {
            textEl.classList.add('changing');
            setTimeout(() => {
                msgIndex = (msgIndex + 1) % LOADING_MESSAGES.length;
                textEl.textContent = LOADING_MESSAGES[msgIndex];
                textEl.classList.remove('changing');
            }, 200);
        }, 800);

        // Simulate computation time
        setTimeout(() => {
            clearInterval(interval);
            indicator.classList.add('hidden');
            resolve();
        }, 3200);
    });
}

// ══════════════════════════════════════
// EVENT HANDLERS
// ══════════════════════════════════════

async function handleCreateUser(e) {
    e.preventDefault();

    const name = document.getElementById('user-name').value.trim();
    const age = parseInt(document.getElementById('user-age').value, 10);

    if (selectedGenres.size === 0) {
        // Flash the genre toggles
        const toggles = document.querySelector('.genre-toggles');
        toggles.style.outline = '2px solid var(--color-error)';
        toggles.style.outlineOffset = '8px';
        toggles.style.borderRadius = '12px';
        setTimeout(() => {
            toggles.style.outline = 'none';
        }, 1500);
        return;
    }

    const preferredGenres = [...selectedGenres];

    // Check if the user already exists to load their existing history!
    const existing = allUsers.find(u => (u.name || `Utilisateur ${u.id}`).toLowerCase() === name.toLowerCase());
    let history = [];
    if (existing && existing.watch_history) {
        history = existing.watch_history.map(h => {
            const film = CATALOG.find(f => f.title.toLowerCase() === h.movie.toLowerCase()) || {
                id: Math.floor(Math.random() * 10000) + 1000,
                title: h.movie,
                genre: h.genre || 'Inconnu',
                director: h.director || 'Inconnu',
                avgRating: 4.0
            };
            return {
                film,
                rating: h.rating,
                date: h.date ? new Date(h.date) : new Date(),
                isMissing: h.rating === null,
                isOutlier: h.rating !== null && (h.rating < 1 || h.rating > 5)
            };
        });
    }

    currentUser = { name, age: age || (existing ? existing.age : 25), preferredGenres, history };

    // Save to utilisateurs.json
    await saveUserToAPI(currentUser);

    renderProfile(currentUser);
    renderCatalog();

    // Generate matplotlib visualisation for this user
    generateMatplotlibViz(name);

    // Smooth scroll to catalog
    document.getElementById('catalog-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

async function handleRecommendations() {
    if (!currentUser) return;

    await showLoading();

    // Generate 9 comparison users on-the-fly
    const compUsers = [];
    for (let i = 1; i <= 9; i++) {
        compUsers.push(generateComparisonUser(i));
    }

    // Run recommendation engines
    const prefRecos = recommendByPreferences(currentUser);
    const simResult = recommendBySimilarity(currentUser, compUsers);
    const clusterResult = recommendByCluster(currentUser, compUsers);

    // Build inspiring message
    const validHistory = currentUser.history.filter(h => h.rating !== null && !h.isOutlier);
    const lastFilm = validHistory.length > 0
        ? validHistory[validHistory.length - 1].film.title
        : currentUser.history[currentUser.history.length - 1].film.title;

    // First recommendation from any source (excluding Pearson)
    const allRecos = [...prefRecos, ...clusterResult.films];
    const firstReco = allRecos.length > 0 ? allRecos[0].title : null;

    const inspiringMsg = firstReco ? { lastFilm, recommendation: firstReco } : null;

    renderRecommendations(prefRecos, simResult, clusterResult, inspiringMsg);

    // Scroll to results
    document.getElementById('reco-results').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ══════════════════════════════════════
// INIT
// ══════════════════════════════════════

async function init() {
    renderGenreToggles();

    // Load existing users from utilisateurs.json
    await loadUsersFromAPI();

    document.getElementById('user-form').addEventListener('submit', handleCreateUser);
    document.getElementById('btn-reco').addEventListener('click', handleRecommendations);
}

init();
