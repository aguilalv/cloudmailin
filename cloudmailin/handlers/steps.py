from cloudmailin.schemas import Email


def assign_campaign_type(email: Email) -> Email:
    """
    Step function to classify the email and assign a campaign type.
    """
    if "sale" in email.subject.lower():
        campaign_type = "promotion"
#    elif "newsletter" in email.subject.lower():
#        campaign_type = "newsletter"
    else:
        campaign_type = "unclassified"

    return email.model_copy(update={"campaign_type": campaign_type})
