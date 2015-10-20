from bs4 import BeautifulSoup as bs
from requests import get, post
from PIL import Image

THSR_URL = "https://irs.thsrc.com.tw"
IMINT = "/IMINT/"
header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2535.0 Safari/537.36",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Language": "en-us",
		"Accept-Encoding": "deflate",
		"Host": "irs.thsrc.com.tw",
		"Referer": "https://irs.thsrc.com.tw/IMINT/"}

TICKET_FORM = {"BookingS1Form:hf:0": "",
        "selectStartStation": 0,
        "selectDestinationStation": 1,
        "trainCon:trainRadioGroup": 0,
        "bookingMethod": "radio22",
        "toTimeInputField": "2015/10/20",
        "toTimeTable": "",
        "toTrainIDInputField": "0545",
        "backTimeInputField": "2015/10/20",
        "backTimeTable": "",
        "backTrainIDInputField": "",
        "ticketPanel:rows:0:ticketAmount": "1F",
        "ticketPanel:rows:1:ticketAmount": "0H",
        "ticketPanel:rows:2:ticketAmount": "0W",
        "ticketPanel:rows:3:ticketAmount": "0E",
        "homeCaptcha:securityCode": "",
        "SubmitButton": "開始查詢"}

INFORM_FORM = {"BookingS3FormSP:hf:0": "",
        "idInputRadio": "radio33",
        "idInputRadio:idNumber": "Your ID",
        "eaiPhoneCon:phoneInputRadio": "radio44",
        "eaiPhoneCon:phoneInputRadio:mobilePhone": "Your Phone",
        "email": "",
        "TicketPassengerInfoInputPanel:passengerDataView:0:passengerDataView2:passengerDataLastName": "Your lastname",
        "TicketPassengerInfoInputPanel:passengerDataView:0:passengerDataView2:passengerDataFirstName": "Your firstname",
        "TicketPassengerInfoInputPanel:passengerDataView:0:passengerDataView2:passengerDataInputRadio": "radio56",
        "TicketPassengerInfoInputPanel:passengerDataView:0:passengerDataView2:passengerDataInputRadio:passengerDataIdNumber": "F129084433",
        "agree": "on",
        "isGoBackM": ""
        }

response = get(THSR_URL + IMINT, verify=False)
cookies = response.cookies
cookies.update(response.history[0].cookies)
print(repr(cookies))
soup = bs(response.text , "html5lib")
link = soup.select("#BookingS1Form")[0]["action"]
img = soup.select("#BookingS1Form_homeCaptcha_passCode")[0]["src"]
print('link = ' + link)

response = get(THSR_URL + img ,headers=header ,cookies=cookies, stream=True, verify=False)
print(repr(response.text))
with open("captcha.png", "wb") as png:
    for chunk in response:
        png.write(chunk)
    png.close()
Image.open("captcha.png").show()

ans = input("read the captcha :")
TICKET_FORM["homeCaptcha:securityCode"] = ans
response = post(THSR_URL + link, data=TICKET_FORM,headers=header, cookies=cookies, verify=False)
soup = bs(response.text, "html5lib")
link = soup.select("#BookingS3FormSP")[0]["action"]
print(link)

response = post(THSR_URL + link, data=INFORM_FORM, headers=header, cookies=cookies, verify=False)
soup = bs(response.text, "html5lib")
