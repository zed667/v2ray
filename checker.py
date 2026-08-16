import json
import re
import socket
import time


def get_tcp_ping(host, port, timeout=2):
  start = time.time()
  try:
    sock = socket.create_connection((host, int(port)), timeout=timeout)
    sock.close()
    return int((time.time() - start) * 1000)
  except Exception:
    return None


def extract_host_port(config):
  # استخراج هاسـت و پورت از لینک‌های vless / trojan / vmess
  match = re.search(r'@([^:]+):(\d+)', config)
  if match:
    return match.group(1), match.group(2)
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
    if not config:
      continue

    host, port = extract_host_port(config)
    if host and port:
      ping = get_tcp_ping(host, port)
      if ping is not None:
        results.append({
            'config': config,
            'host': host,
            'ping': ping,
            'isTimeout': False,
        })

  # مرتب‌سازی بر اساس بهترین پینگ
  results.sort(key=lambda x: x['ping'])

  with open('configs.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
  main()