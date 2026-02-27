from PIL import Image
import os

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".tif", ".tiff")

class CanvasManager:
    """
    Handles image cropping and resizing for specific canvas dimensions. 
    Whilst mainitaining aspect ratio preservation and DPI
    
    """
    def __init__(self, input_dir, output_dir, selected_dimensions):
        """
        Initialize the Canvas processor with source and destination paths.
        
        Args:
            input_dir (str): Directory containing source images to process.
            output_dir (str): Base directory where cropped images will be saved.
            selected_dimensions (list): List of canvas dimension dictionaries to apply.
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.selected_dimensions = selected_dimensions

    def crop_images(self):
        """
        Process all images in the input directory for selected canvas dimensions.
        
        Iterates through supported image formats and applies canvas-specific cropping
        to each image, saving results to output directories.
        """
        for filename in os.listdir(self.input_dir):
            if not filename.lower().endswith(IMAGE_EXTENSIONS):
                continue

            image_name, _ = os.path.splitext(filename)
            image_path = os.path.join(self.input_dir, filename)

            pictures_dir = os.path.join(self.output_dir,image_name,"Pictures")
           
            for canvas in self.selected_dimensions:
                self.process_single_canvas(image_path=image_path,pictures_dir=pictures_dir,canvas=canvas)

    def process_single_canvas(self, image_path, pictures_dir, canvas):

        canvas_id = canvas["id"]
        d1 = canvas["dimension_1"]
        d2 = canvas["dimension_2"]
        dpi = canvas["dpi"]

        with Image.open(image_path) as image:
            width, height = image.size
            ratio = width / height

            # Checks image is landscape or portrait to crop correctly
            if width > height:
                canvas_width = d2
                canvas_height = d1
            else:
                canvas_width = d1
                canvas_height = d2

            pixel_width = int(canvas_width * dpi)
            pixel_height = int(canvas_height * dpi)
            target_ratio = pixel_width / pixel_height

            # If the source image is taller than the target aspect ratio, then crop top/bottom. Otherwise Crop left/right
            if ratio < target_ratio:
                cropped_height = width / target_ratio
                crop = (height - cropped_height) / 2
                cropped = image.crop((0, crop, width, height - crop))
            else:
                cropped_width = height * target_ratio
                crop = (width - cropped_width) / 2
                cropped = image.crop((crop, 0, width - crop, height))

            resized = cropped.resize((pixel_width, pixel_height),Image.Resampling.LANCZOS)
            save_path = os.path.join(pictures_dir,f"{canvas_id}.jpeg")
            resized.save(save_path,quality=100,subsampling=0,dpi=(dpi, dpi))