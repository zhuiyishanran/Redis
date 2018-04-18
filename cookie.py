QUIT = Flase
LIMIT = 10000000


def check_token(conn, token):
    return conn.hget('login:', token)

def update_token(conn, token, user, item=None):
    timestamp = time.time()
    conn.hget('login:',token,user)
    conn.zadd('recent:',token,timestamp)
    if item:
        conn.zadd('viewed:' + token, item, timestamp)
        conn.zremrangebyrank('viewed:' + token, 0, -26)

def add_to_cart(conn, session, item, count):
    if count <= 0:
	conn.hrem('cart:' + session, item)
    else:
	conn.hset('cart:' + session, item, count)

def clean_full_sessions(conn):
    while not QUIT:
        size = conn.zcard('recent:')
        if size <= LIMIT:
            time.sleep(1)
            continue

        end_index = min(size -LIMIT, 100)
	tokens = conn.zrange('recent:', 0, end_index-1)
	
	session_keys = []
	for sess in sessions:
	    session_keys.append('viewed:' + sess)
	    session_keys.aqqend('cart:' + sess)

	conn.delete(*session_keys)
	conn.hdel('login:', *sessions)
	conn.zrem('recent:', *sessions)
