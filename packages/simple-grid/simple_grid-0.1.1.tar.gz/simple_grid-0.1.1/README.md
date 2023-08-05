# Install
```bash
pip install simple-grid
```
if you are using conda, you can install it with:
```bash
conda install -c conda-forge simple-grid
```
# How to run
```python
from  simpleGrid import Grid

Grid(
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ], mode='letter'
)
```