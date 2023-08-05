
# suffuse_log

![Screenshot 2021-07-23 113324](https://user-images.githubusercontent.com/84053244/126813501-a5f428b8-cc96-4c75-9d8b-9735f30f583a.png)

### Overview
suffuse_log is a python library that specializes in ansi-formatting of log messages. It targets 
local scripts that want to output colored logs to a command line terminal. 

**If you are leveraging logging plugins like Splunk, I don't recommend you use this.**

However, If you have CLI's that you want to make more engaging, pretty, or additionally communicate their meaning with color,
then this is the library for you. 

### Install

`pip install suffuse_log`

### Getting Started

```
from suffuse_log import suffuse_formatter

logger = suffuse_formatter.defaultConfig(
    name="my-suffuse-log", log_level_no=10
)

x.info('this is my message')
```


### Features

- Individually color logging attributes!
- Conditionally color multiple logging attributes based on glob patterns or user-defined callables
- Defaults to the popular colorama ansi library
- Allows users to supply their own ansi-style dictionary
