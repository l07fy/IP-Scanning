from django.core.validators import validate_ipv46_address
from django.core.exceptions import ValidationError
from django.core.cache import cache
from ip_scanning.celery import app
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import requests

@app.task
def get_info(ip_address, group_name):

    channel_layer = get_channel_layer()

    # If the result of IP in cache just send it
    cache_key = f"ip_info_{ip_address}"
    cached_result = cache.get(cache_key)
    if cached_result:
        async_to_sync(channel_layer.group_send)(group_name, {"type": "sendinfo", "task_result": cached_result})
        return
    
    # Validating IPs v4 & v6
    try:
        validate_ipv46_address(ip_address)

    except ValidationError:
        result = {'error': f'({ip_address}) is not a valid IP address'}

    else:
        # Error handling for requests
        try:
            response = requests.get(f'https://ipinfo.io/{ip_address}/json')
            # IP Informations
            result = response.json()

        except requests.RequestException as e:
            result = {'error': f'Request failed: {str(e)}'}

        except Exception as e:
            result = {'error': f'An unexpected error occurred: {str(e)}'}

    # Cache the result for 3 hours
    cache.set(cache_key, result, timeout=3600*3)
    
    # Send result
    async_to_sync(channel_layer.group_send)(group_name, {"type": "sendinfo", "task_result": result})