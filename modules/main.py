
import dtlpy as dl

class NotificationInfo:
    def __init__(self, notification_info: dict):
        self.notification_info = notification_info
        self.notification_info = notification_info.get('notificationId', None)
        self.notification_info = notification_info.get('notificationCode', None)
        self.notification_info = notification_info.get('type', None)
        self.notification_info = notification_info.get('context', None)
        self.notification_info = notification_info.get('priority', None)
        self.notification_info = notification_info.get('eventMessage', None)

class EventMessage:
    def __init__(self, event_message: dict):
        self.event_message = event_message
        self.event_message = event_message.get('title', None)
        self.event_message = event_message.get('description', None)
        self.event_message = event_message.get('resourceAction', None)
        self.event_message = event_message.get('resourceId', None)
        self.event_message = event_message.get('resourceType', None)
        self.event_message = event_message.get('resourceName', None)

class ApplicationInput:
    def __init__(self, application_input: dict):
        self.application_input = application_input
        self.application_input = application_input.get('notificationInfo', None)
        self.application_input = application_input.get('recipients', None)
        self.application_input = application_input.get('notificationId', None)

class ServiceRunner(dl.BaseServiceRunner):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def notify(self, input: dict, **kwargs):
        application_input = ApplicationInput(input)
        # with open('email_template.html', 'r') as file:
        #     template_string = file.read()

        req_data = {
            "to": application_input.recipients,
            "from": "notifications@dataloop.ai",
            "subject": application_input.notification_info.event_message.title,
            "body": application_input.notification_info.event_message.description,
        }
        success_pack, response_pack = dl.client_api.gen_request(req_type='post',
                                                                   json_req=req_data,
                                                                   path='/outbox')