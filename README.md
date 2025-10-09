# Expense Tracker

A simple single-page expense tracking application built with HTML, CSS, Python (Flask), and MySQL on AWS RDS.

## Features

- 📝 Add daily expenses with item description, cost, and date
- 💰 View total expenses
- 📊 Display last 5 recent expenses
- 🎨 Responsive design with modern UI
- ☁️ AWS RDS database integration
- 🔄 Real-time updates

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. AWS RDS Setup

1. **Create MySQL Database on AWS RDS:**
   - Go to AWS RDS Console
   - Create a new MySQL database instance
   - Note down the endpoint, username, password, and database name

2. **Configure Security Group:**
   - Allow inbound connections on port 3306 from your IP
   - Or allow from 0.0.0.0/0 for testing (not recommended for production)

3. **Create Database:**
   - Connect to your RDS instance using MySQL client
   - Create a database named `expense_tracker`

### 3. Environment Configuration

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` file with your AWS RDS credentials:
   ```
   RDS_HOST=your-rds-endpoint.region.rds.amazonaws.com
   RDS_USER=admin
   RDS_PASSWORD=your-secure-password
   RDS_DATABASE=expense_tracker
   RDS_PORT=3306
   ```

### 4. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## File Structure

```
FA2-cc/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── templates/
│   └── index.html        # Main dashboard HTML
├── static/
│   └── style.css         # CSS styling
└── README.md             # This file
```

## Database Schema

The application creates a table named `expenses` with the following structure:

```sql
CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item VARCHAR(255) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Endpoints

- `GET /` - Main dashboard page
- `POST /add_expense` - Add a new expense
- `GET /get_expenses` - Get recent expenses and total
- `GET /health` - Health check endpoint

## Security Notes

- Never commit your `.env` file to version control
- Use strong passwords for your RDS instance
- Configure proper security groups for your RDS instance
- Consider using IAM roles instead of hardcoded credentials in production

## Troubleshooting

1. **Database Connection Issues:**
   - Verify your RDS endpoint and credentials
   - Check security group settings
   - Ensure your IP is whitelisted

2. **Module Import Errors:**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`

3. **Application Not Starting:**
   - Check if port 5000 is available
   - Verify environment variables are set correctly

## Future Enhancements

- Add expense categories
- Implement date range filtering
- Add expense editing/deletion
- Export data to CSV
- User authentication
- Charts and visualizations
