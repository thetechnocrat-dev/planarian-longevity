import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

# Constants
radius_petri_dish = 50  # mm
distance_from_center = 80  # mm, for both lights
beam_angle_degrees = 44  # Total viewing angle of the LED
angle_of_incidence_degrees = 45  # Angle of the LED relative to the vertical
half_viewing_angle = beam_angle_degrees / 2  # Half of the total viewing angle
height_of_led = 60  # mm, height of the LED from the level of the Petri dish

# Adjusted function to ensure beams point towards the petri dish and stop at dish level, with direction consideration
def adjusted_side_view_beam_paths(x_offset, angle_of_incidence, half_view_angle, height, direction):
    angles = [
        angle_of_incidence - half_view_angle,
        angle_of_incidence,
        angle_of_incidence + half_view_angle
    ]
    endpoints = []
    for angle in angles:
        x_intercept = direction * (height / np.tan(np.radians(angle)))
        x_intercept_plus_offset = x_offset + x_intercept
        endpoints.append((x_intercept_plus_offset, 0))  # Stop at y=0, the dish level
    return endpoints

# Calculate adjusted endpoints for side view of each LED with direction
left_endpoints = adjusted_side_view_beam_paths(-distance_from_center, angle_of_incidence_degrees, half_viewing_angle, height_of_led, +1)
right_endpoints = adjusted_side_view_beam_paths(distance_from_center, angle_of_incidence_degrees, half_viewing_angle, height_of_led, -1)

# Recreate figure and axis for the corrected side view
fig, ax = plt.subplots()

# Petri dish as a horizontal line
ax.hlines(y=0, xmin=-radius_petri_dish, xmax=radius_petri_dish, colors='grey', linewidths=3, label='Petri Dish')

# Plot the beams as lines from each LED position correctly
for i, (x, y) in enumerate(left_endpoints):
    linestyle = '-' if i == 1 else '--'
    ax.plot([-distance_from_center, x], [height_of_led, y], 'r', linestyle=linestyle)  # Red for left LED
for i, (x, y) in enumerate(right_endpoints):
    linestyle = '-' if i == 1 else '--'
    ax.plot([distance_from_center, x], [height_of_led, y], 'b', linestyle=linestyle)  # Blue for right LED

# Add LED representations
led_left = patches.RegularPolygon((-distance_from_center, height_of_led), numVertices=4, radius=3, orientation=np.radians(0), color='red', label='Left LED')
led_right = patches.RegularPolygon((distance_from_center, height_of_led), numVertices=4, radius=3, orientation=np.radians(0), color='blue', label='Right LED')
ax.add_patch(led_left)
ax.add_patch(led_right)

# Setting plot properties
ax.set_xlim(-100, 100)
ax.set_ylim(-5, 100)
ax.set_aspect('equal', 'box')
ax.set_xlabel('mm')
ax.set_ylabel('mm')
ax.set_title('Side View of Light Beam Paths on Petri Dish')
ax.legend()

# Show the plot
plt.grid(True)
plt.show()
