import re



def totalAmount(text):

    pattern = r"(?i)(total|amount)[^\d]*(\d+[\.,]?\d*)"
    matches = re.findall(pattern, text)
    if matches:
        # Return the last match as it usually contains the final total amount
        return matches[-1][-1]
    return None



