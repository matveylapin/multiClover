# multiClover
## Generator
___
### __Attention__
The program was tested only with these parameters:
- Ubuntu 20.04
- Python 3.8.5
- tkinter 0.1.0
- square drones only
____
### __Use__
For start geometry generator:
```BASH
$ git clone https://github.com/matveylapin/multiClover.git
$ python3 ./multiClover/geometry/generator.py
```
Parametrs:
- Drone size - is side of the green square in mm. 
- Motor Base size - side of the red square in mm.

![Alt-текст](/Images/sizes_drone_md.JPEG)

Generated .toml files will contain in __multiClover/geometry/geometries/clover{i} i-drone number__. clover0 - the main drone through which the control goes, the generator selects the closest to the center of mass of the entire structure
___