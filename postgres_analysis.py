import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
import seaborn as sns

# ۱. تنظیمات اتصال به دیتابیس PostgreSQL
DB_CONFIG = {
    "dbname": "Ecommerce_crm",
    "user": "postgres",
    "password": "1234",  # رمز عبور شما
    "host": "localhost",
    "port": "5432",
}

try:
    # ۲. ایجاد اتصال به دیتابیس
    conn = psycopg2.connect(**DB_CONFIG)

    # ۳. کوئری SQL برای استخراج مجموع خرید هر مشتری
    query = """
    SELECT 
        c.first_name || ' ' || c.last_name AS full_name,
        c.city,
        COUNT(o.order_id) AS total_orders,
        SUM(o.amount) AS total_spent
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name, c.city
    ORDER BY total_spent DESC;
    """

    # بارگذاری داده‌ها در Pandas DataFrame
    df = pd.read_sql_query(query, conn)

    print("--- Data Successfully Retrieved from PostgreSQL ---")
    print(df)

    # بستن اتصال دیتابیس
    conn.close()

    # ۴. رسم و تنظیمات نمودار میله‌ای (Bar Chart)
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x="full_name", y="total_spent", palette="viridis")

    plt.title("Total Spent per Customer (PostgreSQL Data)", fontsize=14)
    plt.xlabel("Customer Name", fontsize=12)
    plt.ylabel("Total Spent (€)", fontsize=12)

    plt.tight_layout()

    # ۵. ذخیره تصویر نمودار در پوشه پروژه
    plt.savefig("customer_spending_chart.png", dpi=300)
    print("\n--- Chart saved successfully as customer_spending_chart.png ---")

    # نمایش نمودار روی صفحه
    plt.show()

except Exception as e:
    print(f"Error connecting to database: {e}")