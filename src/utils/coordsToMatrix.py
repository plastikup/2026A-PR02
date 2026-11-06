def coords_to_matrix(coords: list[list[tuple[int, int]]], coords_size: tuple[int, int], matrix_size: tuple[int, int]):
	matrix = [[0 for _ in range(matrix_size[0])] for _ in range(matrix_size[1])]
	for row in coords:
		for coord in row:
			y = min(max(coord[1] * matrix_size[1] // coords_size[1], 0), matrix_size[1] - 1)
			x = min(max(coord[0] * matrix_size[0] // coords_size[0], 0), matrix_size[0] - 1)
			matrix[y][x] = 1
	return matrix
