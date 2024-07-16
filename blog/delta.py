import json
from django.utils.html import escape

def convert_delta_to_html(delta):
    blogpost_json = json.loads(delta)
    html = blogpost_json.get('html', '') 
    
    return html
