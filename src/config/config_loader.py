import yaml
import os

def get_config_path():
    """
    Locate the configuration file path relative to this module.
    
    Returns:
        str: Absolute path to the YAML configuration file.
    """
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, "config_file.yaml")

class ConfigLoader:
    """
    Manages loading and accessing configuration for canvas dimensions and image formats.

    """
    def __init__(self, canvas_data, extensions):
        """
        Initialize the configuration loader with parsed data.
        
        Args:
            canvas_data (list): List of canvas dimension configurations.
            extensions (list): List of supported image file extensions.
        """
        self._canvas_data = canvas_data
        self._extensions = extensions

    @staticmethod
    def initialise_config_loader():
        """
        Load and parse the YAML file.
        
        Returns:
            ConfigLoader: Initialized loader instance with parsed configuration.
        """
        config_path = get_config_path()
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        canvas_data = config.get("canvas_data", [])
        extensions = config.get("image_extensions", [])
        
        return ConfigLoader(canvas_data, extensions)
    
    def get_canvas_data(self):
        """
        Retrieve the canvas dimension configurations.
        
        Returns:
            list: List of canvas configuration dictionaries with dimension and DPI data.
        """
        return self._canvas_data
    
    def get_extensions(self):
        """
        Retrieve the list of supported image file extensions.
        
        Returns:
            list: List of file extension strings (e.g., ['.jpg', '.png', '.tif']).
        """
        return self._extensions

