import os
import shutil

def move_file(fileNewPath):
    # Extract necessary information from input
    absolute_path = fileNewPath["absolute_path"]
    new_absolute_path = fileNewPath["new_absolute_path"]
    reason_for_move = fileNewPath["reason_for_move"]
    name = fileNewPath["name"]
    
    # Create directory structure if it doesn't exist
    os.makedirs(os.path.dirname(new_absolute_path), exist_ok=True)
    
    # Move the file
    shutil.move(absolute_path, new_absolute_path)
    
    # Prepare the response
    newPath_and_reason = {
        "name": name,
        "new_absolute_path": new_absolute_path,
        "reason_for_move": reason_for_move
    }
    
    return newPath_and_reason