// Parameters
$fn=50; // Smooth curves
cover_depth = 110;
cover_height = 110;
dish_diameter = 100;
dish_height = 15;
dish_thickness = 2;
wall_thickness = 2;
curvature_depth = 5;
vent_slit_width = 2;
vent_slit_height = 5;
vent_slit_spacing = 10; // Spacing between slits
vent_slit_offset = 5; // Offset from the top of the cover
lens_size = 12; // For Raspberry Pi v3 Camera
lens_electronics_size = 7.5; // https://datasheets.raspberrypi.com/camera/camera-module-3-wide-mechanical-drawing.pdf
lens_extension_height = 5;
lens_wall_thickness = 2;
led_hole_diameter = 5;
led_hole_height = 70;
led_bulb_height = 9;
led_hood_overhang = 4;
rpi_width = 56 + 10; // Width of Raspberry Pi
rpi_depth = 17 + 10; // Depth of Raspberry Pi
rpi_height = 85 + 2; // Height of Raspberry Pi
holder_thickness = 3; // Thickness of the Raspberry Pi holder walls
bottom_overhang = 2;
bottom_height = 4;
pi = 3.14159;

cover_width = 70 * 2 + led_bulb_height * 2; // See https://app.radicle.xyz/nodes/seed.radicle.garden/rad:z3qqgNPPywywG2fzkDYDjxuhQCuec/tree/light_coverage_sim.py

// Toggle parts for printing
print_bottom = true;
print_cover = false;
print_dish = false;

module bottom() {
        difference() {
            translate([-bottom_overhang, -bottom_overhang, -wall_thickness]) {
                cube([cover_width + 2 * bottom_overhang, cover_depth + 2 * bottom_overhang, wall_thickness + bottom_height]);
            }
            translate([-wall_thickness / 2, -wall_thickness / 2, 0]) {
                cube([cover_width + wall_thickness, cover_depth + wall_thickness, bottom_height]);    
            }
            translate([(cover_width - (rpi_width + bottom_overhang)) / 2, -bottom_overhang, 0]) {
                cube([rpi_width + bottom_overhang, wall_thickness, bottom_height]);
            }
        }
        translate([cover_width / 2, cover_depth / 2, 0]) {
            difference() {
                    cylinder(h = bottom_height, d = dish_diameter + dish_thickness + bottom_overhang * 4, $fn=100);
                    cylinder(h = bottom_height, d = dish_diameter + dish_thickness + bottom_overhang * 2, $fn=100);
                    cube(
            }
        }
}

module dish() {
    translate([cover_width / 2, cover_depth / 2, 0]) {
        // bottom layer of dish
        cylinder(h = dish_thickness, d = dish_diameter,$fn=100);
    
        // inside of dish
        difference() {
            translate([0, 0, 0]) {
                cylinder(h = dish_height, d = dish_diameter, $fn=100);
            }
            translate([0, 0, dish_diameter * 0.7]) {
                sphere(d = dish_diameter * 1.5, $fn=100);
            }
        }
    
        // outerwall of dish
        difference() {
            cylinder(h = dish_height, d = dish_diameter + dish_thickness, $fn=100);
            cylinder(h = dish_height, d = dish_diameter, $fn=100);
        }
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
    // Raspberry Pi 3 camera has some electronics next to the lens
    // 
    difference() {
        translate([(cover_width - lens_size - lens_wall_thickness) / 2, (cover_depth - lens_size - lens_wall_thickness) / 2, cover_height - lens_extension_height - wall_thickness]) {
            cube([lens_size + lens_wall_thickness, lens_size + lens_electronics_size + lens_wall_thickness, wall_thickness + lens_extension_height]);
        }
        translate([(cover_width - lens_size) / 2, (cover_depth - lens_size) / 2, cover_height - lens_extension_height - wall_thickness]) {
            cube([lens_size, lens_size + lens_electronics_size, wall_thickness + lens_extension_height]);
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
    translate([0, (cover_depth - led_hole_diameter * 4) / 2, led_hole_height + led_hole_diameter]) {
        rotate([0, 45, 0]) {
            cube([led_bulb_height + wall_thickness + led_hood_overhang, led_hole_diameter * 4, wall_thickness]);
        }
    }
    translate([cover_width - wall_thickness, (cover_depth - led_hole_diameter * 4) / 2, led_hole_height + led_hole_diameter]) {
        rotate([0, 135, 0]) {
            cube([led_bulb_height + wall_thickness + led_hood_overhang, led_hole_diameter * 4, wall_thickness]);
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
            translate([(cover_width - lens_size) / 2, (cover_depth - lens_size) / 2, cover_height - wall_thickness]) {
                cube([lens_size, lens_size + lens_electronics_size, wall_thickness]);
            }
            
            ventilation_slits();
            led_holes();
        }

    }
    camera_lens();
    pi_holster();
    led_hoods();
}

// Assembly
if (print_bottom) bottom();
if (print_cover) cover();
if (print_dish) dish();

