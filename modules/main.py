
import dtlpy as dl

class EventMessage:
    def __init__(self, event_message: dict):
        if event_message is None:
            raise ValueError('event_message is None')
        if event_message.get('title', None) is None:
            raise ValueError('title is None')
        if event_message.get('description', None) is None:
            raise ValueError('description is None')
        if event_message.get('resourceAction', None) is None:
            raise ValueError('resourceAction is None')
        if event_message.get('resourceId', None) is None:
            raise ValueError('resourceId is None')
        if event_message.get('resourceType', None) is None:
            raise ValueError('resourceType is None')
        self.title = event_message.get('title', None)
        self.description = event_message.get('description')
        self.resource_action = event_message.get('resourceAction')
        self.resource_id = event_message.get('resourceId')
        self.resource_type = event_message.get('resourceType')
        self.resource_name = event_message.get('resourceName', None)

class NotificationInfo:
    def __init__(self, notification_info: dict):
        if notification_info is None:
            raise ValueError('notification_info is None')
        if notification_info.get('notificationCode', None) is None:
            raise ValueError('notificationCode is None')
        if notification_info.get('context', None) is None:
            raise ValueError('context is None')
        if notification_info.get('priority', None) is None:
            raise ValueError('priority is None')
        if notification_info.get('eventMessage', None) is None:
            raise ValueError('eventMessage is None')
        self.notification_code = notification_info.get('notificationCode')
        self.type = notification_info.get('type', None)
        self.context = notification_info.get('context')
        self.priority = notification_info.get('priority')
        self.event_message = EventMessage(notification_info.get('eventMessage'))


class ApplicationInput:
    def __init__(self, application_input: dict):
        if application_input is None:
            raise ValueError('application_input is None')
        if application_input.get('notificationInfo', None) is None:
            raise ValueError('notificationInfo is None')
        if application_input.get('recipients', None) is None:
            raise ValueError('recipients is None')
        if application_input.get('notificationId', None) is None:
            raise ValueError('notificationId is None')
        self.notification_info = NotificationInfo(application_input.get('notificationInfo'))
        self.recipients = application_input.get('recipients')
        self.notification_id = application_input.get('notificationId')

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
        if application_input.recipients is None or len(application_input.recipients) == 0:
            raise ValueError('recipients is None or empty')
        success_pack, response_pack = dl.client_api.gen_request(req_type='post',
                                                                   json_req=req_data,
                                                                   path='/outbox')