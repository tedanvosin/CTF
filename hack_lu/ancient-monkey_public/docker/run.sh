#!/bin/sh

exec socat -d tcp-listen:1337,fork,reuseaddr EXEC:'./chal.sh',su=nobody,stderr
