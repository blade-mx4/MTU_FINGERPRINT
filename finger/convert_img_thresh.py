import cv2
import os
import glob


def process_directory(input_dir, output_dir, thresh_val=127, extensions=('*.jpg', '*.jpeg', '*.png', '*.bmp')):
    """
    Iterate through all images in input_dir, apply grayscale + binary
    inverse thresholding, and save results to output_dir.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Collect all image paths matching the given extensions
    image_paths = []
    for ext in extensions:
        image_paths.extend(glob.glob(os.path.join(input_dir, ext)))

    if not image_paths:
        print(f"No images found in {input_dir}")
        return

    for path in image_paths:
        img = cv2.imread(path)
        if img is None:
            print(f"Skipping unreadable file: {path}")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, imgz = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)

        filename = os.path.basename(path)
        out_path = os.path.join(output_dir, filename)
        cv2.imwrite(out_path, imgz)
        print(f"Processed: {filename}")

    print(f"Done. {len(image_paths)} image(s) saved to {output_dir}")

if __name__ == "__main__" :
    process_directory(r'C:\Users\blade_mx4\Documents\Datasets\Fingerptint Samples\Real\ID 1\jpg',r'C:\Users\blade_mx4\Documents\Datasets\Fingerptint Samples\Real\ID 1\jpg\train')