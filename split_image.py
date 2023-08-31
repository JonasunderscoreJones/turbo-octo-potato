from PIL import Image
import os

def split_image(image_path, output_folder, square_size):
    # Open the image
    image = Image.open(image_path)

    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get image dimensions
    width, height = image.size

    # Calculate the number of rows and columns
    rows = height // square_size
    columns = width // square_size

    # Iterate over rows and columns to crop and save squares
    for row in range(rows):
        for col in range(columns):
            left = col * square_size
            upper = row * square_size
            right = left + square_size
            lower = upper + square_size
            square = image.crop((left, upper, right, lower))

            # Save the cropped square
            square.save(os.path.join(output_folder, f"image_{row}_{col}.jpg"))

if __name__ == "__main__":
    input_image_path = "path/to/your/input/image.jpg"
    output_folder = "path/to/your/output/folder"
    square_size = 200  # Adjust this to the desired size of each square

    split_image(input_image_path, output_folder, square_size)
