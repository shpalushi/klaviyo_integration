import sys

import requests
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import os
import dotenv


# Create your views here.
from klaviyo_integration.settings import BASE_DIR


def get_course_data(course_sku):
    if course_sku == "course-v1:OXF+FIN+03-2021":
        return ["Register", "Oxford Fintech", "31 March 2021"]
    elif course_sku == "course-v1:OXF+FIN+06-2021":
        return ["Register", "Oxford Fintech", "9 June 2021"]
    elif course_sku == "course-v1:OXF+FIN+10-2021":
        return ["Register", "Oxford Fintech", "13 Oct 2021"]
    elif course_sku == "course-v1:OXF+FIN+01-2022":
        return ["Register", "Oxford Fintech", "19 January 2022"]
    elif course_sku == "course-v1:OXF+CYB+03-2021":
        return ["Register", "Oxford Cyber Security", "31 March 2021"]
    elif course_sku == "course-v1:OXF+CYB+06-2021":
        return ["Register", "Oxford Cyber Security", "16 June 2021"]
    elif course_sku == "course-v1:OXF+CYB+10-2021":
        return ["Register", "Oxford Cyber Security", "13 Oct 2021"]
    elif course_sku == "course-v1:OXF+CYB+01-2022":
        return ["Register", "Oxford Cyber Security", "12 January 2022"]
    elif course_sku == "course-v1:OXF+AIF+03-2021":
        return ["Register", "Oxford AI in Finance", "26 May 2021"]
    elif course_sku == "course-v1:OXF+AIF+10-2021":
        return ["Register", "Oxford AI in Finance", "13 Oct 2021"]
    elif course_sku == "course-v1:OXF+AIF+01-2022":
        return ["Register", "Oxford AI in Finance", "19 January 2022"]
    elif course_sku == "course-v1:MIT+HVN+06-2021":
        return ["Register", "MIT Leading Health Tech Innovation", "16 June 2021"]
    elif course_sku == "course-v1:MIT+HVN+10-2021":
        return ["Register", "MIT Leading Health Tech Innovation", "29 September 2021"]
    elif course_sku == "course-v1:MIT+AIL+07-2021":
        return ["Register", "MIT AI Leadership", "7 July 2021"]
    elif course_sku == "course-v1:MIT+AIL+10-2021":
        return ["Register", "MIT AI Leadership", "6 October 2021"]
    elif course_sku == "TEST+TST101+2021_T1":
        return ["Register", "Test Product", "22 September 2021"]
    elif course_sku == "course-v1:OXF+BCH+09-2021":
        return ["Register", "Oxford Blockchain Strategy", "22 September 2021"]
    elif course_sku == "course-v1:OXF+PLT+10-2021":
        return ["Register", "Oxford Platforms and Digital Disruption Programme", "6 October 2021"]
    elif course_sku == "course-v1:OXF+PLT+01-2022":
        return ["Register", "Oxford Platforms and Digital Disruption Programme", "19 January 2022"]
    elif course_sku == "course-v1:CAM+STF+10-2021":
        return ["Register", "Cambridge Startup Funding Pre-seed to Exit Programme", "13 October 2021"]
    elif course_sku == "course-v1:CAM+REG+10-2021":
        return ["Register", "Cambridge RegTech", "20 October 2021"]
    elif course_sku == "course-v1:MIT+AIS+10-2021":
        return ["Register", "MIT AI + Data Strategy", "20 October 2021"]
    else:
        return ["Register", "Registered directly", "No date"]

@method_decorator(csrf_exempt, name="dispatch")
class KlaviyoData(View):

    def post(self, request):

        print(request.META['HTTP_HOST'])

        # begin: get the user data from request
        data = json.loads(request.body.decode("utf-8"))
        customer_title = data.get("customer_title")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        phone = data.get("phone")
        email = data.get("email")
        date_of_birth = data.get("date_of_birth")
        country = data.get("country")
        way_of_contact = data.get("way_of_contact")
        education = data.get("education")
        institution = data.get("institution")
        work_experience = data.get("work_experience")
        pay_type = data.get("pay_type")
        course_sku = data.get("course_name")
        company_name = data.get("company_name")
        course_name = get_course_data(course_sku)[1]
        lead_type = get_course_data(course_sku)[0]
        course_start_date = get_course_data(course_sku)[2]

        # end: get the user data from request

        # get api key from secrets file
        dotenv_file = os.path.join(BASE_DIR, ".env")

        if os.path.isfile(dotenv_file):
            dotenv.load_dotenv(dotenv_file)
        api_key = os.environ['API_KEY']

        PARAMS = {"api_key":api_key,
                  "email": email}
        # Check if user exists in klaviyo
        get_request = requests.get(url='https://a.klaviyo.com/api/v1/segment/YeA2uH/members', params=PARAMS)
        get_data = get_request.json()
        page_size = get_data['page_size']
        if page_size != 0:
            data_info_id = get_data["data"][0]["person"]["id"]
            put_params = {
                "api_key": api_key,
                "salutation": customer_title,
                "date_of_birth": date_of_birth,
                "education": education,
                "$email": email,
                "$first_name": first_name,
                "institution": institution,
                "$last_name": last_name,
                "pay_type": pay_type,
                "$phone_number": phone,
                "way_of_contact": way_of_contact,
                "experience": work_experience,
                "$country": country,
                "course_sku": course_sku,
                "course_name": course_name,
                "lead_type": lead_type,
                "course_start_date": course_start_date,
                "company_name": company_name
            }
            put_request = requests.put(f'https://a.klaviyo.com/api/v1/person/{data_info_id}', params=put_params)
            if put_request.status_code == 200:
                return JsonResponse({"success": True}, status=200)

        # prepare json body
        json_data_send = {
            "token": api_key,
            "event": "Account creation",
            "customer_properties": {
                "salutation": customer_title,
                "date_of_birth": date_of_birth,
                "education": education,
                "$email": email,
                "$first_name": first_name,
                "institution": institution,
                "$last_name": last_name,
                "pay_type": pay_type,
                "$phone_number": phone,
                "way_of_contact": way_of_contact,
                "experience": work_experience,
                "$country": country,
                "course_sku": course_sku,
                "course_name": course_name,
                "lead_type": lead_type,
                "course_start_date": course_start_date,
                "company_name": company_name
            }
        }

        # prepare and send the request
        url = "https://a.klaviyo.com/api/track"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        http_request = requests.post(url, data=json.dumps(json_data_send), headers=headers);

        # check the status of the response
        if http_request.text == '1':
            return JsonResponse({"success": True}, status=200)
        else:
            return JsonResponse({"success": False}, status=400)