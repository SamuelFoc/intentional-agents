# ESP32 - DHT22 Online Sensor (scatch upload)

---

### **Step 1: Install ESP32 Board Support**
1. Open **Arduino IDE**.
2. Go to **File > Preferences**.
3. In **Additional Board Manager URLs**, paste the following URL:
   ```
   https://dl.espressif.com/dl/package_esp32_index.json
   ```
   - If other URLs are already listed, separate them with a comma.
4. Click **OK**.
5. Go to **Tools > Board > Boards Manager**.
6. Search for **ESP32** and click **Install** on the **ESP32 by Espressif Systems** package.

---

### **Step 2: Select the ESP32 Board and Port**
1. Plug in your ESP32 board using a data-capable USB cable.
2. Go to **Tools > Board** and select your ESP32 model (e.g., `ESP32 Dev Module`).
3. Go to **Tools > Port** and select the COM port associated with your ESP32.
   - If no port is visible, refer to **Step 5** below for troubleshooting.

---

### **Step 3: Load a Sketch**
1. Open an example sketch:
   - Go to **File > Examples > Basics > Blink**.
2. Modify the built-in LED pin, if necessary:
   - For most ESP32 boards, change the `LED_BUILTIN` pin to `2`.

---

### **Step 4: Upload the Sketch**
1. Press the **BOOT** button on your ESP32.
2. Click the **Upload** button (right-arrow icon) in Arduino IDE.
3. When "Connecting..." appears in the IDE, release the **BOOT** button.
4. Wait for the upload to complete.

---

### **Step 5: Troubleshooting – No Board or Port in Arduino IDE**

#### **A. Verify USB Connection**
- Ensure your USB cable is data-capable, not just for charging.
- Try different USB cables and ports.

#### **B. Install CP2102 or CH340 Driver**
Some ESP32 boards require USB-to-serial bridge drivers:
1. **Download Drivers:**
   - [CP210x Driver (Silicon Labs)](https://www.silabs.com/developer-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads)
   - [CH340 Driver](http://www.wch-ic.com/downloads/CH341SER_EXE.html)
2. Install the driver:
   - Extract the ZIP file.
   - Run the installer (e.g., `CP210xVCPInstaller_x64.exe` for 64-bit systems).
   - Restart your computer after installation.

#### **C. Manually Update the Driver**
1. Open **Device Manager** (press `Win + X` > Device Manager).
2. Look for **CP2102 USB to UART Bridge Controller** under **Other devices** or **Ports (COM & LPT)**.
3. If there’s an exclamation mark:
   - Right-click the device and select **Update driver**.
   - Choose **Browse my computer for drivers**.
   - Navigate to the extracted driver folder.
   - Click **Next** to install.

---

### **Step 6: Verify Installation**
1. Open **Device Manager**.
2. Under **Ports (COM & LPT)**, you should see:
   - `Silicon Labs CP210x USB to UART Bridge (COMx)` or `USB-SERIAL CH340 (COMx)`.
3. Note the COM port number and select it in **Tools > Port** in Arduino IDE.

---

### **Step 7: Test and Upload Again**
1. Follow **Step 3** and **Step 4** above.
2. If the sketch uploads successfully, the onboard LED should blink as programmed.

---

If you still face issues, try resetting the ESP32 by pressing the **EN/RST** button during upload or ensure your ESP32 board is not faulty.