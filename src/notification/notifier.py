import os
import sys

# TODO fix this
# Add parent folder to sys.path in order to be able to import
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from typing import List

from notification.discord_sender import DiscordSender
from notification.email_sender import EmailSender
from notification.isender import ISender
from notification.slack_sender import SlackSender
# --- NOVO IMPORT PARA WEBHOOK ---
from notification.webhook_sender import WebhookSender 
# -------------------
from parsers import DAGConfig


class Notifier:
    """Performs the notification delivery through different means as
    defined in the YAML file. Currently it sends notification to email,
    Discord and Slack and Webhooks (like n8n).
    """
    senders = List[ISender]

    def __init__(self, specs: DAGConfig) -> None:
        self.senders = []
        #e-mail
        if specs.report.emails:
            self.senders.append(EmailSender(specs.report))
        #discord
        if specs.report.discord:
            self.senders.append(DiscordSender(specs.report))
        #slack
        if specs.report.slack:
            self.senders.append(SlackSender(specs.report))
        #nova lógica de webhook
        # Verifica se o campo webhook_url foi preenchido no YAML
        if specs.report.webhook_url:
            # Instancia o WebhookSender passando apenas a URL
            self.senders.append(WebhookSender(specs.report.webhook_url))


    def send_notification(self, search_report: str, report_date: str):
        """Sends the notification to the specified email, Discord, Slack or Webhook

        Args:
            search_report (str): The report to be sent
            report_date (str): The date of the report
        """
        # O loop percorre todos os senders ativos e dispara
        for sender in self.senders:
            sender.send_report(search_report, report_date)
