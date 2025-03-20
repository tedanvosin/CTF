#!/bin/bash

echo -n "URL: "
read -r url
exec timeout 30 ./pactester -p proxy.pac -u "$url"
