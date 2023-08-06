def direct_neighbors(matrix, i, j):
  possible_coords = [
    (i, j + 1),
    (i, j - 1),
    (i - 1, j),
    (i + 1, j)
  ]

  return [
    k for k in possible_coords
    if k[0] < len(matrix) and k[1] < len(matrix[i]) and k[0] >= 0 and k[1] >= 0
  ]
def all_neighbors(matrix, i, j):
  possible_coords = [
    (i, j + 1),
    (i, j - 1),
    (i - 1, j),
    (i + 1, j),
    (i - 1, j - 1),
    (i - 1, j + 1),
    (i + 1, j + 1),
    (i + 1, j - 1)
  ]

  return [
    k for k in possible_coords
    if k[0] < len(matrix) and k[1] < len(matrix[i]) and k[0] >= 0 and k[1] >= 0
  ]