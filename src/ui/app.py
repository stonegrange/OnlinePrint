from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from config.config_loader import ConfigLoader
from services.job_runner import run_job

class OnlinePrintUI:
    def __init__(self):
        """
        Initializes the Online Print UI application.
        
        Sets up the main window, variables for input/output paths, and checked dimensions list.
        Calls build_ui to construct the interface.
        """
        self.window = Tk()
        self.input_path_var = StringVar()
        self.output_path_var = StringVar()
        self.checked_dimensions = []

        self.config = ConfigLoader.initialise_config_loader()
        self.canvas_data = self.config.get_canvas_data()
        self.build_ui()

    def build_ui(self):
        """
        Builds the user interface components.
        
        Sets up the window title, canvas, labels, entries, and buttons for input/output paths and start action.
        """
        self.window.title("Online Print Editor")
        self.window.config(padx=50, pady=50)
        self.canvas = Canvas(height=200, width=200)

        #Labels
        self.input_file_path_label = Label(text="Input File Path:")
        self.input_file_path_label.grid(row=1, column=0)
        self.output_file_path_label = Label(text="Output File Path:")
        self.output_file_path_label.grid(row=2, column=0)

        #Entries
        self.input_file_path_label = Entry(textvariable=self.input_path_var, width=50)
        self.input_file_path_label.grid(row=1, column=1)
        self.output_file_path_label = Entry(textvariable=self.output_path_var, width=50)
        self.output_file_path_label.grid(row=2, column=1)

        # Buttons
        self.go_button = Button(text="Start", width=10, command=self.process_data)
        self.go_button.grid(row=4, column=2)
        self.input_file_path_add_button = Button(text="Browse...", width=10, command=self.add_input_file_path)
        self.input_file_path_add_button.grid(row=1, column=4)
        self.output_file_path_add_button = Button(text="Browse...", width=10, command=self.add_output_file_path)
        self.output_file_path_add_button.grid(row=2, column=4)

        self.initialise_checkbuttons()

    #checkbuttons
    def initialise_checkbuttons(self):
        """
        Initializes the checkbuttons for canvas dimensions.
        
        Creates checkbuttons for each canvas size from the config, allowing users to select which dimensions to process.
        """
        self.vars_by_name = {}
        column = 3
        row = 0
        for size in self.canvas_data:
            name = size["id"]
            var = BooleanVar()
            self.vars_by_name[name] = var
            cb = Checkbutton(text=name, variable=var)
            cb.grid(row=row, column=column)
            column += 1

    def add_input_file_path(self):
        """
        Opens a directory selection dialog for the input path.
        
        Allows the user to browse and select the input directory containing images to process.
        Updates the input path entry field with the selected directory.
        """
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.input_file_path_label.delete(0, END)
            self.input_file_path_label.insert(0, folder_path)

    def add_output_file_path(self):
        """
        Opens a directory selection dialog for the output path.
        
        Allows the user to browse and select the output directory where processed images will be saved.
        Updates the output path entry field with the selected directory.
        """
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_file_path_label.delete(0, END)
            self.output_file_path_label.insert(0, folder_path)

    def process_data(self):
        """
        Processes the user input and initiates the job.
        
        Validates input and output paths, collects selected dimensions, and calls the start method.
        Displays success message and closes the window upon completion.
        """
        input_path = self.input_file_path_label.get()
        output_path = self.output_file_path_label.get()
        checked_dimensions = []
        if not input_path or not output_path:
            messagebox.showinfo(title="Oops", message="Please make sure you have selected both input and output file paths.")
            return
        elif input_path == output_path:
            messagebox.showinfo(title="Oops", message="Input and output file paths cannot be the same.")
            return

        for name, var in self.vars_by_name.items():
            #always process 5x7 even if not checked to be used in the mockup generation to reduce file size
            if var.get() or name == "5x7":
                print(f"Processing dimension: {name}")
                checked_dimensions.append(name)
        
        self.checked_dimensions = checked_dimensions

        self.start()

        messagebox.showinfo(title="Success", message="Processing completed successfully.")

        self.window.destroy()

    def start(self):
        """
        Starts the image processing job.
        
        Calls run_job with the input path, output path, and selected dimensions.
        """
        run_job(
            self.input_file_path_label.get(),
            self.output_file_path_label.get(),
            self.checked_dimensions
        )

    def run(self):
        """
        Runs the Tkinter main loop.
        
        Starts the GUI event loop to display the application window.
        """
        self.window.mainloop()