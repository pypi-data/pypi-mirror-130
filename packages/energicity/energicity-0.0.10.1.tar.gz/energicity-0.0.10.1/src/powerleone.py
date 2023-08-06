import requests as req

def sending_sms(kannel_username:str, kannel_password:str, phone_number:str ="23273578902", body:str = "Demo", name:str ="Default"):
    """
    :param kannel_username: Kannel SMS gateway username
    :param phone_number: the phone number of the customer in formation 07XXXXXXX
    """
    params = {"username":kannel_username, "password": kannel_password, "to": f"232{phone_number[-8:]}", "dlr-mask":0, "test":body}


    try:
        sms = req.get(url='http://35.156.141.49:13013/cgi-bin/sendsms', params=params)
        return sms
    except NameError as e:
        print(f"{e}, please add \"import requests as req\" to your code")
        return 0
    except Exception as e:
        print(e)
        return 0