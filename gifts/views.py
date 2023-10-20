from http.client import FOUND
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.response import Response
from .models import Customer, Sales, Offers, Gift, FixOffer
from datetime import date
import csv
import json
import random


def index(request):
    return render(request, "index.html")


def indexWithError(request):
    ctx = {
        "error": "Invalid IMEI"
    }
    return render(request, "index.html", ctx)


""" def uploadIMEI(request):
    with open('datas.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        for row in data:
            okk = IMEINO.objects.create(imei_no=row[0])
            okk.save()
    ctx = {
        "error":"Invalid IMEI"
    }
    return render(request, "index.html",ctx)

def uploadCustomer2(request):
    custs = Customer.objects.all()
    custs.delete()
    with open('datas2.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        for row in data:
            if(row[5]!=''):
                gifts = Gift.objects.get(name=row[5])
                customer = Customer.objects.create(customer_name=row[0],phone_number=row[3],shop_name=row[1],sold_area=row[2],phone_model=row[4],sale_status="SOLD",imei=row[6],how_know_about_campaign=row[8],date_of_purchase=row[7],gift=gifts)
                customer.save()
            else:
                customer = Customer.objects.create(customer_name=row[0],phone_number=row[3],shop_name=row[1],sold_area=row[2],phone_model=row[4],sale_status="SOLD",imei=row[6],how_know_about_campaign=row[8],date_of_purchase=row[7])
                customer.save()

            imeiii = IMEINO.objects.get(imei_no=row[6])
            imeiii.used = True
            imeiii.save()
    ctx = {
        "error":"Invalid IMEI"
    }
    return render(request, "index.html",ctx) """

def exportSummary(request):
    saless = Sales.objects.all()
    

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="summary.csv"'

    #Get the count of each of the gifts on each sales day along with ntc_recharge card, its amount and recharge_card
    writer = csv.writer(response)
    writer.writerow(['date','Gift','count'])
    for sales in saless:
        """ Watch,Recharge Card [100],Recharge Card [50],Earphone,T800 Smart Watch,Dubai Tour,Gold Ring,Water Bottle,Ear Buds,X7 Watch,Baby Watch,Powerbank """

        watch = Customer.objects.filter(gift__name="Watch",date_of_purchase=sales.date).count()
        recharge_card_100 = Customer.objects.filter(gift__name="Recharge Card [100]",date_of_purchase=sales.date).count()
        recharge_card_50 = Customer.objects.filter(gift__name="Recharge Card [50]",date_of_purchase=sales.date).count()
        earphone = Customer.objects.filter(gift__name="Earphone",date_of_purchase=sales.date).count()
        t800_smart_watch = Customer.objects.filter(gift__name="T800 Smart Watch",date_of_purchase=sales.date).count()
        dubai_tour = Customer.objects.filter(gift__name="Dubai Tour",date_of_purchase=sales.date).count()
        gold_ring = Customer.objects.filter(gift__name="Gold Ring",date_of_purchase=sales.date).count()
        water_bottle = Customer.objects.filter(gift__name="Water Bottle",date_of_purchase=sales.date).count()
        ear_buds = Customer.objects.filter(gift__name="Ear Buds",date_of_purchase=sales.date).count()
        x7_watch = Customer.objects.filter(gift__name="X7 Watch",date_of_purchase=sales.date).count()
        baby_watch = Customer.objects.filter(gift__name="Baby Watch",date_of_purchase=sales.date).count()
        powerbank = Customer.objects.filter(gift__name="Powerbank",date_of_purchase=sales.date).count()

        writer.writerow([sales.date,"Watch",watch])
        writer.writerow([sales.date,"Recharge Card [100]",recharge_card_100])
        writer.writerow([sales.date,"Recharge Card [50]",recharge_card_50])
        writer.writerow([sales.date,"Earphone",earphone])
        writer.writerow([sales.date,"T800 Smart Watch",t800_smart_watch])
        writer.writerow([sales.date,"Dubai Tour",dubai_tour])
        writer.writerow([sales.date,"Gold Ring",gold_ring])
        writer.writerow([sales.date,"Water Bottle",water_bottle])
        writer.writerow([sales.date,"Ear Buds",ear_buds])
        writer.writerow([sales.date,"X7 Watch",x7_watch])
        writer.writerow([sales.date,"Baby Watch",baby_watch])
        writer.writerow([sales.date,"Powerbank",powerbank])
    return response


def downloadData(request):
    # Get all data from UserDetail Databse Table
    users = Customer.objects.all()

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all.csv"'

    writer = csv.writer(response)
    writer.writerow(['customer_name', 'shop_name', 'product_name',
                     'phone_number', 'gift', 'date_of_purchase', 'how_know_about_campaign'])

    for user in users:
        if user.gift:
            writer.writerow([user.customer_name, user.shop_name, user.product_name, user.phone_number,
                             user.gift.name, user.date_of_purchase, user.how_know_about_campaign])
        else:
            writer.writerow([user.customer_name, user.shop_name, user.product_name,
                             user.phone_number, user.gift, user.date_of_purchase, user.how_know_about_campaign])
    return response


def downloadDataToday(request):
    # Get all data from UserDetail Databse Table
    today_date = date.today()
    users = Customer.objects.filter(date_of_purchase=today_date)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all.csv"'

    writer = csv.writer(response)
    writer.writerow(['customer_name', 'shop_name', 'product_name',
                     'phone_number', 'gift', 'date_of_purchase', 'how_know_about_campaign'])

    for user in users:
        if user.gift:
            writer.writerow([user.customer_name, user.shop_name, user.product_name, user.phone_number,
                             user.gift.name, user.date_of_purchase, user.how_know_about_campaign])
        else:
            writer.writerow([user.customer_name, user.shop_name, user.product_name,
                             user.phone_number, user.gift, user.date_of_purchase, user.how_know_about_campaign])
    return response


from datetime import date
from django.shortcuts import render, redirect
from .models import Customer, Sales, Offers, Gift, FixOffer

def registerCustomer(request):
    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        contact_number = request.POST.get("phone_number")
        shop_name = request.POST.get("shop_name")
        product_name = request.POST.get("product_name")
        how_know_about_campaign = request.POST.get("how_know_about_campaign")

        # Check if the customer already exists
        existing_customer = Customer.objects.filter(
            customer_name=customer_name,
            phone_number=contact_number,
            shop_name=shop_name,
            product_name=product_name,
            how_know_about_campaign=how_know_about_campaign,
        ).first()

        if existing_customer:
            return redirect('index')

        # Create a new customer
        customer = Customer.objects.create(
            customer_name=customer_name,
            phone_number=contact_number,
            shop_name=shop_name,
            product_name=product_name,
            sale_status="SOLD",
            how_know_about_campaign=how_know_about_campaign,
        )

        # Select Gift
        giftassign = False
        today_date = date.today()

        # Ensure there's a Sales record for today
        sale_today, created = Sales.objects.get_or_create(
            date=today_date,
            defaults={'sales_count': 0}
        )
        get_sale_count = sale_today.sales_count
        sale_today.sales_count +=1
        sale_today.save()

        if not created:
            sale_today.sales_count += 1
            sale_today.save()

        # Check if the customer has a specific gift offer (FixOffer)
        fix_offer = FixOffer.objects.filter(
            phone_number=contact_number, quantity__gt=0
        ).first()

        if fix_offer:
            customer.gift = fix_offer.gift
            customer.save()
            giftassign = True
            fix_offer.quantity = 0
            fix_offer.save()

        if not giftassign:
            for offer in Offers.objects.filter(date_valid=today_date,type_of_offer="After every certain sale"):
                if offer.type_of_offer == "After every certain sale":
                    if (((get_sale_count + 1) % int(offer.offer_condtion_value) == 0)) and (offer.quantity > 0):
                        qty = offer.quantity
                        customer.gift = offer.gift
                        customer.save()
                        offer.quantity = qty - 1
                        offer.save()
                        giftassign = True
                        break
                if offer.type_of_offer == "At certain sale position":
                    if ((get_sale_count + 1) == int(offer.offer_condtion_value)) and (offer.quantity > 0):
                        qty = offer.quantity
                        customer.gift = offer.gift
                        customer.save()
                        offer.quantity = qty - 1
                        offer.save()
                        giftassign = True
                        break

        if not giftassign:
            # Find a weekly offer based on the number of sales
            weekly_offers = Offers.objects.filter(
                date_valid__lte=today_date,
                date_valid__gte=today_date,
                type_of_offer="Weekly Offer",
                sale_numbers__contains=[sale_today.sales_count + 1],
                quantity__gt=0
            ).first()

            if weekly_offers:
                customer.gift = weekly_offers.gift
                customer.save()
                weekly_offers.quantity -= 1
                weekly_offers.save()
                giftassign = True

        return render(request, "output.html", {"customer": customer, "giftassigned": giftassign})
    else:
        return redirect('indexWithError')
