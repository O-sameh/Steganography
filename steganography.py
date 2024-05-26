from PIL import Image
import numpy as np
import os

def messageToBinary(message):
    #Converts the string message to binary representation in range 0:8 bits
    if type(message) == str:
        return''.join([format(ord(char),"08b")for char in message])
    elif type(message) == bytes or type(message) == np.ndarray:
        return''.join([format(char,"08b")for char in message])
    elif type(message) == int:
        return format(message,"08b")
    else:
        raise TypeError("Input type not supported")

def RGB_pixels_ToBinary(pixel):
    r, g, b = pixel
    return format(r, '08b'), format(g, '08b'), format(b, '08b')

def RGBA_pixels_ToBinary(pixel):
    r, g, b, a = pixel
    return format(r, '08b'), format(g, '08b'), format(b, '08b'),format(a, '08b')

def pixels_ToBinary(pixel):
    pixel_binary = int(pixel)
    return format(pixel_binary, '08b')

def encode_message_in_image(image_path,secret_message):
    # Open the image and convert to numpy array
    image = Image.open(image_path)
    image_array = np.array(image)
    mode = image.mode
    if (mode == "RGB" or mode == "RGBA"): height, width, channels = image_array.shape
    else: height, width = image_array.shape
    # Convert the secret message to binary
    binary_secret_msg = messageToBinary(secret_message)
    data_len = len(binary_secret_msg)
    data_index = 0

    n_bytes = (width * height * 3) // 8
    if len(secret_message) > n_bytes:
        raise ValueError ("Error encountered insufficient bytes, need bigger image or less data")
    #Checking if the mode of the picture is RGB or Grayscale
    if mode == "RGB":
    # Iterate over each pixel and modify the least significant bits
        for y in range(height):
            for x in range(width):
                pixel = image_array[y, x]
                #convert RGB values to binary format
                r,g,b = RGB_pixels_ToBinary(pixel)

                # Modify the least significant bit of the red pixel
                if data_index < data_len:
                    pixel[0]= int(r[:-1]+binary_secret_msg[data_index],2)
                    data_index += 1

                # Modify the least significant bit of the green pixel
                if data_index < data_len:
                    pixel[1]= int(g[:-1]+binary_secret_msg[data_index],2)
                    data_index += 1

                # Modify the least significant bit of the blue pixel
                if data_index < data_len:
                    pixel[2]= int(b[:-1]+binary_secret_msg[data_index],2)
                    data_index += 1

                # Stop if the entire secret message is encoded
                if data_index>=data_len:
                    break

            if data_index >= data_len:
                break
        encoded_image = Image.fromarray(image_array)
        return encoded_image

    elif mode == "L":
        for y in range(height):
            for x in range(width):
                pixel = image_array[y, x]
                #convert Pixels values to binary format
                pixel_binary = pixels_ToBinary(pixel)

                # Modify the least significant bit of the red pixel
                if data_index < data_len:

                    # Convert pixel to list to modify it
                    pixel_list = list(pixel_binary)
                    pixel_list[-1] = binary_secret_msg[data_index]

                    # Convert back to integer
                    pixel = int(''.join(pixel_list), 2)
                    image_array[y, x] = pixel
                    data_index += 1
                # Stop if the entire secret message is encoded
                if data_index>=data_len:
                    break

            if data_index >= data_len:
                break
        encoded_image = Image.fromarray(image_array)
        return encoded_image

    elif mode == "RGBA":
        for y in range(height):
            for x in range(width):
                pixel = image_array[y, x]
                #convert RGB values to binary format
                r,g,b,a = RGBA_pixels_ToBinary(pixel)

                # Modify the least significant bit of the red pixel
                if data_index < data_len:
                    pixel[0]= int(r[:-1]+binary_secret_msg[data_index],2)
                    data_index += 1

                # Modify the least significant bit of the green pixel
                if data_index < data_len:
                    pixel[1]= int(g[:-1]+binary_secret_msg[data_index],2)
                    data_index += 1

                # Modify the least significant bit of the blue pixel
                if data_index < data_len:
                    pixel[2]= int(b[:-1]+binary_secret_msg[data_index],2)
                    data_index += 1

                # Modify the least significant bit of the alpha pixel
                if data_index < data_len:
                    pixel[2]= int(a[:-1]+binary_secret_msg[data_index],2)
                    data_index += 1

                # Stop if the entire secret message is encoded
                if data_index>=data_len:
                    break

            if data_index >= data_len:
                break
        encoded_image = Image.fromarray(image_array)
        return encoded_image
    else:
        raise TypeError("Image type not supported")

def has_extra_spaces(text):
    # Remove extra spaces using split and join
    cleaned_text = ' '.join(text.split())
    # Check if cleaned text is different from the original1
    return cleaned_text != text

def remove_extra_spaces(text):
    return ' '.join(text.split())


def encode_message_in_text(text,secret_message):
    # Open the text file 
    with open(text, 'r') as file:
        content = file.read()
        
    if has_extra_spaces(content):
        content = remove_extra_spaces(content)  
    
    binary_message = messageToBinary(secret_message)
    result_text = ""
    binary_index = 0
        
    
    for char in content:
        if char == " " and binary_index < len(binary_message):     
            if binary_message[binary_index] == "1":
                result_text+="  "
            else:
                result_text+=" "
            binary_index += 1     
        else:
            result_text+=char            
    while(binary_index < len(binary_message)):
        result_text+="  " if binary_index == "1" else " "
        binary_index+=1
    with open('Text\\encoded.txt', 'w') as file:
    # Write the string to the file
        file.write(result_text)
        
if __name__ == "__main__":
    # image_path = "Images\Cameraman_grayscale.jpg"
    # secret_message = "Omar_221101036$"
    # encoded_image=encode_message_in_image(image_path,secret_message)
    # directory = "Images"
    # if not os.path.exists(directory):
    #     os.makedirs(directory)
    # encoded_image.save(os.path.join(directory, "encoded_image.png"))
    encode_message_in_text("Text\\original_text.txt","Omar_221101036$")

