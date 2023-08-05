class UserNotFound(Exception):
  """Raised when user doesn't exist(404 error)."""
  pass

class ProjectNotFound(Exception):
  """Raised when project doesn't exist(404 error)."""
  pass

class StudioNotFound(Exception):
  """Raised when studio doesn't exist(404 error)."""
  pass

class PostNotFound(Exception):
  """Raised when post doesn't exist(404 error)."""
  pass

class TopicNotFound(Exception):
  """Raised when topic doesn't exist(404 error)."""
  pass

class PageNotFound(Exception):
  """Raised when there is a 404 error in frontpage API"""
  pass

class InvalidValue(Exception):
  """
  Raised when invalid value is passed through in the decoder.
  Check whether the input is int, is of even digits, ends with "00" and encoded only with the ScraGet encoder.
  """
  pass