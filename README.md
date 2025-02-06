
# PersianText Node for ComfyUI

**PersianText Node**, is an essential tool for designers and creators working with **ComfyUI**. This node provides a powerful and flexible solution for rendering text with a wide range of styling options, including full support for **Persian/Farsi** and **Arabic** scripts. Whether you're creating posters, or text-based visuals, this node brings advanced typography features to your workflow.
<br>
<br>
<div dir="rtl">
نود PersianText در ComfyUI به شما امکان می‌دهد متن‌های فارسی را با پشتیبانی کامل از اتصال حروف و راست‌چین (RTL) ایجاد کنید. این نود گزینه‌های پیشرفته‌ای برای طراحی متن ارائه می‌دهد، از جمله:

پشتیبانی کامل از زبان فارسی و عربی <br>
انتخاب فونت دلخواه: کافیست فایل فونت .ttf را به پوشه Fonts اضافه کنید.<br>
چرخش متن: متن را حول مرکز خود بچرخانید.<br>
تنظیم سایه: رنگ، فاصله و میزان محوشدگی سایه را شخصی‌سازی کنید.<br>
تنظیم موقعیت و اندازه متن: متن را دقیقاً در موقعیت دلخواه خود قرار دهید.<br>



## معلومات للمستخدمين العرب: 
نود PersianText في ComfyUI يتيح لك إنشاء نصوص عربية بسهولة مع دعم كامل لاتجاه النص من اليمين إلى اليسار (RTL) والاتصالات بين الحروف. الميزات الرئيسية: <br>

دعم كامل للنصوص العربية والفارسية<br>
إضافة خطوط مخصصة: يمكنك وضع ملفات الخط .ttf في مجلد Fonts.<br>
تدوير النص: تدوير النص حول مركزه الخاص.<br>
خيارات الظل: تخصيص اللون والمسافة والتمويه.<br>
تحكم دقيق في الموضع والحجم: ضع النص في المكان الذي تريده بدقة.<br>
هذا النود أداة رائعة لتصميم الجرافيك بالنصوص العربية والفارسية!<br>
</div>
<br>

![image](https://github.com/user-attachments/assets/926ad95b-9038-40fc-9b37-7f3726c2fb2a)


<br>

---

## 🌟 Features

### 🔤 **Full Support for Persian/Farsi and Arabic Scripts**
- Render text seamlessly in **Persian/Farsi** or **Arabic**, with correct **glyph shaping** and **right-to-left (RTL) alignment**. 
- Built-in integration with **arabic-reshaper** ensures proper character connections and shaping for complex scripts.

### 🎨 **Rich Text Styling Options**
- **Custom Fonts**: Place your favorite `.ttf` fonts in the `Fonts` folder and instantly use them in the node.
- **Dynamic Colors**: Choose text, background, and shadow colors from a predefined palette or provide custom hex codes.
- **Adjustable Text Size**: From tiny captions to large headings, control text size with precision.
- **Alignment Options**: Align your text horizontally (`left`, `center`, `right`) and vertically (`top`, `center`, `bottom`).
- **Offset Controls**: Fine-tune the text position with adjustable `X` and `Y` offsets.
- **Rotations**: Rotate text **around its own center**, ensuring precise alignment and perfect positioning.

### 🌌 **Enhanced Styling for Shadows**
- Add beautiful shadows to your text with customizable:
  - **Shadow Distance**
  - **Shadow Blur Intensity**
  - **Shadow Color**

### 🖼️ **Flexible Canvas Dimensions**
- Specify custom canvas sizes (from 1x1 up to 4096x4096 pixels) to fit your design needs.

---

## 📂 Installation and Setup

Search for `PersianText` in "Comfy Manager" or alternatively:

1. Go to comfyUI custom_nodes folder, `ComfyUI/custom_nodes/`
2. Clone the repository `git clone https://github.com/shahkoorosh/ComfyUI-PersianText.git`
3. Install the requirements `pip install -r requirements.txt`
4. **Add Your Fonts**:
   - Navigate to the `Fonts` folder inside the repository.
   - Add your favorite `.ttf` fonts. Any `.ttf` font placed in this folder will appear in the font dropdown menu in the node.
5. Restart ComfyUI.

---

## 🚀 How to Use

1. Open ComfyUI and locate the **PersianText Node** under the category `🎨KG`.
2. Connect the node to your workflow.
3. Configure the inputs:
   - **Text**: Write your message in Persian/Farsi, Arabic, or any other supported language.
   - **Font**: Select a font from the dropdown menu (populated by fonts in the `Fonts` folder).
   - **Styling**: Customize size, colors, alignment, rotation, and shadow options to match your design.
   - **Canvas Dimensions**: Set the `image_width` and `image_height` to define your canvas size.
4. Execute the node to render the styled text.

---

## 🛠️ Advanced Customization

- **Custom Colors**: Use predefined colors from the palette or define your own hex codes (e.g., `#FF5733` for a vibrant orange).
- **Precise Placement**: Adjust offsets (`offset_x`, `offset_y`) for pixel-perfect positioning.
- **Rotations Around Text Center**: Apply rotations to text, ensuring it pivots around its **own center** rather than the canvas center.
- **Shadow Effects**: Experiment with shadow distance, blur, and color to create stunning visuals.

---

## 📜 Input Parameters

| Parameter               | Type      | Description                                                                                     |
|-------------------------|-----------|-------------------------------------------------------------------------------------------------|
| `text`                 | String    | The text to render. Fully supports Persian/Farsi, Arabic, and other languages.                  |
| `font`                 | Dropdown  | Select a font from the `Fonts` folder.                                                         |
| `size`                 | Integer   | Specify the font size.                                                                          |
| `text_color`           | Dropdown  | Choose a color for the text from the palette.                                                   |
| `text_color_hex`       | String    | Enter a custom hex code for the text color (optional).                                          |
| `background_color`     | Dropdown  | Choose a background color for the canvas.                                                      |
| `background_color_hex` | String    | Enter a custom hex code for the background color (optional).                                    |
| `horizontal_align`     | Dropdown  | Align text horizontally (`left`, `center`, `right`).                                            |
| `vertical_align`       | Dropdown  | Align text vertically (`top`, `center`, `bottom`).                                              |
| `rotation`             | Float     | Rotate the text around its **own center**.                                                     |
| `offset_x`             | Integer   | Adjust the horizontal position of the text.                                                    |
| `offset_y`             | Integer   | Adjust the vertical position of the text.                                                      |
| `shadow_distance`      | Integer   | Set the distance of the shadow from the text.                                                   |
| `shadow_blur`          | Integer   | Adjust the intensity of the shadow blur.                                                        |
| `shadow_color`         | Dropdown  | Choose a color for the shadow.                                                                  |
| `shadow_color_hex`     | String    | Enter a custom hex code for the shadow color (optional).                                        |
| `image_width`          | Integer   | Specify the width of the canvas.                                                                |
| `image_height`         | Integer   | Specify the height of the canvas.                                                               |
| `direction`            | Dropdown  | Choose the text direction (`LTR` or `RTL`).                                                     |

---

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

