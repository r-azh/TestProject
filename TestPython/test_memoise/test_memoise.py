# todo

class HashInfo:
    created_at = datetime.now()
    hash = ''
    expiry_ts = datetime.now()
    module_id = ''
    user_id = 2


@memoize(ttl=3600)
def get_info_from_hash(hash):
    return db.query.filter(HashInfo.hash == hash).first()
