from core.create_folders import make_output_structure
from core.crop_task import Canvas

def run_job(input_dir, output_dir, selected_dimensions):
    """
    Orchestrate the image cropping and processing workflow.
    
    Sets up the output directory structure, retrieves canvas configuration for selected dimensions,
    then processes all images by cropping and resizing them according to the specified canvas dimensions.
    
    Args:
        input_dir (str): Path to directory containing source images.
        output_dir (str): Path to directory where processed images will be organized.
        selected_dimensions (list): List of canvas dimension dictionaries with 'id', 'dimension_1', 
                                   'dimension_2', and 'dpi' properties.
    """
    make_output_structure(input_dir, output_dir)

    canvas = Canvas(
        input_dir=input_dir,
        output_dir=output_dir,
        selected_dimensions=selected_dimensions
    )

    canvas.crop_images()