
def md5(user):
    import hashlib
    import time
    try:
        cur_time = str(time.time())
        m = hashlib.md5(bytes(user, encoding = "utf-8"))
        m.update(bytes(cur_time, encoding = "utf-8"))
        return m.hexdigest()
    except:
        raise Exception("Fail To Generate Token !")