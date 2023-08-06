import boto3
from jinja2 import Template
from datetime import datetime


class DuplicateTemplateException(Exception):
    """ You tried to add a template that already exists. """


class EmailFailedToSendException(Exception):
    """ Email failed to send. """


class EmailClient():
    """ A simple email client for AWS SES system."""
    def __init__(self, sender, region_name="us-west-2"):
        self.sender = sender
        self.client =  boto3.client('ses',region_name=region_name)
        self.templates = dict()

    def add_template(self, template):
        template_name = template.split(".")
        if len(template_name) != 2:
            raise ImproperTemplateNameException("That template has an invalid name!")
        elif template_name[1] != "html":
            raise ImproperTemplateNameException("That template is not html!")
        else:
            template_name = template_name[0]

        if self.templates.get(template_name):
            raise DuplicateTemplateException(
                "That template name has already been created!")

        with open(template, 'r') as f:
            template = Template(f.read())
        self.templates[template_name] = template

    def send_email(self, receiver, template, subject, data):
        if type(data) is not dict and type(data) is not None:
            raise TypeError("Data must be a dictionary or None!")
        if type(receiver) is not list and type(receiver) is not str:
            raise TypeError("Receiver must be a list or string!")

        if not data:
            data = dict()
        filled_template = self.templates[template].render(**data)

        if type(receiver) == str:
            receiver = [receiver]

        try:
            self.client.send_email(
                    Destination={'ToAddresses': receiver},
                    Message={
                        'Body': {
                            'Html': {
                                'Charset': "UTF-8",
                                'Data': filled_template
                            },
                        },
                        'Subject': {
                            'Charset': "UTF-8",
                            'Data': subject,
                        },
                    },
                    Source=self.sender,
                )
        # Display an error if something goes wrong.
        except ClientError:
            print(f"Failed to send email to {receiver} at {datetime.now()}.")
            raise EmailFailedToSendException()
        else:
            print(f"Sent email to {receiver} at{datetime.now()}.")
