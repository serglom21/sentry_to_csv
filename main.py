import requests
import os
import csv
from dotenv import load_dotenv

def main():
    load_dotenv()
    data = []
    data_file = open("export.csv", "w")
    csv_writer = csv.writer(data_file)
    count = 0
    headers = {
        "Content-Type": "application/json",
        "Authorization" : "Bearer " + os.environ["AUTH_TOKEN"]
    }
    response = requests.get(os.environ["API_URL"], headers = headers)
    if response is not None and response.status_code == 200:
        response_data = response.json()
        data = data + response_data["data"]
        #print(response_data["data"])
        next = response.links.get('next', {}).get('url')
        while next and len(data) < 1000:
            print(len(data))
            url = response.links.get('next', {}).get('url')
            response = requests.get(url, headers = headers)
            next = response.links.get('next', {}).get('results') == 'true'
            response_data = response.json()
            #print(response_data["data"])
            data = data + response_data["data"]
    
    if len(data) > 0:
        for entry in data:
            if count == 0:
                headers = ["project", "title", "issue.id","issue", "last_seen", "count"]
                '''
                header = entry.keys()
                csv_writer.writerow(header)
                count += 1
                '''
                csv_writer.writerow(headers)
                count += 1
            
            row = [
                entry["project"],entry["title"],entry["issue.id"],entry["issue"],entry["last_seen()"],entry["count()"]
            ]
            '''
            assigned = ""
            if entry["assignedTo"] is not None:
                assigned = entry["assignedTo"]["name"]
            row = [
                entry["project"]["name"], entry["title"], entry["id"], entry["lastSeen"], entry["shortId"], assigned, entry["count"]
            ]'''

            csv_writer.writerow(row)

    data_file.close()


if __name__ == "__main__":
    main()