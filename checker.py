import json
import re
import socket
import time
from urllib.parse import unquote, urlparse


def get_tcp_ping(host, port, timeout=2):
  start = time.time()
  try:
    # حل دامنه به IP
    ip = socket.gethostbyname(host)
    sock = socket.create_connection((ip, int(port)), timeout=timeout)
    sock.close()
    return int((time.time() - start) * 1000)
  except Exception:
    return None


def parse_config(config_str):
  try:
    config_str = config_str.strip()
    if not config_str:
      return None, None

    if config_str.startswith(('vless://', 'trojan://')):
      # استخراج هاسـت و پورت
      parts = config_str.split('@')
      if len(parts) > 1:
        host_port = parts[1].split('?')[0].split('#')[0]
        host, port = host_port.split(':')
        return host.strip(), int(port)
  except Exception:
    pass
  return None, None


def main():
  try:
    with open('ghost.txt', 'r', encoding='utf-8') as f:
      lines = f.readlines()
  except FileNotFoundError:
    print('ghost.txt not found!')
    return

  results = []
  for line in lines:
    config = line.strip()
    host, port = parse_config(config)

    if host and port:
      ping = get_tcp_ping(host, port)
      if ping is not None and ping < 2500:
        results.append({
            'config': config,
            'host': host,
            'ping': ping,
            'isTimeout': False,
        })

  # مرتب‌سازی بر اساس کمترین پینگ
  results.sort(key=lambda x: x['ping'])

  with open('configs.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
  main()