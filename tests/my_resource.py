class MyResource:
    def __enter__(self):
        # Setup phase
        self.resource1 = "Resource 1"
        self.resource2 = "Resource 2"
        print("my_resource.py:Setting up resources...")
        return self  # Return self or a tuple of resources

    def __exit__(self, exc_type, exc_value, traceback):
        # Cleanup phase
        print("my_resource.py:Cleaning up resources...")
        return False  # Suppress exceptions if needed

    def get_resources(self):
        return self.resource1, self.resource2
