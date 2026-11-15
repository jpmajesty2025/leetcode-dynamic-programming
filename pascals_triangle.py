"""
You are given an integer numRows.

Return the first numRows of Pascal's triangle.

In Pascal's triangle, each number is the sum of the two numbers directly above it and the first and last 
number on each row must be equal to 1
"""

def generate(numRows: int) -> list[list[int]]:
    """Return the first numRows of Pascal's triangle."""
    if numRows <= 0:
        return []

    triangle = [[1]]  # Initialize the triangle with the first row

    for i in range(1, numRows):
        row = [1]  # Start each row with a 1
        for j in range(1, i):
            # Each number is the sum of the two numbers directly above it
            row.append(triangle[i - 1][j - 1] + triangle[i - 1][j])
        row.append(1)  # End each row with a 1
        triangle.append(row)

    return triangle