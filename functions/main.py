
import dtlpy as dl


class ServiceRunner(dl.BaseServiceRunner):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def notify(self, message: str, recipients: List[str], subscription=None, message_context=None, **kwargs):
        # implement your logic here
        pass
