import jwt


def parse_token(token, secret):
    try:
        return jwt.decode(token, secret, algorithms=["HS256"])
    except Exception as e:
        return None
