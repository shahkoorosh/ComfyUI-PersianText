[![ComfyUI](https://img.shields.io/badge/ComfyUI-Compatible-orange)](https://github.com/comfyanonymous/ComfyUI)
![Node Type](https://img.shields.io/badge/Node_Type:-%20Text%20Rendering-6A5ACD)
[![Python](https://img.shields.io/badge/Python-+3.10-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/github/license/shahkoorosh/ComfyUI-PersianText)](https://github.com/shahkoorosh/ComfyUI-PersianText/blob/main/LICENSE)
![version](https://img.shields.io/badge/Version-2.0.0-darkblue)
[![GitHub Repo stars](https://img.shields.io/github/stars/shahkoorosh/ComfyUI-PersianText?style=social)](https://github.com/shahkoorosh/ComfyUI-PersianText/stargazers)


# PersianText Node for ComfyUI

**PersianText Node** is a ComfyUI tool for creating styled text in **Persian/Farsi**, **Arabic**, and **English/Latin** scripts. Perfect for posters and multilingual designs, it offers flexible typography features.

<br>
<br>

## ⚠️ Breaking Changes in v2.0.0

* **Dual-Language Support**: Now supports mixed Farsi/Arabic *and* English text. Select separate fonts for each language.
* **Improved HEX Input**: HEX color inputs now work with or without the `#` prefix.
* **Transparent Background**: Added the option to generate text (and shadows) with a transparent background.
* **Bug Fixes**: Resolved minor issues for improved stability.

---



> [!IMPORTANT]
>The `python-bidi` package is a dependency required for proper rendering of Persian (Farsi) / Arabic text in the ComfyUI-PersianText custom node. It includes a C extension that may require additional setup, especially in environments like ComfyUI with embedded Python. This guide provides step-by-step instructions for installing and testing `python-bidi` using multiple options based on your setup and any issues you encounter.<br> [How to install python-bidi](#python-bidi-installation-guide)

<br>
<br>
<br>

<div dir="rtl">

نود PersianText در ComfyUI به شما امکان می‌دهد متن‌های فارسی و انگلیسی را با پشتیبانی کامل از اتصال حروف ایجاد کنید. این نود گزینه‌های پیشرفته‌ای برای طراحی متن ارائه می‌دهد، از جمله:<br>
پشتیبانی چندزبانه: نمایش متون فارسی/فارسی، عربی و انگلیسی/لاتین با تنظیم صحیح چیدمان راست به چپ/چپ به راست و شکل‌دهی به حروف.<br>
فونت‌های سفارشی: افزودن فونت‌های .ttf یا .otf به پوشه فونت‌ها.<br>
گزینه‌های استایل:<br>
تنظیم اندازه متن، رنگ‌ها (از طریق پالت یا کد هگز) و چیدمان.<br>
چرخاندن متن و افزودن سایه‌های قابل تنظیم (فاصله، تاری، رنگ).<br>
تنظیم اندازه بوم و حاشیه‌ها.<br>

<br>

### معلومات للمستخدمين العرب: <br>
نود PersianText في ComfyUI يتيح لك إنشاء نصوص عربية بسهولة مع دعم كامل لاتجاه النص من اليمين إلى اليسار (RTL) والاتصالات بين الحروف. الميزات الرئيسية: <br>
الدعم متعدد اللغات: عرض النصوص بالفارسية/الفارسية، العربية، والإنجليزية/اللاتينية مع محاذاة RTL/LTR الصحيحة وتشكيل الحروف.<br>
الخطوط المخصصة: إضافة خطوط .ttf أو .otf إلى مجلد الخطوط.<br>
خيارات التصميم:<br>
ضبط حجم النص، الألوان (من خلال اللوحة أو الكود السداسي)، والمحاذاة.<br>
تدوير النص وإضافة ظلال قابلة للتخصيص (المسافة، التمويه، اللون).<br>
تحديد حجم اللوحة والهوامش.<br>
</div>
<br>

![image](https://github.com/user-attachments/assets/fd396567-14d5-4780-92d1-6d8e4b0c998c)



<br>

---

## 🌟 Features

### 🔤 **Full Support for Persian/Farsi and Arabic Scripts**
- **Multilingual Support**: Renders Persian, Arabic, and English text with proper RTL/LTR and glyph shaping.
- **Custom Fonts**: Use `.ttf` or `.otf` fonts from the `Fonts` folder.
- **Styling**:
  - **Dynamic Colors**: Choose text, background, and shadow colors from a predefined palette or provide custom hex codes.
  - **Alignment Options**: Align your text horizontally (`left`, `center`, `right`) and vertically (`top`, `center`, `bottom`).
  - **Offset Controls**: Fine-tune the text position with adjustable `X` and `Y` offsets.
  - **Rotations**: Rotate text **around its own center**, ensuring precise alignment and perfect positioning.
- **Transparent Background**: Optional for workflow flexibility.
- Specify custom canvas sizes (from 1x1 up to 4096x4096 pixels) to fit your design needs.

### 🌌 **Enhanced Styling for Shadows**
- Add beautiful shadows to your text with customizable:
  - **Shadow Distance**
  - **Shadow Blur Intensity**
  - **Shadow Color**




---

## 📂 Installation and Setup

Search for `PersianText` in "Comfy Manager" or alternatively:

1. Go to comfyUI custom_nodes folder, `ComfyUI/custom_nodes/`
2. Clone the repository `git clone https://github.com/shahkoorosh/ComfyUI-PersianText.git`
3. Install the requirements `pip install -r requirements.txt`
4. **Add Your Fonts**:
   - Navigate to the `Fonts` folder inside the repository.
   - Add `.ttf` or `.otf` fonts to the `Fonts` folder. (Any `.ttf` or `.otf` font placed in this folder will appear in the font dropdown menu in the node.)
5. Restart ComfyUI.

---
### python-bidi Installation Guide
### Prerequisites
- **Python**: Ensure you have Python installed (ComfyUI typically includes an embedded Python in its portable distribution, e.g., `python_embeded`).
- **ComfyUI**: This guide assumes you are using the ComfyUI Windows portable version (e.g., `ComfyUI_windows_portable`).
- **Administrator Privileges**: Some steps may require admin rights to install build tools or dependencies.

---

### Installation Options

### Option 1: Basic Installation in ComfyUI Environment
This is the simplest approach, reinstalling `python-bidi` within ComfyUI's embedded Python environment.

1. **Activate ComfyUI's Embedded Python**:
   - Open a command prompt and navigate to your ComfyUI directory (e.g., `D:\ComfyUI_windows_portable`).
   - Run the following commands to set up and update `pip`:
     ```bash
     python_embeded\python.exe -m ensurepip
     python_embeded\python.exe -m pip install --upgrade pip
     ```
     - Note: If you get `No module named ensurepip`, it’s okay—proceed to the next step, as `pip` is likely already present.

2. **Install `python-bidi`**:
   - Install the package using ComfyUI's Python:
     ```bash
     python_embeded\python.exe -m pip install python-bidi
     ```

3. **Verify Installation**:
   - Test if the module is available:
     ```bash
     python_embeded\python.exe -c "from bidi.algorithm import get_display; print('Success')"
     ```
   - **Expected Output**: `Success` (no errors).
   - **If Successful**: Proceed to ComfyUI.
   - **If Error (e.g., `ModuleNotFoundError: No module named 'bidi.bidi'`)**: The C extension didn’t compile. Move to [Option 2](#option-2-install-build-tools) or [Option 3](#option-3-use-a-prebuilt-wheel).

---

### Option 2: Install Build Tools
If Option 1 fails due to a missing C extension (`bidi.bidi`), install Microsoft Visual C++ Build Tools to compile it.

1. **Install Visual C++ Build Tools**:
   - Download the installer from [Microsoft Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
   - Run the installer and select the **"Desktop development with C++"** workload.
   - Ensure the following components are included:
     - MSVC v142 - VS 2019 C++ x64/x86 build tools (or the latest version).
     - Windows SDK (e.g., 10.0 or the latest).
     - English language pack (if needed).
   - Click **Install** and wait for completion (may take time).
   - Restart your computer after installation.

2. **Reinstall `python-bidi`**:
   - Uninstall the existing version:
     ```bash
     python_embeded\python.exe -m pip uninstall python-bidi -y
     ```
   - Reinstall with compilation:
     ```bash
     python_embeded\python.exe -m pip install python-bidi
     ```

3. **Verify Installation**:
   - Run the verification command:
     ```bash
     python_embeded\python.exe -c "from bidi.algorithm import get_display; print('Success')"
     ```
   - **Expected Output**: `Success`.
   - **If Successful**: Proceed to ComfyUI.
   - **If Error**: Note the error message and try [Option 3](#option-3-use-a-prebuilt-wheel), then report the details to the repository maintainers.

---

### Option 3: Use a Prebuilt Wheel
If compilation fails even with build tools (e.g., due to Python version incompatibility), use a prebuilt wheel.

1. **Check Python Version**:
   - Determine your Python version:
     ```bash
     python_embeded\python.exe -c "import sys; print(sys.version)"
     ```
   - Note the version (e.g., `3.10.12`) and architecture (e.g., `win_amd64` for 64-bit).

2. **Download a Wheel**:
   - Visit [PyPI](https://pypi.org/project/python-bidi/#files) or [Wheelodex](https://www.wheelodex.org/projects/python-bidi/).
   - Download a `.whl` file matching your Python version and architecture (e.g., `python_bidi-0.6.6-cp310-cp310-win_amd64.whl` for Python 3.10 on 64-bit Windows).
   - Save the file to a convenient location (e.g., `E:\Downloads`).

3. **Install the Wheel**:
   - Install the downloaded wheel:
     ```bash
     python_embeded\python.exe -m pip install "E:\Downloads\python_bidi-0.6.6-cp310-cp310-win_amd64.whl"
     ```

4. **Verify Installation**:
   - Run the verification command:
     ```bash
     python_embeded\python.exe -c "from bidi.algorithm import get_display; print('Success')"
     ```
   - **Expected Output**: `Success`.
---

## 🚀 How to Use

1. Find **PersianText Node** in ComfyUI under `🎨KG`.
2. Configure:
   - **Text**: Enter Persian, Arabic, English, or mixed text.
   - **Fonts**: Choose Farsi/Arabic and English/Latin fonts.
   - **Style**: Set size, colors, alignment, rotation, shadow, and padding.
   - **Canvas**: Set width, height, or enable transparent background.
3. Run to generate text image and mask.


---

## 📜 Input Parameters

| Parameter               | Type      | Description                              |
|-------------------------|-----------|------------------------------------------|
| Text                   | String    | Persian, Arabic, English, or mixed text. |
| Farsi/Arabic Font      | Dropdown  | Font for Persian/Arabic text.           |
| English/Latin Font     | Dropdown  | Font for English/Latin text.            |
| Size                   | Integer   | Font size (1-256).                      |
| Text Color             | Dropdown  | Text color from palette.                |
| Text Color Hex         | String    | Custom text color (e.g., `#000000`).    |
| Background Color       | Dropdown  | Background color from palette.          |
| Background Color Hex   | String    | Custom background color (e.g., `#FFFFFF`). |
| Horizontal Align       | Dropdown  | `left`, `center`, `right`.              |
| Vertical Align         | Dropdown  | `top`, `center`, `bottom`.              |
| Image Width            | Integer   | Canvas width (1-4096).                  |
| Image Height           | Integer   | Canvas height (1-4096).                 |
| Rotation               | Float     | Text rotation (-360 to 360).            |
| Offset X               | Integer   | Horizontal offset (-256 to 256).        |
| Offset Y               | Integer   | Vertical offset (-256 to 256).          |
| Shadow Distance        | Float     | Shadow offset (0-256).                  |
| Shadow Blur            | Float     | Shadow blur (0-256).                    |
| Shadow Color           | Dropdown  | Shadow color from palette.              |
| Shadow Color Hex       | String    | Custom shadow color (e.g., `#000000`).  |
| Padding                | Integer   | Space around text (0-256).              |
| Transparent Background | Boolean   | Enable transparent background.          |

---

### Troubleshooting
- **Compilation Errors**: If you see errors during `pip install python-bidi` (e.g., missing `cl.exe`), ensure the Visual C++ Build Tools installation includes the C++ workload and SDK. You may need to repair the installation via the Visual Studio Installer.
- **Persistent Issues**: If none of the options work, share the full error output from the `pip install` or verification command with the repository maintainers for further assistance.
- **Python Version Mismatch**: Ensure the wheel or installation matches your ComfyUI Python version (check with the version command above).

## 📂 Contributing and Support

Feel free to submit issues or pull requests to improve the **PersianText Node**. Your contributions and feedback are always welcome!

---

## 🙏 Acknowledgments

This project would not have been possible without the incredible work of two outstanding contributors to the ComfyUI ecosystem:

### **Suzie** ([Suzie1](https://github.com/Suzie1))  
Thank you for creating **Comfyroll Studio**, which inspired many features and design principles of this node. Your innovative nodes set a benchmark for quality and functionality, and they were instrumental in shaping the **PersianText Node**. Without your work, this project would have taken significantly more time and effort to build.

### **Matteo Spinelli** ([cubiq](https://github.com/cubiq))  
A huge thank you for **ComfyUI Essentials**, a cornerstone project that provided essential utilities and best practices for node creation. Your code laid a strong foundation for the development of this node, and your contributions continue to empower the ComfyUI community.

---

Both of your contributions to the ComfyUI ecosystem have been invaluable, and this project is deeply grateful for the groundwork you’ve provided. Thank you for your dedication and effort in making the community stronger! 🌟

---
Thank you for using ComfyUI-PersianText!
