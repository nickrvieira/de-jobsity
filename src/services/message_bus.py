import os
from adapters.slack import SlackAlert
from domain import events


SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL", "CHANNEL_SAMPLE")
SLACK_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "BOT_TOKEN")
slack_alert = SlackAlert(SLACK_TOKEN)

params = {"channel":SLACK_CHANNEL}

NOTIFICATION_MAPPING = {
    events.PipelineStarted: [slack_alert,],
    events.PipelineFinish: [slack_alert,],
}


def handle(event: events.Event):
    for handle in NOTIFICATION_MAPPING[type(event)]:
        handle.alert(event.msg, **params)

