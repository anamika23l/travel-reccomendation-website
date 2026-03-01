import urllib.request
import urllib.parse
import json

# Test all interest categories
categories = ["mountain", "beach", "culture", "adventure", "religious"]

url = "http://127.0.0.1:5000/api/suggest-trip"

for interest in categories:
    data = {"budget": 50000, "duration": 5, "interest": interest}
    
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), 
                                     headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            count = len(result.get('recommendations', []))
            print(f"✓ {interest}: {count} destinations found")
            if result.get('recommendations'):
                names = [r['name'] for r in result['recommendations'][:3]]
                print(f"  Top: {', '.join(names)}")
    except Exception as e:
        print(f"✗ {interest}: Error - {e}")
