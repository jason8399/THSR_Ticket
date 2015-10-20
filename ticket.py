from bs4 import BeautifulSoup as bs
from requests import get, post
from PIL import Image

THSR_URL = "https://irs.thsrc.com.tw"
IMINT = "/IMINT/"
header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2535.0 Safari/537.36"}
TICKET_FORM = {"BookingS1Form:hf:0": "",
        "selectStartStation": "0",
        "selectDestinationStation": "1",
        "trainCon:trainRadioGroup": "0",
        "bookingMethod": "radio22",
        "toTimeInputField": "2015/10/20",
        "toTimeTable": "",
        "toTrainIDInputField": "0605",
        "backTimeInputField": "2015/10/20",
        "backTimeTable": "",
        "backTrainIDInputField": "",
        "ticketPanel:rows:0:ticketAmount": "1F",
        "ticketPanel:rows:1:ticketAmount": "0H",
        "ticketPanel:rows:2:ticketAmount": "0W",
        "ticketPanel:rows:3:ticketAmount": "0E",
        "homeCaptcha:securityCode": "",
        "SubmitButton": "開始查詢"}

response = get(THSR_URL + IMINT, verify=False)
cookies = response.cookies
soup = bs(response.text , "html5lib")
link = soup.select("#BookingS1Form")[0]["action"]
img = soup.select("#BookingS1Form_homeCaptcha_passCode")[0]["src"]
print('link = ' + link)

response = get(THSR_URL + img ,cookies=cookies, stream=True, verify=False)
print(repr(response.text))
with open("captcha.png", "wb") as png:
    for chunk in response:
        png.write(chunk)
    png.close()
Image.open("captcha.png").show()

ans = input("read the captcha :")
TICKET_FORM["homeCaptcha:securityCode"] = ans
response = post(THSR_URL + link, data=TICKET_FORM, cookies=cookies, verify=False)
soup = bs(response.text, "html5lib")
import pdb; pdb.set_trace()
print(soup.select("#BookingS3FormSP")[0]["action"])

