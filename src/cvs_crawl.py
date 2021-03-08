import requests
from datetime import datetime
from slack_sdk.webhook import WebhookClient
from time import sleep
import json

UPDATE_FREQUENCY_SECS = 120
HEALTHCHECK_PERIOD_HRS = 3
SLACK_URL = "https://hooks.slack.com/services/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"
webhook = WebhookClient(SLACK_URL)

def make_request():
    url = "https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.TX.json?vaccineinfo"

    payload = {}
    headers = {
        'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
        'Accept': '*/*',
        'referer': 'https://www.cvs.com/immunizations/covid-19-vaccine',
        'Cookie': 'QuantumMetricSessionLink=https://cvs.quantummetric.com/#/users/search?autoreplay=true&qmsessioncookie=a486ae7e7af5f1fdbabe948733bd938d&ts=1614760879-1614847279; cookietest=1; pe=p1; acctdel_v1=on; adh_new_ps=on; adh_ps_pickup=on; adh_ps_refill=on; buynow=off; sab_displayads=on; db-show-allrx=on; disable-app-dynamics=on; disable-sac=on; dpp_cdc=off; dpp_drug_dir=off; dpp_sft=off; getcust_elastic=on; echome_lean6=off-p0; enable_imz=on; enable_imz_cvd=on; enable_imz_reschedule_instore=off; enable_imz_reschedule_clinic=off; flipp2=on; gbi_cvs_coupons=true; ice-phr-offer=off; v3redirecton=false; mc_cloud_service=on; mc_hl7=on; mc_ui_ssr=off-p2; mc_videovisit=on; memberlite=on; pivotal_forgot_password=off-p0; pivotal_sso=off-p0; pbmplaceorder=off; pbmrxhistory=on; ps=on; rxdanshownba=off; rxdfixie=on; rxd_bnr=on; rxd_dot_bnr=on; rxdpromo=on; rxduan=on; rxlite=on; rxlitelob=off; rxm=on; rxm_phone_dob=off-p1; rxm_demo_hide_LN=off; rxm_phdob_hide_LN=on; rxm_rx_challenge=on; s2c_akamaidigitizecoupon=on; s2c_digitizecoupon=on; s2c_herotimer=off-p0; s2c_papercoupon=off-p0; s2c_persistEcCookie=on; s2c_smsenrollment=on; s2cHero_lean6=on; sft_mfr_new=on; sftg=on; show_exception_status=on; v2-dash-redirection=on; akavpau_vp_www_cvs_com_minuteclinic_covid19=1613711153~id=8c915cf93a8b1314c57560f7940aa16c; aat1=off-p1; DG_ZID=37EF9ACF-846B-3414-9730-C9E5E33825F2; DG_ZUID=22846785-4135-3BD8-80D4-2CEF03BF28E9; DG_HID=54B2FDF1-F7B6-35E8-A253-25389F858DAB; DG_SID=70.113.93.126:RlJG8qMrtdiyzGQP7oDQmZBg4vSfB0teCdOtpp+7/HU; mt.v=2.2116454697.1613710735480; _gcl_au=1.1.702815414.1613710736; _4c_mc_=9da2a04c-7cb4-4063-bd4c-a206a0520712; AMCVS_06660D1556E030D17F000101%40AdobeOrg=1; s_cc=true; ASP.NET_SessionId=14gunsbdgiutbk4x2xsvdhib; echomeln6=off-p0; mc_home_new=off2-p0; s2c_beautyclub=off-p0; s2c_dmenrollment=off-p0; s2c_newcard=off-p0; akavpau_vp_www_cvs_com_minuteclinic=1614804487~id=de95220ddaccf6ab0be2568f992f9e35; _group1=quantum; QuantumMetricUserID=29f1dc6ec3fabad1cb59a77081f7ee16; gbi_visitorId=ckltwnm7j00013h973bttzskh; s_cmp=coronavirus-lp-vaccine-sd-statetool; CVPF=3dX5ucP1oVA3zg11ZhGEkoXQgs9alqxZIWllno4cqM0gvHTGD6aQDRw; mt.cem=210210-MC-B2C-COVID - 210210-MC-Testing-VaxAlert,control | 201211-Minute-Clinic-COVID - 201211_dWeb_RadioButton,Experiment | 210111-MCcom-HP-Header - 210111-MCcom-HP-Header,2ctaExperiment | 210216-MCcom-Header-Banner - B-JUST-the-homepage-header; DG_IID=DB1F8150-B6DF-326B-B8A2-BC2DA64D681C; DG_UID=95D899DE-8C64-37C4-823F-79B6A9ECBCC8; dashboard_v1=off; refill_chkbox_remove=off-p0; akavpau_vp_www_cvs_com_vaccine_covid19=1615133300~id=f77d2e1e259f093dfb0d87f336bfff19; ak_bmsc=166A59B7E5953940EFF3064E8CA0D8AB17C7323E560E0000C37E456048CE2F15~plsUkETWGAnyxQ9f81eRFUYzJ5NY6BFAbBn9zN7yJbTzck9ZWiMnF97X/y5/mASYKPffNNDrmXa7HB08hes5SxA5zGODP45T0lKrpGL/Y/AQ1BL3VVsRbiymHya8dW1q9yP9I3bp7l4DytH4dnThVRscUhV8wF2W0lwrwXZRyuS6Calfjb77dpiSYfb55nzJbhjRb64zEOou4cSd8Ks6+R5uUZ9lUOzLmeSnNcqaCfCcg=; akavpau_vp_www_cvs_com_vaccine=1615167771~id=4370eb4bd8081e30fa1ad319391e0147; bm_sz=E05AD8587CE9D974F804D727A9B65659~YAAQPjLHF5OAKQJ4AQAAUyx3DwsPhL91P3PfvtNEQtr/yMqFnr0a4u09IBu3r7i4lnp3DtX8cH4ahG6UK7cKOM4yKlH3F1CHzQd9Ej0UTzhj4H3lrocqCid7HIA2jyP6EcA8a4HmciM3KMatBkEaBwrkqgDUpcnZOLg+C2+xngPXCxiaLiKvHMCMJuSD; mt.sc=%7B%22i%22%3A1615167172912%2C%22d%22%3A%5B%5D%7D; _abck=3448F0E489A9A32F6FE5129CE22D16BA~0~YAAQPjLHF7GAKQJ4AQAAzzJ3DwXrmKuIeTZUMOU1vtIbwtnwdGf6JAwkFdFYBuJvjpEi3WPORiG7rxCIjul5NacE12F0UFQVHWQ9yiGeHfL65oRCkmKuCjzLzpVH5KQtThmqmxhs8t9rO3p1R8wA6LRFcP7umw4GkaSfHqQB7ZNBrFj8XkXDPwLKY663K0Tksc/EmBAD6kKcyQxtL88Y2VsU72Gw/xW0IRBEhSnRPgVsLsGCLeLNHq6GlfheM5ZLGND2dVzF/fh96zxmgkqy6mtxTznTdyk2NxJHnkKOkYeCXLWMPYCmx7ITYzzAEr+NYGZwhonWb5BHO5gpuCCIIwQCpFT0YIay9G1OUd7JH/UwEsYMBxv87LqsA5XC+t8jjqs8jYFLinYgHhT2Htw6v+P4eGsd~-1~||-1||~-1; AMCV_06660D1556E030D17F000101%40AdobeOrg=-330454231%7CMCIDTS%7C18694%7CMCMID%7C90195445996811973713049425882275694097%7CMCAAMLH-1615771973%7C9%7CMCAAMB-1615771973%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1615174373s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.1.2; mt.mbsh=%7B%22fs%22%3A1615167174545%2C%22sf%22%3A1%2C%22lf%22%3A1615167174547%7D; QuantumMetricSessionID=1aae34395a01e956a3f5676b15f51d06; gbi_sessionId=cklzwu8iz00003h96kqm944ix; JSESSIONID=AhNWG5bWvv-BwvWSmIzMdr_2sinvfaliIvxg3gwT.commerce_1212; current_page_name=cvs|dweb|promo|promoLandingTemplate.jsp|PROMO: Page Not Found; previous_page_name=; previous_page_url=https://www.cvs.com/promo/promoLandingTemplate.jsp?promoLandingId=pagenotfound; favorite_store=10888/30.267400/-97.743400/AUSTIN/TX; mp_cvs_mixpanel=%7B%22distinct_id%22%3A%20%221780f79ac6c7ec-087a6b1e933fac-33697709-13c680-1780f79ac6dd13%22%2C%22bc_persist_updated%22%3A%201615167335534%7D; akavpau_www_cvs_com_general=1615168125~id=bc42f74d5bbe52e247e5a83bb99b2a85; qm-ssc=true; gpv_p10=www.cvs.com%2Fimmunizations%2Fcovid-19-vaccine; bm_sv=5D1B76E9E341A3938FCEC70980833875~OyQ59MP37cO+iRiZF9NhkGsTSjeZJxhy45OdNeHBL+hy4Za7Zb0xHf7uj/qkrK9lUkcrF7UMva34MXTEOGexSLYfZ5I7hr/g9//Ro74xSMaf4WwQLYWH02Rt1dGDXtmHrH+ZFKr7zKvVlwjSoR0wqw==; RT="z=1&dm=cvs.com&si=2d838344-4612-466f-8eaf-6da74f65abe4&ss=klzwtxm5&sl=9&tt=aap&bcn=%2F%2F173e2546.akstat.io%2F&ld=c2n3&nu=1ssnj1p3&cl=c700"; gpv_e5=cvs%7Cdweb%7Cimmunizations%7Ccovid-19-vaccine%7Cpromo%3A%20covid-19%20vaccines%20in%20texas%20modal; s_sq=%5B%5BB%5D%5D; utag_main=v_id:0177b8a7ba7f001ea3620f674f1303079003107100942$_sn:14$_ss:0$_st:1615169540798$vapi_domain:cvs.com$_pn:4%3Bexp-session$ses_id:1615167172888%3Bexp-session; qmexp=1615169544501'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if (response.status_code != 200):
        send_alert('Non-200 status code. Worth looking into this one')
        send_alert(response)
        quit()

    return response.text


def check_is_updated():
    try:
        response = make_request()
        obj = json.loads(response)
        txAvailability = obj['responsePayloadData']['data']['TX']
        austinSummary = list(filter(lambda item: item["city"] == "AUSTIN", txAvailability))[0]
        if austinSummary['status'] != 'Fully Booked':
            return True
        return False
    except:
        return True


def send_alert(text):
    webhook.send(text=text)

appts_available = False
while True:
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    print("Running invocation at " + current_time)
    appts_available = check_is_updated()
    if appts_available == True:
        print('Update detected.')
        send_alert('Appointments may be available!')
    else:
        print('No update detected.')
    sleep(UPDATE_FREQUENCY_SECS)

