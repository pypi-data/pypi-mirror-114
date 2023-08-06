# Colored Terminal
	* Python support for colored text in terminal

```python
from cterminal import *

cprint(style.RED + "test")
"""@params for cprint()
 - string: 			Required (can be multiple strings)
 - separator: 		Optional, default is " "
 - end: 			Optional, default is "\n"
 - file:			Optional, default is sys.stdout
 - flush:			Optional, default is False
"""

your_fg_color = getfgfromrgb(r, g, b)
your_bg_color = getbgfromrgb(r, g, b)
```

## Supported

| Platform      | Colors        |
| ------------- | ------------- |
| Windows		| Yes			|
| Linux			| Yes			|


| Colors        |
| ------------- |
| BLACK      	|
| RED      		|
| GREEN 		|
| YELLOW		|
| BLUE			|
| MAGENTA		|
| CYAN			|
| WHITE			|
| UNDERLINE		|
