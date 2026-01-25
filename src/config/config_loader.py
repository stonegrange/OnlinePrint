import yaml
import os

def get_config_path():
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, "config_file.yaml")

class ConfigLoader:
    def __init__(self, canvas_data, extensions):
        self._canvas_data = canvas_data
        self._extensions = extensions

    @staticmethod
    def initialise_config_loader():
        config_path = get_config_path()
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        canvas_data = config.get("canvas_data", [])
        extensions = config.get("image_extensions", [])
        
        return ConfigLoader(canvas_data, extensions)
    
    def get_canvas_data(self):
        return self._canvas_data
    
    def get_extensions(self):
        return self._extensions

