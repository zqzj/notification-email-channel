
import dtlpy as dl


class ServiceRunner(dl.BaseServiceRunner):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def notify(self, message, message_context, target, subscription, **kwargs):
        # implement your logic here
        pass
