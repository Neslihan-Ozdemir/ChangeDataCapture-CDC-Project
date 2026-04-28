import time
import mysql.connector
from pymongo import MongoClient

mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="************",
    database="cdc_db",
    autocommit=True
)

mysql_cursor = mysql_conn.cursor(dictionary=True)


mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["cdc_logs"]
mongo_collection = mongo_db["changes"]

print("CDC uygulaması çalışıyor... (MySQL -> MongoDB)")

def fetch_new_logs():

    query = """
        SELECT log_id, operation, table_name, order_id, customer_id,
               product, amount, status, changed_at
        FROM Orders_log
        WHERE transferred = 0
        ORDER BY log_id ASC
    """
    mysql_cursor.execute(query)
    return mysql_cursor.fetchall()

def mark_log_as_transferred(log_id):

    update_query = "UPDATE Orders_log SET transferred = 1 WHERE log_id = %s"
    mysql_cursor.execute(update_query, (log_id,))
    mysql_conn.commit()

def fetch_new_customer_logs():
        query = """
            SELECT log_id, operation, table_name, customer_id, name, email, changed_at
            FROM Customers_log
            WHERE transferred = 0
            ORDER BY log_id ASC
        """
        mysql_cursor.execute(query)
        return mysql_cursor.fetchall()

def mark_customer_log_as_transferred(log_id):
    update_query = "UPDATE Customers_log SET transferred = 1 WHERE log_id = %s"
    mysql_cursor.execute(update_query, (log_id,))
    mysql_conn.commit()


def transfer_logs_to_mongo():
    logs = fetch_new_logs()

    if not logs:
        print("Yeni log kaydı yok.")


    for log in logs:
        doc = {
            "operation": log["operation"],
            "table": log["table_name"],
            "order_id": log["order_id"],
            "customer_id": log["customer_id"],
            "product": log["product"],
            "amount": float(log["amount"]) if log["amount"] is not None else None,
            "status": log["status"],
            "changed_at": log["changed_at"].isoformat() if log["changed_at"] else None
        }


        mongo_collection.insert_one(doc)
        print(f"MongoDB'ye aktarıldı → Orders_log log_id={log['log_id']} operation={log['operation']}")

        mark_log_as_transferred(log["log_id"])


    # --- Customers_log aktarımı ---
    customer_logs = fetch_new_customer_logs()

    for log in customer_logs:
        doc = {
            "operation": log["operation"],
            "table": log["table_name"],
            "customer_id": log["customer_id"],
            "name": log["name"],
            "email": log["email"],
            "changed_at": log["changed_at"].isoformat() if log["changed_at"] else None
        }

        mongo_collection.insert_one(doc)
        print(f"MongoDB'ye aktarıldı → Customers_log log_id={log['log_id']} operation={log['operation']}")

        mark_customer_log_as_transferred(log["log_id"])


if __name__ == "__main__":
    try:
        while True:
            transfer_logs_to_mongo()
            time.sleep(3)
    except KeyboardInterrupt:
        print("CDC uygulaması durduruldu.")
    finally:
        mysql_cursor.close()
        mysql_conn.close()
        mongo_client.close()