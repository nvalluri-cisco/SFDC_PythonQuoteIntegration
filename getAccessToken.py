import requests
url = "https://id.cisco.com/oauth2/default/v1/token"#"https://cloudsso.cisco.com/as/token.oauth2"
client_id = "vxc8fp57sedzekwxqdfhtcfv"#"fa1e6aeb187c4ade9a9b218bf58ea1ed"
client_secret = "Bv3Hzf38xecbxZhjsfeW4UGE"#"9023c0dFda1f42cCAadE2DB4A25a0f71"
auth = (client_id, client_secret)

def get_nonprod_oauth():
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    data = {"grant_type": "client_credentials"}
    try:
        apiResponse = requests.request("POST", url, auth = auth, data = data, headers=headers)
        if apiResponse.status_code == 200:
            print(
                'Connection Established to test sso and data has been posted... Please review the response for access token ')
            print(
                '------------------------------------------------------------------------------------------------------')
        else:
            print('Unable to establish the connection...Please try after some time')
        apiRespData = apiResponse.json()
        #print(apiRespData)
        #print(apiRespData['token_type']+' '+apiRespData['access_token'])
        return apiRespData['token_type']+' '+apiRespData['access_token']
    except requests.exceptions.HTTPError as errh:
        print("HTTP Transport Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting to the URL:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error Occurred:", errt)
    except requests.exceptions.TooManyRedirects as errtoo:
        # Tell the user their URL was bad and try a different one
        print("Too many redirects Error:", errtoo)
    except requests.exceptions.RequestException as eothers:
        # catastrophic error.
        print("Other errors:", eothers)

def refresh_token(token):
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    data = {"grant_type": "refresh_token","refresh_token" : token,'redirect_uri': 'wwwin.cisco.com'}
    print(data)
    try:
        apiResponse = requests.request("POST", url, auth=auth, data=data, headers=headers)
        if apiResponse.status_code == 200:
            print(
                'Connection Established to test sso and data has been posted... Please review the response for access token ')
            print(
                '------------------------------------------------------------------------------------------------------')
        else:
            print('Unable to establish the connection...Please try after some time')
            print('Status code ' + str(apiResponse.status_code))

        apiRespData1 = apiResponse.json()
        return apiRespData['access_token']
    except requests.exceptions.HTTPError as errh:
        print("HTTP Transport Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting to the URL:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error Occurred:", errt)
    except requests.exceptions.TooManyRedirects as errtoo:
        # Tell the user their URL was bad and try a different one
        print("Too many redirects Error:", errtoo)
    except requests.exceptions.RequestException as eothers:
        # catastrophic error.
        print("Other errors:", eothers)

if __name__ == '__main__':
    token = get_nonprod_oauth()
    print(token)
