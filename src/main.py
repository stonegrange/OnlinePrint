from ui.app import OnlinePrintUI

def main():
    """
    Entry point for the Online Print Editor application.
    
    Initializes the UI and starts the main event loop, making the application
    available for user interaction and image processing operations.
    """
    app = OnlinePrintUI()
    app.run()

if __name__ == "__main__":
    main()