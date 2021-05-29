# DarkMatter-Python: Riddhiman Roy's branch

## Convention to enable single line imports ##
To import src into files within src or outside of it, place the following line on top:

```
import src as rocket
```
Then, whenever calling from src or any existing class, use the following:

```
rocket.<insert classname>()
```

When developing new files, make sure to import src as well. After the new file is complete or at a point where it can be imported, add the following type of line to src/__init__.py:
```
from <filename> import *
```

## Pushing to this repo ##

If you're working on this repo, push to a branch with your name. In time, changes will be merged with main.


Happy coding!

