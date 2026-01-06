import urllib.parse

def format_detailed_result(json_res):
    if not json_res or json_res.get("status") != "found":
        return "⚠️ **Koi record nahi mila!**"
    
    all_results = []
    
    # JSON mein 'data' ek list hai, isliye hum har record ko loop karenge
    for index, person in enumerate(json_res.get("data", []), start=1):
        name = person.get('name', 'N/A').upper()
        fname = person.get('fname', 'N/A').upper()
        mobile = person.get('mobile', 'N/A')
        alt_mobile = person.get('alt', 'N/A')
        circle = person.get('circle', 'N/A')
        id_val = person.get('id', 'N/A')
        
        # Address cleaning logic
        raw_addr = person.get('address', 'N/A')
        # Aapke JSON mein '!' hai, use comma se badal rahe hain
        addr = raw_addr.replace('!', ', ').strip(', ')
        
        # Google Maps Link
        maps_query = urllib.parse.quote(addr)
        maps_link = f"https://www.google.com/maps/search/{maps_query}"
        
        result_text = (
            f"📂 **RECORD #{index}**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 **Name:** `{name}`\n"
            f"👨‍💼 **Father:** `{fname}`\n"
            f"📱 **Mobile:** `{mobile}`\n"
            f"📞 **Alt:** `{alt_mobile}`\n"
            f"🌐 **Circle:** `{circle}`\n"
            f"🆔 **ID:** `{id_val}`\n"
            f"🏠 **Address:** `{addr}`\n"
            f"📍 [View on Google Maps]({maps_link})\n"
        )
        all_results.append(result_text)
    
    # Saare records ko ek saath join karke bhejenge
    return "\n".join(all_results)

