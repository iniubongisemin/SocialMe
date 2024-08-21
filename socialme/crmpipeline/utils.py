# from django.core.mail import send_mail
# from crm_pipeline.task import send_email_via_mailgun
from crmpipeline.tasks import send_email
from django.template import Template, Context
from django.core import signing
from decouple import config
from crmpipeline.reusables import status_code as code
from rest_framework.response import Response


def stage_notification(stage_instance, deal):
    subject = stage_instance.email_subject
    body = stage_instance.email_body
    to_email = deal.email

    # Encode the deal_id using a token
    # invitation_token = signing.dumps(deal.id, key=config("SIGNING_KEY"))
    # BASE_URL = config("BACKEND_BASE_URL")
    
    
    context = {
        "deal_name": deal.deal_title,
    }

    # Create a Template object with the decoded custom message
    email_template = Template(body)

    # Render the email message with the context
    email_message = email_template.render(Context(context))

    send_email(subject, email_message, to_email, deal_id=deal.deal_id)


class DataResponse:
    def __init__(self, success: bool, status_code: int, data, message: str) -> None:
        """
        Response data in json
        """
        self.success = success
        self.message = message
        self.data = data
        self._code = code()[status_code]

    def respond(self) -> Response:
        data = dict(message=self.message, success=self.success, response=self.data)
        return Response(data=data, status=self._code)

