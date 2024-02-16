from PIL import Image
from cryptography.fernet import Fernet


def generate_key():
    return Fernet.generate_key()

def encrypt(message, key):
    cipher = Fernet(key)
    encrypted_message = cipher.encrypt(message.encode())
    return encrypted_message

def decrypt(encrypted_message, key):
    cipher = Fernet(key)
    decrypted_message = cipher.decrypt(encrypted_message).decode()
    return decrypted_message

def bytes_to_binary(text):
    binary = ''.join(format(byte, '08b') for byte in text)
    return binary

def binary_to_bytes(binary_string):
    byte_array = bytearray(int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8))
    return bytes(byte_array)

def hide_text_in_image(text, path):
    image_path = path
    text_to_hide = text

    binary_text = bytes_to_binary(text_to_hide)

    img = Image.open(image_path)
    width, height = img.size

    if len(binary_text) > (width * height * 3):  
        raise ValueError("Text is too long to be hidden in this image.")

    binary_text += '1111111111111110'  

    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))

            for color_channel in range(3): 
                if data_index < len(binary_text):
                    pixel[color_channel] = pixel[color_channel] & 254 | int(binary_text[data_index])
                    data_index += 1

            img.putpixel((x, y), tuple(pixel))

    output_path = input("Enter the path for the output image (include .png extension): ")
    img.save(output_path)
    print("Text hidden in the image and saved as", output_path)

def extract_text_from_image():
    image_path = input("Enter the path of the image from which to extract text: ")
    img = Image.open(image_path)
    binary_text = ''
    delimiter = '1111111111111110'

    for y in range(img.height):
        for x in range(img.width):
            if binary_text[-len(delimiter):] == delimiter:
                break
            pixel = img.getpixel((x, y))
            for color_channel in pixel:
                binary_text += str(color_channel & 1)
                if binary_text[-len(delimiter):] == delimiter:
                    break

    delimiter_index = binary_text.find(delimiter)
    if delimiter_index != -1:
        binary_text = binary_text[:delimiter_index]

    text = binary_to_bytes(binary_text)
    print(f"The extracted text is: {text}")
    return text

choice = input("IF YOU HAVENT GENERATED A PASSWORD YET, THEN USE CHOICE 3.\nEncrypt - 1\nDecrypt - 2\nGenerate New Password - 3\n")
if choice == "1":
    message = input("Enter Your message: ")
    password_path = input("Enter the password file path: ")
    with open(password_path, "rb") as file:
        password = file.read()
        file.close()
    path = input("Enter the path of the image: ")
    text = encrypt(message, password)
    print(text)
    hide_text_in_image(text, path)
elif choice == "2":
    path = input("Enter the password file path: ")
    with open(path, "rb") as file:
        password = file.read()
        file.close()
    msg = extract_text_from_image()
    text = decrypt(msg, password)
    print("Extracted Text:", text)
elif choice == "3":
    password = generate_key()
    file_path = "password.dat"
    with open(file_path, "wb") as file:
        file.write(password)
        file.close()