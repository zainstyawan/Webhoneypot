def sql_injection(text):
    patterns = [
        "'", '"', "--", " OR ", " UNION ", " SELECT ",
        " DROP ", " AND ", " INSERT ", " DELETE "
    ]
    text = text.upper()
    for p in patterns:
        if p in text:
            return True
    return False
