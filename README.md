# Ace_Combat_8_Keybind_Configurator
A lightweight, standalone graphical user interface (GUI) designed to easily parse, view, and remap custom hardware bindings for the Logitech/Saitek X56 Rhino HOTAS system inside Ace Combat 8.

## Key Features
• Zero Setup Auto-Detection: Automatically targets and opens the hidden game engine configurations sub-directory located within the local application user data (%localappdata%\BANDAI NAMCO Entertainment\ACE COMBAT 8\Saved\Config\Windows).  

• Logitech Profiler Nomenclature Sync: Maps hardcoded game input parameters directly to actual hardware names printed on the controller chassis (e.g., Trigger, Pinky Switch, SW 1-6, TGL 1-4, and handle rotaries).  

• Automatic Backup Engine: Safety checks initialization writes by dynamically generating a .bak copy of the pristine environment directory layout before modifying data matrices.  

• Axis Behavior Continuity Filters: Features specialized multi-axis rules for throttle grips and joysticks (X, Y, Rz, Rx, Ry), maintaining baseline flight option logic natively.  

## Requirements
[Python](https://www.python.org/downloads/)

[PyGame](https://pypi.org/project/pygame/)

###Optional:
[PyInstaller](https://pypi.org/project/pyinstaller/) 
>If building from source

[PyGame-CE](https://github.com/pygame-community/pygame-ce)
>Use this version of pygame if you can't properly install pygame from above.

## Restoring From .bak File
1. Press Win + R on your keyboard to open the Run dialog box.
2. Paste the following path into the box and press Enter:
    %localappdata%\BANDAI NAMCO Entertainment\ACE COMBAT 8\Saved\Config\Windows
3. Locate your active configuration file (FlightStick.ini) and either delete it or move it to a safe location outside the folder.
4. Locate the backup file (FlightStick.ini.bak).
5. Right-click the backup file, select Rename, and remove the .bak extension so that it reads exactly FlightStick.ini.
