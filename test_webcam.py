import cv2
from ultralytics import YOLO
from collections import defaultdict

# 📱 Replace with your DroidCam IP
droidcam_url = "http://10.103.190.109:4747/video"

# 📷 Connect to mobile camera
cap = cv2.VideoCapture(droidcam_url)

# 🔍 Load YOLOv5 model (or YOLOv8 if using that)
model = YOLO("yolov5s.pt")  # You can use 'yolov8n.pt' if you prefer

# 🏷️ Define fixed items with prices (you can update this list)
item_prices = {
    'bottle': 30,
    'book': 50,
    'cell phone': 100,
    'remote': 40,
    'cup': 25
}

# 🛒 Track cart items
cart = defaultdict(int)

print("🔁 Smart Checkout Started... Show item to mobile camera.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame from mobile camera")
        break

    # 🧠 Detect items with YOLO
    results = model(frame)[0]
    names = model.model.names

    for box in results.boxes:
        cls_id = int(box.cls[0])
        class_name = names[cls_id]

        if class_name in item_prices:
            cart[class_name] += 1

    # 🖼️ Show the feed
    cv2.imshow("📱 Mobile Camera - Press Q to stop", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ✅ Final Bill
print("\n🧾 Final Bill:")
total = 0
for item, qty in cart.items():
    price = item_prices[item] * qty
    total += price
    print(f"- {item.title()} x{qty} → ₹{price}")

print(f"🟢 Total Payable: ₹{total}")

# 🔚 Cleanup
cap.release()
cv2.destroyAllWindows()
