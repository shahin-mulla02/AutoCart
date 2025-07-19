import cv2
from ultralytics import YOLO
import numpy as np
from collections import defaultdict
import urllib.request

# ✅ Load YOLO model
model = YOLO("yolov8n.pt")

# 📱 Your mobile IP webcam URL
url = "http://10.103.190.109:4747/video"  # Use your phone’s IP

# 🧾 Product prices
product_prices = {
    "bottle": 30,
    "book": 50,
    "cell phone": 80,
    "person": 0
}

# 🛒 Cart to store detected items
cart = defaultdict(int)

print("🛒 Smart Checkout Started... Show items to your mobile camera.")

while True:
    try:
        # Get frame from mobile camera
        img_resp = urllib.request.urlopen(url)
        img_np = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_np, -1)

        # Run YOLO detection on frame
        results = model.predict(source=frame, imgsz=640, conf=0.5, verbose=False)

        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]

                if label in product_prices:
                    cart[label] += 1
                    print(f"✅ {label} added to cart. Total: {cart[label]}")
                    break

        # Show camera feed
        cv2.imshow("📱 Smart Checkout - Mobile Cam", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    except Exception as e:
        print("❌ Error:", e)
        break

cv2.destroyAllWindows()

# 💵 Final Billing
print("\n🧾 Final Bill:")
total = 0
for item, count in cart.items():
    price = product_prices[item] * count
    print(f"- {item.title()} x{count} → ₹{price}")
    total += price

print(f"🟢 Total Payable: ₹{total}")
