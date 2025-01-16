import sys
import img2pdf
import os
from PIL import Image
from pypdf import PdfWriter
import shutil
from pathlib import Path


# Function to convert an image to a PDF file
def img2pdfFunction(img_path):
    pdf_path = img_path[:img_path.rindex('.')] + '.pdf'  # Create PDF path by replacing the file extension

    # Opening the image file
    image = Image.open(img_path)

    # Convert the image to PDF format using img2pdf
    pdf_bytes = img2pdf.convert(image.filename)

    # Create a new PDF file and write the converted bytes
    file = open(pdf_path, "wb")
    file.write(pdf_bytes)

    # Close the image and file objects
    image.close()
    file.close()

    return pdf_path  # Return the path of the created PDF


# Function to validate a provided directory
def get_valid_directory(directory):
    while True:
        directory = directory.strip()  # Remove any leading or trailing whitespace
        directory = directory.replace('"', '')  # Remove quotes if present
        path = Path(directory)

        # Check if the provided path exists and is a directory
        if path.is_dir():
            print(f"Valid directory: {directory}")
            return directory  # Return the valid directory path
        else:
            print("Invalid directory. Please try again.")  # Prompt user for a valid directory


# Function to request file paths from the user and validate them
def request_and_validate_filepath():
    img_path_list = []  # Initialize an empty list to store valid file paths

    while True:
        img_path = input("Enter file address (Enter '"'done'"' to finish): ").strip()  # Get input and remove leading/trailing whitespace
        img_path = img_path.replace('"', '')  # Remove quotes if present

        if os.path.exists(img_path):  # Check if the path exists
            img_path_list.append(img_path)  # Add to the list if valid
            print("Successfully added!")
        elif not os.path.exists(img_path) and img_path.lower() != 'done':
            print("Invalid file path. Please try again.")

        if img_path.lower() == 'done' and len(img_path_list) != 0:  # Exit if user is done and list is not empty
            return img_path_list  # Return the list of valid file paths
        elif img_path.lower() == 'done' and len(img_path_list) == 0:  # Exit if user is done and list is not empty
           print('At least one valid file address must be provided.')


# Initialize a PDF writer object for merging
merger = PdfWriter()
merged_filename = ''  # Placeholder for the merged file's name
pdf_path_list = []  # List to store paths of converted PDF files

# Request and validate image file paths from the user
image_path_list = request_and_validate_filepath()

# Convert each image to PDF and store the paths
for img in image_path_list:
    pdf_path_list.append(img2pdfFunction(img))

# Ask the user for the directory to save the merged file
inputted_directory = input(
    'Enter file directory to save in (If you enter nothing, the merged file will be saved to Downloads): ')
if inputted_directory.strip() == '':
    # Automatically detect the Downloads folder
    downloads_folder = str(Path.home() / "Downloads")
    print(f"Downloads folder path: {downloads_folder}")
    downloads_folder = downloads_folder.replace('"', '')  # Remove quotes if present

    target_dir = downloads_folder  # Default save location (can change by editing this line)
else:
    target_dir = get_valid_directory(inputted_directory)  # Validate user-provided directory

# Move individual PDFs to the target directory and append them to the merger
for pdf in pdf_path_list:
    print('PDF is: ' + pdf)
    merger.append(pdf)  # Append the PDF to the merger
    shutil.move(pdf, target_dir)  # Move the individual PDF to the target directory
    print(pdf + ' moved successfully')

merged_filename = input("What do you want the merged pdf file to be called?: ")
if(merged_filename.strip() == ''):
    merged_filename = 'merged'
# Define the full path for the merged PDF file
merged_file_path = os.path.join(target_dir, merged_filename + '.pdf')

# Write the merged PDF to the target directory
merger.write(merged_file_path)
merger.close()  # Close the merger object
