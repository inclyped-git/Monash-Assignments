from PIL import Image

# Define the bitmap for the digit 2
digit_2_bitmap = [
    [0, 0, 1],
    [1, 1, 0],
    [1, 0, 1],
    [0, 1, 1],
    [0, 0, 0]
]

# Create a new image with mode "RGB" and size 3x5
image = Image.new("RGB", (len(digit_2_bitmap[0]), len(digit_2_bitmap)), "white")

# Load the pixels of the image
pixels = image.load()

# Set the color of each pixel based on the bitmap
for y in range(len(digit_2_bitmap)):
    for x in range(len(digit_2_bitmap[0])):
        if digit_2_bitmap[y][x] == 0:
            pixels[x, y] = (0, 0, 0)  # Black pixel
        else:
            pixels[x, y] = (255, 255, 255)  # White pixel

# Display the image
image.show()