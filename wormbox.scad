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
lens_hole_diameter = 10; // Diameter of the camera lens hole
pi_width = 56 + 4; // Width of Raspberry Pi plus clearance
pi_depth = 17 + 4; // Depth of Raspberry Pi plus clearance
pi_height = 85 + 2; // Height of Raspberry Pi plus clearance
holder_thickness = 3; // Thickness of the Raspberry Pi holder walls

// Option to toggle parts for printing
print_bottom = false; // Set to true to print the bottom
print_cover = true; // Set to true to print the cover

// Free-floating bottom
module bottom() {
    cube([box_width, box_depth, wall_thickness]); // Simple bottom plate
}

pi = 3.14159;

max_angle = atan((box_height - pi_height) / pi_depth) * 180 / pi; // Max angle to meet the cover opening

// Raspberry Pi holster with parametric angle
module pi_holster() {
    translate([-pi_depth, (box_depth - pi_width) / 2, box_height - pi_height]) {
        // Back wall of the holster
        cube([holder_thickness, pi_width, pi_height]);
        // Parametric angled bottom support plane
        translate([0, 0, 0])
            rotate([0, max_angle, 0])
                cube([pi_depth / cos(max_angle * pi / 180), pi_width, holder_thickness]); // Adjusted length for the bottom holster
        // Side support bars
        translate([0, 0, pi_height - holder_thickness])
            cube([pi_depth, holder_thickness, holder_thickness]); // Rear upper bar
        translate([0, pi_width - holder_thickness, pi_height - holder_thickness])
            cube([pi_depth, holder_thickness, holder_thickness]); // Front upper bar
    }
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

// Cover with side ventilation slits, camera lens hole, and Raspberry Pi holster
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

            // Camera lens hole on the top
            translate([box_width/2 + overlap, box_depth/2 + overlap, box_height - wall_thickness])
                cylinder(h = wall_thickness, r = lens_hole_diameter/2, $fn = 50);
        }
    }
    pi_holster();
}

// Assembly
if (print_bottom) bottom();
if (print_cover) cover();
