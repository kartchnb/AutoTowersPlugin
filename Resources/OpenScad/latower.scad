/* [General Parameters] */
// The label to add to the tower
Tower_Label = "LINEAR ADV";

// The label to add the to right column
Column_Label = "";

// Text to prefix to the section labels
Section_Label_Prefix = "";

// Text to suffix to the section labels
Section_Label_Suffix = "";

// The starting value (temperature or fan speed)
Starting_Value = 0;

// The ending value (temperature or fan speed) of the tower
Ending_Value = 0.2;

// The amount to change the value (temperature or fan speed) between sections
Value_Change = 0.02;

// The height of each section of the tower
Section_Height = 8.401;

// Size of the tower
Tower_Size = 70;


/* [Advanced Parameters] */
// The font to use for tower text
Font = "Arial:style=Bold";

// Should sections be labeled?
Label_Sections = true;

// The height of the section labels in relation to the height of each section
Section_Label_Height_Multiplier = 0.401;

// The height of the tower label in relation to the length of the column
Tower_Label_Height_Multiplier = 0.601;

// The height of the column label in relation to the height of each section
Column_Label_Height_Multiplier = 0.301;

// The value to use for creating the model preview (lower is faster)
Preview_Quality_Value = 24;

// The value to use for creating the final model render (higher is more detailed)
Render_Quality_Value = 24;

// A small value used to improve rendering in preview mode
Iota = 0.001;



/* [Development Parameters] */
// Orient the model for creating a screenshot
Orient_for_Screenshot = false;

// The viewport distance for the screenshot 
Screenshot_Vpd = 140.00;

// The viewport field of view for the screenshot
Screenshot_Vpf = 22.50;

// The viewport rotation for the screenshot
Screenshot_Vpr = [ 75.00, 0.00, 300.00 ];

// The viewport translation for the screenshot
Screenshot_Vpt = [ 0.00, 0.00, 15.00 ];


/* [Calculated parameters] */
// Calculate the rendering quality
$fn = $preview ? Preview_Quality_Value : Render_Quality_Value;

// Ensure the value change has the correct sign
Value_Change_Corrected = Ending_Value > Starting_Value
    ? abs(Value_Change)
    : -abs(Value_Change);

// Determine how many sections to generate
Section_Count = ceil(abs(Ending_Value - Starting_Value) / abs(Value_Change));

// Calculate the font size
Section_Label_Font_Size = Section_Height * Section_Label_Height_Multiplier;
Tower_Label_Font_Size = Section_Height * Tower_Label_Height_Multiplier;
Column_Label_Font_Size = Section_Height * Column_Label_Height_Multiplier; 

// Calculate the depth of the labels
Label_Depth = 0.401/2;



// Generate the model
module Generate_Model()
{
    // Generate the tower proper by iteritively generating a section for each retraction value
    module Generate_Tower()
    {
        // Create each section
        for (section = [0: Section_Count - 1])
        {
            // Determine the value for this section
            value = Starting_Value + (Value_Change_Corrected * section);

            // Determine the offset of the section
            z_offset = section*Section_Height;

            // Generate the section itself and move it into place
            translate([0, 0, z_offset])
                Generate_Section(str(value));
        }
        
    }



    // Generate a single section of the tower with a given label
    module Generate_Section(label)
    {
        difference()
        {
            union() {
                // Create lines between sections
                Generate_Extrusion(Section_Height-0.5);
                scale([0.995, 0.995, 1])
                    Generate_Extrusion(Section_Height);
            }

            // Carve out the label for this section
            if (Label_Sections)
                Generate_SectionLabel(label);
        }
    }
    
    // Generate extruded polygon for tower segment
    module Generate_Extrusion(extrusion_height)
    {
        linear_extrude(
        height = extrusion_height , 
        center = true, 
        convexity = 10, 
        twist = 0)
            polygon(points=[
                [-Tower_Size/2,Tower_Size/2],
                [Tower_Size/2,Tower_Size/2],
                [Tower_Size/2,0],
                [0,-Tower_Size/2],
                [-Tower_Size/2,0]],
            paths=[[0,1,2,3,4]]);
    };

    // Generate the text that will be carved into the square section column
    module Generate_SectionLabel(label)
    {
        full_label = str(Section_Label_Prefix, label, Section_Label_Suffix);
        translate([Tower_Size/2 + Iota, Section_Height*2, 0])
        rotate([90, 0, 90])
        translate([0, 0, -Label_Depth])
        linear_extrude(Label_Depth + Iota)
            text(text=full_label, font=Font, size=Section_Label_Font_Size, halign="center", valign="top");
    }



    // Generate the text that will be carved along the left side of the tower
    module Generate_TowerLabel(label)
    {
        translate([-Tower_Size/2 - Iota, Tower_Size/4 + Section_Height/2, Section_Height/2])
        rotate([-90, -90, 90])
        translate([0, 0, -Label_Depth])
        linear_extrude(Label_Depth + Iota)
            text(text=label, font=Font, size=Tower_Label_Font_Size, halign="left", valign="center");
    }



    // Generate the curved text that will be carved into the first rounded section column
    module Generate_ColumnLabel(label)
    {
        translate([-Tower_Size/2 - Iota, Tower_Size/4 - Section_Height/2, Section_Height/2])
        rotate([-90, -90, 90])
        translate([0, 0, -Label_Depth])
        linear_extrude(Label_Depth + Iota)
            text(text=label, font=Font, size=Column_Label_Font_Size, halign="left", valign="center");
    }



    module Generate()
    {

        difference()
        {
            Generate_Tower();

            // Create the tower label
            Generate_TowerLabel(Tower_Label);

            // Create the column label
            Generate_ColumnLabel(Column_Label);
        }
    }



    Generate();
}



// Generate the model
Generate_Model();

// Orient the viewport
$vpd = Orient_for_Screenshot ? Screenshot_Vpd : $vpd;
$vpf = Orient_for_Screenshot ? Screenshot_Vpf : $vpf;
$vpr = Orient_for_Screenshot ? Screenshot_Vpr : $vpr;
$vpt = Orient_for_Screenshot ? Screenshot_Vpt : $vpt;
