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
        return ["Register", "Oxford Fintech", "31/032021"]
    elif course_sku == "course-v1:OXF+FIN+06-2021":
        return ["Register", "Oxford Fintech", "09/06/2021"]
    elif course_sku == "course-v1:OXF+FIN+10-2021":
        return ["Register", "Oxford Fintech", "13/10/2021"]
    elif course_sku == "course-v1:OXF+FIN+01-2022":
        return ["Register", "Oxford Fintech", "19/01/2022"]
    elif course_sku == "course-v1:OXF+CYB+03-2021":
        return ["Register", "Oxford Cyber Security", "31/03/2021"]
    elif course_sku == "course-v1:OXF+CYB+06-2021":
        return ["Register", "Oxford Cyber Security", "16/06/2021"]
    elif course_sku == "course-v1:OXF+CYB+10-2021":
        return ["Register", "Oxford Cyber Security", "13/10/2021"]
    elif course_sku == "course-v1:OXF+CYB+01-2022":
        return ["Register", "Oxford Cyber Security", "12/01/2022"]
    elif course_sku == "course-v1:OXF+AIF+03-2021":
        return ["Register", "Oxford AI in Finance", "26/05/2021"]
    elif course_sku == "course-v1:OXF+AIF+10-2021":
        return ["Register", "Oxford AI in Finance", "13/10/2021"]
    elif course_sku == "course-v1:OXF+AIF+01-2022":
        return ["Register", "Oxford AI in Finance", "19/01/2022"]
    elif course_sku == "course-v1:MIT+HVN+06-2021":
        return ["Register", "MIT Leading Health Tech Innovation", "16/06/2021"]
    elif course_sku == "course-v1:MIT+HVN+10-2021":
        return ["Register", "MIT Leading Health Tech Innovation", "29/09/2021"]
    elif course_sku == "course-v1:MIT+AIL+07-2021":
        return ["Register", "MIT AI Leadership", "07/07/2021"]
    elif course_sku == "course-v1:MIT+AIL+10-2021":
        return ["Register", "MIT AI Leadership", "06/10/2021"]
    elif course_sku == "TEST+TST101+2021_T1":
        return ["Register", "Test Product", "22/09/2021"]
    elif course_sku == "course-v1:OXF+BCH+09-2021":
        return ["Register", "Oxford Blockchain Strategy", "22/09/2021"]
    elif course_sku == "course-v1:OXF+PLT+10-2021":
        return ["Register", "Oxford Platforms and Digital Disruption Programme", "06/10/2021"]
    elif course_sku == "course-v1:OXF+PLT+01-2022":
        return ["Register", "Oxford Platforms and Digital Disruption Programme", "19/01/2022"]
    elif course_sku == "course-v1:CAM+STF+10-2021":
        return ["Register", "Cambridge Startup Funding Pre-seed to Exit Programme", "13/10/2021"]
    elif course_sku == "course-v1:CAM+REG+10-2021":
        return ["Register", "Cambridge RegTech", "20/10/2021"]
    elif course_sku == "course-v1:MIT+AIS+10-2021":
        return ["Register", "MIT AI + Data Strategy", "20/10/2021"]
    else:
        return ["Register", "Registered directly", "No date"]

def get_course_list_id_by_name(course_name):
    if 'Oxford AI in Finance and Open Banking Programme' in course_name:
        return 'WcKGQ9';
    elif 'Oxford Cyber Security for Business Leaders' in course_name:
        return 'TZxxBB';
    elif 'Oxford Fintech Programme' in course_name:
        return 'Xc6gPR';
    elif 'Oxford Blockchain Strategy Programme' in course_name:
        return 'TwVVNu';
    elif 'Oxford Platforms and Digital Disruption Programme' in course_name:
        return 'VKzR9b';
    elif 'Oxford Digital Finance Executive Series' in course_name:
        return 'SfNK2f';
    elif 'AI Leadership' in course_name:
        return 'RDERB6';
    elif 'AI Startups & Innovation Programme' in course_name:
        return 'SviuU3';
    elif 'Cambridge RegTech: AI for Financial Regulation, Risk, and Compliance Programme' in course_name:
        return 'TV2tsc';
    elif 'Cambridge Startup Funding: Pre-seed to Exit Programme' in course_name:
        return 'TugwLF';
    elif 'Data Strategy: Leverage AI for Business' in course_name:
        return 'UF9Pah';
    elif 'Leading Health Tech Innovation' in course_name:
        return 'VKjeTG';
    else:
        return  -1;


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
        biller_email = data.get("biller_email")

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
                "whoispaying": pay_type,
                "$phone_number": phone,
                "how_can_we_contact_you_about_this_course": way_of_contact,
                "experience": work_experience,
                "$country": country,
                "course_sku": course_sku,
                "courseName": course_name,
                "lead_status": lead_type,
                "course_start_date": course_start_date,
                "Organization": company_name,
                "Biller_email": biller_email
            }
            put_request = requests.put(f'https://a.klaviyo.com/api/v1/person/{data_info_id}', params=put_params)
            if put_request.status_code == 200:
                # get api key from secrets file
                dotenv_file = os.path.join(BASE_DIR, ".env")

                if os.path.isfile(dotenv_file):
                    dotenv.load_dotenv(dotenv_file)
                api_key = os.environ['API_KEY']
                data = json.loads(request.body.decode("utf-8"))

                ######This data needs to be sent#######
                email = data.get("email")
                course_name = data.get("course_title")
                list_id = get_course_list_id_by_name(course_name)
                phone = data.get('phone')
                ######This data needs to be sent#######

                url = f"https://a.klaviyo.com/api/v2/list/{list_id}/members"

                querystring = {"api_key": api_key}

                payload = {"profiles": [{"email": email}]}
                headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }

                response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

                if '"id"' in response.text:
                    return JsonResponse({"success": "Also included"}, status=200)
                else:
                    return JsonResponse({"success": False}, status=400)

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
                "whoispaying": pay_type,
                "$phone_number": phone,
                "how_can_we_contact_you_about_this_course": way_of_contact,
                "experience": work_experience,
                "$country": country,
                "course_sku": course_sku,
                "courseName": course_name,
                "lead_status": lead_type,
                "course_start_date": course_start_date,
                "Organization": company_name,
                "Biller_email": biller_email
            }
        }

        # prepare and send the request
        url = "https://a.klaviyo.com/api/track"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        http_request = requests.post(url, data=json.dumps(json_data_send), headers=headers);

        # check the status of the response
        if http_request.text == '1':
            # get api key from secrets file
            dotenv_file = os.path.join(BASE_DIR, ".env")

            if os.path.isfile(dotenv_file):
                dotenv.load_dotenv(dotenv_file)
            api_key = os.environ['API_KEY']
            data = json.loads(request.body.decode("utf-8"))

            ######This data needs to be sent#######
            email = data.get("email")
            course_name = data.get("course_title")
            list_id = get_course_list_id_by_name(course_name)
            phone = data.get('phone')
            ######This data needs to be sent#######

            url = f"https://a.klaviyo.com/api/v2/list/{list_id}/members"

            querystring = {"api_key": api_key}

            payload = {"profiles": [{"email": email}]}
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

            if '"id"' in response.text:
                return JsonResponse({"success": "Also included"}, status=200)
            else:
                return JsonResponse({"success": False}, status=400)
        else:
            return JsonResponse({"success": False}, status=400)

@method_decorator(csrf_exempt, name="dispatch")
class KlaviyoDataList(View):

    def post(self, request):
        # get api key from secrets file
        dotenv_file = os.path.join(BASE_DIR, ".env")

        if os.path.isfile(dotenv_file):
            dotenv.load_dotenv(dotenv_file)
        api_key = os.environ['API_KEY']
        data = json.loads(request.body.decode("utf-8"))

        ######This data needs to be sent#######
        email = data.get("email")
        course_name = data.get("course_title")
        list_id = get_course_list_id_by_name(course_name)
        phone = data.get('phone')
        ######This data needs to be sent#######

        url = f"https://a.klaviyo.com/api/v2/list/{list_id}/members"

        querystring = {"api_key": api_key}

        payload = {"profiles": [{"email": email}]}
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

        if '"id"' in response.text:
            return JsonResponse({"success": True}, status=200)
        else:
            return JsonResponse({"success": False}, status=400)
