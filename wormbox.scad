// Parameters
$fn=50; // Smooth curves
box_width = 100; // Width of the box
box_depth = 100; // Depth of the box
box_height = 120; // Height of the box
wall_thickness = 5; // Thickness of the walls
lift_height = 100; // Starting lift height of the cover above the base
overlap = 1; // How much the cover overlaps the bottom platform
vent_slit_width = 2; // Width of ventilation slits
vent_slit_height = 5; // Height of ventilation slits
vent_slit_spacing = 10; // Spacing between ventilation slits
vent_slit_offset = 5; // Offset from the top of the box for the ventilation slits
clearance = 0.2; // Increased clearance to avoid rendering glitches

// Free-floating bottom
module bottom() {
    // No need to translate down as we will ensure the cover does not touch the base
    cube([box_width, box_depth, wall_thickness]);
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
    // Calculate the translation height based on the animation time $t
    // The cover starts fully lifted (lift_height) and moves down, stopping just above the base
    height = lift_height * (1 - $t) + clearance; // Add clearance to prevent touching

    translate([0, 0, height]) { // Move the cover down during the animation
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
bottom();
cover();
