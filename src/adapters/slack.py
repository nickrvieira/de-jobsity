import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from utils.logger import get_logger_instance


class SlackAlert:

    def __init__(self, slack_token, **kwargs):
        self.client = WebClient(token=slack_token)
        self.logger = get_logger_instance()

    def alert(self, msg: str, channel: str):
        try:
            self.client.chat_postMessage(
                channel=channel,
                text='Pipeline Processing Event',
                blocks=json.dumps(self.format_message(msg)),
        )
        except SlackApiError as e:
            self.logger.exception(e)
            self.logger.error("Slack API not working properly - Message: %s", msg)


    def format_message(self, msg:str):
        slack_message = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Processing Pipeline Event*"
                }
            },
            {
                "type": "divider"
            }
        ]
        body = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": msg
            }
        }

        slack_message.append(body)

        return slack_message