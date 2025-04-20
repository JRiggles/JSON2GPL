#!/usr/bin/env python3

import json
import tkinter.messagebox as tkm
from pathlib import Path
from sys import argv
# from tkinter.filedialog import askopenfilename


def hex_to_rgb(hex_color) -> tuple[int, int, int]:
    """Convert a hex color value (e.g. "#7f7fff') to an (R, G, B) tuple"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError(f'Invalid hex color format: {hex_color}')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b)


def convert_json_to_gpl(json_file) -> None:
    """
    Read color palette information from a JSON file (such as one exported from
    Sip) and convert it to GPL format.

    The expected JSON structure should contain at array the following:
    - 'colors': a list of color objects, each with a 'name' and 'hex' key
    - 'name': the name of the palette
    ```
    {
        "name": "My Palette",
        "colors": [
            {"name": "NormalRed", "hex": "#ff7f7f"},
            {"name": "NormalGreen", "hex": "#7fff7f"},
            {"name": "NormalBlue", "hex": "#7f7fff"}
        ]
    }
    ```
    """
    # open JSON palette file and read data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    palette_name = data.get('name', 'Untitled Palette')
    colors = data.get('colors', [])

    # create GPL header and body lines
    lines = [
        'GIMP Palette',
        f'#Name: {palette_name}',
        f'#Colors: {len(colors)}',
        f'#Converted from {json_file.name}',
    ]

    for color in colors:
        hex_color = color.get('hex', '')
        rgb = hex_to_rgb(hex_color)
        name = color.get('name', '')
        # format each line with right-aligned RGB vals and the color hex/name
        lines.append(
            f'{rgb[0]:3d} {rgb[1]:3d} {rgb[2]:3d}    #{hex_color} "{name}"'
        )

    # write GPL file
    gpl_file = json_file.with_suffix('.gpl')
    with open(gpl_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def remove_json_file(json_file) -> None:
    """Remove the JSON file after conversion"""
    try:
        json_file.unlink()
    except Exception as e:
        tkm.showerror(
            title='Error',
            message=f'Could not remove the JSON file: {e}',
        )


def main() -> None:
    try:
        if len(argv) > 1:  # if a file is passed as an argument, use that file
            palette_file = Path(argv[1])
            if palette_file.suffix == '.json':
                convert_json_to_gpl(palette_file)
                remove_json_file(palette_file)
    except Exception as e:
        tkm.showerror(
            title='Error',
            message=f'An error occurred while converting palette data: {e}',
        )


if __name__ == '__main__':
    main()
