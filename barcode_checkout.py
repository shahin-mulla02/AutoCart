import cv2
from pyzbar.pyzbar import decode
import pyttsx3
import winsound
import time
from datetime import datetime

# Initialize pyttsx3 engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # speaking speed

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define price list
price_list = {
    "1234567890128": ("Chips Packet", 30),
    "5780201379628": ("Toothpaste", 45),
    "9780201379624": ("Soap", 25)
}

cart = {}
last_scanned = {}
SCAN_DELAY = 10  # seconds delay per barcode

# Speak welcome message once
speak("Welcome to Smart Checkout. Show barcode to the camera.")

# Use IP camera stream
camera_url = "http://10.103.190.109:4747/video"
cap = cv2.VideoCapture(camera_url)

print("🛒 Smart Checkout Started... Show barcode to the mobile camera.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame")
        break

    current_time = time.time()

    for barcode in decode(frame):
        barcode_data = barcode.data.decode('utf-8')

        if barcode_data in price_list:
            last_time = last_scanned.get(barcode_data)

            if last_time is None or (current_time - last_time >= SCAN_DELAY):
                item_name, price = price_list[barcode_data]

                if item_name in cart:
                    cart[item_name]["qty"] += 1
                else:
                    cart[item_name] = {"qty": 1, "price": price}

                total = sum(info["qty"] * info["price"] for info in cart.values())

                print(f"✅ {item_name} added to cart. Quantity: {cart[item_name]['qty']}")

                winsound.Beep(1000, 150)  # beep sound feedback

                speak("Item added to cart")  # simple voice feedback

                last_scanned[barcode_data] = current_time
                break

    cv2.imshow("📦 Barcode Scanner - Press Q to Exit", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Generate and print final bill
print("\n🧾 Final Bill:")
total = 0
bill_lines = []
for item, info in cart.items():
    item_total = info["qty"] * info["price"]
    total += item_total
    line = f"- {item} x{info['qty']} → ₹{item_total}"
    bill_lines.append(line)
    print(line)

print(f"🟢 Total Payable: ₹{total}")
bill_lines.append(f"\nTotal: ₹{total}")

# Save bill to text file
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"final_bill_{timestamp}.txt"
with open(filename, "w", encoding="utf-8") as f:
    f.write("Smart Checkout Bill\n")
    f.write("\n".join(bill_lines))
print(f"💾 Bill saved to {filename}")

# Speak thank you message before exiting
speak("Thank you and visit again!")

# Cleanup
cap.release()
cv2.destroyAllWindows()
