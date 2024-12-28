from cloudmailin.handlers.base_handler import BaseHandler
from cloudmailin.handlers.steps import assign_campaign_type


class CampaignClassifierHandler(BaseHandler):
    """
    A specialized handler that classifies emails into campaign types.
    """
    steps = [assign_campaign_type]
