import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import plaid
from plaid.api import plaid_api
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from plaid.configuration import Configuration
from plaid.api_client import ApiClient
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Plaid configuration
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')  # sandbox, development, or production

# Configure Plaid client
configuration = Configuration(
    host=getattr(plaid.Environment, PLAID_ENV, plaid.Environment.Sandbox),
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    }
)
api_client = ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

class FinanceAgent:
    def __init__(self):
        self.categories = {
            'Food and Drink': ['restaurant', 'cafe', 'grocery', 'food', 'dining'],
            'Transportation': ['gas', 'uber', 'lyft', 'taxi', 'parking', 'metro', 'bus'],
            'Shopping': ['amazon', 'target', 'walmart', 'mall', 'store', 'retail'],
            'Entertainment': ['netflix', 'spotify', 'movie', 'concert', 'game', 'entertainment'],
            'Bills & Utilities': ['electric', 'gas bill', 'water', 'internet', 'phone', 'utility'],
            'Healthcare': ['doctor', 'pharmacy', 'hospital', 'medical', 'health'],
            'Travel': ['hotel', 'airline', 'booking', 'travel', 'vacation'],
            'Other': []
        }
        
    def categorize_transaction(self, description, amount, merchant_name=None):
        """Categorize transaction based on description and merchant"""
        description_lower = description.lower()
        merchant_lower = merchant_name.lower() if merchant_name else ""
        
        for category, keywords in self.categories.items():
            if category == 'Other':
                continue
            for keyword in keywords:
                if keyword in description_lower or keyword in merchant_lower:
                    return category
        return 'Other'
    
    def detect_anomalies(self, transactions_df):
        """Detect spending anomalies using statistical methods"""
        if len(transactions_df) < 10:
            return []
        
        # Group by category and calculate spending patterns
        anomalies = []
        
        for category in transactions_df['category'].unique():
            category_transactions = transactions_df[transactions_df['category'] == category]
            amounts = category_transactions['amount'].abs()
            
            if len(amounts) < 3:
                continue
                
            # Use IQR method for anomaly detection
            Q1 = amounts.quantile(0.25)
            Q3 = amounts.quantile(0.75)
            IQR = Q3 - Q1
            threshold = Q3 + 1.5 * IQR
            
            anomalous_transactions = category_transactions[amounts > threshold]
            
            for _, transaction in anomalous_transactions.iterrows():
                anomalies.append({
                    'transaction_id': transaction['transaction_id'],
                    'description': transaction['description'],
                    'amount': transaction['amount'],
                    'category': category,
                    'date': transaction['date'],
                    'reason': f'Unusually high spending in {category} (${transaction["amount"]:.2f} vs avg ${amounts.mean():.2f})'
                })
        
        return anomalies
    
    def analyze_spending_patterns(self, transactions_df):
        """Analyze spending patterns and provide insights"""
        if transactions_df.empty:
            return {}
        
        # Calculate trends
        insights = {
            'total_spending': float(transactions_df['amount'].sum()),
            'avg_transaction': float(transactions_df['amount'].mean()),
            'category_breakdown': {},
            'monthly_trends': {},
            'top_merchants': {}
        }
        
        # Category breakdown
        category_spending = transactions_df.groupby('category')['amount'].sum().abs()
        insights['category_breakdown'] = category_spending.to_dict()
        
        # Monthly trends (only if date column exists)
        if 'date' in transactions_df.columns:
            transactions_df['month'] = pd.to_datetime(transactions_df['date']).dt.to_period('M')
            monthly_totals = transactions_df.groupby('month')['amount'].sum().abs()
            insights['monthly_trends'] = {str(k): float(v) for k, v in monthly_totals.items()}
        
        # Top merchants
        if 'merchant_name' in transactions_df.columns:
            top_merchants = transactions_df.groupby('merchant_name')['amount'].sum().abs().nlargest(5)
            insights['top_merchants'] = top_merchants.to_dict()
        
        return insights
    
    def suggest_budget_tweaks(self, transactions_df, current_income=None):
        """Suggest budget optimizations based on spending patterns"""
        if transactions_df.empty:
            return []
        
        suggestions = []
        category_spending = transactions_df.groupby('category')['amount'].sum().abs()
        total_spending = category_spending.sum()
        
        # Analyze each category
        for category, amount in category_spending.items():
            percentage = (amount / total_spending) * 100
            
            if category == 'Food and Drink' and percentage > 25:
                suggestions.append({
                    'category': category,
                    'current_spending': float(amount),
                    'percentage': float(percentage),
                    'suggestion': 'Consider meal planning and cooking at home more often',
                    'potential_savings': float(amount * 0.2)
                })
            elif category == 'Entertainment' and percentage > 15:
                suggestions.append({
                    'category': category,
                    'current_spending': float(amount),
                    'percentage': float(percentage),
                    'suggestion': 'Look for free entertainment options or subscription optimizations',
                    'potential_savings': float(amount * 0.15)
                })
            elif category == 'Shopping' and percentage > 20:
                suggestions.append({
                    'category': category,
                    'current_spending': float(amount),
                    'percentage': float(percentage),
                    'suggestion': 'Implement a 24-hour rule before purchases and use shopping lists',
                    'potential_savings': float(amount * 0.25)
                })
        
        # Income-based suggestions
        if current_income:
            spending_ratio = total_spending / current_income
            if spending_ratio > 0.8:
                suggestions.append({
                    'category': 'Overall',
                    'current_spending': float(total_spending),
                    'percentage': float(spending_ratio * 100),
                    'suggestion': 'Your spending is high relative to income. Consider reducing discretionary expenses',
                    'potential_savings': float(total_spending * 0.1)
                })
        
        return suggestions

# Initialize the finance agent
finance_agent = FinanceAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/create_link_token', methods=['POST'])
def create_link_token():
    """Create a link token for Plaid Link"""
    try:
        request_data = LinkTokenCreateRequest(
            products=[Products('transactions')],
            client_name="Personal Finance Agent",
            country_codes=[CountryCode('US')],
            language='en',
            user=LinkTokenCreateRequestUser(client_user_id='user_' + str(datetime.now().timestamp()))
        )
        response = client.link_token_create(request_data)
        return jsonify({'link_token': response['link_token']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/exchange_public_token', methods=['POST'])
def exchange_public_token():
    """Exchange public token for access token"""
    try:
        public_token = request.json.get('public_token')
        
        request_data = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = client.item_public_token_exchange(request_data)
        
        access_token = response['access_token']
        
        # Store access token (in production, store securely in database)
        # For demo purposes, we'll store in session or return to client
        return jsonify({
            'access_token': access_token,
            'item_id': response['item_id']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts', methods=['POST'])
def get_accounts():
    """Get account information"""
    try:
        access_token = request.json.get('access_token')
        
        request_data = AccountsGetRequest(access_token=access_token)
        response = client.accounts_get(request_data)
        
        accounts = []
        for account in response['accounts']:
            accounts.append({
                'account_id': account['account_id'],
                'name': account['name'],
                'type': account['type'],
                'subtype': account['subtype'],
                'balance': account['balances']['current']
            })
        
        return jsonify({'accounts': accounts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions', methods=['POST'])
def get_transactions():
    """Get and analyze transactions"""
    try:
        access_token = request.json.get('access_token')
        days_back = request.json.get('days', 30)
        
        start_date = datetime.now() - timedelta(days=days_back)
        end_date = datetime.now()
        
        request_data = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date.date(),
            end_date=end_date.date()
        )
        response = client.transactions_get(request_data)
        
        # Process transactions
        transactions = []
        for transaction in response['transactions']:
            categorized = finance_agent.categorize_transaction(
                transaction['name'],
                transaction['amount'],
                transaction.get('merchant_name', '')
            )
            
            transactions.append({
                'transaction_id': transaction['transaction_id'],
                'account_id': transaction['account_id'],
                'amount': float(transaction['amount']),
                'date': transaction['date'].isoformat(),
                'description': transaction['name'],
                'merchant_name': transaction.get('merchant_name', ''),
                'category': categorized,
                'original_category': transaction['category'][0] if transaction['category'] else 'Other'
            })
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(transactions)
        
        # Perform analysis
        anomalies = finance_agent.detect_anomalies(df)
        insights = finance_agent.analyze_spending_patterns(df)
        suggestions = finance_agent.suggest_budget_tweaks(df)
        
        return jsonify({
            'transactions': transactions,
            'anomalies': anomalies,
            'insights': insights,
            'budget_suggestions': suggestions,
            'total_transactions': len(transactions)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/demo_data', methods=['GET'])
def get_demo_data():
    """Generate demo data for testing without Plaid connection"""
    import random
    
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
    
    return jsonify({
        'transactions': demo_transactions,
        'anomalies': anomalies,
        'insights': insights,
        'budget_suggestions': suggestions,
        'total_transactions': len(demo_transactions),
        'demo_mode': True
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)