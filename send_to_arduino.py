import sys
import serial
import time
# Usage: python send_to_arduino.py https://tapix.app/your-slug

SERIAL_PORT = 'COM3'  # Change this to your Arduino's port (e.g., '/dev/ttyACM0' for Linux/Mac)
BAUD_RATE = 115200

def main():
    if len(sys.argv) != 2:
        print("Usage: python send_to_arduino.py <url>")
        sys.exit(1)
    url = sys.argv[1]
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
            time.sleep(2)  # Wait for Arduino to reset
            ser.write((url + '\n').encode('utf-8'))
            print(f"Sent to Arduino: {url}")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        messages.error(request, f"Failed to send to Arduino: {e.stdout} {e.stderr}")

if __name__ == "__main__":
    main()