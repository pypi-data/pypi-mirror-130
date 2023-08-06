from django.db import models


class DigRule(models.Model):
    """
        Blocker: block allthe listed IPs for listed URLs
        Allower: allow only the listed IPs for listed URLs
        *** Only first row is counted ***
    """
    blocker_url_patterns = models.TextField(null=True, blank=True, help_text="Separate URL patterns with new line. Regex supported in each new line.")
    blocker_ip_patterns = models.TextField(null=True, blank=True, help_text="Separate IP patterns with new line. Regex supported in each new line.")
    allower_url_patterns = models.TextField(null=True, blank=True, help_text="Separate URL patterns with new line. Regex supported in each new line.")
    allower_ip_patterns = models.TextField(null=True, blank=True, help_text="Separate IP patterns with new line. Regex supported in each new line.")
