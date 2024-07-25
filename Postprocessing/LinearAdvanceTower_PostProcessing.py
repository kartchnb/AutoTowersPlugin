# This script was adapted (copied) from TempTower_PostProcessing
#
# Version 0.1 - 25 Jul 2024:
#   Created for https://github.com/kartchnb/AutoTowersGenerator/issues/41
__version__ = '0.1'

from UM.Logger import Logger

from . import PostProcessingCommon as Common



def execute(gcode, base_height:float, section_height:float, initial_layer_height:float, layer_height:float, start_kfactor:float, kfactor_change:float, enable_lcd_messages:bool, enable_advanced_gcode_comments:bool):
    
    # Log the post-processing settings
    Logger.log('d', f'Beginning PA Tower post-processing script version {__version__}')
    Logger.log('d', f'Base height = {base_height} mm')
    Logger.log('d', f'Section height = {section_height} mm')
    Logger.log('d', f'Initial printed layer height = {initial_layer_height}')
    Logger.log('d', f'Printed layer height = {layer_height} mm')
    Logger.log('d', f'Starting K-factor = {start_kfactor} C')
    Logger.log('d', f'K-factor change = {kfactor_change} C')
    Logger.log('d', f'Enable LCD messages = {enable_lcd_messages}')
    Logger.log('d', f'Advanced Gcode Comments = {enable_advanced_gcode_comments}')

    # Document the settings in the g-code
    gcode[0] += f'{Common.comment_prefix} PA Tower post-processing script version {__version__}\n'
    gcode[0] += f'{Common.comment_prefix} Base height = {base_height} mm\n'
    gcode[0] += f'{Common.comment_prefix} Section height = {section_height} mm\n'
    gcode[0] += f'{Common.comment_prefix} Initial printed layer height = {initial_layer_height} mm\n'
    gcode[0] += f'{Common.comment_prefix} Printed layer height = {layer_height} mm\n'
    gcode[0] += f'{Common.comment_prefix} Starting K-factor = {start_kfactor} C\n'
    gcode[0] += f'{Common.comment_prefix} K-factor change = {kfactor_change} C\n'
    gcode[0] += f'{Common.comment_prefix} Enable LCD messages = {enable_lcd_messages}\n'
    gcode[0] += f'{Common.comment_prefix} Advanced Gcode comments = {enable_advanced_gcode_comments}\n'

    # Start at the selected starting K-factor
    current_kfactor = start_kfactor - kfactor_change # The current kfactor will be incremented when the first section is encountered

    # Iterate over each line in the g-code
    for line_index, line, lines, start_of_new_section in Common.LayerEnumerate(gcode, base_height, section_height, initial_layer_height, layer_height, enable_advanced_gcode_comments):

        # Handle each new tower section
        if start_of_new_section:

            # Increment the K-factor for this new tower section
            current_kfactor += kfactor_change

            # Configure the new K-factor in the gcode
            if enable_advanced_gcode_comments :
                lines.insert(2, f'M900 K{current_kfactor} {Common.comment_prefix} setting K-factor to {current_kfactor}')
            else :
                lines.insert(2, f'M900 K{current_kfactor}')

            # Display the new K-factor on the printer's LCD
            if enable_lcd_messages:
                lines.insert(3, f'M117 K {current_kfactor}')
                if enable_advanced_gcode_comments :
                    lines.insert(3, f'{Common.comment_prefix} Displaying "K {current_kfactor}" on the LCD')

        # Handle lines within each section
        else:
            if Common.IsLinAdvChangeLine(line):
                # Comment out the line
                new_line = f';{line}'
                if enable_advanced_gcode_comments:
                    new_line += f' {Common.comment_prefix} preventing K-factor change within the tower section'
                lines[line_index] = line

    Logger.log('d', 'AutoTowersGenerator completing PA Tower post-processing')
    
    return gcode