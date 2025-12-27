#블록리스트 관리 파일

BLCOKLIST = set()

def add_to_blocklist(jti):
    BLCOKLIST.add(jti)

def remove_from_blocklist(jti):
    BLCOKLIST.discard(jti)