import requests
from datetime import datetime
from slack_sdk.webhook import WebhookClient
import threading
from time import sleep
import json

UPDATE_FREQUENCY_SECS = 120
HEALTHCHECK_PERIOD_HRS = 3
SLACK_URL = "https://hooks.slack.com/services/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"
webhook = WebhookClient(SLACK_URL)


def check_is_updated():
    try:
        url = \
            'https://www.cvs.com/Services/ICEAGPV1/immunization/1.0.0/getIMZStores'

        payload = \
            '{"requestMetaData":{"appName":"CVS_WEB","lineOfBusiness":"RETAIL","channelName":"WEB","deviceType":"DESKTOP","deviceToken":"7777","apiKey":"a2ff75c6-2da7-4299-929d-d670d827ab4a","source":"ICE_WEB","securityType":"apiKey","responseFormat":"JSON","type":"cn-dep"},"requestPayloadData":{"selectedImmunization":["CVD"],"distanceInMiles":200,"imzData":[{"imzType":"CVD","ndc":["59267100002","59267100003","59676058015","80777027399"],"allocationType":"1"}],"searchCriteria":{"addressLine":"78702"}}}'
        headers = {
            'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
            'Accept': 'application/json',
            'X-Distil-Ajax': 'xebztatfusvxtdxdzzerd',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
            'Content-Type': 'application/json',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Cookie': 'pe=p1; bm_sz=6BA2845F36D44B9C13431034F867036D~YAAQODsvF2J0vu13AQAALniW/Qs6UNel6i7uJvyP+z8Ajgx7m4vr9S40OqDR1Khs31Pmif+kzeWiIUUvEjC6a0ariRcfJR5AdScRTdvbva6ju/KiAbDJDelfgbSTouOCwPt2doxZ/TZxDTo/XHpDjCik2fr0CRH2m9iEnTa0iT0LDl+4NA7KYdyWDJ8=; _abck=B6B66F5353FC31317D7BFEAF26352C70~-1~YAAQODsvF2N0vu13AQAALniW/QW0ZxXSVN0hq3/KM6Krqhl3CgQNPGrIx8J2RGFpXwbNr53YjOw6GM7/ZSRpWVLLpD8oFU0apk3ddqOU8eSbYmC6ZFyMTeugQQzjkRcHCd4H7cMZ1gZl2wZi8Z3R2YAaNcoe8z/FD2SPxLM8VejhNHQBF15TvFQKXssSlJVXdNX02PzCBvNp99aerFIREcXGcHCy0OD7nzfBchqQu+90XkIRraHILdjei+OL7v498UY8hobQWiV5zbJW/VVSXYEjuH+UZHyouDxtH0IPg+uSrq7NlkRdo7psWZovjak0SKC7F4xkxIjAwH9ryUP0dx4uHSGX+GCCEZCFbPTywCzDrijqTlGf/LkhlkKUIG8eHsJsyJP9zg==~-1~-1~-1; ADRUM_BT=R:0|i:1684|g:b7b19e20-6bc2-442e-86af-d3765c64ca0c124969|e:163|n:customer1_d6c575ca-3f03-4481-90a7-5ad65f4a5986',
        }
        response = requests.request('POST', url, headers=headers, data=payload)
        obj = json.loads(response.text)
        availabilityStatus = obj['responseMetaData']['statusDesc']
        matchString = "No stores with immunizations found"
        return availabilityStatus != matchString
    except:
        return True


def send_alert():
    url = "https://www.cvs.com/vaccine/intake/store/cvd-store-select/first-dose-select"
    text = 'Appointments may be available! Go to ' + url
    webhook.send(text=text)


def healthcheck():
    timer = threading.Timer(HEALTHCHECK_PERIOD_HRS * 60 * 60, healthcheck)
    timer.start()
    text = 'Healthcheck: Bot is still running.'
    webhook.send(text=text)
    return timer


timer = healthcheck()
appts_available = False
while True:
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    print("Running invocation at " + current_time)
    appts_available = check_is_updated()
    if appts_available == True:
        print('Update detected.')
        send_alert()
    else:
        print('No update detected.')
    sleep(UPDATE_FREQUENCY_SECS)

print('Function terminating.')
timer.stop()
