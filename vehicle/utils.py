
queryset = [
    {
      'id': 1, 
      'name': 'Godfred',
      },
    {
      'id': 1, 
      'name': 'Messi',
      },
    {
      'id': 2, 
      'name': 'Jessi',
      },
    {
      'id': 2, 
      'name': 'Lizzie',
      },
    {
      'id': 3, 
      'name': 'Joe',
      },
]



def singleOutDuplicates(val, arr):
  if val.token not in arr:
    arr.append(val.token)
    return True
  
  return False


def remove_duplicates(_queryset):
  _include = []
  qs = filter(lambda x: singleOutDuplicates(x, _include), _queryset)
  return list(qs)
  
  
  
