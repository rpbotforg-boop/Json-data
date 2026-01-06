import urllib.parse

def format_detailed_result(json_res):
    if not json_res or json_res.get("status") != "found":
        return "⚠️ **Koi data nahi mila!**\nCheck karein ki query sahi hai ya nahi."
    
    person = json_res["data"][0]
    name = person.get('name', 'N/A').upper()
    mobile = person.get('mobile', 'N/A')
    addr = person.get('address', 'N/A').replace('!', ', ')
    
    maps_link = f"https://www.google.com/maps/search/{urllib.parse.quote(addr)}"
    
    report = (
        "📂 **SEARCH RESULT FOUND**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Name:** `{name}`\n"
        f"📱 **Mobile:** `{mobile}`\n"
        f"🏠 **Address:** `{addr}`\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"📍 [Click Here for Location]({maps_link})"
    )
    return report
