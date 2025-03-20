function FindProxyForURL(url, host) {
  if (host == "flu.xxx") {
    return "DIRECT";
  }
  return "PROXY 127.0.0.1:8080";
}
