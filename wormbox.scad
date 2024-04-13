// Parameters
$fn=50; // Smooth curves
box_width = 100; // Width of the box
box_depth = 100; // Depth of the box
box_height = 120; // Height of the box
wall_thickness = 5; // Thickness of the walls
overlap = 1; // How much the cover overlaps the bottom platform
vent_slit_width = 2; // Width of ventilation slits
vent_slit_height = 5; // Height of ventilation slits
vent_slit_spacing = 10; // Spacing between ventilation slits
vent_slit_offset = 5; // Offset from the top of the box for the ventilation slits
clearance = 0.2; // Increased clearance to avoid rendering glitches

// Option to toggle parts for printing
print_bottom = true; // Set to true to print the bottom
print_cover = true; // Set to true to print the cover

// Free-floating bottom
module bottom() {
    cube([box_width, box_depth, wall_thickness]); // Simple bottom plate
}

// Ventilation slits near the top of the sides
module ventilation_slits() {
    for(x = [overlap + vent_slit_spacing : vent_slit_spacing : box_width + overlap - vent_slit_spacing]) {
        translate([x, -clearance, box_height - vent_slit_offset - vent_slit_height]) {
            cube([vent_slit_width, wall_thickness + 2 * clearance, vent_slit_height + clearance]);
        }
        translate([x, box_depth + wall_thickness - clearance, box_height - vent_slit_offset - vent_slit_height]) {
            cube([vent_slit_width, wall_thickness + 2 * clearance, vent_slit_height + clearance]);
        }
    }
}

// Cover with side ventilation slits
module cover() {
    translate([0, 0, clearance]) { // Adjust for optimal print orientation
        difference() {
            // The outer shape of the cover
            cube([box_width + 2 * overlap, box_depth + 2 * overlap, box_height]);

            // Subtracting the inner part to create hollow space and walls, with clearance
            translate([overlap, overlap, 0])
                cube([box_width, box_depth, box_height - wall_thickness + clearance]);

            // Subtract ventilation slits from the cover sides, with clearance
            ventilation_slits();
        }
    }
}

// Assembly
if (print_bottom) bottom();
if (print_cover) cover();
