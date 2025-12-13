import sys
from PIL import Image

def crop_center_landscape(image_path, output_path, aspect_ratio=(16, 9)):
    with Image.open(image_path) as img:
        width, height = img.size
        target_height = int(width * aspect_ratio[1] / aspect_ratio[0])
        
        if target_height > height:
             # Image is too wide, crop width
            target_width = int(height * aspect_ratio[0] / aspect_ratio[1])
            left = (width - target_width) / 2
            top = 0
            right = (width + target_width) / 2
            bottom = height
        else:
            # Image is too tall, crop height
            target_width = width
            left = 0
            top = (height - target_height) / 2
            right = width
            bottom = (height + target_height) / 2
            
        cropped_img = img.crop((left, top, right, bottom))
        cropped_img.save(output_path)
        print(f"Cropped image saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python crop_image.py <input_path> <output_path>")
        sys.exit(1)
        
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    crop_center_landscape(input_path, output_path)
