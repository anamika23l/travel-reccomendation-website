import os
import shutil

# Source and destination paths
source_folder = "c:/TravelAI-Website/images"
dest_folder = "c:/TravelAI-Website/static/images"

# Create destination folder if it doesn't exist
os.makedirs(dest_folder, exist_ok=True)

# Copy all jpg files
for filename in os.listdir(source_folder):
    if filename.lower().endswith('.jpg'):
        source_path = os.path.join(source_folder, filename)
        dest_path = os.path.join(dest_folder, filename)
        shutil.copy2(source_path, dest_path)
        print(f"Copied: {filename}")

print(f"\nTotal images copied: {len(os.listdir(dest_folder))}")
