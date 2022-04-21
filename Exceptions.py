class InvaildURL(ValueError):
    def __init__(self, URL, message="Invaild URL"):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.URL = URL