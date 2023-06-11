import base64
import dtlpy as dl

template = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>

<head>
    <meta content="IE=edge" http-equiv="X-UA-Compatible" />
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
    <meta content="width=device-width, initial-scale=1.0" name="viewport" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">

    <title>confirmation email</title>
    <style type="text/css">
        @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
        .body{
            margin: 0;
            width: 1200px;
            height: 750px;
            background: #F8F8F8;
            font-family: Roboto;
        }
        .email-notification-body{
            font-weight: 400;
            position: absolute;
            margin-left:230px;
            color:black !important;
        }
        .mail-body{
            width:740px;
            height: 750px;
            box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 4px;
            background: #FFFFFF;
            padding: 50px;
        }
        .mail-header{
            display: block;
            margin-bottom: 40px;
        }
        .mail-header-img{
            display: inline-block;
            width: 127px ;
            height: 22px;
        }
        .mail-title{
            margin-bottom: 30px;
        }
        .mail-title-head{
            font-size: 30px;
            font-weight: 600;
            margin-bottom: 20px;
            color:black !important;
        }
        .mail-title-content{
            color:#171723;
            font-size: 14px;
        }
        .mail-next-date-display-none{
            display: none;
        }
        .mail-notes{
            font-size: 12px;
            color:#767676;
            line-height: 20px;
        }
        .mail-separator{
            width:85%;
            border: 1px solid #E4E4E4;
        }
        .mail-end{
            color:#999999;
            font-size: 12px;
        }
        a{
            color:#516AFF;
            text-decoration:none;
        }
        .mail-links{
            margin-bottom: 40px;
        }
        .link-title {
            margin-bottom: 10px;
            color: #171723;
        }
        .contact-support {
            margin-bottom: 270px;
        }
        .pad-left {
            padding-left: 34px;
        }
        .notification-icon{
            display: inline-block;
            height: 24px;
            width: 24px;
        }
        .mail-title-text{
            padding-left: 10px;
        }
    </style>
</head>

<body dir="ltr" class="body" background="#F4F6FB" style="background-color: #F4F6FB;">
    <div class="email-notification-body">
        <div class="mail-body">
            <div class="mail-header">
                <img class ="mail-header-img" src="@@dataloopLogo@@" alt="Dataloop logo" />
            </div>
            <div class="mail-title">

                <div class="mail-title-head">
                    <img class="notification-icon" src="@@notificationIcon@@" alt="notification icon" />
                    <span class="mail-title-text">##title##</span>
                </div>
                <div class="mail-title-content pad-left">##description##</div>
            </div>
            <div class="mail-links pad-left">
                <div class="link-title">
                    To view the problem, follow the links below:
                </div>
                $$projectLink$$
                $$serviceLink$$
            </div>
            <div class="contact-support pad-left">
                If you have any questions, you can get in touch with us at <a href="mailto: support@dataloop.ai">support@dataloop.ai</a>
            </div>
            <div class="mail-separator"></div>
            <div class="mail-end">This message was generated automatically. Please do not reply to this email.</div>
        </div>
    </div>
</body>

</html>

'''

class EventMessage:
    def __init__(self, event_message: dict):
        if event_message is None:
            raise ValueError('event_message is None')
        if event_message.get('title', None) is None:
            raise ValueError('title is None')
        if event_message.get('description', None) is None:
            raise ValueError('description is None')
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
        self.resource_names = dict()

    def get_resource_name(self, resource_id, callback: callable):
        if resource_id in self.resource_names:
            return self.resource_names[resource_id]
        else:
            try:
                resource = callback(resource_id)
                self.resource_names[resource_id] = resource.name
                return resource.name
            except:
                return resource_id

    @staticmethod
    def get_service(service_id):
        return dl.services.get(service_id=service_id)

    @staticmethod
    def get_project(project_id):
        return dl.projects.get(project_id=project_id)

    def build_logo_attachment(self):
        dataloop_image_id = 'dataloop_logo'
        dataloop_logo_file_content = open('../assets/logo-dataloop.png', 'rb').read()
        dataloop_logo_base64_utf8_str = base64.b64encode(dataloop_logo_file_content).decode('utf-8')
        return {
            "filename": "logo-dataloop",
            "contentType": "image/png",
            "content_id": dataloop_image_id,
            "content": dataloop_logo_base64_utf8_str,
            "disposition": "inline"
        }

    def insertLinks(self, html_template_string, application_input: ApplicationInput):
        compiled = html_template_string
        project = application_input.notification_info.context.get('project', None)
        service = application_input.notification_info.context.get('service', None)
        replaced_project = False
        replaced_service = False

        if project is not None:
            env_prefix = dl.client_api.environments[dl.client_api.environment].get('url', None)
            project_link_prefix = env_prefix + "projects/"
            project_name = self.get_resource_name(project, self.get_project)
            compiled = compiled.replace('$$projectLink$$',
                                        '<div><span style="color: #171723;">Project:</span><a href={0}>{1}</a></div>'.format(
                                            project_link_prefix+project, project_name))
            replaced_project = True
            if service is not None:
                service_link_prefix = env_prefix+"projects/{}/services/".format(project)
                service_name = self.get_resource_name(service, self.get_service)
                compiled = compiled.replace('$$serviceLink$$',
                                            '<div><span style="color: #171723;">Service:</span><a href={0}>{1}</a></div>'.format(
                                                service_link_prefix+service, service_name))
                replaced_service = True

        if not replaced_project:
            compiled = compiled.replace('$$projectLink$$', '')
        if not replaced_service:
            compiled = compiled.replace('$$serviceLink$$', '')

        return compiled

    def build_icon_attachment(self, application_input: ApplicationInput):
        priority = application_input.notification_info.priority
        icon_image_id = 'notification_icon'
        icon_file = None
        if priority <= 50:
            icon_file = open('../assets/icon-dl-info-filled.png', 'rb').read()
        elif priority <= 75:
            icon_file = open('../assets/icon-dl-alert-filled.png', 'rb').read()
        else:
            icon_file = open('../assets/icon-dl-error-filled.png', 'rb').read()

        dataloop_logo_base64_utf8_str = base64.b64encode(icon_file).decode('utf-8')
        return {
            "filename": "notification-icon-dataloop",
            "contentType": "image/png",
            "content_id": icon_image_id,
            "content": dataloop_logo_base64_utf8_str,
            "disposition": "inline"
        }

    def compile_html(self, html_template_string, application_input: ApplicationInput):
        attachments = []
        compiled = html_template_string
        compiled = compiled.replace('##title##', application_input.notification_info.event_message.title)
        compiled = compiled.replace('##description##', application_input.notification_info.event_message.description)
        logo_attachment = self.build_logo_attachment()
        attachments.append(logo_attachment)
        icon_attachment = self.build_icon_attachment(application_input=application_input)
        attachments.append(icon_attachment)
        compiled = compiled.replace('@@dataloopLogo@@', 'cid:'+logo_attachment['content_id'])
        compiled = compiled.replace('@@notificationIcon@@', 'cid:' + icon_attachment['content_id'])
        #   todo: replace icon with attachment once it works
        compiled = self.insertLinks(html_template_string=compiled, application_input=application_input)
        return compiled, attachments

    def email(self, input: dict, **kwargs):
        application_input = ApplicationInput(input)
        # with open('email_template.html', 'r') as file:
        #     template_string = file.read()

        template_string = template

        [compiled_html, attachments] = self.compile_html(html_template_string=template_string, application_input=application_input)

        req_data = {
            "to": application_input.recipients,
            "from": "notifications@dataloop.ai",
            "subject": application_input.notification_info.event_message.title,
            "body": compiled_html,
            "attachments": attachments
        }
        if application_input.recipients is None or len(application_input.recipients) == 0:
            return
        dl.client_api.gen_request(req_type='post', json_req=req_data, path='/outbox')