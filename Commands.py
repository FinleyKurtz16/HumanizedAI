from datetime import datetime

def aehnlichkeit(a, b):
    from difflib import SequenceMatcher
    return SequenceMatcher(None, a, b).ratio()

def handle_commands(text):
    if aehnlichkeit(text.lower(), 'sage mir wie spät es ist') > 0.6:
        current_hour = datetime.now().strftime("%H")
        current_minute = datetime.now().strftime("%M")
        if(str(current_minute) == "00"):
            return("Es ist " + current_hour + " Uhr.")
        else:
            return("Es ist " + current_hour + " Uhr " + current_minute + ".")

    elif aehnlichkeit(text.lower(), 'schalte mein licht ein') > 0.6:
        return("Dein Licht wird jetzt eingeschaltet")

    elif aehnlichkeit(text.lower(), 'wie geht es dir') > 0.6:
        return("Mir geht es gut und dir?")

    else:
        return None
