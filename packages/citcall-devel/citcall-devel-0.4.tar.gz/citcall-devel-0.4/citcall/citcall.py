from .exception import MissingKeywordArgument
import re
import requests
import base64
import json

"""

Citcall REST API for Python. 
API support for Synchchronous Miscall, Asynchronous miscall, and Sms.

"""
class Citcall:
    URL_CITCALL = "https://gateway.citcall.com"
    VERSION = "/v3"
    METHOD_SMS = "/sms"
    METHOD_SYNC_MISCALL = "/call"
    METHOD_ASYNC_MISCALL = "/asynccall"
    METHOD_VERIFY_MOTP = "/verify"

    
    def __init__(self, **kwargs):
        """
        The constructor for Citcall class.

        Keyword Arguments *require or **optional :
            *userid  = (str)
            *apikey  = (str) 
        
        """
        if not "userid" in kwargs.keys() or not "apikey" in kwargs.keys():
            raise MissingKeywordArgument("missing keyword argument")

        if not isinstance(kwargs['userid'], str):
            raise TypeError("userid must string type")

        if not isinstance(kwargs['apikey'], str):
            raise TypeError("apikey must string type")

        self.userid = kwargs['userid']
        self.apikey = kwargs['apikey']
        
        
        
    

    def sync_miscall(self, **kwargs):
        """
        Synchronous miscall

        Keyword Arguments *require OR **optional :
            *msisdn         = (str)
            *gateway        = (int)
            **valid_time    = (int)
            **limit_try     = (int)            
        
        Return : 
            (dict)
        """
        if "msisdn" in kwargs.keys() and "gateway" in kwargs.keys():
            msisdn = kwargs['msisdn']
            gateway = kwargs['gateway']

            if gateway > 5 or gateway < 0:
                result = {
                    "rc": "06",
                    "info": "invalid gateway"
                }
                return result

            else:
                continue_status = False
                msisdn = self.__clean_msisdn(msisdn)
                msisdn = re.sub('/[^0-9]/', '', msisdn)
                if msisdn[0:2] == "62":
                    if len(msisdn) > 10 and len(msisdn) < 15:
                        prefix = msisdn[0:5]
                        if msisdn > 13:
                            if self.is_three(prefix):
                                continue_status = True
                        else:
                            continue_status = True
                else:
                    if len(msisdn) > 9 and len(msisdn) < 18:
                        continue_status = True

                if continue_status:
                    param_hit = {
                        "msisdn": msisdn,
                        "gateway": gateway,
                    }

                    valid_verify = True
                    if "valid_time" in kwargs.keys():
                        valid_time = kwargs["valid_time"]
                        if isinstance(valid_time, int) and valid_time > 0:
                            if "limit_try" in kwargs.keys():
                                limit_try = kwargs["limit_try"]
                                if not isinstance(limit_try, int) and valid_time <= 0:
                                    valid_verify = False
                                else:
                                    param_hit['valid_time'] = valid_time
                                    param_hit['limit_try'] = limit_try
                        else:
                            valid_verify = False

                    if valid_verify:
                        method = "sync_miscall"
                        result = self.__send_request(param_hit, method)
                    else:
                        result = {
                            "rc": "06",
                            "info": "invalid verify data",
                        }
                        return result

                    return json.loads(result)
        else:
            result = {
                "rc": "88",
                "info": "missing parameter",
            }

    def async_miscall(self, **kwargs):
        """
        Asynchronous miscall

        Keyword Arguments *require OR **optional :
            *msisdn         = (str)
            *gateway        = (int)
            **valid_time    = (int)
            **limit_try     = (int)            
        
        Return : 
            (dict)
        """
        if "msisdn" in kwargs.keys() and "gateway" in kwargs.keys():
            msisdn = kwargs["msisdn"]
            gateway = kwargs["gateway"]

            if gateway > 5 or gateway < 0:
                result = {
                    "rc": "06",
                    "info": "invalid gateway",
                }
                return result
            else:
                continue_status = False
                msisdn = self.__clean_msisdn(msisdn)
                msisdn = re.sub('/[^0-9]/', '', msisdn)
                if msisdn[0:2] == "62":
                    if len(msisdn) > 10 and len(msisdn) < 15:
                        prefix = msisdn[0:5]
                        if len(msisdn) > 13:
                            if self.is_three(prefix):
                                continue_status = True
                        else:
                            continue_status = True
                else:
                    if len(msisdn) > 9 and len(msisdn) < 18:
                        continue_status = True

            if continue_status:
                param_hit = {
                    "msisdn": msisdn,
                    "gateway": gateway,
                }
                valid_verify = True
                if "valid_time" in kwargs.keys():
                    valid_time = kwargs["valid_time"]
                    if isinstance(valid_time, int) and valid_time > 0:
                        if "limit_try" in kwargs.keys():
                            limit_try = kwargs["limit_try"]
                            if not isinstance(valid_time, int) and valid_time <= 10:
                                continue_status = False
                            else:
                                param_hit["valid_time"] = valid_time
                                param_hit["limit_try"] = limit_try
                    else:
                        valid_verify = False

                if valid_verify:
                    method = "async_miscall"
                    result = self.__send_request(param_hit)
                    result = json.loads(result)
                    return result
                else:
                    result = {
                        "rc": "06",
                        "info": "invalid verify data",
                    }
                    return result

        else:
            result = {
                "rc": "06",
                "info": "missing parameter",
            }
            return result

    def __send_request(self, param, method):
        userid = self.userid
        apikey = self.apikey
        tmp_auth = userid + ":" + apikey
        auth = base64.b64encode(tmp_auth.encode())

        if method == "sync_miscall":
            action = Citcall.METHOD_SYNC_MISCALL
        elif method == "async_miscall":
            action = Citcall.METHOD_ASYNC_MISCALL
        elif method == "sms":
            action = Citcall.METHOD_SMS
        elif method == "verify_otp":
            action = Citcall.METHOD_VERIFY_MOTP
        else:
            pass

        request_url = Citcall.URL_CITCALL + Citcall.VERSION + action
        content = json.dumps(param)
        headers = {
            "Content-Type": "application/json",
            "Authorization": auth,
            "Content-Length": str(len(content)),
        }
        response = requests.post(request_url, data=content, headers=headers)
        response_txt = response.text
        return response_txt

    def sms(self, **kwargs):
        """
        SMS

        Keyword Arguments *require OR **optional :
            *msisdn             = (str)
            *senderid           = (str)
            *text               = (str)
                  
        Return : 
            (dict)
        """
        if "msisdn" in kwargs.keys() and "senderid" in kwargs.keys() and "text" in kwargs.keys():
            msisdn = kwargs["msisdn"]
            senderid = kwargs["senderid"]
            text = kwargs["text"]
            new_list = []
            tmp_list = msisdn.split(",")
            for val in tmp_list:
                msisdn = self.__clean_msisdn(val)
                msisdn = re.sub('/[^0-9]/', '', msisdn)
                if msisdn[0:2] == "62":
                    if len(msisdn) > 10 and len(msisdn) < 15:
                        prefix = msisdn[0:5]
                        if len(msisdn) > 13:
                            if self.is_three(prefix):
                                new_list.append(msisdn)
                    else:
                        result = {
                            "rc": "06",
                            "info": "invalid msisdn or msisdn has invalid format!",
                        }
                        return result
                else:
                    if len(msisdn) > 9 and len(msisdn) < 18:
                        new_list.append(msisdn)
                    else:
                        result = {
                            "rc": "06",
                            "info": "invalid msisdn or msisdn has invalid format!",
                        }
                        return result
            msisdn = ",".join(new_list)
            if senderid.lower().split() == "citcall":
                senderid = senderid.upper()
            param_hit = {
                "msisdn": msisdn,
                "senderid": senderid,
                "text": text,
            }
            method = "sms"
            result = self.__send_request(param_hit, method)
        else:
            result = {
                "rc": "88",
                "info": "missing parameter",
            }
            return result

        return json.loads(result)

    def verify_motp(self, **kwargs):
        """
        Verify Miscall OTP

        Keyword Arguments *require OR **optional :
            *msisdn        = (str)
            *trxid         = (str)
            *token         = (str)
                  
        Return : 
            (dict)
        """
        if "msisdn" in kwargs.items() and "trxid" in kwargs.items() and "token" in kwargs.items():
            if kwargs["token"].is_numeric():
                if len(kwargs["token"]) > 3:
                    msisdn = kwargs["msisdn"]
                    trxid = kwargs["trxid"]
                    token = kwargs["token"]
                    continue_status = False
                    msisdn = self.__clean_msisdn(msisdn)
                    msisdn = re.sub('/[^0-9]/', '', msisdn)
                    if msisdn[0:2] == "62":
                        if len(msisdn) > 10 and len(msisdn) < 15:
                            prefix = msisdn[0:5]
                            if len(msisdn) > 13:
                                if self.is_three(prefix):
                                    continue_status = True
                            else:
                                continue_status = True
                    else:
                        if len(msisdn) > 9 and len(msisdn) < 18:
                            continue_status = True

                    if continue_status:
                        param_hit = {
                            "msisdn": msisdn,
                            "trxid": trxid,
                            "token": token,
                        }

                        method = "verify_otp"
                        result = self.__send_request(param_hit, method)
                    else:
                        result = {
                            "rc": "06",
                            "info": "invalid mobile number",
                        }
                        return result
                else:
                    result = {
                        "rc": "06",
                        "info": "invalid token, token length minimum 4 digits",
                    }
                    return result
            else:
                result = {
                    "rc":"06",
                    "info":"invalid token, token length minimum 4 digits",
                }
                return result
        else:
            result = {
                "rc":"88",
                "info":"missing parameter",
            }
            return result

        return json.loads(result)


    def is_three(self, prefix):
        """
        Cek prefix is three

        Parameter :
            prefix -> (str)

        Return :
            (boolean)
        """
        if prefix == "62896":
            return True
        elif prefix == "62897":
            return True
        elif prefix == "62898":
            return True
        elif prefix == "62899":
            return True
        elif prefix == "62895":
            return True
        else:
            return False



    def __clean_msisdn(self, msisdn):
        if msisdn[0:1] != "+":
            msisdn = "+" + msisdn

        if msisdn[0:2] == "+0":
            msisdn = "+62" + msisdn[2:]

        if msisdn[0:1] == "0":
            msisdn = "+62" + msisdn[2:]

        return msisdn