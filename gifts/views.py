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


def registerCustomer(request):
    if request.method == "POST":
        customer_name = request.POST["customer_name"]
        contact_number = request.POST["phone_number"]
        shop_name = request.POST["shop_name"]
        product_name = request.POST["product_name"]
        how_know_about_campaign = request.POST["how_know_about_campaign"]

        custt = Customer.objects.filter(
            customer_name=customer_name,
            phone_number=contact_number,
            shop_name=shop_name,
            product_name=product_name,
            how_know_about_campaign=how_know_about_campaign
        )

        if custt:
            return redirect('index')

        customer = Customer.objects.create(
            customer_name=customer_name,
            phone_number=contact_number,
            shop_name=shop_name,
            product_name=product_name,
            sale_status="SOLD",
            how_know_about_campaign=how_know_about_campaign
        )
        customer.save()
        giftassign = False

        """ Select Gift """
        today_date = date.today()
        offers_all = Offers.objects.filter(date_valid=today_date)
        sales_all = Sales.objects.all()
        check = 0
        for sale in sales_all:
            if sale.date == today_date:
                check = 1
        if check == 0:
            saless = Sales.objects.create(sales_count=0, date=today_date)
            saless.save()

        sale_today = Sales.objects.get(date=today_date)
        get_sale_count = sale_today.sales_count
        sale_today.sales_count = get_sale_count + 1
        sale_today.save()

        dsd = FixOffer.objects.all()
        myoff = False

        for off in dsd:
            if (contact_number in off.phone_number):
                if (off.quantity > 0):
                    customer.gift = off.gift
                    customer.save()
                    giftassign = True
                    myoff = True
                    off.quantity = 0
                    off.save()
                    break

        found = False

        if myoff == False:
            while found == False:
                offidlist = []
                for offer in offers_all:
                    offidlist.append(offer.id)
                rand_idx = random.choice(offidlist)
                getofff = Offers.objects.get(id=rand_idx)
                if getofff.quantity > 0:
                    if getofff.type_of_offer == "After every certain sale":
                        if (getofff.quantity > 0):
                            """ Grant Gift """
                            qty = getofff.quantity
                            customer.gift = getofff.gift
                            customer.save()
                            getofff.quantity = qty - 1
                            getofff.save()
                            giftassign = True
                            found = True
                            break
                    else:
                        if (getofff.quantity > 0):
                            """ Grant Gift """
                            qty = getofff.quantity
                            customer.gift = getofff.gift
                            customer.save()
                            getofff.quantity = qty - 1
                            getofff.save()
                            giftassign = True
                            found = True
                            break

        if not giftassign:
            weekly_offers = Offers.objects.filter(
                date_valid__lte=today_date, date_valid__gte=today_date, type_of_offer="Weekly Offer"
            )

            for offer in weekly_offers:
                if (get_sale_count + 1) in offer.sale_numbers and offer.quantity > 0:
                    qty = offer.quantity
                    customer.gift = offer.gift
                    customer.save()
                    offer.quantity = qty - 1
                    offer.save()
                    giftassign = True
                    break

        return render(request, "output.html", {"customer": customer, "giftassigned": giftassign})
    else:
        return redirect('indexWithError')
