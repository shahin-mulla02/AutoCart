import cv2

# ✅ Your DroidCam mobile camera URL
url = "http://10.103.190.109:4747/video"

# 📷 Connect to camera
cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Camera connection failed")
        break

    # 👁️ Show video
    cv2.imshow("📱 Mobile Camera Test - Press Q to exit", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 🔚 Clean up
cap.release()
cv2.destroyAllWindows()
