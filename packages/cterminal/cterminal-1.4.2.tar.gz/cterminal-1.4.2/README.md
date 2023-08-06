# Colored Terminal
	* Python support for colored text in terminal

```python
from cterminal import *

your_fg_color = getfgfromrgb(r, g, b)
your_bg_color = getbgfromrgb(r, g, b)
"""@params for getfgfromrbg()/getbgfromrgb()
 - r, g, b:         Required, type(Int)
"""

cprint(style.RED + "test")
"""@params for cprint()
 - string: 			Required (can be multiple strings)
 - separator: 		Optional, default is " "
 - end: 			Optional, default is "\n"
 - file:			Optional, default is sys.stdout
 - flush:			Optional, default is False
"""

cinput(style.RED + "test-input >> ")
"""@params for cinput()
 - prompt:          Required (can be a string concatenate)
"""

# Only for Windows
cmd.setname("NAME") # Set the window title
cmd.showcursor() # Hide the cursor
cmd.hidecursor() # Show the cursor
cmd.startcursorblinking() # Start the cursor blinking mode
cmd.stopcursorblinking() # Stop the cursor blinking mode
cmd.createscreenbuffer() # Create a new screen
cmd.switchtomainscreenbuffer() # Switch to the main screen
```

## Supported

| Platform         | Colors            | Terminal Tools    |
| ---------------- | ----------------- | ----------------- | 
| Windows		   | Yes		       | Yes               |
| Linux			   | Yes			   | No                |

## Builtin styles

| Foreground       | ...               |
| ---------------- | ----------------- |
| BLACK      	   | BLACK_BRIGHT      |
| RED      		   | RED_BRIGHT        |
| GREEN 		   | GREEN_BRIGHT      |
| YELLOW		   | YELLOW_BRIGHT     |
| BLUE			   | BLUE_BRIGHT       |
| MAGENTA		   | MAGENTA_BRIGHT    |
| CYAN			   | CYAN_BRIGHT       |
| WHITE		   	   | WHITE_BRIGHT      |


| Background       | ...               |
| ---------------- | ----------------- |
| BG_BLACK         | BG_BLACK_BRIGHT   |
| BG_RED           | BG_RED_BRIGHT     |
| BG_GREEN         | BG_GREEN_BRIGHT   |
| BG_YELLOW        | BG_YELLOW_BRIGHT  |
| BG_BLUE          | BG_BLUE_BRIGHT    |
| BG_MAGENTA       | BG_MAGENTA_BRIGHT |
| BG_CYAN          | BG_CYAN_BRIGHT    |
| BG_WHITE         | BG_WHITE_BRIGHT   |


| Font Style       |
| ---------------- |
| BOLD		       |
| UNDERLINE        |
| REVERSED         |


| Output Params    |
| ---------------- |
| RESET            |
