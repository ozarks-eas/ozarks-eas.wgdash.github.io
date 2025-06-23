import xml.etree.ElementTree as ET
import requests
import json
import os
import time

def fetch_and_parse_ipaws_cap(url):
    try:
        # Fetch the CAP XML data from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues

        # Parse the CAP XML content
        root = ET.fromstring(response.content)

        # Define the CAP namespace
        namespace = {'cap': 'urn:oasis:names:tc:emergency:cap:1.2'}

        # Initialize a list to store parsed alerts
        alerts = []

        # Iterate through each <alert> element in the feed
        for alert in root.findall('cap:alert', namespace):
            alert_info = {}
            alert_info['identifier'] = alert.find('cap:identifier', namespace).text if alert.find('cap:identifier', namespace) is not None else None
            alert_info['sender'] = alert.find('cap:sender', namespace).text if alert.find('cap:sender', namespace) is not None else None
            alert_info['sent'] = alert.find('cap:sent', namespace).text if alert.find('cap:sent', namespace) is not None else None
            alert_info['status'] = alert.find('cap:status', namespace).text if alert.find('cap:status', namespace) is not None else None
            alert_info['msgType'] = alert.find('cap:msgType', namespace).text if alert.find('cap:msgType', namespace) is not None else None
            alert_info['scope'] = alert.find('cap:scope', namespace).text if alert.find('cap:scope', namespace) is not None else None

            # Extract information from the <info> block
            info = alert.find('cap:info', namespace)
            if info is not None:
                alert_info['category'] = info.find('cap:category', namespace).text if info.find('cap:category', namespace) is not None else None
                alert_info['event'] = info.find('cap:event', namespace).text if info.find('cap:event', namespace) is not None else None
                alert_info['urgency'] = info.find('cap:urgency', namespace).text if info.find('cap:urgency', namespace) is not None else None
                alert_info['severity'] = info.find('cap:severity', namespace).text if info.find('cap:severity', namespace) is not None else None
                alert_info['certainty'] = info.find('cap:certainty', namespace).text if info.find('cap:certainty', namespace) is not None else None
                alert_info['headline'] = info.find('cap:headline', namespace).text if info.find('cap:headline', namespace) is not None else None
                alert_info['description'] = info.find('cap:description', namespace).text if info.find('cap:description', namespace) is not None else None
                alert_info['instruction'] = info.find('cap:instruction', namespace).text if info.find('cap:instruction', namespace) is not None else None

                # Extract area information
                area = info.find('cap:area', namespace)
                if area is not None:
                    alert_info['areaDesc'] = area.find('cap:areaDesc', namespace).text if area.find('cap:areaDesc', namespace) is not None else None
                    polygon = area.find('cap:polygon', namespace)
                    if polygon is not None:
                        alert_info['polygon'] = polygon.text

            # Add the parsed alert to the list
            alerts.append(alert_info)

        return alerts

    except requests.exceptions.RequestException as e:
        print(f"Error fetching CAP data: {e}")
        return None
    except ET.ParseError as e:
        print(f"Error parsing CAP XML: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def save_alerts_to_file(alerts, file_path):
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write the alerts to the file as JSON
        with open(file_path, "w") as f:
            json.dump(alerts, f, indent=4)
        print(f"Alerts saved to {file_path}")
    except Exception as e:
        print(f"Error saving alerts to file: {e}")

if __name__ == "__main__":
    cap_url = "https://apps.fema.gov/IPAWSOPEN_EAS_SERVICE/rest/feed"  # URL for the CAP feed
    output_file = "/app/api/IPAWSCAP.json"  # Path to save the parsed alerts

    while True:
        print("Fetching and parsing CAP feed...")
        alerts = fetch_and_parse_ipaws_cap(cap_url)
        if alerts:
            save_alerts_to_file(alerts, output_file)
        else:
            print("No alerts fetched or an error occurred.")
        
        # Wait for 60 seconds before fetching again
        time.sleep(60)
        
        
