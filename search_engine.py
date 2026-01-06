import urllib.parse

def format_detailed_result(json_res):
    if not json_res or json_res.get("status") != "found":
        return "❌ **Koi record nahi mila.**"
    
    results = json_res.get("data", [])
    count = json_res.get("count", 0)
    
    report = f"🔍 **Search Results Found: {count}**\n"
    report += "━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for i, person in enumerate(results, 1):
        # Extracting fields
        name = person.get('name', 'N/A').upper()
        fname = person.get('fname', 'N/A').upper()
        mobile = person.get('mobile', 'N/A')
        alt = person.get('alt', 'N/A')
        email = person.get('email', 'N/A')
        aadhar = person.get('id', 'N/A') 
        circle = person.get('circle', 'N/A')
        
        # Address Cleaning (! to space)
        raw_address = person.get('address', 'N/A')
        clean_address = raw_address.replace('!', ' ').strip()
        
        # Google Maps link generation
        maps_query = urllib.parse.quote(clean_address)
        maps_link = f"https://www.google.com/maps/search/?api=1&query={maps_query}"
        
        report += (
            f"👤 **RECORD {i}**\n"
            f"📝 **Name:** `{name}`\n"
            f"👨‍💼 **Father:** `{fname}`\n"
            f"📱 **Mobile:** `{mobile}`\n"
            f"📞 **Alt:** `{alt}`\n"
            f"📧 **Gmail:** `{email if email else 'N/A'}`\n"
            f"🆔 **Aadhar/ID:** `{aadhar}`\n"
            f"📡 **Operator:** `{circle}`\n"
            f"🏠 **Address:** `{clean_address}`\n"
            f"📍 **[View on Google Maps]({maps_link})**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
        )
    return report
  
