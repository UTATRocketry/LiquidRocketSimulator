# DarkMatter-Python: Riddhiman Roy's branch

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

Happy coding!

