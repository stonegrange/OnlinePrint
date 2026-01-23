from PIL import Image
import os

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".tif", ".tiff")

class Canvas:
    """
    Creates a canvas depending on a config file and manipulates the image for 
    the use of creating multiple instances of the same image at different aspect 
    ratios and dimensions.
    """

    def __init__(self, id, dpi, dimension_1, dimension_2, input_dir, output_dir, selected_dimensions):
        """
        Initializes a Canvas instance for image cropping.
        
        Args:
            id (str): Identifier for the canvas size (e.g., '5x7').
            dpi (int): Dots per inch for the output image.
            dimension_1 (float): First dimension of the canvas (width or height).
            dimension_2 (float): Second dimension of the canvas (height or width).
            input_dir (str): Path to the input directory containing images.
            output_dir (str): Path to the output directory for processed images.
            selected_dimensions (list): List of selected canvas dimensions.
        """
        self.id = id
        self.dpi = dpi
        self.dimension_1 = dimension_1
        self.dimension_2 = dimension_2
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.selected_dimensions = selected_dimensions

    def crop_image(self):
        """
        Crops and scales an image to the specified target size while maintaining
        the aspect ratio. It will determine wether to create the canvas in portrait
        or landscape depending on the dimensions of the image. Names the files after
        their id

        e.g. A image will be writted as 5x7 if dimension_1 = 5 and dimension_2 = 7.

        Args:
            image_path (str): The path to the input image file.

            dest_dir (str): The path to save the file.
        """
        for filename in os.listdir(self.input_dir):
            if not filename.lower().endswith(IMAGE_EXTENSIONS):
                continue
            name, extension = os.path.splitext(filename)

            image_path = os.path.join(self.input_dir, filename)
            image = Image.open(image_path)
            width, height = image.size
            ratio = width/height
        
            #checks the orientation of the image to determine whether to create the 
            #canvas landscape or portrait.
        
            if width > height:
                canvas_width = self.dimension_2
                canvas_height = self.dimension_1
            else:
                canvas_width = self.dimension_1
                canvas_height = self.dimension_2

            pixel_width = int(canvas_width * self.dpi)
            pixel_height = int(canvas_height * self.dpi)
            target_aspect_ratio = pixel_width/pixel_height

            #Crops the image at the top and bottom if the image is portait.
            if ratio < target_aspect_ratio:
                cropped_height = width / target_aspect_ratio
                crop_amount_height = (height - cropped_height)/2
                cropped_image = image.crop((0, crop_amount_height, width, height - crop_amount_height))
            else:
                cropped_width = height * target_aspect_ratio
                crop_amount_width = (width - cropped_width)/2
                cropped_image = image.crop((crop_amount_width, 0, width - crop_amount_width, height))

            remove_extension = image_path.rsplit('.', 1)[0]

            dest_dir = os.path.join(self.output_dir, os.path.basename(remove_extension))

            save_path = rf"{dest_dir}\Pictures\{self.id}.jpeg"

            resized_image = cropped_image.resize((pixel_width, pixel_height), Image.Resampling.LANCZOS)
            resized_image.save(save_path, quality=100, subsampling=0, dpi=(self.dpi,self.dpi))

            image.close()

# def make_mockup_folders(image_path):
#     """
#     Create a folder at the specified path; If the folder already exists, 
#     raise a FileExistsError.
    
#     Args:
#         image_path (str): The path to the input image file.

#     Returns:
#         mockup_folders (dict): A dictionary containing the paths to the folders for Portrait and Landscape images.
#     """
#     mockup_folders = {}
#     folder_names = ["Portrait", "Landscape"]
#     #creates a folder called "mockup_folders" inside "image_path".
#     mockup_path = os.path.join(image_path, "Mock Ups")
#     make_folder_from_folder_path(mockup_path)
#     #creates folders inside "mockup_path" with the name based strings inside the dictionary "folder_names".
#     for folder in folder_names:
#         folder_path = os.path.join(mockup_path, folder)
#         make_folder_from_folder_path(folder_path)
#         mockup_folders[folder] = folder_path
#     return mockup_folders

# def walk_through_images(image_path):
#     """
#     Walks through the images in a specified folder and copies the 5x7.jpeg image to 
#     the appropriate mockup folder
    
#     Args:
#         image_path (str): The path to the input image file.

#         mockup (dict): A dictionary containing the paths to the folders for Portrait and Landscape images.
#     """
#     for root, dirs, files in os.walk(image_path):
#         #walks though the image_path until it finds a file called 5x7.jpeg.
#         for file in files: 
#             if file == "5x7.jpeg":
#                 src_path = os.path.join(root, file)
#                 #copies the image and renames the image to have the base folders name.
#                 orig_image_name = os.path.basename(os.path.normpath(root))
#                 shutil.copy(src_path+ "/" + orig_image_name + ".jpg")
#                 break

# def initialise_images():
#     files_folder_path = r"F:/D drive/Pictures/ETSY/PUBLIC DOMAIN/TEST"
#     files = os.listdir(files_folder_path)
#     return files, files_folder_path

# def make_folder_from_file_path(image_path):
#     """
#     Create a folder at the specified path based on the name of a file; if it 
#     does not already exist. If the folder already exists, raise a FileExistsError.

#     Creates a folder at the specified path ready for frame mockup template creation.
    
#     Args:
#         image_path (str): The path to the input image file.

#     Returns:
#         dest_dire: The absolute file path of the new directory.
#     """
#     dest_dir = image_path.rsplit('.', 1)[0]
#     return make_folder_from_folder_path(dest_dir)

# def make_folder_from_folder_path(folder_path):
#     """
#     Create a folder at the specified path based on the name of a folder; if it 
#     does not already exist. If the folder already exists, raise a FileExistsError.

#     Creates a folder at the specified path ready for frame mockup template creation.
    
#     Args:
#         folder_path (str): The path to the input folder.

#     Returns:
#         folder_path: The absolute file path of the new directory.
#     """
#     if not os.path.exists(folder_path):
#         try:
#             os.mkdir(folder_path)
#         except OSError as e:
#             print(f"Error creating directory {folder_path}, skipping...")
#             if e.errno != errno.EEXIST:
#                 raise
#     return folder_path

# def main():
#     canvas_data = get_canvas_data()
#     extensions = get_extensions()
#     files, files_folder_path = initialise_images()
#     for file in files:
#         if file.endswith(tuple(extensions)):
#             image_path = (rf"{files_folder_path}\{file}")
#             dest_dir = make_folder_from_file_path(image_path)
#             for size in canvas_data:
#                 id = size['id']
#                 canvas_dimension_1 = size['dimension_1']
#                 canvas_dimension_2 = size['dimension_2']
#                 dpi = size['dpi']
#                 aspect_ratio = Canvas(id, canvas_dimension_1, canvas_dimension_2, dpi, size)
#                 aspect_ratio.crop_image(image_path, dest_dir)
#     mockup = make_mockup_folders(files_folder_path)
#     walk_through_images(files_folder_path, mockup)
#     return 0

# if __name__ == "__main__":
#     sys.exit(main())

