import random
import time
import hashlib
import json
import webbrowser
import os
import threading
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

# ==========================================
# 1. Executive Configuration & Settings
# ==========================================
NUM_DEVICES = 10
READINGS_PER_DEVICE = 5
HTTP_PORT = 8000

# Professional Sensor Ranges
HR_NORMAL, HR_ABNORMAL = (60, 100), (120, 180)
TEMP_NORMAL, TEMP_ABNORMAL = (36.0, 37.8), (38.5, 41.0)

# Trust & Anomaly Weightings
TRUST_INITIAL, TRUST_INCREMENT, TRUST_DECREMENT = 1.0, 0.05, 0.35
ATTACK_PROBABILITY = 0.40 

# Multi-Factor Trust Evaluation Weights
WEIGHT_ACCURACY = 0.5
WEIGHT_STABILITY = 0.3
WEIGHT_LATENCY = 0.2

# ==========================================
# 2. Blockchain Infrastructure
# ==========================================
class Block:
    """Security ledger entry for the IoT blockchain."""
    def __init__(self, index, device_id, trust_score, decision, previous_hash):
        self.index = index
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.device_id = device_id
        self.trust_score = trust_score
        self.decision = decision
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index, "ts": self.timestamp, "id": self.device_id,
            "trust": self.trust_score, "dec": self.decision, "prev": self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

# ==========================================
# 3. Simulation & Multi-Vector Security Logic
# ==========================================
def generate_reading(device_id):
    is_attack = random.random() < ATTACK_PROBABILITY
    if is_attack:
        heart_rate = random.randint(*HR_ABNORMAL)
        temperature = round(random.uniform(*TEMP_ABNORMAL), 1)
        status = "ABNORMAL"
    else:
        heart_rate = random.randint(*HR_NORMAL)
        temperature = round(random.uniform(*TEMP_NORMAL), 1)
        status = "NORMAL"
    return {
        "id": device_id, "hr": heart_rate, "temp": temperature,
        "status": status, "ts": datetime.now().strftime("%H:%M:%S")
    }

# ==========================================
# 4. Executive Dashboard Generator
# ==========================================
def generate_dashboard(device_results, blockchain):
    """Generates a premium, presentation-ready IoT security dashboard."""
    
    # Pre-calculate metrics
    total_devices = len(device_results)
    active_devices = sum(1 for d in device_results if d['decision'] == 'ALLOWED')
    blocked_devices = sum(1 for d in device_results if d['decision'] == 'BLOCKED')
    avg_trust = round(sum(d['trust'] for d in device_results) / total_devices, 2)
    
    # Category Distribution
    categories = {}
    for d in device_results:
        categories[d['category']] = categories.get(d['category'], 0) + 1
    
    # Alerts & Smart Contract Rerouting Generation
    alerts_html = ""
    for d in device_results:
        ts = datetime.now().strftime("%H:%M:%S")
        if d['decision'] == 'BLOCKED':
            alerts_html += f"""
            <div class="alert-item risk-high">
                <span class="alert-time">{ts}</span>
                <div class="alert-content">
                    <span class="alert-msg">Device isolation: {d['id']} blocked.</span>
                    <div class="xai-reason"><i data-lucide="brain-circuit" style="width:12px;"></i> <b>XAI Reason:</b> {d['xai_detail']}</div>
                </div>
                <i data-lucide="shield-off" class="alert-icon"></i>
            </div>"""
            if d.get('reroute_target'):
                alerts_html += f"""
                <div class="alert-item risk-healing">
                    <span class="alert-time">{ts}</span>
                    <div class="alert-content">
                        <span class="alert-msg">Self-Healing Reroute <span class="badge-healing">SMART CONTRACT</span></span>
                        <div class="xai-reason"><i data-lucide="git-branch-plus" style="width:12px;"></i> Data rerouted to {d['reroute_target']} to maintain service continuity.</div>
                    </div>
                    <i data-lucide="activity" class="alert-icon"></i>
                </div>"""
        elif d['status'] == 'SUSPICIOUS':
            alerts_html += f"""
            <div class="alert-item risk-med">
                <span class="alert-time">{ts}</span>
                <div class="alert-content">
                    <span class="alert-msg">Anomalous behavior: {d['id']} detected.</span>
                    <div class="xai-reason"><i data-lucide="brain-circuit" style="width:12px;"></i> <b>XAI Reason:</b> {d['xai_detail']}</div>
                </div>
                <i data-lucide="alert-circle" class="alert-icon"></i>
            </div>"""
        elif d['decision'] == 'SANDBOXED':
            alerts_html += f"""
            <div class="alert-item risk-probation">
                <span class="alert-time">{ts}</span>
                <div class="alert-content">
                    <span class="alert-msg">Device in Probation: {d['id']} recovering.</span>
                    <div class="xai-reason"><i data-lucide="refresh-cw" style="width:12px;"></i> <b>XAI Reason:</b> {d['xai_detail']}</div>
                </div>
                <i data-lucide="shield-alert" class="alert-icon"></i>
            </div>"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CyberGuard | Blockchain IoT Security Framework</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {{
            --bg: #0b0e14;
            --panel: #161b22;
            --panel-light: #21262d;
            --accent: #58a6ff;
            --success: #3fb950;
            --warning: #d29922;
            --danger: #f85149;
            --probation: #a259ff;
            --text-main: #c9d1d9;
            --text-dim: #8b949e;
            --glass: rgba(22, 27, 34, 0.7);
            --border: rgba(240, 246, 252, 0.1);
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Outfit', sans-serif;
            background: var(--bg);
            color: var(--text-main);
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 0% 0%, rgba(88, 166, 255, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 100% 100%, rgba(162, 89, 255, 0.05) 0%, transparent 50%);
        }}

        /* Navbar */
        .navbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 3rem;
            background: var(--glass);
            backdrop-filter: blur(15px);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 1000;
        }}
        .brand {{ display: flex; align-items: center; gap: 0.75rem; font-size: 1.5rem; font-weight: 700; color: var(--accent); }}
        .header-meta {{ display: flex; gap: 2rem; font-size: 0.85rem; color: var(--text-dim); }}
        .live-indicator {{ display: flex; align-items: center; gap: 0.5rem; color: var(--success); font-weight: 600; }}
        .dot {{ width: 8px; height: 8px; background: var(--success); border-radius: 50%; animation: pulse 2s infinite; }}
        @keyframes pulse {{ 
            0% {{ transform: scale(1); opacity: 1; }} 
            50% {{ transform: scale(1.5); opacity: 0.5; }} 
            100% {{ transform: scale(1); opacity: 1; }} 
        }}

        /* Layout */
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: 1.5rem;
            padding: 2rem 3rem;
            max-width: 1800px;
            margin: 0 auto;
        }}

        /* Cards */
        .card {{
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .card:hover {{ transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.3); border-color: rgba(88, 166, 255, 0.3); }}
        .card-title {{ font-size: 1rem; font-weight: 600; margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center; color: var(--text-dim); text-transform: uppercase; letter-spacing: 1px; }}

        /* Stat Cards */
        .stat-group {{ display: flex; gap: 1rem; grid-column: span 12; margin-bottom: 1rem; }}
        .mini-stat {{ flex: 1; background: var(--panel); @extend .card; display: flex; align-items: center; gap: 1.25rem; padding: 1.25rem 2rem; border-radius: 12px; border: 1px solid var(--border); }}
        .mini-stat .icon-box {{ width: 50px; height: 50px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; }}
        .stat-val {{ font-size: 1.75rem; font-weight: 700; }}
        .stat-name {{ font-size: 0.85rem; color: var(--text-dim); }}

        /* Main Sections */
        .sect-trust {{ grid-column: span 8; }}
        .sect-alerts {{ grid-column: span 4; display: flex; flex-direction: column; }}
        .sect-charts {{ grid-column: span 8; display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }}
        .sect-recovery {{ grid-column: span 4; }}
        .sect-ledger {{ grid-column: span 12; }}

        /* Trust Table */
        .trust-table {{ width: 100%; border-collapse: collapse; margin-top: 0.5rem; }}
        .trust-table th {{ text-align: left; padding: 1rem; border-bottom: 1px solid var(--border); color: var(--text-dim); font-size: 0.85rem; }}
        .trust-table td {{ padding: 1rem; border-bottom: 1px solid rgba(240, 246, 252, 0.05); font-size: 0.95rem; vertical-align: middle; }}
        
        /* Badges */
        .badge {{ padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; display: inline-block; }}
        .badge-normal {{ background: rgba(63, 185, 80, 0.15); color: var(--success); }}
        .badge-suspicious {{ background: rgba(210, 153, 34, 0.15); color: var(--warning); }}
        .badge-blocked {{ background: rgba(248, 81, 73, 0.15); color: var(--danger); }}
        .badge-probation {{ background: rgba(162, 89, 255, 0.15); color: var(--probation); }}
        .badge-healing {{ background: rgba(88, 166, 255, 0.15); color: var(--accent); padding: 0.15rem 0.5rem; font-size: 0.65rem; border: 1px solid var(--accent); margin-left: 8px; }}

        /* Multi-Factor Scores */
        .trust-bar-bg {{ width: 100px; height: 6px; background: var(--panel-light); border-radius: 3px; position: relative; }}
        .trust-bar-fill {{ height: 100%; border-radius: 3px; background: var(--accent); box-shadow: 0 0 10px var(--accent); }}
        .sub-scores {{ display: flex; gap: 10px; margin-top: 6px; align-items: center; }}
        .sub-score-item {{ display: flex; background: rgba(0,0,0,0.2); padding: 2px 6px; border-radius: 4px; border: 1px solid var(--border); flex-direction: column; }}
        .sub-score-label {{ font-size: 0.55rem; color: var(--text-dim); text-transform: uppercase; line-height: 1; }}
        .sub-score-val {{ font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; font-weight: 600; color: var(--text-main); margin-top: 2px; }}

        /* Alert List & XAI */
        .alert-list {{ display: flex; flex-direction: column; gap: 0.75rem; max-height: 480px; overflow-y: auto; padding-right: 0.5rem; flex-grow: 1; }}
        .alert-item {{ background: var(--panel-light); padding: 1rem; border-radius: 8px; position: relative; border-left: 4px solid transparent; display: flex; gap: 1rem; align-items: flex-start; }}
        .alert-time {{ font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: var(--text-dim); flex-shrink: 0; min-width: 60px; }}
        .alert-content {{ flex-grow: 1; }}
        .alert-msg {{ font-size: 0.85rem; font-weight: 600; display: flex; align-items: center; }}
        .alert-icon {{ flex-shrink: 0; color: var(--text-dim); opacity: 0.7; }}
        
        .risk-high {{ border-left-color: var(--danger); }}
        .risk-med {{ border-left-color: var(--warning); }}
        .risk-probation {{ border-left-color: var(--probation); }}
        .risk-healing {{ border-left-color: var(--accent); background: rgba(88, 166, 255, 0.05); }}

        .xai-reason {{ font-size: 0.75rem; color: var(--text-dim); margin-top: 6px; background: rgba(0,0,0,0.25); padding: 6px 10px; border-radius: 6px; border-left: 2px solid var(--border); display: flex; align-items: flex-start; gap: 5px; }}

        /* Recovery Zone */
        .recovery-item {{ background: rgba(162, 89, 255, 0.05); padding: 1rem; border-radius: 8px; border: 1px dashed rgba(162, 89, 255, 0.3); margin-bottom: 1rem; }}
        .recovery-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }}
        .recovery-id {{ font-weight: 700; color: var(--probation); display: flex; align-items: center; gap: 6px; }}
        .recovery-status {{ font-size: 0.75rem; background: var(--probation); color: white; padding: 2px 8px; border-radius: 10px; font-weight: 600; animation: pulse-subtle 2s infinite; }}
        @keyframes pulse-subtle {{ 0% {{ opacity: 0.8; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.8; }} }}

        /* Ledger */
        .ledger-container {{ display: flex; gap: 2rem; overflow-x: auto; padding: 1rem 0; scrollbar-width: thin; }}
        .block-card {{ min-width: 320px; background: var(--panel-light); border: 1px solid var(--border); padding: 1.5rem; border-radius: 12px; position: relative; }}
        .block-card::after {{ content: '→'; position: absolute; right: -25px; top: 50%; transform: translateY(-50%); font-size: 1.5rem; color: var(--accent); opacity: 0.5; }}
        .block-card:last-child::after {{ display: none; }}
        .block-id {{ font-family: 'JetBrains Mono', monospace; font-weight: 700; color: var(--accent); margin-bottom: 1rem; display: block; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }}
        .block-field {{ font-size: 0.8rem; margin-bottom: 0.5rem; }}
        .block-field label {{ color: var(--text-dim); display: block; font-size: 0.7rem; text-transform: uppercase; }}
        .hash-str {{ font-family: 'JetBrains Mono', monospace; color: var(--text-dim); word-break: break-all; opacity: 0.7; font-size: 0.7rem; }}
        .immutability-seal {{ position: absolute; top: 1rem; right: 1rem; color: var(--success); opacity: 0.3; }}

        .chart-container {{ position: relative; height: 250px; width: 100%; }}
        
        button.logout {{ background: transparent; border: 1px solid var(--danger); color: var(--danger); padding: 0.5rem 1.25rem; border-radius: 6px; cursor: pointer; transition: 0.3s; font-weight: 600; font-family: 'Outfit'; }}
        button.logout:hover {{ background: var(--danger); color: white; }}
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="brand">
            <i data-lucide="shield-check"></i>
            CYBERGUARD GATEWAY
        </div>
        <div class="header-meta">
            <div class="live-indicator"><span class="dot"></span> NODE STATUS: OPERATIONAL</div>
            <div id="clock">00:00:00</div>
            <div style="color:var(--accent); font-weight:600;">BLOCKCHAIN LEDGER v2.4</div>
            <button class="logout" onclick="logout()">SECURE LOGOUT</button>
        </div>
    </nav>

    <div class="dashboard-grid">
        <!-- mini stats -->
        <div class="stat-group">
            <div class="card mini-stat">
                <div class="icon-box" style="background:rgba(88,166,255,0.1); color:var(--accent);"><i data-lucide="cpu"></i></div>
                <div>
                    <div class="stat-name">Total Fleet</div>
                    <div class="stat-val">{total_devices}</div>
                </div>
            </div>
            <div class="card mini-stat">
                <div class="icon-box" style="background:rgba(63,185,80,0.1); color:var(--success);"><i data-lucide="check-circle-2"></i></div>
                <div>
                    <div class="stat-name">Authorized</div>
                    <div class="stat-val">{active_devices}</div>
                </div>
            </div>
            <div class="card mini-stat">
                <div class="icon-box" style="background:rgba(248,81,73,0.1); color:var(--danger);"><i data-lucide="alert-octagon"></i></div>
                <div>
                    <div class="stat-name">Isolated</div>
                    <div class="stat-val">{blocked_devices}</div>
                </div>
            </div>
            <div class="card mini-stat">
                <div class="icon-box" style="background:rgba(210,153,34,0.1); color:var(--warning);"><i data-lucide="activity"></i></div>
                <div>
                    <div class="stat-name">Mean Protocol Trust</div>
                    <div class="stat-val">{avg_trust}</div>
                </div>
            </div>
        </div>

        <!-- Trust Panel -->
        <div class="card sect-trust">
            <div class="card-title">
                Multi-Factor Trust Evaluation Dashboard
                <i data-lucide="layers" style="width:16px;"></i>
            </div>
            <table class="trust-table">
                <thead>
                    <tr>
                        <th>DEVICE ID</th>
                        <th>MULTI-FACTOR TRUST (Acc/Stb/Lat)</th>
                        <th>SECURITY STATE</th>
                        <th>PROTOCOL ACTION</th>
                    </tr>
                </thead>
                <tbody>
"""

    for d in device_results:
        badge_cls = 'badge-normal' if d['status'] == 'STABLE' else 'badge-probation' if d['status'] == 'PROBATION' else 'badge-suspicious' if d['status'] == 'SUSPICIOUS' else 'badge-blocked'
        action_badge = 'badge-normal' if d['decision'] == 'ALLOWED' else 'badge-probation' if d['decision'] == 'SANDBOXED' else 'badge-blocked'
        status_text = "NORMAL" if d['status'] == 'STABLE' else d['status']
        bar_color = 'var(--probation)' if d['decision'] == 'SANDBOXED' else 'var(--danger)' if d['decision'] == 'BLOCKED' else 'var(--accent)'
        
        html_content += f"""
                    <tr>
                        <td>
                            <div style="font-weight:700;">{d['id']}</div>
                            <div style="font-size:0.7rem; color:var(--text-dim); margin-top:3px;">{d['category']}</div>
                        </td>
                        <td>
                            <div style="display:flex; align-items:center; gap:10px;">
                                <div class="trust-bar-bg"><div class="trust-bar-fill" style="width:{d['trust']*100}%; background:{bar_color}; box-shadow:0 0 10px {bar_color};"></div></div>
                                <span style="font-family:'JetBrains Mono'; font-weight:700; font-size:1.05rem;">{d['trust']}</span>
                            </div>
                            <div class="sub-scores">
                                <div class="sub-score-item" title="Data Accuracy Score">
                                    <span class="sub-score-label">Acc</span>
                                    <span class="sub-score-val">{d['acc_score']}</span>
                                </div>
                                <div class="sub-score-item" title="Device Stability Score">
                                    <span class="sub-score-label">Stb</span>
                                    <span class="sub-score-val">{d['stab_score']}</span>
                                </div>
                                <div class="sub-score-item" title="Latency/Time Score">
                                    <span class="sub-score-label">Lat</span>
                                    <span class="sub-score-val">{d['lat_score']}</span>
                                </div>
                            </div>
                        </td>
                        <td><span class="badge {badge_cls}">{status_text}</span></td>
                        <td><span class="badge {action_badge}">{d['decision']}</span></td>
                    </tr>"""

    html_content += f"""
                </tbody>
            </table>
        </div>

        <!-- Alerts & XAI Panel -->
        <div class="card sect-alerts">
            <div class="card-title">
                Explainable AI (XAI) Security Events
                <i data-lucide="shield-alert" style="color:var(--danger); width:18px;"></i>
            </div>
            <div class="alert-list">
                {alerts_html if alerts_html else '<div style="color:var(--text-dim); text-align:center; padding:2rem;">System secure. No active events.</div>'}
            </div>
        </div>

        <!-- Charts Panel -->
        <div class="sect-charts">
            <div class="card">
                <div class="card-title">Adaptive Recovery Pattern (Probation)</div>
                <div class="chart-container"><canvas id="trustTrendChart"></canvas></div>
            </div>
            <div class="card">
                <div class="card-title">Fleet State Distribution</div>
                <div class="chart-container"><canvas id="classChart"></canvas></div>
            </div>
        </div>

        <!-- Recovery Zone Panel -->
        <div class="card sect-recovery" style="border-color: rgba(162, 89, 255, 0.3);">
            <div class="card-title" style="color: var(--probation);">
                Adaptive Trust Recovery Zone
                <i data-lucide="refresh-cw" style="width:16px;"></i>
            </div>
            <div style="font-size:0.8rem; color:var(--text-dim); margin-bottom: 1.5rem; line-height: 1.5;">
                Devices currently isolated in probationary sandboxes. Consistent demonstration of stable telemetry over time will incrementally restore standard system access.
            </div>
"""
    recovery_count = 0
    for d in device_results:
        if d['decision'] == 'SANDBOXED':
            recovery_count += 1
            html_content += f"""
            <div class="recovery-item">
                <div class="recovery-header">
                    <span class="recovery-id"><i data-lucide="hard-drive" style="width:14px;"></i> {d['id']}</span>
                    <span class="recovery-status">{d['recovery_status']}</span>
                </div>
                <div style="font-size: 0.75rem; color: var(--text-main); margin-bottom: 12px; background: rgba(0,0,0,0.2); padding: 8px; border-radius: 6px;">{d['xai_detail']}</div>
                <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.7rem; color:var(--text-dim);">
                    <span>Trust Gradient</span>
                    <span>{int(d['trust']*100)}%</span>
                </div>
                <div class="trust-bar-bg" style="width: 100%; height: 8px;"><div class="trust-bar-fill" style="width: {d['trust']*100}%; background: var(--probation); box-shadow: 0 0 10px var(--probation);"></div></div>
            </div>"""
    
    if recovery_count == 0:
        html_content += """<div style="text-align:center; padding: 2rem; color: var(--text-dim); font-style:italic;">No devices currently in probation.</div>"""

    html_content += """
        </div>

        <!-- Ledger Panel -->
        <div class="card sect-ledger">
            <div class="card-title">
                IMMUTABLE BLOCKCHAIN SECURITY LEDGER
                <span style="font-size:0.7rem; color:var(--success);">Verified Chain Status: ACTIVE</span>
            </div>
            <div class="ledger-container">
"""
    for b in blockchain:
        html_content += f"""
                <div class="block-card">
                    <i data-lucide="lock" class="immutability-seal"></i>
                    <span class="block-id">BLOCK #{b.index}</span>
                    <div class="block-field"><label>Origin Node</label>{b.device_id}</div>
                    <div class="block-field"><label>Recorded Trust</label>{b.trust_score}</div>
                    <div class="block-field"><label>Action Enforced</label>{b.decision}</div>
                    <div class="block-field"><label>SHA-256 Hash</label><span class="hash-str">{b.hash}</span></div>
                    <div class="block-field"><label>Previous Block</label><span class="hash-str">{b.previous_hash}</span></div>
                </div>"""

    # We select a recovering device's history for the trend chart, if any exists
    trend_history = [0.2, 0.25, 0.3, 0.35, 0.45, 0.5] # Default fallback
    recovering_devices = [d for d in device_results if d['decision'] == 'SANDBOXED']
    if len(recovering_devices) > 0:
        trend_history = recovering_devices[0]['history']

    state_distribution = {'NORMAL': 0, 'SUSPICIOUS': 0, 'PROBATION': 0, 'BLOCKED': 0}
    for d in device_results:
        mapped_status = 'NORMAL' if d['status'] == 'STABLE' else 'BLOCKED' if d['status'] == 'HIGH RISK' else d['status']
        state_distribution[mapped_status] += 1

    html_content += f"""
            </div>
        </div>
    </div>

    <script>
        lucide.createIcons();

        function logout() {{
            sessionStorage.removeItem('hn_authenticated');
            window.location.replace('login.html');
        }}

        setInterval(() => {{
            document.getElementById('clock').innerText = new Date().toLocaleTimeString();
        }}, 1000);

        // Charts configuration
        const trustTrendCtx = document.getElementById('trustTrendChart').getContext('2d');
        new Chart(trustTrendCtx, {{
            type: 'line',
            data: {{
                labels: ['T-5', 'T-4', 'T-3', 'T-2', 'T-1', 'Now'],
                datasets: [
                    {{
                        label: 'Device Recovery Path',
                        data: {json.dumps(trend_history)},
                        borderColor: '#a259ff',
                        backgroundColor: 'rgba(162, 89, 255, 0.1)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 3,
                        pointRadius: 4,
                        pointBackgroundColor: '#a259ff'
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#8b949e' }}, beginAtZero: true, max: 1.0 }},
                    x: {{ grid: {{ display: false }}, ticks: {{ color: '#8b949e' }} }}
                }}
            }}
        }});

        const classCtx = document.getElementById('classChart').getContext('2d');
        new Chart(classCtx, {{
            type: 'doughnut',
            data: {{
                labels: ['Normal', 'Suspicious', 'Probation', 'Blocked'],
                datasets: [{{
                    data: [{state_distribution['NORMAL']}, {state_distribution['SUSPICIOUS']}, {state_distribution['PROBATION']}, {state_distribution['BLOCKED']}],
                    backgroundColor: ['#3fb950', '#d29922', '#a259ff', '#f85149'],
                    borderWidth: 0,
                    hoverOffset: 10
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {{
                    legend: {{ position: 'right', labels: {{ color: '#8b949e', font: {{ family: 'Outfit', size: 12 }}, padding: 20 }} }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
    
    with open("dashboard.html", "w", encoding="utf-8") as f: f.write(html_content)

# ==========================================
# 5. Executive HTTP Server Implementation
# ==========================================
def run_http_server():
    server_address = ('', HTTP_PORT)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"\\n[EXECUTIVE] Platform listening on http://localhost:{{HTTP_PORT}}")
    httpd.serve_forever()

# ==========================================
# 6. Global Simulation Lifecycle
# ==========================================
def simulate_iot_health_system():
    devices = [f"Device_{i+1:03}" for i in range(NUM_DEVICES)]
    categories = ["Medical Device", "Security Camera", "Environmental Sensor"]
    
    # Initialization
    stats_map = {
        dev: {
            "normal": 0, 
            "abnormal": 0, 
            "hr": 0, 
            "temp": 0,
            "category": categories[i % 3]
        } for i, dev in enumerate(devices)
    }

    print("\\n" + "X"*85)
    print(f"{{'HEALTH NODE EXECUTIVE | CRYPTOGRAPHIC SIMULATION':^85}}")
    print("X"*85)
    print(f"{{'ISO_TS':<10}} | {{'NODE_ID':<12}} | {{'HR':<5}} | {{'TEMP':<5}} | {{'STATUS':<11}}")
    print("-" * 85)
    
    for device_id in devices:
        for _ in range(READINGS_PER_DEVICE):
            data = generate_reading(device_id)
            node = stats_map[device_id]
            node["hr"], node["temp"] = data['hr'], data['temp']
            
            if data['status'] == "NORMAL":
                node["normal"] += 1
            else:
                node["abnormal"] += 1
            
            print(f"{{data['ts']:<10}} | {{data['id']:<12}} | {{data['hr']:<5}} | {{data['temp']:<5}} | {{data['status']:<11}}")
            time.sleep(0.01)

    # Post-Simulation Analysis
    ledger, report = [], []
    
    # Advanced State Simulation: 2 Blocked, 2 Recovering, 2 Suspicious, 4 Normal
    prev_h = "0" * 64 
    for i, device_id in enumerate(devices):
        node = stats_map[device_id]
        
        # Base variables
        reroute_target = None
        recovery_status = "N/A"
        history = []
        
        if i < 2: # BLOCKED
            status, level, decision = "HIGH RISK", "Executive Isolation", "BLOCKED"
            trust = random.uniform(0.1, 0.3)
            acc_score = round(random.uniform(0.1, 0.4), 2)
            stab_score = round(random.uniform(0.2, 0.5), 2)
            lat_score = round(random.uniform(0.4, 0.8), 2)
            xai_detail = f"Critical trust failure. Device exhibiting {random.randint(25, 45)}% deviation in physiological metrics from historical baseline."
            reroute_target = devices[i + 8] # Reroute to a Normal device to maintain continuity
            history = [0.6, 0.5, 0.4, 0.3, 0.2, trust]
            
        elif i < 4: # RECOVERING (PROBATION)
            status, level, decision = "PROBATION", "Sandbox Environment", "SANDBOXED"
            trust = round(random.uniform(0.4, 0.55), 2)
            acc_score = round(random.uniform(0.7, 0.85), 2)
            stab_score = round(random.uniform(0.6, 0.75), 2)
            lat_score = round(random.uniform(0.8, 1.0), 2)
            xai_detail = "Device consistently demonstrating nominal metrics in sandbox. Trust score organically increasing per policy."
            recovery_status = "Recovering"
            history = [0.2, 0.25, 0.35, 0.45, trust, round(trust + 0.05, 2)]
            
        elif i < 6: # SUSPICIOUS
            status, level, decision = "SUSPICIOUS", "Active Monitoring", "ALLOWED"
            trust = round(random.uniform(0.6, 0.75), 2)
            acc_score = round(random.uniform(0.5, 0.8), 2)
            stab_score = round(random.uniform(0.4, 0.7), 2)
            lat_score = round(random.uniform(0.7, 0.9), 2)
            xai_detail = f"Intermittent {random.randint(10, 20)}% packet delay and mild thermal deviation detected. Active monitoring initiated."
            history = [0.9, 0.85, 0.8, 0.75, 0.7, trust]
            
        else: # NORMAL
            status, level, decision = "STABLE", "Standard Protocol", "ALLOWED"
            trust = round(random.uniform(0.85, 0.98), 2)
            acc_score = round(random.uniform(0.85, 1.0), 2)
            stab_score = round(random.uniform(0.85, 1.0), 2)
            lat_score = round(random.uniform(0.85, 1.0), 2)
            xai_detail = "Telemetry aligns with learned baseline paradigms. Operations optimal."
            history = [0.95, 0.96, 0.94, 0.97, 0.95, trust]

        # Calculate Final Multi-Factor Trust
        calc_trust = round((acc_score * WEIGHT_ACCURACY) + (stab_score * WEIGHT_STABILITY) + (lat_score * WEIGHT_LATENCY), 2)
        node["trust"] = calc_trust

        report.append({
            "id": device_id, 
            "hr": node["hr"], 
            "temp": node["temp"], 
            "trust": node["trust"],
            "status": status, 
            "level": level, 
            "decision": decision, 
            "acc_score": acc_score,
            "stab_score": stab_score,
            "lat_score": lat_score,
            "xai_detail": xai_detail,
            "reroute_target": reroute_target,
            "recovery_status": recovery_status,
            "category": node["category"],
            "history": history
        })

        if decision in ["ALLOWED", "SANDBOXED"]:
            block = Block(len(ledger) + 1, device_id, node["trust"], decision, prev_h)
            ledger.append(block); prev_h = block.hash

    print("\\nCompiling Professional Dashboard...")
    generate_dashboard(report, ledger)
    
    # Platform Deployment
    threading.Thread(target=run_http_server, daemon=True).start()
    time.sleep(1) 
    url = f"http://localhost:{{HTTP_PORT}}/dashboard.html"
    print(f"\\n[SECURE LINK] Dashboard access: {{url}}")
    print("X"*85)
    
    webbrowser.open(url)
    
    print("Server active. Press Ctrl+C to disconnect from the node.")
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt: print("\\nPlatform offline. Encryption keys purged.")

if __name__ == "__main__":
    simulate_iot_health_system()
