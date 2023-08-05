# Fugapedia API
Documentation: https://fugapedia.xyz/api.php

## Examples
Getting an article

```python
from fugapedia import Fugapedia, OutputType

# Connecting to the API using your own key
# key - your key
# ver - app version (default: 1)
fp = Fugapedia(key="your_key")

# Getting the article "Kirill Baranov"
# article (required) - the title of the article (spaces in the title of the article must be filled in with "_", for example: "Kirill_Baranov")
# output_type (optional) - output type
# limit (optional) - symbol limit
result = fp.get_article(article="Kirill_Baranov", output_type=OutputType.TEXT, limit=100)
```
