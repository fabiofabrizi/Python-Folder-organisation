# Imports for working with the filesystem and regex
import os
import re
import shutil 

# Specify the target directory where the script has to work
directory = r'C:\Users\fabio\Downloads' 

# 2. Dictionary of folders and matching terms
# The key is the subfolder and the value (list) are the terms to match
terms_dict = {
    "Periodization": ["Triphasic", "Periodization", "Periodized"],
    "Sprints": ["Vince", "Acceleration", "Velocity", "400m", "100m", "30"],
    "Data_Analysis": ["report", "monthly", "summary"],
    "Python" : ["Python", "Machine", "Algorithms", "Statistical", "Statistics"],
    "distance" : ["Endurance", "Distance"],
    "hurdles" : ["Hurdles", "100mH", "400mH", "60mH"],
    "CE": ["Combined", "Decathlon", "Heptathlon", "Pentathlon"],
    "Contrast_Training" : ["Contrast", "French"], 
    "Munster AAI" : ["Munster", "Ireland"],
    "WMAC" : ["WMAC", "Muskerry"]
}


# 3. Check the target directory
if not os.path.isdir(directory):
    print(f"❌ Error: Target directory not found at '{directory}'")
    exit()

print(f"--- Starting Batch File Organization in: {directory} ---")

# 4. Iterate through the dictionary items (folder_name, word_list)
for folder_name, word_list in terms_dict.items():
    
    # 5. Define the destination folder
    # Create the full path for it to happen
    dir_to_move = os.path.join(directory, folder_name)

    # 6. Validate/Create destination folder
    # Then move to next item in the dictionary 
    if not os.path.isdir(dir_to_move):
        try:
            os.makedirs(dir_to_move)
            print(f"\n📁 Created destination directory: {dir_to_move}")
        except OSError as e:
            print(f"\n❌ Error: Could not create destination directory '{dir_to_move}'. Skipping this group. Details: {e}")
            continue 

    # 7. Build and Compile the Regular Expression Pattern
    pattern_string = "|".join(word_list)
    regex = re.compile(pattern_string, re.IGNORECASE)

    print(f"\n--- Processing Folder: {folder_name} ---")
    print(f"Matching Terms: {word_list}")
    
    # 8. Get files and Process/Move
    moved_files = []
    error_moving_files = []
    
    try:
        # Get a fresh list of files for the current iteration
        file_names = os.listdir(directory)
    except PermissionError:
        print(f"❌ Error: Permission denied to access '{directory}'. Skipping.")
        continue # Move to the next item in the dictionary

    for filename in file_names:
        # Check for a match anywhere in the filename
        if regex.search(filename):
            source_path = os.path.join(directory, filename)
            destination_path = os.path.join(dir_to_move, filename)

            # Ensure it's a file and not the destination folder itself
            if os.path.isfile(source_path) and not (os.path.samefile(source_path, dir_to_move) if os.path.isdir(dir_to_move) else False):
                try:
                    # Move the file
                    shutil.move(source_path, destination_path)
                    moved_files.append(filename)
                except Exception as e:
                    error_moving_files.append((filename, str(e)))

    # 9. Output Results for the current batch
    if len(moved_files) > 1:
        print(f"✅ Successfully moved {len(moved_files)} files to {folder_name}:")
    elif len(moved_files) == 0:
        print(f"❌ No files to move to {folder_name}:")
    for file in moved_files:
        print(f"- {file}")

    if error_moving_files:
        print(f"⚠️ Encountered {len(error_moving_files)} errors while moving files:")
        for file, error in error_moving_files:
            print(f"- {file}: {error}")

print("\n--- File Organization Completed ---")