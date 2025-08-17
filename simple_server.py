#!/usr/bin/env python3
"""
Simple HTTP Server for Personal Finance Agent
Alternative launcher if Flask has connection issues
"""

import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import random
from datetime import datetime, timedelta

# Import our finance agent
try:
    from app import FinanceAgent, finance_agent
    print("✅ Finance Agent imported successfully")
except ImportError as e:
    print(f"❌ Could not import Finance Agent: {e}")
    sys.exit(1)

class FinanceHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            # Serve the main HTML page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                with open('templates/index.html', 'r') as f:
                    html_content = f.read()
                self.wfile.write(html_content.encode())
            except FileNotFoundError:
                self.wfile.write(b'<h1>Personal Finance Agent</h1><p>HTML template not found</p>')
                
        elif parsed_path.path == '/api/demo_data':
            # Generate demo data
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Generate demo transactions
            demo_data = self.generate_demo_data()
            self.wfile.write(json.dumps(demo_data, indent=2).encode())
            
        elif parsed_path.path == '/health':
            # Health check endpoint
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            health_data = {
                "status": "healthy",
                "service": "Personal Finance Agent",
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(health_data).encode())
            
        else:
            # Default 404
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>404 - Not Found</h1>')
    
    def generate_demo_data(self):
        """Generate realistic demo financial data"""
        import pandas as pd
        
        # Generate sample transactions
        demo_transactions = []
        categories = list(finance_agent.categories.keys())[:-1]  # Exclude 'Other'
        
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
        anomalies = finance_agent.detect_anomalies(df)
        insights = finance_agent.analyze_spending_patterns(df)
        suggestions = finance_agent.suggest_budget_tweaks(df, current_income=5000)
        
        return {
            'transactions': demo_transactions,
            'anomalies': anomalies,
            'insights': insights,
            'budget_suggestions': suggestions,
            'total_transactions': len(demo_transactions),
            'demo_mode': True
        }

def main():
    port = 9000
    
    # Change to the correct directory
    os.chdir('/workspace')
    
    print("🏦 Personal Finance Agent - Simple Server")
    print("=" * 50)
    print(f"🚀 Starting server on port {port}...")
    print(f"🌐 Open http://localhost:{port} in your browser")
    print(f"🔍 Health check: http://localhost:{port}/health")
    print(f"🎮 Demo data: http://localhost:{port}/api/demo_data")
    print("=" * 50)
    
    try:
        server = HTTPServer(('0.0.0.0', port), FinanceHandler)
        print(f"✅ Server running successfully on all interfaces")
        print("Press Ctrl+C to stop the server")
        server.serve_forever()
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use. Trying port {port + 1}...")
            try:
                server = HTTPServer(('0.0.0.0', port + 1), FinanceHandler)
                print(f"✅ Server running on port {port + 1}")
                print(f"🌐 Open http://localhost:{port + 1} in your browser")
                server.serve_forever()
            except Exception as e2:
                print(f"❌ Could not start server: {e2}")
        else:
            print(f"❌ Server error: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")

if __name__ == "__main__":
    main()