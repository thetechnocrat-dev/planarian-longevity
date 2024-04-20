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
lens_hole_diameter = 12; // Diameter of the camera lens hole
lens_extension_height = 15; // Height of the lens extension above the cover
lens_outer_diameter = lens_hole_diameter + 2 * 1; // Outer diameter of the lens (adding 1mm thickness on all sides)
lens_inner_diameter = lens_hole_diameter; // Inner diameter remains as the lens hole diameter
led_hole_diameter = 5; // Diameter of the LED hole
lens_wall_thickness = 2; // Thickness of the lens wall
led_hole_spacing = 30; // Spacing from the center of the camera hole to the center of the LED hole
pi_width = 56 + 10; // Width of Raspberry Pi
pi_depth = 17 + 10; // Depth of Raspberry Pi
pi_height = 85 + 2; // Height of Raspberry Pi
holder_thickness = 3; // Thickness of the Raspberry Pi holder walls

// Option to toggle parts for printing
print_bottom = false; // Set to true to print the bottom
print_cover = true; // Set to true to print the cover

// Free-floating bottom
module bottom() {
    cube([box_width, box_depth, wall_thickness]); // Simple bottom plate
}

pi = 3.14159;

max_angle = atan((box_height - pi_height) / pi_depth); // Max angle to meet the cover opening

// Raspberry Pi holster with parametric angle
module pi_holster() {
    translate([-pi_depth, (box_depth - pi_width) / 2, box_height - pi_height]) {
        // Back wall of the holster
        cube([holder_thickness, pi_width, pi_height]);
        // Parametric angled bottom support plane, use radians directly
        translate([0, 0, 0])
            rotate([0, max_angle, 0])  // Convert to degrees only for rotate function
                cube([pi_depth / cos(max_angle), pi_width, holder_thickness]);
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
        translate([x, 0, box_height - vent_slit_offset - vent_slit_height]) {
            cube([vent_slit_width, wall_thickness, vent_slit_height]);
        }
    }
    for(x = [overlap + vent_slit_spacing : vent_slit_spacing : box_width + overlap - vent_slit_spacing]) {
        translate([x, box_width, box_height - vent_slit_offset - vent_slit_height]) {
            cube([vent_slit_width, wall_thickness, vent_slit_height]);
        }
    }
}


// Camera lens module
module camera_lens() {
    translate([box_width/2 + overlap, box_depth/2 + overlap, box_height - wall_thickness - lens_extension_height])
        difference() {         
            cylinder(h = lens_extension_height, r = (lens_hole_diameter/2) + lens_wall_thickness, $fn = 50);
            cylinder(h = lens_extension_height, r = (lens_hole_diameter/2), $fn = 50);
        }
}


// Cover with side ventilation slits, camera lens, camera hole, Raspberry Pi holster, and LED holes
module cover() {
    translate([0, 0, 0]) { // Adjust for optimal print orientation 
        difference() {
            // The outer shape of the cover
            cube([box_width + 2 * overlap, box_depth + 2 * overlap, box_height]);

            // Subtracting the inner part to create hollow space and walls
            translate([overlap, overlap, 0])
                cube([box_width, box_depth, box_height - wall_thickness]);

            // Subtracting camera hole through the cover and the lens
            translate([box_width/2 + overlap, box_depth/2 + overlap, box_height - wall_thickness - lens_extension_height])
                cylinder(h = wall_thickness + lens_extension_height, r = lens_hole_diameter/2, $fn = 50);

            // Subtract ventilation slits from the cover sides
            ventilation_slits();

            // LED holes on the top, positioned along the y-axis
            translate([box_width/2 + overlap, box_depth/2 + overlap - led_hole_spacing, box_height - wall_thickness])
                cylinder(h = wall_thickness, r = led_hole_diameter/2, $fn = 50);
            translate([box_width/2 + overlap, box_depth/2 + overlap + led_hole_spacing, box_height - wall_thickness])
                cylinder(h = wall_thickness, r = led_hole_diameter/2, $fn = 50);
        }
        camera_lens();
    }
    pi_holster();
}


// Assembly
if (print_bottom) bottom();
if (print_cover) cover();
