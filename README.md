# Personal Finance Agent 🏦💡

A smart, AI-powered personal finance management system that connects to your bank accounts via Plaid API to provide intelligent spending insights, anomaly detection, and personalized budget recommendations.

## ✨ Features

- **🔗 Secure Bank Integration**: Connect bank accounts securely using Plaid API
- **📊 Smart Categorization**: Automatically categorize transactions using intelligent keyword matching
- **🚨 Anomaly Detection**: Detect unusual spending patterns using statistical analysis (IQR method)
- **💡 Budget Optimization**: Get personalized suggestions to optimize your spending habits
- **📈 Visual Analytics**: Beautiful charts and insights for spending patterns and trends
- **🎮 Demo Mode**: Try the app with sample data without connecting real accounts
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile devices

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Pandas, Scikit-learn
- **Frontend**: HTML5, JavaScript, TailwindCSS, Chart.js
- **API Integration**: Plaid API for bank connections
- **Data Analysis**: Pandas for data processing, statistical anomaly detection
- **Visualization**: Chart.js for interactive charts and graphs

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- A Plaid account (free sandbox available)
- Git

### 1. Clone the Repository

```bash
git clone <repository-url>
cd personal-finance-agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Copy the example environment file and configure your Plaid credentials:

```bash
cp .env.example .env
```

Edit `.env` with your Plaid credentials:

```env
PLAID_CLIENT_ID=your_plaid_client_id
PLAID_SECRET=your_plaid_secret_key
PLAID_ENV=sandbox
```

### 4. Get Plaid API Credentials

1. Sign up for a free account at [Plaid Dashboard](https://dashboard.plaid.com/signup)
2. Create a new app in the dashboard
3. Copy your Client ID and Secret Key
4. For development, use the sandbox environment

### 5. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 🎯 How It Works

### 1. **Bank Connection**
- Uses Plaid Link to securely connect to 11,000+ financial institutions
- Fetches transaction data for the last 30 days
- No sensitive banking credentials stored on our servers

### 2. **Smart Categorization**
The system automatically categorizes transactions using intelligent keyword matching:
- **Food & Drink**: Restaurants, cafes, grocery stores
- **Transportation**: Gas, rideshare, public transport
- **Shopping**: Retail stores, online purchases
- **Entertainment**: Streaming services, movies, concerts
- **Bills & Utilities**: Electric, internet, phone bills
- **Healthcare**: Medical expenses, pharmacy
- **Travel**: Hotels, airlines, bookings

### 3. **Anomaly Detection**
Uses statistical analysis (Interquartile Range method) to detect unusual spending:
- Compares each transaction to historical patterns in the same category
- Flags transactions that are significantly higher than normal
- Provides context about why the transaction is considered anomalous

### 4. **Budget Suggestions**
Analyzes spending patterns to provide actionable recommendations:
- **High Food Spending**: Suggests meal planning and home cooking
- **Entertainment Overages**: Recommends free alternatives and subscription audits
- **Excessive Shopping**: Implements 24-hour purchase rules
- **Income Ratio Analysis**: Warns if spending exceeds 80% of income

## 📱 User Interface

### Dashboard Features

- **Summary Cards**: Total spending, transaction count, averages, anomaly alerts
- **Interactive Charts**: 
  - Doughnut chart for category breakdown
  - Line chart for monthly spending trends
- **Anomaly Alerts**: Highlighted unusual transactions with explanations
- **Budget Suggestions**: Actionable recommendations with potential savings
- **Transaction History**: Searchable, sortable list of recent transactions

### Demo Mode

Try the application without connecting real bank accounts:
- Click "Try Demo" to load sample transaction data
- Explore all features with realistic financial data
- Perfect for testing and demonstration purposes

## 🔒 Security & Privacy

- **No Data Storage**: Transaction data is processed in real-time, not stored
- **Plaid Security**: Bank-level security through Plaid's infrastructure
- **Local Processing**: All analysis happens on your server
- **Environment Variables**: Sensitive credentials kept in environment files

## 🛠️ Development

### Project Structure

```
personal-finance-agent/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── templates/
│   └── index.html        # Main web interface
├── static/
│   ├── css/             # Custom stylesheets
│   └── js/              # Custom JavaScript
└── README.md            # This file
```

### Key Components

- **FinanceAgent Class**: Core logic for categorization, anomaly detection, and analysis
- **Flask Routes**: API endpoints for Plaid integration and data processing
- **Frontend**: Responsive single-page application with real-time updates

### Extending the System

1. **Add New Categories**: Update the `categories` dictionary in `FinanceAgent`
2. **Improve Anomaly Detection**: Modify the `detect_anomalies` method
3. **Custom Suggestions**: Enhance the `suggest_budget_tweaks` method
4. **New Visualizations**: Add charts in the frontend JavaScript

## 📊 API Endpoints

- `GET /` - Main dashboard interface
- `POST /api/create_link_token` - Initialize Plaid Link
- `POST /api/exchange_public_token` - Exchange tokens
- `POST /api/accounts` - Get account information
- `POST /api/transactions` - Fetch and analyze transactions
- `GET /api/demo_data` - Load sample data for demo

## 🚀 Deployment

### Production Considerations

1. **Environment**: Set `PLAID_ENV=production` for live data
2. **HTTPS**: Use SSL certificates for secure communication
3. **Database**: Consider adding persistent storage for user preferences
4. **Caching**: Implement caching for improved performance
5. **Authentication**: Add user authentication for multi-user support

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the [Plaid API documentation](https://plaid.com/docs/)
2. Verify your environment variables are set correctly
3. Ensure you're using the correct Plaid environment (sandbox/development/production)
4. Check the Flask console for error messages

## 🎉 Demo

Visit the live demo: [Personal Finance Agent Demo](your-demo-url)

Or run locally and click "Try Demo" to see sample data in action!

---

**Built with ❤️ for better financial awareness and smarter spending decisions.**
