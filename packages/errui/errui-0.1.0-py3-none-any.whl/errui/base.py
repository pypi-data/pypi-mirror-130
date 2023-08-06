import traceback



class BaseWindow:
    """Templatable class for error windows"""

    def __init__(self, *exc_types: tuple[type[Exception]], **options: dict):
        self.exc_types = exc_types
        self.options = options

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # Open the window with defined exception types
        # Let other types pass through and get raised

        # Recreate exception
        exception = exc_type(exc_value).with_traceback(exc_traceback)

        # Check whether to even process the exception
        if not self.is_valid(exception):
            return False

        # Open window with exception
        return self.open(exception)
        
    def is_valid(self, exception: Exception) -> bool:
        """Determine whether to let an exception through."""
        raise NotImplementedError()

    def create_traceback_message(self, exception: Exception) -> str:
        """Create error message from exception."""
        return "".join(traceback.format_exception(
                    type(exception), exception, exception.__traceback__))

    def open(self, exception: Exception) -> bool:
        """Open a window for the end-user to decide action."""
        raise NotImplementedError()