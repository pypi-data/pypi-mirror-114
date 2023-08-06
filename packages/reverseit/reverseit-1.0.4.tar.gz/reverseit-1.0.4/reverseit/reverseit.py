def reverseit(data: str or list or dict):
    if(type(data) == str or type(data) == list):
      return data[::-1]
    elif(type(data) == dict):
      return dict(reversed(list(data.items())))
