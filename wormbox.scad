// Parameters
$fn=50; // Smooth curves
cover_depth = 100;
cover_height = 120;
wall_thickness = 2;
vent_slit_width = 2;
vent_slit_height = 5;
vent_slit_spacing = 10; // Spacing between slits
vent_slit_offset = 5; // Offset from the top of the cover
lens_hole_diameter = 14;
lens_extension_height = 5;
lens_outer_diameter = lens_hole_diameter + 2 * 1;
lens_inner_diameter = lens_hole_diameter;
lens_wall_thickness = 2;
led_hole_diameter = 5;
led_hole_height = 60;
led_bulb_height = 9;
led_hood_overhang = 2;
rpi_width = 56 + 10; // Width of Raspberry Pi
rpi_depth = 17 + 10; // Depth of Raspberry Pi
rpi_height = 85 + 2; // Height of Raspberry Pi
holder_thickness = 3; // Thickness of the Raspberry Pi holder walls
pi = 3.14159;

cover_width = 80 * 2 + led_bulb_height * 2; // See https://app.radicle.xyz/nodes/seed.radicle.garden/rad:z3qqgNPPywywG2fzkDYDjxuhQCuec/tree/light_coverage_sim.py

// Toggle parts for printing
print_bottom = false;
print_cover = true;

module bottom() {
    translate([-wall_thickness, -wall_thickness, -wall_thickness]) {
        cube([cover_width + 2 * wall_thickness, cover_depth + 2 * wall_thickness, 2 * wall_thickness]);
    }
}

module pi_holster() {
    // Back of the holster
    translate([(cover_width - rpi_width) / 2, -rpi_depth, cover_height - rpi_height]) {
        cube([rpi_width, holder_thickness, rpi_height]);

        // Angled bottom support plane
        max_angle = atan((cover_height - rpi_height) / rpi_depth); // Max angle to meet the cover opening
        rotate([-max_angle, 0, 0]) {
            cube([rpi_width, sqrt(pow(rpi_depth, 2) + pow((cover_height - rpi_height), 2)), holder_thickness]);
        }
    }

    // Side support bars
    translate([(cover_width - rpi_width) / 2, -rpi_depth, cover_height - holder_thickness]) {
        cube([holder_thickness, rpi_depth, holder_thickness]);
    }
    translate([rpi_width + (cover_width - rpi_width) / 2 - holder_thickness, -rpi_depth, cover_height - holder_thickness]) {
        cube([holder_thickness, rpi_depth, holder_thickness]);
    }
}

module ventilation_slits() {
    for(y = [vent_slit_spacing : vent_slit_spacing : cover_depth]) {
        translate([0, y, cover_height - vent_slit_offset - vent_slit_height]) {
            cube([vent_slit_width, wall_thickness, vent_slit_height]);
        }
    }
    for(y = [vent_slit_spacing : vent_slit_spacing : cover_depth]) {
        translate([cover_width - wall_thickness, y, cover_height - vent_slit_offset - vent_slit_height]) {
            cube([vent_slit_width, wall_thickness, vent_slit_height]);
        }
    }
}


module camera_lens() {
    translate([cover_width/2, cover_depth/2, cover_height - wall_thickness - lens_extension_height]) {
        difference() {         
            cylinder(h = lens_extension_height, r = (lens_hole_diameter / 2) + lens_wall_thickness, $fn = 50);
            cylinder(h = lens_extension_height, r = (lens_hole_diameter / 2), $fn = 50);
        }
    }
}

module led_holes() {
    translate([0, cover_depth / 2, led_hole_height])
        rotate([0, 90, 0]) {
        cylinder(h = wall_thickness, r = led_hole_diameter / 2, $fn = 50);
    }

    translate([cover_width, cover_depth / 2, led_hole_height])
        rotate([0, -90, 0]) {
        cylinder(h = wall_thickness, r = led_hole_diameter / 2, $fn = 50);
    }
}

// reduces glare
module led_hoods() {
    translate([0, cover_depth / 2 - led_hole_diameter, led_hole_height + led_hole_diameter]) {
        rotate([0, 45, 0]) {
            cube([led_bulb_height + wall_thickness + led_hood_overhang, led_hole_diameter * 2, wall_thickness]);
        }
    }
    translate([cover_width - wall_thickness, cover_depth / 2 - led_hole_diameter, led_hole_height + led_hole_diameter]) {
        rotate([0, 135, 0]) {
            cube([led_bulb_height + wall_thickness + led_hood_overhang, led_hole_diameter * 2, wall_thickness]);
        }
    }
}

module cover() {
    translate([0, 0, 0]) { 
        difference() {
            // The outer shape of the cover
            cube([cover_width, cover_depth, cover_height]);

            // Subtract the inner part to create hollow space and walls
            translate([wall_thickness, wall_thickness, 0]) {
                cube([cover_width - 2 * wall_thickness, cover_depth - 2 * wall_thickness, cover_height - wall_thickness]);
            }

            // Subtract camera hole through the cover and the lens
            translate([cover_width/2, cover_depth/2, cover_height - wall_thickness - lens_extension_height]) {
                cylinder(h = wall_thickness + lens_extension_height, r = lens_hole_diameter / 2, $fn = 50);
            } 
            ventilation_slits();
            led_holes();
        }
        camera_lens();
    }
    pi_holster();
    led_hoods();
}

// Assembly
if (print_bottom) bottom();
if (print_cover) cover();

