# Hashtags Extract
Hashtags extract from string

## Installation

```
pip install Hashtags-Extract
```

## Usage

```py
import hashtags_extract

string = "Hello, #SupportOpensource"

# with #
print(hashtags_extract.hashtags(string))
# => ["#SupportOpensource"]

# without #
print(hashtags_extract.hashtags(string, hash=False))
# => ["SupportOpensource"]

# for total hashtags
print(len(hashtags_extract.hashtags(string)))
# => 1
```
