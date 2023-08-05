# Progress Bar

This is a simple terminal progress bar for python,
<br>
no libraries required.
<br>
## Usage
```python
from nspb import ProgressBar

pb = ProgressBar(size=100, length=100, prefix='', suffix='', decimals=1, fill='█', infos=False, printEnd ="\r", file=sys.stdout) # With full params
pb = ProgressBar(size=100, length=100) # Simplest declaration

for i in range(100 + 1):
	pb.update(i) # The value of update can be any int value, for example it can be the downloaded size of a file
```