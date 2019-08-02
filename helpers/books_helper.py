def update_book_payload(payload, **kwargs):
    for key, value in kwargs.items():
        payload[key] = value
    return payload
