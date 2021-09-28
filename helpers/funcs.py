import uuid


def serviceTokenGenerator(_str = 'TOKEN'):
  id = uuid.uuid4().int
  return '{}-{}'.format(_str, str(id)[:5])

