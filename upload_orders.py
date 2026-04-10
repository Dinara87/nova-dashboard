import requests
import json
import time

API_KEY = "aYnq353mhsgFFRPowywaW1FWdHIn0GAl"  
CRM_URL = "https://uzakbaevadinara87.retailcrm.ru"

with open("mock_orders.json", "r", encoding="utf-8") as f:
    orders = json.load(f)

success = 0
errors = 0

for i, order in enumerate(orders):
    order_clean = order.copy()
    order_clean.pop("orderType", None)
    order_clean.pop("orderMethod", None)

    response = requests.post(
        f"{CRM_URL}/api/v5/orders/create",
        data={
            "apiKey": API_KEY,
            "order": json.dumps(order_clean)
        }
    )
    result = response.json()
    if result.get("success"):
        success += 1
        print(f"[{i+1}/50] ✅ {order['firstName']} {order['lastName']}")
    else:
        errors += 1
        print(f"[{i+1}/50] ❌ Ошибка: {result}")
    time.sleep(0.3)

print(f"\nГотово! Успешно: {success}, Ошибок: {errors}")