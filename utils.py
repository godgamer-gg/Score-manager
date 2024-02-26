import json    

def pprint(data):
        json_str = json.dumps(data, indent=4)
        print(json_str)