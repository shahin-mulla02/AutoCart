from ultralytics import YOLO
import cv2

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

# Barcode mapping
barcode_items = {
    '1001': ('Juice Bottle', 30),
    '1002': ('Chips Packet', 20),
    '1003': ('Soap Box', 25)
}

cart = {}

# Track if we just placed something (to avoid multiple prompts)
waiting_for_barcode = False
previous_frame_had_hand = False

# Open webcam
cap = cv2.VideoCapture(0)
print("🛒 Smart Cart with Barcode Running... Press Q to stop\n")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Camera error")
        break

    results = model(frame)[0]

    hand_detected = False

    for box in results.boxes:
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]

        if class_name == 'person':  # Using 'person' to simulate hand detection
            hand_detected = True
            break

    if previous_frame_had_hand and not hand_detected and not waiting_for_barcode:
        # Hand was there, now it's gone → Item placed
        print("\n🛑 Item placed! Enter barcode:")
        barcode = input("📦 Barcode: ")

        if barcode in barcode_items:
            item, price = barcode_items[barcode]
            cart[item] = cart.get(item, 0) + 1
            print(f"✅ Added: {item} → ₹{price}")
        else:
            print("❌ Invalid barcode!")

        waiting_for_barcode = True

    # Reset barcode input flag if hand is not seen for a while
    if not hand_detected:
        waiting_for_barcode = False

    previous_frame_had_hand = hand_detected

    # Show detection
    frame = results.plot()
    cv2.imshow("Barcode Smart Cart - Press Q to Exit", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Show final bill
print("\n🧾 Final Bill:")
total = 0
for item, qty in cart.items():
    line = f"- {item} x{qty} → ₹{qty * barcode_items[barcode][1]}"
    print(line)
    total += qty * barcode_items[barcode][1]
print(f"🟢 Total Payable: ₹{total}")
