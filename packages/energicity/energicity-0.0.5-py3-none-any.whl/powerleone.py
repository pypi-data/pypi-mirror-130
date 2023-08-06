import requests as req

def sending_sms(phone_number, message_body, name="Default", automatic_send="Yes"):
    message_body = message_body
    message_body = message_body.replace(" ", "+")
    sms_text = f'''http://35.156.141.49:13013/cgi-bin/sendsms?username=kannel&password=kannel&to=232{phone_number[-8:]}&dlr-mask=0&text={message_body}'''

    try:
        if automatic_send in ["Yes", "y", "yes"]:
            get_res = req.get(url=sms_text)
            print(sms_text)
            #print(f"the SMS is send to {name} with {phone_number} number")
        else:
            print(f"{name} SMS\nSMS: {sms_text}")
    except NameError as e:
        print(f"{e}, please add \"import requests as req\" to your code")
    except HTTPError as e:
        print(f"{e}\nThere is an error with the SMS Gateway")