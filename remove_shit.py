import os

# Define the folder where you want to remove "-min" from filenames
folder_path = "."

# Iterate through all files in the folder
for filename in os.listdir(folder_path):
    if "-min" in filename:
        # Generate the new filename by removing "-min"
        new_filename = filename.replace("-min", "")

        # Create the full path to the old and new files
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)

        # Rename the file
        os.rename(old_file_path, new_file_path)

print("File renaming complete.")
