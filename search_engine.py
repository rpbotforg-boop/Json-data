import urllib.parse

def format_detailed_result(json_res):
    if not json_res or json_res.get("status") != "found":
        return "⚠️ **Koi data nahi mila!**"
    
    person = json_res["data"][0]
    name = person.get('name', 'N/A').upper()
    fname = person.get('fname', 'N/A').upper()
    mobile = person.get('mobile', 'N/A')
    id_val = person.get('id', 'N/A')
    
    # Address logic
    raw_addr = person.get('address', 'N/A')
    addr = raw_addr.replace('!', ', ')
    
    maps_query = urllib.parse.quote(addr)
    maps_link = f"https://www.google.com/maps/search/?api=1&query={maps_query}"
    
    report = (
        "📂 **SEARCH RESULT FOUND**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Name:** `{name}`\n"
        f"👨‍💼 **Father:** `{fname}`\n"
        f"📱 **Mobile:** `{mobile}`\n"
        f"🆔 **ID/Aadhar:** `{id_val}`\n"
        f"🏠 **Address:** `{addr}`\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"📍 [Google Maps Location]({maps_link})"
    )
    return report

