# mask-canvas

This is a canvas module to draw some lines and arcs where you can register masks.

![Screenshot from 2024-01-30 22-28-34](https://github.com/teo646/mask-canvas/assets/61399931/2dffbd33-83ca-4622-9def-3b13970b1510)
![Screenshot from 2024-02-08 22-56-26](https://github.com/teo646/mask-canvas/assets/61399931/a8009cda-614d-4af0-8a0e-cf2ddc320cb1)

This module uses mathmatical ways to get acurate intersections between lines and mask. 
So you don't need to draw on 2d array image which has limitation of pixel based drawing.
(you cannot draw a line from float number coordinates to float number coordinates because grid is only defined on integer points)


### Prerequisites

cv2, numpy but will be install automatically via pip install -e.

### Installing

1. create virtual environment(venv)
```
python -m venv .venv
source .venv/bin/activate
```

2. install module
```
git clone https://github.com/teo646/mask-canvas.git
cd maskCanvas
pip install -e .
```


## Running the tests
```
python example/masking.py
python example/circle.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details


