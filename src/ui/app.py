import threading
from tkinter import *
from tkinter import filedialog, messagebox
from config.config_loader import ConfigLoader
from services.job_runner import run_job
class OnlinePrintUI:
    def __init__(self):
        """
        Initialize the Online Print UI application.
        
        Creates the main Tkinter window, initializes string variables for file paths,
        loads configuration data for available canvas dimensions, and builds the user interface.
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
        Construct the complete user interface layout.
        
        Configures window properties, creates and places labels, text entry fields, 
        browse buttons, and initializes checkbuttons for available canvas dimensions.
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

        self.status_var = StringVar(value="Idle")

        self.initialise_checkbuttons()

    def initialise_checkbuttons(self):
        """
        Create checkbox controls for each available canvas dimension.
        
        Dynamically generates checkbutton widgets for all canvas sizes loaded from configuration,
        allowing users to select which dimensions to apply during image processing

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
        Open a file browser dialog to select the input directory.
        
        """
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.input_file_path_label.delete(0, END)
            self.input_file_path_label.insert(0, folder_path)

    def add_output_file_path(self):
        """
        Open a file browser dialog to select the output directory.
        
        """
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_file_path_label.delete(0, END)
            self.output_file_path_label.insert(0, folder_path)

    def get_selected_dimensions(self):
        selected = []

        for canvas in self.canvas_data:
            canvas_id = canvas["id"]
            var = self.vars_by_name.get(canvas_id)

            # Always process 5x7, for use in the mockups to reduce file size as it is the smallest element.
            if canvas_id == "5x7" or (var and var.get()):
                selected.append(canvas)

        return selected

    def process_data(self):
        """
        Validate input parameters and begin the image processing workflow.
        
        Checks that both input and output paths are provided and differ from each other,
        collects selected canvas dimensions, and initiates the background processing job.
        """
        input_path = self.input_file_path_label.get()
        output_path = self.output_file_path_label.get()
        if not input_path or not output_path:
            messagebox.showinfo(title="Oops", message="Please make sure you have selected both input and output file paths.")
            return
        elif input_path == output_path:
            messagebox.showinfo(title="Oops", message="Input and output file paths cannot be the same.")
            return

        self.checked_dimensions = self.get_selected_dimensions()

        self.start()

    def run_background_job(self):
        """
        Execute the image processing job in the background thread.
        
        Retrieves current input/output paths and selected dimensions, then invokes the job runner.
        Handles job completion or failure by scheduling appropriate UI callbacks.
        """
        try:
            input_path = self.input_file_path_label.get()
            output_path = self.output_file_path_label.get()
            selected_dimensions = self.checked_dimensions

            run_job(input_path, output_path, selected_dimensions)

            self.window.after(0, self.on_job_finished)

        except Exception as e:
            self.window.after(0, self.on_job_failed, e)

    def on_job_finished(self):
        self.go_button.config(state="normal")
        self.status_var.set("Done")

        messagebox.showinfo(title="Success", message="Processing completed successfully.")
        self.window.destroy()

    def on_job_failed(self, error):
        self.go_button.config(state="normal")
        self.status_var.set(f"Error: {error}")
        messagebox.showinfo(title="Error", message=f"An error occurred: {error}")
    
    def start(self):
        """
        Launch the image processing job in a background thread.
        
        Disables user interaction during processing, updates status indicator, 
        and spawns a daemon thread to perform cropping operations without blocking the UIe processing has started.
        Runs the job in a separate thread to keep the UI responsive.
        """
        self.go_button.config(state="disabled")
        self.status_var.set("Processing...")
        worker = threading.Thread(target=self.run_background_job, daemon=True)
        worker.start()

    def run(self):
        self.window.mainloop()