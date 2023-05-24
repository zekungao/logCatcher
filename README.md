# logCatcher

Used to catch metrics from log/documents without generic format.

For example, if you find a log file which has its own format to report metrics, BUT YOU DO NOT KNOW ITS PROTOCOL!

This repo is just an encapsulation of python regex.
Which make you to specify a format to catch metrics from logs.
And then report your metrics in json

## dependency

python3

## installation and run

NO INSTALLATION!

Just clone it and import the module into you python script

try to run my unittest by

```python
./test.py
```

## guidance

You are able to fimd some example in `test.py` (which is unittest of this repo)

First you are able to create a catcher to handle your task:

```python
from src.catcher import Catcher, Block, Metric

catcher = Catcher() # create a new catcher
```

You have two way to add source for it

```python
catcher.content = "xxx" # specify the contents
catcher.read("file_name") # specify log file path
```

Our target is to report a Json.
So you are able to add `block` to handle a bundle of metric with classify

```python
block = catcher.add("block nam", Block("key feature", 8))
```

"key feature" means the key feature you need to match in this block of log.
Which means you need to find a line that you wanna match.
This line must have this key feature.
The integer after key feature is how many lines you wanna catch after you key feature matched line.
Then you are going to catcher a "block" of log

for example, in `test/PrimeTime.report.example.global.max`
try `Block("Setup violations", 8)`, you are going to get:

```log
Setup violations
------------------------------------------------------------------------
            Total     reg->reg      in->reg     reg->out      in->out
------------------------------------------------------------------------
WNS     -23.19247    -23.19247      0.00000      0.00000      0.00000
TNS  -32613.46737 -32613.46737      0.00000      0.00000      0.00000
NUM          3209         3209            0            0            0
------------------------------------------------------------------------

```

Then add metrics catch in your block.
Here you are able to use `FloatMetric` object to catch int/double without specify regex.

```python
block.add("total", FloatMetric(0))
```

Above code means get the first variable in your block, `-23.19247`
You need to know this catch has not line limit.

Then you are able to transform all data collected by catcher into json:

```python
catcher.to_json()
```

Or directly write it down to a json file

```python
catcher.writer("path.json")
```
