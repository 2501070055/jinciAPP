import hashlib
import time


if __name__ == '__main__':
    ctime = time.time()

    key = 'zrrwhnqh199817'
    new_key = "%s|%s" % (key, ctime)
    print(new_key)

    m = hashlib.md5()
    m.update(bytes(new_key, encoding='utf-8'))
    md5_key = m.hexdigest()
    md5_key_key = "%s|%s" % (md5_key, ctime)
    print(md5_key_key)
