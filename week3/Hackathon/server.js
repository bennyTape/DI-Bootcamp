const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const { spawn } = require('child_process');

const app = express();
const PORT = 3000;
const DATA_FILE = path.join(__dirname, 'utilisateurs.json');
const VIZ_FILE  = path.join(__dirname, 'visualisation.png');

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

// Read utilisateurs.json
app.get('/api/users', (req, res) => {
    try {
        if (fs.existsSync(DATA_FILE)) {
            const data = fs.readFileSync(DATA_FILE, 'utf8');
            res.json(JSON.parse(data));
        } else {
            res.json([]);
        }
    } catch (error) {
        console.error('Error reading utilisateurs.json:', error);
        res.status(500).json({ error: 'Failed to read users data' });
    }
});

// Save user to utilisateurs.json
app.post('/api/users', (req, res) => {
    try {
        let users = [];
        if (fs.existsSync(DATA_FILE)) {
            const data = fs.readFileSync(DATA_FILE, 'utf8');
            users = JSON.parse(data);
        }

        // Add new user
        users.push(req.body);

        // Write back to file
        fs.writeFileSync(DATA_FILE, JSON.stringify(users, null, 2), 'utf8');
        
        res.json({ success: true, user: req.body });
    } catch (error) {
        console.error('Error saving to utilisateurs.json:', error);
        res.status(500).json({ error: 'Failed to save user data' });
    }
});

// Update existing user
app.put('/api/users/:name', (req, res) => {
    try {
        let users = [];
        if (fs.existsSync(DATA_FILE)) {
            const data = fs.readFileSync(DATA_FILE, 'utf8');
            users = JSON.parse(data);
        }

        const userName = req.params.name;
        const index = users.findIndex(u => u.name === userName);

        if (index !== -1) {
            users[index] = req.body;
            fs.writeFileSync(DATA_FILE, JSON.stringify(users, null, 2), 'utf8');
            res.json({ success: true, user: req.body });
        } else {
            res.status(404).json({ error: 'User not found' });
        }
    } catch (error) {
        console.error('Error updating utilisateurs.json:', error);
        res.status(500).json({ error: 'Failed to update user data' });
    }
});

// ── Generate/update visualisation.png via Python script ──────────────────────
app.post('/api/generate-viz', (req, res) => {
    const userName = req.body && req.body.name ? req.body.name : '';

    const scriptPath = path.join(__dirname, 'generate_viz.py');
    const args = userName ? [scriptPath, userName] : [scriptPath];

    const py = spawn('python', args, { cwd: __dirname });

    let stdout = '';
    let stderr = '';

    py.stdout.on('data', (data) => { stdout += data.toString(); });
    py.stderr.on('data', (data) => { stderr += data.toString(); });

    py.on('close', (code) => {
        if (code === 0) {
            console.log('Visualization generated:', stdout.trim());
            res.json({ success: true, message: stdout.trim() });
        } else {
            console.error('Python error:', stderr);
            res.status(500).json({ success: false, error: stderr });
        }
    });

    py.on('error', (err) => {
        console.error('Failed to start Python:', err);
        res.status(500).json({ success: false, error: 'Python not found or script error: ' + err.message });
    });
});

// Serve visualisation.png with no-cache headers so the browser always reloads it
app.get('/visualisation.png', (req, res) => {
    if (fs.existsSync(VIZ_FILE)) {
        res.set({
            'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
            'Content-Type': 'image/png'
        });
        res.sendFile(VIZ_FILE);
    } else {
        res.status(404).json({ error: 'visualisation.png not found' });
    }
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
    console.log(`Serving files from: ${__dirname}`);
});
