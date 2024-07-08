import matplotlib.pyplot as plt

# Your list of points
points = [(0, 0), (6, 0), (6, -5), (4, -5), (4, -7), (6, -7), (6, -9), (1, -9), (1, -7), (0, -7), (0, -5), (2, -5), (2, -2), (0, -2), (0, 0)]

# Unpack the points into x and y coordinates
x, y = zip(*points)

# Create a figure and axis
fig, ax = plt.subplots()

# Plot the polygon
ax.fill(x, y, alpha=0.3)  # Adjust alpha for transparency

# Set equal scaling
ax.set_aspect('equal', adjustable='box')

# Add grid, labels and title
ax.grid(True)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Polygon')

# Show the plot
plt.show()
