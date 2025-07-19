import cv2
import numpy as np
import urllib.request

# ✅ Replace with your DroidCam link
url = 'http://10.103.190.109:4747/video'

while True:
    try:
        # 🧠 Get image from mobile camera
        img_resp = urllib.request.urlopen(url)
        img_np = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_np, -1)

        # ✅ Show camera feed
        cv2.imshow("📱 Mobile Camera Feed", frame)

        # ⏹️ Exit with 'q'
        if cv2.waitKey(1) == ord('q'):
            break

    except Exception as e:
        print("⚠️ Error:", e)
        break

cv2.destroyAllWindows()
