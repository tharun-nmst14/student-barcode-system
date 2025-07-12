import cv2
from pyzbar.pyzbar import decode
import webbrowser

def scan_barcode():
    cap = cv2.VideoCapture(1)  # Your working camera index

    if not cap.isOpened():
        print("❌ Unable to access the camera.")
        return

    print("📷 Camera started. Show a barcode... (Press 'q' to quit)")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to capture frame.")
            break

        for barcode in decode(frame):
            roll_number = barcode.data.decode('utf-8')
            print(f"✅ Barcode detected: {roll_number}")

            # Open student profile in browser
            profile_url = f"http://127.0.0.1:8000/profile/{roll_number}/"
            webbrowser.open(profile_url)

            cap.release()
            cv2.destroyAllWindows()
            return

        cv2.imshow("Barcode Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_barcode()
