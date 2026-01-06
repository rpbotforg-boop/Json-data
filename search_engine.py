import urllib.parse

def format_detailed_result(json_res):
    if not json_res or json_res.get("status") != "found":
        return "❌ **Record nahi mila!**"
    
    results = json_res.get("data", [])
    report = f"🔍 **Results Found: {len(results)}**\n━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for i, person in enumerate(results, 1):
        name = person.get('name', 'N/A').upper()
        fname = person.get('fname', 'N/A').upper()
        mobile = person.get('mobile', 'N/A')
        aadhar = person.get('id', 'N/A')
        
        # Address Cleaning
        raw_addr = person.get('address', 'N/A')
        clean_addr = raw_addr.replace('!', ' ').strip()
        
        # Maps link
        maps_query = urllib.parse.quote(clean_addr)
        maps_link = f"https://www.google.com/maps/search/?api=1&query={maps_query}"
        
        report += (
            f"👤 **RECORD {i}**\n"
            f"📝 **Name:** `{name}`\n"
            f"👨‍💼 **Father:** `{fname}`\n"
            f"📱 **Mobile:** `{mobile}`\n"
            f"🆔 **Aadhar/ID:** `{aadhar}`\n"
            f"🏠 **Address:** `{clean_addr}`\n"
            f"📍 **[View on Maps]({maps_link})**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
        )
    return report

