import re
import requests
import time
import ddddocr
import base64
import simplejson
def sms1(phone):
    sms_url='https://login.ceconline.com/thirdPartLogin.do'
    sms_home='https://login.ceconline.com/pcMobileNumberRegister.do'
    hearder={
        'accept': 'text/plain, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': '',
        'origin': 'https://login.ceconline.com',
        'referer': 'https://login.ceconline.com/pcMobileNumberRegister.do',
        'ec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
        'x-requested-with': 'XMLHttpRequest'
    }
    home_data = requests.get(url=sms_home,headers=hearder).text
    home_data_fuid=re.findall('<input type="hidden" name="fuid" id="fuid"  value="(.*?)"/> ',home_data)[0]
    sms_post='https://login.ceconline.com/Captchastr.do?fuid='+str(home_data_fuid)
    sms_data = requests.get(url=sms_post, headers=hearder).text
    sms_data=simplejson.loads(sms_data)
    sms_data=sms_data['img']
    print(sms_data)
    imgdata = base64.b64decode(sms_data)
    # 将图片保存为文件
    with open("temp.png", 'wb') as f:
        f.write(imgdata)
    ocr = ddddocr.DdddOcr()
    with open('temp.png', 'rb') as f:
        img_bytes = f.read()
    result = ocr.classification(img_bytes)
    data_post = {
        'mobileNumber': phone,
        'method': 'getDynamicCode',
        'fuid': home_data_fuid,
        'verifyType': 'MOBILE_NUM_REG',
        'kaptcha': result,
        'captcharType': 'verifyCode',
        'time': int(time.time() * 1000)
    }
    print(result)
    data=requests.post(url=sms_url,data=data_post,headers=hearder).text
    print(data)

phome='手机号码'
sms1(phome)
