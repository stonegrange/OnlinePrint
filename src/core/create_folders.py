import os
import errno
import shutil

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".tif", ".tiff")

def make_output_structure(input_dir, output_dir):
    """
    Creates the output directory structure for processed images.
    
    Sets up the main output directory and subdirectories for each image in the input directory.
    Creates 'MockUps' and 'Pictures' subdirectories in each image folder and copies the original image.
    
    Args:
        input_dir (str): Path to the input directory containing images.
        output_dir (str): Path to the output directory where structure will be created.
    """
    try:
        os.makedirs(output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(IMAGE_EXTENSIONS):
            continue

        name, extension = os.path.splitext(filename)

        image_folder = os.path.join(output_dir, name)
        picture_folder = os.path.join(image_folder, "Pictures")
        mockups_folder = os.path.join(image_folder, "MockUps")

        # Create image folder
        try:
            os.makedirs(image_folder)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        # Create MockUps folder
        try:
            os.makedirs(mockups_folder)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        # Create Pictures folder
        try:
            os.makedirs(picture_folder)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        # Copy original image to image folder
        src = os.path.join(input_dir, filename)
        dst = os.path.join(image_folder, filename)

        shutil.copy2(src, dst)