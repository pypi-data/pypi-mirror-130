import logging
import slack_alerts

log = logging.getLogger(__name__)

class SlackRapper(object):
    def __init__(self, **kwargs):
        """
        :param webhook_filename: The webhook filename pointing to a channel that you want to post a message to
        """
        self.slack_alerter = logging.getLogger(__name__)
        try:
            self.filename = kwargs['webhook_filename']
            with open(self.filename, 'r') as file:
                webhook = file.read()
            self.slack_alerter = slack_alerts.Alerter('{}'.format(webhook))
        except FileNotFoundError as e:
            self.slack_alerter.error(f'{self.filename} file not found; using default logger')
            raise
        except KeyError as e:
            self.slack_alerter.warning(f"file not provided; using default logger")

    def notify(self, message):
        self.slack_alerter.info(message)