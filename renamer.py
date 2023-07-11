import os

directory = "C:/Users/PC/Desktop/Scrapper/Collection"  # Replace with your directory path

# Get the list of files in the directory
files = os.listdir(directory)

# Iterate over each file in the directory
for filename in files:
    try:
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # Add the prefix "AsuraScans" to the file name
            new_filename = filename.split("_")[1]

            # Construct the full paths of the old and new file names
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)

            # Rename the file
            os.rename(old_path, new_path)

            print(f"File renamed: {new_path}")
    except:
        print("hata")
