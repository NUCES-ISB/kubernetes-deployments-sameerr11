from flask import Flask, jsonify
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database connection parameters from environment variables
DB_HOST = os.environ.get('POSTGRES_HOST', 'postgres')
DB_NAME = os.environ.get('POSTGRES_DB', 'postgres')
DB_USER = os.environ.get('POSTGRES_USER', 'postgres')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'postgres')

def get_db_connection():
    """Create a database connection."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        app.logger.error(f"Database connection error: {e}")
        return None

@app.route('/')
def index():
    """Root endpoint to verify the app is running."""
    return jsonify({
        'status': 'ok',
        'message': 'Flask application is running!'
    })

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'message': 'Service is healthy'
    })

@app.route('/db-test')
def db_test():
    """Test database connection."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('SELECT version();')
            version = cursor.fetchone()
            cursor.close()
            conn.close()
            return jsonify({
                'status': 'ok',
                'message': 'Database connection successful',
                'version': version
            })
        except Exception as e:
            if conn:
                conn.close()
            return jsonify({
                'status': 'error',
                'message': f'Database query error: {str(e)}'
            }), 500
    else:
        return jsonify({
            'status': 'error',
            'message': 'Failed to connect to the database'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 