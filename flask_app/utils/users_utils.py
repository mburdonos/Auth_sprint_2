def valid_pagination(number, size):
    if number and size:
        if int(number) > 0 and int(size) > 0:
            return {"number": int(number), "size": int(size)}
