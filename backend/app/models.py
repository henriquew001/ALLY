class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    async def authenticate(username, password):
      # Replace this with your actual authentication logic, e.g., database lookup
      if username == "testuser" and password == "password":
          return User(1, "testuser", "password")
      return None
