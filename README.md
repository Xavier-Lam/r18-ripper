# R18-Ripper
[![Donate with Bitcoin](https://en.cryptobadges.io/badge/micro/1BdJG31zinrMFWxRt2utGBU2jdpv8xSgju)](https://en.cryptobadges.io/donate/1BdJG31zinrMFWxRt2utGBU2jdpv8xSgju)

Rips purchased japanese adult video off r18.com.

## Installation
    git clone https://github.com/Xavier-Lam/r18-ripper.git
    cd r18-ripper
    python setup.py install

## Quickstart
You need to capture the m3u8 request to get the url to download.

    r18-ripper <m3u8url> -o file.ts

## Usage
    r18-ripper [-h] [-b BANDWIDTH] -o OUTPUT_FILE [--proxy PROXY] [-r] [-s SLICE] [--trusted-proxy] [-u USER_AGENT] uri

    positional arguments:
    uri                   m3u8 stream address

    optional arguments:
    -h, --help            show this help message and exit
    -b BANDWIDTH, --bandwidth BANDWIDTH
                            choose the bandwidth of the stream
    -o OUTPUT_FILE, --output-file OUTPUT_FILE
    --proxy PROXY         using a proxy to get stream
    -r, --raw             save raw ts files to disk
    -s SLICE, --slice SLICE
    --trusted-proxy       ignore server certification errors when using a proxy
    -u USER_AGENT, --user-agent USER_AGENT
                        customize user-agent string


## TroubleShooting
1. Got response status code 429

    This may caused by requests your stream too frequently, capture another m3u8 url to download may solve the problem. If you got a 503 status code, just visit the m3u8 url directly in your browser to pass the cloudflare's check.

2. Downloaded ts file can't play
    
    Capture a new url and re-rip the stream.

## Known issues
I ripped two videos from r18.com, and when I use ffmpeg to check these videos' errors, it reported many 'Application provided invalid, non monotonically increasing dts to muxer in stream' errors, I don't know why these errors happened and if I should ignore them or not. I watched these video and these video looks fine.
![](https://i.imgur.com/EIaSFht.jpg)
