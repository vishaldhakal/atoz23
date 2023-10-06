from pyexpat import model
from statistics import mode
from django.db import models


class Sales(models.Model):
    sales_count = models.IntegerField(default=0)
    date = models.DateField(
        auto_now=False, auto_created=False, auto_now_add=False)

    def __str__(self):
        return str(self.sales_count)


class Gift(models.Model):
    name = models.CharField(max_length=400)
    image_url = models.FileField()

    def __str__(self):
        return self.name


class Offers(models.Model):

    OFFER_CHOICES = [
        ("After every certain sale", "After every certain sale"),
        ("At certain sale position", "At certain sale position"),
        ("Weekly Offer", "Weekly Offer"),
    ]

    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    date_valid = models.DateField(auto_now_add=False, auto_now=False)
    quantity = models.IntegerField()
    type_of_offer = models.CharField(max_length=800, choices=OFFER_CHOICES)
    offer_condtion_value = models.IntegerField()
    sale_numbers = models.JSONField(null=True, blank=True)


    def __str__(self):
        return "Offer on "+self.gift.name




class Customer(models.Model):

    CAMPAIGN_CHOICES = [
        ("Facebook Ads", "Facebook Ads"),
        ("Reatil Shop", "Reatil Shop"),
        ("Google Ads", "Google Ads"),
        ("Others", "Others"),
    ]

    customer_name = models.CharField(max_length=400)
    shop_name = models.TextField(default="A to Z")
    product_name = models.CharField(max_length=800)
    phone_number = models.CharField(max_length=400)
    sale_status = models.CharField(max_length=400, default="SOLD")
    prize_details = models.CharField(
        max_length=900, default="Happy Vijaya Dashami & Dipawali 2079")
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE, null=True)
    date_of_purchase = models.DateField(auto_now_add=True, auto_now=False)
    how_know_about_campaign = models.CharField(
        max_length=800, choices=CAMPAIGN_CHOICES)

    def __str__(self):
        return self.customer_name

class FixOffer(models.Model):
    phone_number = models.CharField(max_length=400)
    customer_name = models.CharField(max_length=400)
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()