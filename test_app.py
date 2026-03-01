import sys
sys.path.insert(0, 'c:/TravelAI-Website')

from app import app
print("✓ Flask app loaded successfully!")
print("✓ All routes are configured:")
for rule in app.url_map.iter_rules():
    print(f"  {rule.endpoint}: {rule.rule}")
