#!/usr/bin/env python3
"""
Personal Finance Agent - Command Line Interface
Direct access to all features without web server dependencies
"""

import os
import sys
import json
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import FinanceAgent
    print("✅ Finance Agent loaded successfully")
except ImportError as e:
    print(f"❌ Error importing Finance Agent: {e}")
    sys.exit(1)

class FinanceCLI:
    def __init__(self):
        self.agent = FinanceAgent()
        self.current_data = None
        
    def print_banner(self):
        print("🏦" + "="*60 + "🏦")
        print("           PERSONAL FINANCE AGENT - CLI")
        print("          Intelligent Financial Analysis")
        print("🏦" + "="*60 + "🏦")
        print()
    
    def generate_demo_data(self):
        """Generate realistic demo financial data"""
        print("📊 Generating demo financial data...")
        
        demo_transactions = []
        categories = list(self.agent.categories.keys())[:-1]  # Exclude 'Other'
        
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
        print("🔍 Analyzing transactions...")
        anomalies = self.agent.detect_anomalies(df)
        insights = self.agent.analyze_spending_patterns(df)
        suggestions = self.agent.suggest_budget_tweaks(df, current_income=5000)
        
        self.current_data = {
            'transactions': demo_transactions,
            'anomalies': anomalies,
            'insights': insights,
            'budget_suggestions': suggestions,
            'total_transactions': len(demo_transactions),
            'demo_mode': True
        }
        
        print("✅ Demo data generated successfully!")
        return self.current_data
    
    def display_summary(self):
        """Display financial summary"""
        if not self.current_data:
            print("❌ No data available. Generate demo data first.")
            return
            
        data = self.current_data
        insights = data['insights']
        
        print("\n💰 FINANCIAL SUMMARY")
        print("-" * 40)
        print(f"Total Spending:     ${abs(insights.get('total_spending', 0)):,.2f}")
        print(f"Total Transactions: {data.get('total_transactions', 0):,}")
        print(f"Average Transaction: ${abs(insights.get('avg_transaction', 0)):,.2f}")
        print(f"Anomalies Detected: {len(data.get('anomalies', []))}")
        print("-" * 40)
    
    def display_categories(self):
        """Display spending by category"""
        if not self.current_data:
            print("❌ No data available. Generate demo data first.")
            return
            
        insights = self.current_data['insights']
        categories = insights.get('category_breakdown', {})
        
        print("\n📊 SPENDING BY CATEGORY")
        print("-" * 50)
        
        total = sum(categories.values())
        for category, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total * 100) if total > 0 else 0
            bar_length = int(percentage / 5)  # Scale bar to 20 chars max
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"{category:<20} ${amount:>8.2f} {bar} {percentage:>5.1f}%")
        print("-" * 50)
    
    def display_anomalies(self):
        """Display spending anomalies"""
        if not self.current_data:
            print("❌ No data available. Generate demo data first.")
            return
            
        anomalies = self.current_data.get('anomalies', [])
        
        print("\n🚨 SPENDING ANOMALIES")
        print("-" * 60)
        
        if not anomalies:
            print("✅ No anomalies detected. Great job staying consistent!")
        else:
            for i, anomaly in enumerate(anomalies, 1):
                print(f"{i}. {anomaly['description']}")
                print(f"   💰 Amount: ${anomaly['amount']:.2f}")
                print(f"   📅 Date: {anomaly['date'][:10]}")
                print(f"   ⚠️  Reason: {anomaly['reason']}")
                print()
        print("-" * 60)
    
    def display_suggestions(self):
        """Display budget suggestions"""
        if not self.current_data:
            print("❌ No data available. Generate demo data first.")
            return
            
        suggestions = self.current_data.get('budget_suggestions', [])
        
        print("\n💡 BUDGET OPTIMIZATION SUGGESTIONS")
        print("-" * 65)
        
        if not suggestions:
            print("✅ Your spending looks well-balanced!")
        else:
            for i, suggestion in enumerate(suggestions, 1):
                print(f"{i}. {suggestion['category']}")
                print(f"   💰 Current: ${suggestion['current_spending']:.2f} ({suggestion['percentage']:.1f}%)")
                print(f"   💡 Suggestion: {suggestion['suggestion']}")
                print(f"   💚 Potential Savings: ${suggestion['potential_savings']:.2f}")
                print()
        print("-" * 65)
    
    def display_transactions(self, limit=10):
        """Display recent transactions"""
        if not self.current_data:
            print("❌ No data available. Generate demo data first.")
            return
            
        transactions = self.current_data.get('transactions', [])
        
        print(f"\n📝 RECENT TRANSACTIONS (Last {limit})")
        print("-" * 80)
        print(f"{'Date':<12} {'Category':<15} {'Description':<25} {'Amount':>10}")
        print("-" * 80)
        
        # Sort by date and show recent ones
        sorted_transactions = sorted(transactions, key=lambda x: x['date'], reverse=True)
        
        for transaction in sorted_transactions[:limit]:
            date = transaction['date'][:10]
            category = transaction['category'][:14]
            description = transaction['description'][:24]
            amount = f"${transaction['amount']:.2f}"
            
            print(f"{date:<12} {category:<15} {description:<25} {amount:>10}")
        
        print("-" * 80)
    
    def export_data(self, filename=None):
        """Export data to JSON file"""
        if not self.current_data:
            print("❌ No data available. Generate demo data first.")
            return
            
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"finance_analysis_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.current_data, f, indent=2, default=str)
            print(f"✅ Data exported to {filename}")
        except Exception as e:
            print(f"❌ Export failed: {e}")
    
    def run_interactive(self):
        """Run interactive CLI"""
        self.print_banner()
        
        while True:
            print("\n🔧 Available Commands:")
            print("1. Generate Demo Data")
            print("2. Show Summary")
            print("3. Show Categories")
            print("4. Show Anomalies")
            print("5. Show Suggestions")
            print("6. Show Transactions")
            print("7. Export Data")
            print("8. Quit")
            
            try:
                choice = input("\n👉 Enter your choice (1-8): ").strip()
                
                if choice == '1':
                    self.generate_demo_data()
                elif choice == '2':
                    self.display_summary()
                elif choice == '3':
                    self.display_categories()
                elif choice == '4':
                    self.display_anomalies()
                elif choice == '5':
                    self.display_suggestions()
                elif choice == '6':
                    limit = input("How many transactions to show? (default 10): ").strip()
                    limit = int(limit) if limit.isdigit() else 10
                    self.display_transactions(limit)
                elif choice == '7':
                    filename = input("Export filename (press Enter for auto): ").strip()
                    self.export_data(filename if filename else None)
                elif choice == '8':
                    print("\n👋 Thanks for using Personal Finance Agent!")
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main function"""
    cli = FinanceCLI()
    
    # Check if arguments provided for direct commands
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'demo':
            cli.print_banner()
            data = cli.generate_demo_data()
            cli.display_summary()
            cli.display_categories()
            cli.display_anomalies()
            cli.display_suggestions()
        elif command == 'quick':
            cli.print_banner()
            cli.generate_demo_data()
            cli.display_summary()
            cli.display_categories()
        else:
            print("Available commands: demo, quick")
            print("Or run without arguments for interactive mode")
    else:
        # Interactive mode
        cli.run_interactive()

if __name__ == "__main__":
    main()