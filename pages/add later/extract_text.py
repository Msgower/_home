from PIL import Image
import pytesseract

img = Image.open("poster.png")
text_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

for i, text in enumerate(text_data['text']):
    if tetx.strip() != "":
        print({
            "content": text,
            "position": [text_data['left'][i], text_data['top'][i]],
            "size": [text_data['width'][i], text_data['height'][i]]
        })
        