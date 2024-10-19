from PIL import Image
import os 

def genData(data):
    """Convert string data into binary representation."""
    newd = [format(ord(i), '08b') for i in data]
    print("Binary data to encode:", newd)
    return newd

def modPix(pix, data):
    """Modify pixel values according to the binary data."""
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        pix = [value for _ in range(3) for value in imdata.__next__()[:3]]

        for j in range(8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                pix[j] += 1

        if (i == lendata - 1):
            pix[-1] += 1 if pix[-1] % 2 == 0 else 0
        else:
            pix[-1] -= 1 if pix[-1] % 2 != 0 else 0

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    """Encode the data into the image."""
    w, h = newimg.size
    x, y = 0, 0

    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        print(f"Encoding pixel: {pixel} at position: ({x},{y})")

        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def encode():
    """Main function to encode data into an image."""
    img = input("Enter image name(with extension): ")
    try:
        image = Image.open(img, 'r')
    except FileNotFoundError:
        print("Error: Image file not found.")
        return

    data = input("Enter data to be encoded: ")
    if len(data) == 0:
        raise ValueError('Data is empty')

    # Check if image is large enough to hold the data
    max_data_length = (image.size[0] * image.size[1] * 3) // 8
    if len(data) > max_data_length:
        print(f"Error: Data too long! Maximum allowable length is {max_data_length} characters.")
        return

    newimg = image.copy()
    encode_enc(newimg, data)

    new_img_name = input("Enter the name of the new image(with extension): ")
    if os.path.exists(new_img_name):
        print("Error: File already exists. Please choose a different name.")
        return

    newimg.save(new_img_name)


def decode(img):
    """Decode the data from the image."""
    try:
        image = Image.open(img, 'r')
    except FileNotFoundError:
        print("Error: Image file not found.")
        return ""

    data = iter(image.getdata())
    binary_string = ''
    decoded_message = ''
    
    while True:
        try:
            pixels = [value for value in data.__next__()[:3]]
            binary_string += ''.join(['1' if pixel % 2 != 0 else '0' for pixel in pixels])
            print(f"Current binary string: {binary_string}") 

            while len(binary_string) >= 8:
                byte = binary_string[:8]
                binary_string = binary_string[8:]
                character = chr(int(byte, 2))
                print(f"Decoded byte: {byte} -> {character}")  
                
                if character == '\x00':
                    break
                decoded_message += character

        except StopIteration:
            break

    return decoded_message


def main():
    """Main program loop."""
    while True:
        print(":: Welcome to Steganography ::")
        print("1. Encode")
        print("2. Decode")
        print("3. Exit")
        choice = input("Choose an option (1-3): ")

        if choice == '1':
            encode()
        elif choice == '2':
            img = input("Enter image name(with extension): ")
            decoded_word = decode(img)
            print("Decoded Word: " + decoded_word)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
