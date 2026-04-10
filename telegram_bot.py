import requests
import time

# === ВСТАВЬ СВОИ ДАННЫЕ ===
API_KEY = "aYnq353mhsgFFRPowywaW1FWdHIn0GAl"
CRM_URL = "https://uzakbaevadinara87.retailcrm.ru"
TG_TOKEN = "8671800123:AAF5xfrqEDLcqDcYbT9kwR2uOCdTxnVLmfk"
TG_CHAT_ID = "336116161"
# ==========================

seen_ids = set()

def get_orders():
    res = requests.get(
        f"{CRM_URL}/api/v5/orders",
        params={"apiKey": API_KEY, "limit": 100}
    )
    return res.json().get("orders", [])

def send_telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        data={"chat_id": TG_CHAT_ID, "text": message}
    )

def calc_total(order):
    return order.get("summ", 0)

print("Бот запущен! Слежу за заказами...")

for order in get_orders():
    seen_ids.add(order["id"])

print(f"Уже существующих заказов: {len(seen_ids)}")

while True:
    orders = get_orders()
    for order in orders:
        if order["id"] not in seen_ids:
            seen_ids.add(order["id"])
            total = calc_total(order)
            print(f"🆕 Новый заказ найден: id={order['id']}, сумма={total}")
            if total > 50000:
                msg = (
                    f"🔔 Новый крупный заказ!\n"
                    f"👤 {order.get('firstName')} {order.get('lastName')}\n"
                    f"💰 Сумма: {total:,} ₸\n"
                    f"📍 Город: {order.get('delivery', {}).get('address', {}).get('city', '—')}"
                )
                send_telegram(msg)
                print(f"✅ Отправлено уведомление: {total} ₸")
            else:
                print(f"⚠️ Сумма меньше 50,000 — уведомление не отправляем")
    print("🔄 Проверка завершена, жду 30 сек...")
    time.sleep(30)
