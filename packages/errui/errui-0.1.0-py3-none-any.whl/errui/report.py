import tkinter as tk

from .base import BaseWindow



class DebugReportWindow(BaseWindow):
    """Display error message and let the end-user decide
    whether to ignore exception and continue the program,
    or to let the exception pass through.
    """
    
    def is_valid(self, exception: Exception) -> bool:
        return isinstance(exception, self.exc_types)

    def open(self, exception: Exception) -> bool:
        # Output for whether to suppress exception or not
        self.suppress = False

        # Options
        title = self.options.get('title', 'Error Message')
        width, height = self.options.get('size', (400, 300))
        font = self.options.get('font', 'sans-serif')
        message = self.options.get('message', 'A non-fatal error has occured.')

        # Root
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f'{width}x{height}')


        # Frame with prompt and buttons

        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP)
        
        # Prompt
        prompt = tk.Label(
            frame,
            text=message,
            font=font,
            borderwidth=8
        )
        prompt.pack(side=tk.LEFT)

        # Abort button
        abort_button = tk.Button(frame, text="Abort", command=self.root.destroy)
        abort_button.pack(side=tk.LEFT)

        # Ignore button
        ignore_button = tk.Button(frame, text="Ignore", command=self.ignore)
        ignore_button.pack(side=tk.LEFT)


        # Error message
        message = tk.Text(
            self.root,
            font='monospace',
            bg='black', fg='white',
            padx=8, pady=8
        )
        message.insert(tk.END, self.create_traceback_message(exception))
        message.config(state='disable')
        message.pack()

        # Launch window
        self.root.mainloop()
        return self.suppress

    def ignore(self):
        """Destroy window and set to suppress exception."""
        self.root.destroy()
        self.suppress = True