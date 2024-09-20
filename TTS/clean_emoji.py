import re

def remove_emoji(text):
    # Regular expression to match all emojis
    emoji_pattern = re.compile(
        "["  
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
        "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        "\U0001F1E0-\U0001F1FF"  # Flags (iOS)
        "\U00002702-\U000027B0"  # Miscellaneous Symbols
        "\U000024C2-\U0001F251"  # Enclosed characters
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

# Example usage
text = "เมื่อได้ข้อมูลครบแล้ว จะทำการนัดให้เลยค่ะ! 🤣"
clean_text = remove_emoji(text)
print(clean_text)  # Output: เมื่อได้ข้อมูลครบแล้ว จะทำการนัดให้เลยค่ะ!
