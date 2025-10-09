from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector
from datetime import datetime
import os
from decimal import Decimal

app = Flask(__name__)

# AWS RDS Configuration
DB_CONFIG = {
    'host': 'database-4.c3wwio6c8bng.eu-north-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'Janhvi123',
    'database': 'expenses_db',  # <-- use this
    'port': 3306,
    'connect_timeout': 10
}

def get_db_connection():
    """Get database connection"""
    try:
        print("Connecting to RDS...")
        connection = mysql.connector.connect(**DB_CONFIG)
        print("Connected successfully!")
        return connection
    except mysql.connector.Error as e:
        print(f"❌ Error connecting to database: {e}")
        return None

        return None

def init_database():
    """Initialize database tables"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        
        # Create expenses table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            item VARCHAR(255) NOT NULL,
            cost DECIMAL(10, 2) NOT NULL,
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        try:
            cursor.execute(create_table_query)
            connection.commit()
            print("Database initialized successfully")
        except mysql.connector.Error as e:
            print(f"Error creating table: {e}")
        finally:
            cursor.close()
            connection.close()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/add_expense', methods=['POST'])
def add_expense():
    """Add new expense"""
    try:
        item = request.form.get('item')
        cost = float(request.form.get('cost'))
        date = request.form.get('date')
        
        if not item or not cost or not date:
            return jsonify({'error': 'All fields are required'}), 400
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            
            insert_query = "INSERT INTO expenses (item, cost, date) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (item, cost, date))
            connection.commit()
            
            cursor.close()
            connection.close()
            
            return jsonify({'success': True, 'message': 'Expense added successfully'})
        else:
            return jsonify({'error': 'Database connection failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_expenses')
def get_expenses():
    """Get last 5 expenses and total"""
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            
            # Get last 5 expenses (now including ID)
            cursor.execute("""
                SELECT id, item, cost, date 
                FROM expenses 
                ORDER BY created_at DESC 
                LIMIT 5
            """)
            recent_expenses = cursor.fetchall()
            
            # Get total expenses
            cursor.execute("SELECT SUM(cost) as total FROM expenses")
            total_result = cursor.fetchone()
            total = float(total_result['total']) if total_result['total'] else 0
            
            cursor.close()
            connection.close()
            
            # Convert Decimal to float for JSON serialization
            for expense in recent_expenses:
                expense['cost'] = float(expense['cost'])
                expense['date'] = expense['date'].strftime('%Y-%m-%d')
            
            return jsonify({
                'recent_expenses': recent_expenses,
                'total': total
            })
        else:
            return jsonify({'error': 'Database connection failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        connection = get_db_connection()
        if connection:
            connection.close()
            return jsonify({'status': 'healthy', 'database': 'connected'})
        else:
            return jsonify({'status': 'unhealthy', 'database': 'disconnected'}), 500
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/delete_expense/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """Delete an expense by ID"""
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            
            # Delete the expense
            delete_query = "DELETE FROM expenses WHERE id = %s"
            cursor.execute(delete_query, (expense_id,))
            connection.commit()
            
            affected_rows = cursor.rowcount
            cursor.close()
            connection.close()
            
            if affected_rows > 0:
                return jsonify({'success': True, 'message': 'Expense deleted successfully'})
            else:
                return jsonify({'error': 'Expense not found'}), 404
        else:
            return jsonify({'error': 'Database connection failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask app...")
    init_database()
    print("Database initialized, starting server...")
    app.run(debug=True, host='0.0.0.0', port=5000)

