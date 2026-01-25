from config.config_loader import ConfigLoader
from core.create_folders import make_output_structure
from core.crop_task import Canvas

def run_job(input_dir, output_dir, selected_dimensions):
    """
    Runs the image cropping job for selected canvas dimensions.
    
    Sets up the output structure and processes each selected canvas size by creating
    a Canvas instance and calling crop_image to process all images in the input directory.
    
    Args:
        input_dir (str): Path to the input directory containing images.
        output_dir (str): Path to the output directory for processed images.
        selected_dimensions (list): List of selected canvas dimension IDs to process.
    """
    config = ConfigLoader.initialise_config_loader()
    canvas_data = config.get_canvas_data()
    make_output_structure(input_dir, output_dir)
    for size in canvas_data:
        id = size["id"]
        dpi = size["dpi"]
        dimension_1 = size["dimension_1"]
        dimension_2 = size["dimension_2"]
        if id not in selected_dimensions:
            continue

        canvas = Canvas(id, dpi, dimension_1, dimension_2, input_dir, output_dir, selected_dimensions)
        canvas.crop_image()