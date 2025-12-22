def is_inappropriate(text: str) -> bool:
    text = text.lower()

    # List of blocked keywords
    banned_words = [
        "nude", "kill", "violence", "terrorist", "suicide",
        "porn", "attack", "self-harm", "bomb", "abuse"
    ]

    # If message contains any banned word → block it
    return any(word in text for word in banned_words)
