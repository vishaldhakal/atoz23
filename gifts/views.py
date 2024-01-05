from http.client import FOUND
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.response import Response
from .models import Customer, Sales, Offers, Gift, FixOffer
from datetime import date
import csv
import json
import random
import re
from rest_framework.decorators import api_view
from transformers import AutoModel, AutoTokenizer
import torch

model_name = "syubraj/sentence_similarity_nepali"
model = AutoModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

sentence_array = [
    "घर/जग्गा नामसारीको सिफारिस गरी पाऊँ",
    "मोही लगत कट्टाको सिफारिस पाउं",
    "घर कायम सिफारीस पाउं",
    "अशक्त सिफारिस",
    "छात्रबृत्तिको लागि सिफारिस पाऊँ",
    "आदिवासी जनजाति प्रमाणित गरी पाऊँ",
    "अस्थायी बसोबासको सिफारिस पाऊँ",
    "स्थायी बसोबासको सिफारिस गरी पाऊँ",
    "आर्थिक अवस्था कमजोर सिफारिस पाऊँ",
    "नयाँ घरमा विद्युत जडान सिफारिस पाऊँ",
    "धारा जडान सिफारिस पाऊँ",
    "दुबै नाम गरेको ब्यक्ति एक्कै हो भन्ने सिफारिस पाऊँ",
    "ब्यवसाय बन्द सिफारिस पाऊँ",
    "व्यवसाय ठाउँसारी सिफारिस पाऊँ",
    "कोर्ट–फिमिनाहा सिफारिस पाऊँ",
    "नाबालक सिफारिस पाऊँ",
    "चौपाया सिफारिस पाऊँ",
    "संस्था दर्ता गरी पाऊँ",
    "विद्यालय ठाउँसारी सिफारिस पाऊँ",
    "विद्यालय संचालन/कक्षा बृद्धिको सिफारिस पाऊँ",
    "जग्गा दर्ता सिफारिस पाऊँ",
    "संरक्षक सिफारिस पाऊँ",
    "बाटो कायम सिफारिस पाऊँ",
    "जिवित नाता प्रमाणित गरी पाऊँ",
    "मृत्यु नाता प्रमाणित गरी पाऊँ",
    "निःशुल्क स्वास्थ्य उपचारको लागि सिफारिस पाऊँ",
    "संस्था दर्ता सिफारिस पाऊँ",
    "घर बाटो प्रमाणित गरी पाऊँ",
    "चारकिल्ला प्रमाणित गरि पाउ",
    "जन्म मिति प्रमाणित गरि पाउ",
    "बिवाह प्रमाणित गरि पाऊँ",
    "घर पाताल प्रमाणित गरी पाऊँ",
    "हकदार प्रमाणित गरी पाऊँ",
    "अबिवाहित प्रमाणित गरी पाऊँ",
    "जग्गाधनी प्रमाण पूर्जा हराएको सिफारिस पाऊँ",
    "व्यवसाय दर्ता गरी पाऊँ",
    "मोही नामसारीको लागि सिफारिस गरी पाऊँ",
    "मूल्याङ्कन गरी पाऊँ",
    "तीन पुस्ते खोली सिफारिस गरी पाऊँ",
    "पुरानो घरमा विद्युत जडान सिफारिस पाऊँ",
    "सामाजिक सुरक्षा भत्ता नाम दर्ता सम्बन्धमा",
    "बहाल समझौता",
    "कोठा खोली पाऊँ",
    "अपाङ्ग सिफारिस पाऊँ",
    "नापी नक्सामा बाटो नभएको फिल्डमा बाटो भएको सिफारिस",
    "धारा नामसारी सिफारिस पाऊँ",
    "विद्युत मिटर नामसारी सिफारिस",
    "फोटो टाँसको लागि तीन पुस्ते खोली सिफारिस पाऊ",
    "कोठा बन्द सिफारिस पाऊँ",
    "अस्थाई टहराको सम्पत्ति कर तिर्न सिफारिस गरी पाऊँ",
    "औषधि उपचार बापत खर्च पाउँ भन्ने सम्वन्धमा",
    "नागरिकता र प्रतिलिपि सिफारिस",
    "अंग्रेजीमा सिफारिस"
]

@api_view(["POST"])
def check_similarity(request):
    try:
        #get data from form data
        voice_text = request.POST['voice_text']

        # Sample voice input (replace this with your actual voice-to-text conversion)
        """ voice_text = "कस्तो सिफारिस गर्नुपर्छ अस्थायी बसोबासको?" """

        # Tokenize the voice_text
        voice_inputs = tokenizer(voice_text, return_tensors="pt")

        # Get the model output (embedding)
        model_output = model(**voice_inputs).logits

        # Calculate similarity scores
        similarity_scores = []
        for sentence in sentence_array:
            sentence_inputs = tokenizer(sentence, return_tensors="pt")
            sentence_output = model(**sentence_inputs).logits

            # You might want to use a different score if the model provides one
            similarity_score = torch.nn.functional.cosine_similarity(model_output, sentence_output).item()
            similarity_scores.append(similarity_score)

        # Find the most similar sentence
        max_similarity_index = similarity_scores.index(max(similarity_scores))
        most_similar_sentence = sentence_array[max_similarity_index]

        result = {
            "voice_text": voice_text,
            "most_similar_sentence": most_similar_sentence,
            "max_similarity_index" : max_similarity_index,
            "similarity_score": max(similarity_scores)
        }

        return Response(result)

    except Exception as e:
        return Response({'error': str(e)})

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
    writer.writerow(['Gift','Date','Count'])
    giftsss = Gift.objects.all()
    for sales in saless:
        for gift in giftsss:
            writer.writerow([gift.name,sales.date,Customer.objects.filter(gift=gift,date_of_purchase=sales.date).count()])
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
        existing_customer = Customer.objects.filter(phone_number=contact_number).first()

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
            # Find a weekly offer based on the number of sales
            weekly_offers = Offers.objects.filter(
                date_valid__lte=today_date,
                date_valid__gte=today_date,
                type_of_offer="Weekly Offer"
            )

            for offer in weekly_offers:
                if ((get_sale_count + 1) in offer.sale_numbers) and (offer.quantity > 0):
                    qty = offer.quantity
                    customer.gift = offer.gift
                    customer.save()
                    offer.quantity = qty - 1
                    offer.save()
                    giftassign = True
                    break

        if not giftassign:
            for offer in Offers.objects.filter(date_valid=today_date).order_by('?'):
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

        return render(request, "output.html", {"customer": customer, "giftassigned": giftassign})
    else:
        return redirect('indexWithError')
