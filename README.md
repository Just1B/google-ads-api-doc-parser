# Google Ads Api Doc Parser

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

Parse the Google Ads api documentation and :

- export fields in a text file for the API Query
- export a big query json schema

## Requirements

<br>

    pip3 install -r requirements.txt

## Run

    python3 main.py -r REPORT_NAME

## Example : ad_group_criterion

![index](https://github.com/Just1B/google-ads-api-doc-parser/raw/master/images/example.png)

    python3 main.py -r ad_group_criterion

![index](https://github.com/Just1B/google-ads-api-doc-parser/raw/master/images/outputs.png)

# Licence

The MIT License

Copyright (c) 2021 JUST1B

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
