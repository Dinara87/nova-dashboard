import requests
import json

# ===ДАННЫЕ ===
API_KEY = "aYnq353mhsgFFRPowywaW1FWdHIn0GAl"
CRM_URL = "https://uzakbaevadinara87.retailcrm.ru"
SUPABASE_URL = "https://qkiubeqmdysqvleyeqtw.supabase.co"      
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFraXViZXFtZHlzcXZsZXllcXR3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU4MTQxODAsImV4cCI6MjA5MTM5MDE4MH0.m22tmU1_TF34kMIAI_CCwijz9tSlwKE_AaNfzrcHB-E"


# Получаем заказы из RetailCRM
print("Получаем заказы из RetailCRM...")
response = requests.get(
    f"{CRM_URL}/api/v5/orders",
    params={"apiKey": API_KEY, "limit": 100}
)
data = response.json()
orders = data.get("orders", [])
print(f"Найдено заказов: {len(orders)}")

# Загружаем в Supabase
print("Загружаем в Supabase...")
success = 0
errors = 0

for order in orders:
    # Считаем сумму заказа
    total = sum(
        item.get("initialPrice", 0) * item.get("quantity", 1)
        for item in order.get("items", [])
    )

    custom = order.get("customFields", {})
    utm = custom.get("utm_source", "") if isinstance(custom, dict) else ""

    row = {
        "crm_id": order.get("id"),
        "first_name": order.get("firstName", ""),
        "last_name": order.get("lastName", ""),
        "phone": order.get("phone", ""),
        "city": order.get("delivery", {}).get("address", {}).get("city", ""),
        "total_sum": total,
        "status": order.get("status", ""),
        "utm_source": utm
    }

    res = requests.post(
        f"{SUPABASE_URL}/rest/v1/orders",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        },
        data=json.dumps(row)
    )

    if res.status_code == 201:
        success += 1
        print(f"✅ {row['first_name']} {row['last_name']} — {total} ₸")
    else:
        errors += 1
        print(f"❌ Ошибка: {res.text}")

print(f"\nГотово! Успешно: {success}, Ошибок: {errors}")