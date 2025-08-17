#!/usr/bin/env python3
"""
Personal Finance Agent - Static HTML Report Generator
Creates a standalone HTML report without web server dependencies
"""

import os
import sys
import json
import pandas as pd
import random
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import FinanceAgent
    print("✅ Finance Agent loaded successfully")
except ImportError as e:
    print(f"❌ Error importing Finance Agent: {e}")
    sys.exit(1)

def generate_demo_data():
    """Generate realistic demo financial data"""
    agent = FinanceAgent()
    
    demo_transactions = []
    categories = list(agent.categories.keys())[:-1]  # Exclude 'Other'
    
    for i in range(50):
        category = random.choice(categories)
        base_amount = {
            'Food and Drink': 25,
            'Transportation': 15, 
            'Shopping': 60,
            'Entertainment': 30,
            'Bills & Utilities': 100,
            'Healthcare': 80,
            'Travel': 200
        }.get(category, 40)
        
        amount = round(random.uniform(base_amount * 0.5, base_amount * 2), 2)
        date = datetime.now() - timedelta(days=random.randint(1, 30))
        
        demo_transactions.append({
            'transaction_id': f'demo_{i}',
            'account_id': 'demo_account',
            'amount': amount,
            'date': date.isoformat(),
            'description': f'{category} purchase #{i}',
            'merchant_name': f'{category} Merchant',
            'category': category,
            'original_category': category
        })
    
    # Convert to DataFrame for analysis
    df = pd.DataFrame(demo_transactions)
    
    # Perform analysis
    anomalies = agent.detect_anomalies(df)
    insights = agent.analyze_spending_patterns(df)
    suggestions = agent.suggest_budget_tweaks(df, current_income=5000)
    
    return {
        'transactions': demo_transactions,
        'anomalies': anomalies,
        'insights': insights,
        'budget_suggestions': suggestions,
        'total_transactions': len(demo_transactions),
        'demo_mode': True
    }

def generate_html_report(data):
    """Generate HTML report"""
    insights = data['insights']
    
    # Category data for chart
    category_data = insights.get('category_breakdown', {})
    categories = list(category_data.keys())
    amounts = list(category_data.values())
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personal Finance Agent - Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 3px solid #667eea;
        }}
        .header h1 {{
            color: #333;
            margin: 0;
            font-size: 2.5em;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .summary-card {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }}
        .summary-card h3 {{
            margin: 0 0 10px 0;
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .summary-card .value {{
            font-size: 2.2em;
            font-weight: bold;
            margin: 0;
        }}
        .section {{
            margin-bottom: 40px;
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            border-left: 5px solid #667eea;
        }}
        .section h2 {{
            color: #333;
            margin-top: 0;
            margin-bottom: 20px;
            font-size: 1.5em;
        }}
        .chart-container {{
            position: relative;
            height: 400px;
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .anomaly-item, .suggestion-item {{
            background: white;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 10px;
            border-left: 4px solid #dc3545;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        .suggestion-item {{
            border-left-color: #ffc107;
        }}
        .transaction-table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
        }}
        .transaction-table th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
        }}
        .transaction-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}
        .transaction-table tr:hover {{
            background: #f8f9fa;
        }}
        .category-badge {{
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
        }}
        .timestamp {{
            text-align: center;
            color: #666;
            margin-top: 30px;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏦 Personal Finance Agent</h1>
            <p>Intelligent Financial Analysis Report</p>
        </div>
        
        <div class="summary-grid">
            <div class="summary-card">
                <h3>Total Spending</h3>
                <p class="value">${abs(insights.get('total_spending', 0)):,.2f}</p>
            </div>
            <div class="summary-card">
                <h3>Transactions</h3>
                <p class="value">{data.get('total_transactions', 0):,}</p>
            </div>
            <div class="summary-card">
                <h3>Average Transaction</h3>
                <p class="value">${abs(insights.get('avg_transaction', 0)):,.2f}</p>
            </div>
            <div class="summary-card">
                <h3>Anomalies Detected</h3>
                <p class="value">{len(data.get('anomalies', []))}</p>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Spending by Category</h2>
            <div class="chart-container">
                <canvas id="categoryChart"></canvas>
            </div>
        </div>
        
        <div class="section">
            <h2>🚨 Spending Anomalies</h2>
            {generate_anomalies_html(data.get('anomalies', []))}
        </div>
        
        <div class="section">
            <h2>💡 Budget Optimization Suggestions</h2>
            {generate_suggestions_html(data.get('budget_suggestions', []))}
        </div>
        
        <div class="section">
            <h2>📝 Recent Transactions</h2>
            {generate_transactions_html(data.get('transactions', []))}
        </div>
        
        <div class="timestamp">
            Report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
        </div>
    </div>
    
    <script>
        // Create category chart
        const ctx = document.getElementById('categoryChart').getContext('2d');
        
        new Chart(ctx, {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(categories)},
                datasets: [{{
                    data: {json.dumps(amounts)},
                    backgroundColor: [
                        '#8B5CF6', '#06B6D4', '#10B981', '#F59E0B',
                        '#EF4444', '#EC4899', '#6366F1', '#84CC16'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            padding: 20,
                            font: {{
                                size: 14
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    
    return html_content

def generate_anomalies_html(anomalies):
    """Generate HTML for anomalies section"""
    if not anomalies:
        return "<p>✅ No spending anomalies detected. Great job staying consistent!</p>"
    
    html = ""
    for anomaly in anomalies:
        html += f"""
        <div class="anomaly-item">
            <h4>{anomaly['description']}</h4>
            <p><strong>Amount:</strong> ${anomaly['amount']:.2f}</p>
            <p><strong>Date:</strong> {anomaly['date'][:10]}</p>
            <p><strong>Reason:</strong> {anomaly['reason']}</p>
        </div>
        """
    return html

def generate_suggestions_html(suggestions):
    """Generate HTML for suggestions section"""
    if not suggestions:
        return "<p>✅ Your spending looks well-balanced! No specific recommendations at this time.</p>"
    
    html = ""
    for suggestion in suggestions:
        html += f"""
        <div class="suggestion-item">
            <h4>{suggestion['category']}</h4>
            <p><strong>Current Spending:</strong> ${suggestion['current_spending']:.2f} ({suggestion['percentage']:.1f}% of total)</p>
            <p><strong>Suggestion:</strong> {suggestion['suggestion']}</p>
            <p><strong>Potential Savings:</strong> <span style="color: #28a745; font-weight: bold;">${suggestion['potential_savings']:.2f}</span></p>
        </div>
        """
    return html

def generate_transactions_html(transactions):
    """Generate HTML for transactions table"""
    # Sort transactions by date (most recent first)
    sorted_transactions = sorted(transactions, key=lambda x: x['date'], reverse=True)
    
    html = """
    <table class="transaction-table">
        <thead>
            <tr>
                <th>Date</th>
                <th>Description</th>
                <th>Category</th>
                <th>Amount</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for transaction in sorted_transactions[:20]:  # Show last 20 transactions
        date = transaction['date'][:10]
        description = transaction['description']
        category = transaction['category']
        amount = f"${transaction['amount']:.2f}"
        
        html += f"""
            <tr>
                <td>{date}</td>
                <td>{description}</td>
                <td><span class="category-badge">{category}</span></td>
                <td>{amount}</td>
            </tr>
        """
    
    html += """
        </tbody>
    </table>
    """
    
    return html

def main():
    """Main function"""
    print("🏦 Personal Finance Agent - Report Generator")
    print("=" * 50)
    
    # Generate demo data
    print("📊 Generating demo financial data...")
    data = generate_demo_data()
    print("✅ Demo data generated successfully!")
    
    # Generate HTML report
    print("📄 Creating HTML report...")
    html_content = generate_html_report(data)
    
    # Save report
    filename = f"finance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, 'w') as f:
        f.write(html_content)
    
    print(f"✅ Report saved as: {filename}")
    print(f"🌐 Open the file in your browser to view the report")
    print(f"📁 Full path: {os.path.abspath(filename)}")

if __name__ == "__main__":
    main()