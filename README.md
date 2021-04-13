# battery-charge-control
This is a simple alert system made in Python that monitors the charge of the PC. The goal is to prevent the battery from constantly being uncalibrated.

**Note: this aplication is suposed to work in Ubuntu (Linux in general) and was tested in Ubuntu 18.04 LTS**

## Basic usage

Go to desktop and create a file with _.desktop_ extension, name it as you want e.g. _"battery.desktop"_ With bash simply:
```bash
$ cd ~/Desktop
$ touch battery.desktop
$ chmod +x battery.desktop
```

inside of that file you must add the following text (change `/path/to/battery-charge-control` for the path to cloned repo)
```desktop
#!/usr/bin/env xdg-open
[Desktop Entry]
Name=Battery Checker
Comment=Battery level checker
Exec=/path/to/battery-charge-control/py_bat_notification.py
Icon=/path/to/battery-charge-control/battery.png
Terminal=true
Type=Application
```

and then just double click on the new app with the battery icon.

## Appearance

![imagen](https://user-images.githubusercontent.com/55881458/114626672-550e9f00-9cb4-11eb-9a3e-9846c1177c32.png)
