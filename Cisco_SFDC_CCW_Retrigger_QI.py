import csv, json, collections , random, time, requests
from getAccessToken import get_nonprod_oauth

csvfile = "endpoint.csv"
csv_file_path = csvfile
ccw_qi_url = "https://apix.cisco.com/api/ccwquote/core/acv/dataMigration"

"""
Request Body :
{
  "applicationArea" : {
    "transactionInput" : "1058139976",
    "internalTransactionId" : 945735160557445,
    "consumerName" : "QUOTING"
  },
  "dataArea" : {
    "userId" : "kclaremo",
    "requestType" : "QI",
    "quoteObjectIds" : [ 4738976139 ],
    "opptyId" : "0067d00000JvlUjAAJ",
    "jobId" : "JOBkclaremo1657788399496"
  }
}
 
"""
#Define the parent dict
#CSV to have the following columns in this order
#oppty_id,ccw_quote_id,email
with open(csv_file_path, encoding='utf-8') as csv_file_handler:
    csv_reader = csv.DictReader(csv_file_handler)
    for rows in csv_reader:
        json_req_payload_dict = {}
        part1 = collections.OrderedDict()
        part2 = collections.OrderedDict()
        part1["transactionInput"] = 1058139976
        part1["internalTransactionId"] = random.randrange(950000000000000, 960000000000000, 15)
        part1["consumerName"] = "QUOTING"
        json_req_payload_dict["applicationArea"] = part1
        part2['requestType'] = "QI"
        for key, value in rows.items():
            if key == 'oppty_id':
                part2['opptyId'] = value
            elif key == 'email':
                part2['userId'] = value
                #epoc time.
                part2['jobId'] = "JOB"+ value + str(int(time.time()))
            elif key == 'ccw_quote_id':
                part2['quoteObjectIds'] = value.split(', ')
        json_req_payload_dict["dataArea"] = part2
        #print(json_req_payload_dict)
        csv2json = json.dumps(json_req_payload_dict, indent=2)
        print(csv2json)
        token_info = get_nonprod_oauth()
        #print(token_info)
        headers = {'Content-type': 'application/json',"Authorization": token_info}
        #print(headers)
        try:
            apiResponse = requests.request("POST", url=ccw_qi_url, data=csv2json, headers=headers)
            if apiResponse.status_code == 200:
                print(
                    'Connection established to CCW QI URL and data has been posted..')
            else:
                print('Unable to establish connection to CCW URL...Please try after some time')
                print(apiResponse.status_code)
            apiRespData = apiResponse.json()
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
        time.sleep(30)
        print("Request complete")