class InvaildURL(ValueError):
    def __init__(self, URL, message="Invaild URL"):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.URL = URL

class InvaildTag(ValueError):
    def __init__(self,message="Invaild Tag"):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)