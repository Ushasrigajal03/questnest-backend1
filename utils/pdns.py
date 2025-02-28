import requests
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class PowerDNSClient:
    def __init__(self):
        self.api_url = settings.PDNS_API_URL  # e.g., "http://pdns-droplet-ip:8081/api/v1"
        self.api_key = settings.PDNS_API_KEY
        self.zone = settings.PDNS_ZONE  # e.g., "questnest.in."
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def create_subdomain(self, subdomain, target_ip=None, target_url=None):
        """
        Create a new subdomain in PowerDNS
        
        Args:
            subdomain: The subdomain name (without the main domain)
            target_ip: IP address to point the A record to (optional)
            target_url: URL to create a CNAME record for (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Construct the full domain name
            full_domain = f"{subdomain}.{self.zone.rstrip('.')}"
            
            # Get the zone details
            zone_url = f"{self.api_url}/servers/localhost/zones/{self.zone}"
            zone_response = requests.get(zone_url, headers=self.headers)
            
            if zone_response.status_code != 200:
                logger.error(f"Failed to get zone details: {zone_response.text}")
                return False
            
            zone_data = zone_response.json()
            
            # Create record data
            records = []
            
            if target_ip:
                # Create an A record
                records.append({
                    "name": full_domain + ".",
                    "type": "A",
                    "ttl": 3600,
                    "records": [{"content": target_ip, "disabled": False}]
                })
            elif target_url:
                # Create a CNAME record
                records.append({
                    "name": full_domain + ".",
                    "type": "CNAME",
                    "ttl": 3600,
                    "records": [{"content": target_url + ".", "disabled": False}]
                })
            else:
                # Default to Traefik IP if neither is provided
                target_ip = settings.TRAEFIK_IP
                records.append({
                    "name": full_domain + ".",
                    "type": "A",
                    "ttl": 3600,
                    "records": [{"content": target_ip, "disabled": False}]
                })
            
            # Add the new records to the zone
            for record in records:
                # Check if the record already exists
                existing_records = [r for r in zone_data.get("rrsets", []) 
                                   if r["name"] == record["name"] and r["type"] == record["type"]]
                
                if existing_records:
                    # Update existing record
                    update_url = f"{zone_url}/rrsets"
                    update_data = {
                        "rrsets": [
                            {
                                "name": record["name"],
                                "type": record["type"],
                                "ttl": record["ttl"],
                                "changetype": "REPLACE",
                                "records": record["records"]
                            }
                        ]
                    }
                    update_response = requests.patch(update_url, json=update_data, headers=self.headers)
                    if update_response.status_code != 204:
                        logger.error(f"Failed to update record: {update_response.text}")
                        return False
                else:
                    # Create new record
                    update_url = f"{zone_url}/rrsets"
                    update_data = {
                        "rrsets": [
                            {
                                "name": record["name"],
                                "type": record["type"],
                                "ttl": record["ttl"],
                                "changetype": "REPLACE",
                                "records": record["records"]
                            }
                        ]
                    }
                    update_response = requests.patch(update_url, json=update_data, headers=self.headers)
                    if update_response.status_code != 204:
                        logger.error(f"Failed to create record: {update_response.text}")
                        return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating subdomain in PowerDNS: {str(e)}")
            return False