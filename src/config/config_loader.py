import yaml
import os

#config_path = r"F:/D drive/CODE/ETSY/config_file.yaml"
base_dir = os.path.dirname(__file__)
config_path = os.path.join(base_dir, "config_file.yaml")


def initialise_config():
    """
    Loads the configuration from the YAML file.
    
    Returns:
        dict: The configuration data loaded from config_file.yaml.
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load_all(file)
        config_list = list(config)
        return config_list[0]
    
def with_canvas_data(func):
    """
    Decorator to extract canvas_data from the config.
    
    Args:
        func: The function to decorate.
    
    Returns:
        function: The decorated function that returns only the canvas_data.
    """
    def wrapper(*args, **kwargs):
        config = func(*args, **kwargs)
        return config["canvas_data"]
    return wrapper

def with_extensions(func):
    """
    Decorator to extract extensions from the config.
    
    Args:
        func: The function to decorate.
    
    Returns:
        function: The decorated function that returns only the extensions.
    """
    def wrapper(*args, **kwargs):
        config = func(*args, **kwargs)
        return config["extensions"]
    return wrapper

@with_canvas_data
def get_canvas_data():
    """
    Retrieves the canvas data from the configuration.
    
    Returns:
        list: A list of canvas configurations.
    """
    return initialise_config()

@with_extensions
def get_extensions():
    """
    Retrieves the file extensions from the configuration.
    
    Returns:
        list: A list of supported file extensions.
    """
    return initialise_config()
