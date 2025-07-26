import pandas as pd
import os

def convert_csv_to_yolo():
    # Read the CSV file
    csv_path = 'dataset/train/bat_ball.csv'
    df = pd.read_csv(csv_path)
    
    # Create a dictionary to map class names to numbers
    class_mapping = {'ball': 0, 'bat': 1}
    
    # Group by image name
    grouped = df.groupby('name')
    
    # Create labels directory if it doesn't exist
    labels_dir = 'dataset/train/labels'
    os.makedirs(labels_dir, exist_ok=True)
    
    # Process each image
    for image_name, group in grouped:
        # Create the label file name (same as image name but with .txt extension)
        label_filename = image_name.replace('.png', '.txt')
        label_path = os.path.join(labels_dir, label_filename)
        
        with open(label_path, 'w') as f:
            for _, row in group.iterrows():
                # Get class number
                class_num = class_mapping[row['class']]
                
                # Get coordinates and dimensions
                x_center = row['x-axis'] + row['width'] / 2  # Convert to center coordinates
                y_center = row['y-axis'] + row['height'] / 2
                width = row['width']
                height = row['height']
                
                # Normalize coordinates (divide by image dimensions)
                x_center_norm = x_center / row['image_width']
                y_center_norm = y_center / row['image_height']
                width_norm = width / row['image_width']
                height_norm = height / row['image_height']
                
                # Write in YOLO format: class x_center y_center width height
                f.write(f"{class_num} {x_center_norm:.6f} {y_center_norm:.6f} {width_norm:.6f} {height_norm:.6f}\n")
    
    print(f"Conversion completed! Labels saved in {labels_dir}")
    print(f"Total images processed: {len(grouped)}")

if __name__ == "__main__":
    convert_csv_to_yolo() 