import hashlib

#md5加盐加密
def _hashed_with_salt(info, salt):        
    m = hashlib.md5()
    m.update(info.encode('utf-8'))
    m.update(salt)
    return m.hexdigest()

