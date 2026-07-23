from flask import Flask, request, jsonify
import mysql.connector
import os
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EasyPay")

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "mysql")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "easypay")


def get_connection(database=None):
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=database
    )


def initialize_database():

    logger.info("Waiting for MySQL...")

    conn = None

    for i in range(30):
        try:
            conn = get_connection()
            logger.info("Connected to MySQL")
            break
        except Exception:
            logger.info(f"MySQL not ready ({i+1}/30)")
            time.sleep(5)

    if conn is None:
        raise Exception("Unable to connect to MySQL")

    cursor = conn.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")

    conn.database = DB_NAME

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (

        id INT AUTO_INCREMENT PRIMARY KEY,

        name VARCHAR(100) NOT NULL,

        email VARCHAR(100) NOT NULL,

        balance DECIMAL(10,2) NOT NULL DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # Add balance column if upgrading an existing DB
    try:
        cursor.execute("""
        ALTER TABLE customers
        ADD COLUMN balance DECIMAL(10,2) NOT NULL DEFAULT 0
        """)
    except Exception:
        pass

    conn.commit()

    cursor.close()
    conn.close()

    logger.info("Database initialized")


initialize_database()


def get_db():

    for i in range(5):
        try:
            return get_connection(DB_NAME)
        except Exception:
            logger.info("Retrying MySQL connection...")
            time.sleep(2)

    raise Exception("Database unavailable")


@app.route("/")
def home():

    return jsonify({
        "application": "EasyPay Backend",
        "version": "1.0",
        "status": "Running"
    })


@app.route("/health")
def health():

    try:
        conn = get_db()
        conn.close()

        return jsonify({
            "status": "UP",
            "database": "Connected"
        }), 200

    except Exception as e:

        return jsonify({
            "status": "DOWN",
            "error": str(e)
        }), 500


@app.route("/customers", methods=["GET"])
def get_customers():

    try:

        conn = get_db()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                name,
                email,
                balance,
                created_at
            FROM customers
            ORDER BY id
        """)

        customers = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(customers), 200

    except Exception as e:

        logger.exception(e)

        return jsonify({
            "message": "Unable to fetch customers"
        }), 500


@app.route("/customers", methods=["POST"])
def add_customer():

    try:

        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        balance = data.get("balance", 0)

        if not name or not email:

            return jsonify({
                "message": "Name and Email are required"
            }), 400

        conn = get_db()

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO customers(
                name,
                email,
                balance
            )
            VALUES(%s,%s,%s)
        """, (name, email, balance))

        conn.commit()

        customer_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({

            "message": "Customer Added",

            "id": customer_id

        }), 201

    except Exception as e:

        logger.exception(e)

        return jsonify({
            "message": "Unable to add customer"
        }), 500


@app.route("/customers/<int:id>", methods=["DELETE"])
def delete_customer(id):

    try:

        conn = get_db()

        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM customers WHERE id=%s",
            (id,)
        )

        if cursor.rowcount == 0:

            cursor.close()
            conn.close()

            return jsonify({
                "message": "Customer not found"
            }), 404

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Customer deleted"
        }), 200

    except Exception as e:

        logger.exception(e)

        return jsonify({
            "message": "Unable to delete customer"
        }), 500


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )