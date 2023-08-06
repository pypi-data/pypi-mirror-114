class IPFSConnectionError(Exception):
    """Exception raised for errors when connectoin not stablis.
    Attributes:
        salary -- input salary which caused the error
        message -- explanation of the error
    """
    def __init__(self, message="your ipfs server is not working correctly please run : ipfs daemon"):
        self.message = message
        super().__init__(self.message)