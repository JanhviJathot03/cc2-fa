from flask import Flask, render_template, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# AWS RDS Configuration
DB_CONFIG = {
    'host': 'database-6.c3wwio6c8bng.eu-north-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'janhvi123',
    'database': 'shopping_db',
    'port': 3306,
    'connect_timeout': 10
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def init_database():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS shopping_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            item_name VARCHAR(255) NOT NULL,
            quantity INT NOT NULL DEFAULT 1,
            category VARCHAR(100) NOT NULL,
            priority VARCHAR(20) NOT NULL,
            purchased BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        try:
            cursor.execute(create_table_query)
            connection.commit()
        except mysql.connector.Error as e:
            print(f"Error creating table: {e}")
        finally:
            cursor.close()
            connection.close()

@app.route('/')
def index():
    return render_template('shopping.html')

@app.route('/add_item', methods=['POST'])
def add_item():
    try:
        item_name = request.form.get('item_name')
        quantity = int(request.form.get('quantity', 1))
        category = request.form.get('category')
        priority = request.form.get('priority')
        if not item_name or not category or not priority:
            return jsonify({'error': 'Required fields missing'}), 400
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO shopping_items (item_name, quantity, category, priority) VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (item_name, quantity, category, priority))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_items')
def get_items():
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT id, item_name, quantity, category, priority, purchased FROM shopping_items ORDER BY created_at DESC LIMIT 5
            """)
            recent_items = cursor.fetchall()
            cursor.execute("""
                SELECT category, COUNT(*) as count FROM shopping_items GROUP BY category
            """)
            categories = cursor.fetchall()
            cursor.execute("SELECT COUNT(*) as pending FROM shopping_items WHERE purchased = 0")
            pending = cursor.fetchone()['pending']
            cursor.close()
            connection.close()
            return jsonify({
                'recent_items': recent_items,
                'categories': categories,
                'pending': pending
            })
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/toggle_purchased/<int:item_id>', methods=['PUT'])
def toggle_purchased(item_id):
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT purchased FROM shopping_items WHERE id = %s", (item_id,))
            result = cursor.fetchone()
            if not result:
                return jsonify({'error': 'Item not found'}), 404
            new_status = 1 if result[0] == 0 else 0
            cursor.execute("UPDATE shopping_items SET purchased = %s WHERE id = %s", (new_status, item_id))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'success': True, 'purchased': bool(new_status)})
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM shopping_items WHERE id = %s", (item_id,))
            connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            connection.close()
            if affected_rows > 0:
                return jsonify({'success': True})
            else:
                return jsonify({'error': 'Item not found'}), 404
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
