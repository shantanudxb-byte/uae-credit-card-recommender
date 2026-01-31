from flask import Flask, jsonify, render_template_string
from app.analytics import AnalyticsTracker
import json

app = Flask(__name__)
tracker = AnalyticsTracker()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Analytics Dashboard</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
        .metric { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric-value { font-size: 32px; font-weight: bold; color: #1a73e8; }
        .metric-label { color: #666; margin-top: 5px; }
        .section { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
        h1 { color: #333; }
        h2 { color: #555; margin-top: 0; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f8f9fa; font-weight: 600; }
        .refresh { background: #1a73e8; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
        .refresh:hover { background: #1557b0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>💳 Credit Card Recommender Analytics</h1>
        <button class="refresh" onclick="location.reload()">🔄 Refresh</button>
        
        <div class="metrics" id="metrics"></div>
        
        <div class="section">
            <h2>Top Recommended Cards</h2>
            <table id="topCards"></table>
        </div>
        
        <div class="section">
            <h2>Recent Sessions</h2>
            <table id="sessions"></table>
        </div>
    </div>
    
    <script>
        fetch('/api/dashboard/data')
            .then(r => r.json())
            .then(data => {
                document.getElementById('metrics').innerHTML = `
                    <div class="metric">
                        <div class="metric-value">${data.total_sessions}</div>
                        <div class="metric-label">Total Sessions</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${data.conversion_rate}%</div>
                        <div class="metric-label">Conversion Rate</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${data.avg_recommendations}</div>
                        <div class="metric-label">Avg Recommendations</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${data.total_apply_clicks}</div>
                        <div class="metric-label">Apply Clicks</div>
                    </div>
                `;
                
                document.getElementById('topCards').innerHTML = `
                    <tr><th>Card Name</th><th>Times Recommended</th><th>Click Rate</th></tr>
                    ${data.top_cards.map(c => `
                        <tr>
                            <td>${c.card_name}</td>
                            <td>${c.count}</td>
                            <td>${c.click_rate}%</td>
                        </tr>
                    `).join('')}
                `;
                
                document.getElementById('sessions').innerHTML = `
                    <tr><th>Session ID</th><th>Salary</th><th>Goals</th><th>Cards</th><th>Applied</th></tr>
                    ${data.recent_sessions.map(s => `
                        <tr>
                            <td>${s.session_id.substring(0, 8)}...</td>
                            <td>${s.salary} AED</td>
                            <td>${s.goals || 'N/A'}</td>
                            <td>${s.cards_recommended}</td>
                            <td>${s.applied ? '✅' : '❌'}</td>
                        </tr>
                    `).join('')}
                `;
            });
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(HTML)

@app.route('/api/dashboard/data')
def get_data():
    metrics = tracker.get_metrics()
    return jsonify(metrics)

if __name__ == '__main__':
    app.run(port=8501, debug=False)
