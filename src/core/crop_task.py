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

