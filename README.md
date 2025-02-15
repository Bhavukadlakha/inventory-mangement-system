# 📦 Inventory Management System

A **Python-based Inventory Management System** that helps track stock, sales, and employee performance efficiently. Built using **SQLite** for data storage, it includes advanced features like billing, sales tracking, and a planned AI-powered sales prediction model.

## 🚀 Features

✅ **Stock Management** – Track available products, update inventory, and receive restock alerts.  
✅ **Billing System** – Generate and save bills, apply discounts, and manage transactions.  
✅ **Sales Tracking** – Monitor total sales for the day, week, and month with filtering options.  
✅ **Employee Sales Tracking** – Track individual employee sales and discount percentages.  
✅ **Incentive Calculation** – Calculate incentives based on employee sales performance.  
✅ **Upcoming Features:**
   - **AI-Powered Sales Prediction** – Forecast stock needs using data analytics.
   - **Customer Chatbot** – Auto-reply to customer queries on WhatsApp.
   - **Sales Dashboard** – Visualize sales data dynamically using Plotly.

## 🛠️ Technologies Used

- **Python** (Tkinter for GUI, Pandas, Matplotlib, Plotly)
- **SQLite** (Database for storing inventory, sales, and employee data)
- **Plotly** (For interactive data visualization)
- **yowsup** (For WhatsApp chatbot integration)

## 📂 Project Structure

```
📦 inventory-management-system
├── 📂 database
│   ├── products.xlsx            # Product inventory data
│   ├── bill.db                  # Billing database
│   ├── bill_products.db          # Sales records
│   ├── employees.db              # Employee details
├── 📂 src
│   ├── main.py                   # Main application file
│   ├── billing.py                 # Billing module
│   ├── sales_tracking.py          # Sales tracking UI
│   ├── chatbot.py                 # WhatsApp chatbot (Upcoming)
│   ├── ai_sales_prediction.py     # AI model for sales forecasting (Upcoming)
├── 📜 README.md
├── 📜 requirements.txt             # List of dependencies
└── 📜 LICENSE
```

## 🖥️ Installation & Setup

1. **Clone the repository:**  
   ```bash
   git clone https://github.com/your-username/inventory-management-system.git
   cd inventory-management-system
   ```

2. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**  
   ```bash
   python src/main.py
   ```

## 📊 Screenshots (Upcoming)

*Will be added after UI enhancements.*

## 🤝 Contributing

Feel free to submit issues and pull requests! Contributions are welcome. 😊

## 📜 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.
