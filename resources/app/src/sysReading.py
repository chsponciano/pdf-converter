from Reading import Reading

import sys
sys.stdout.reconfigure(encoding='utf-8')

status = sys.argv[1]
path   = sys.argv[2]

try:
    read = Reading()
    out = read.select_file(path) if status == '1' else read.convert(path)
    print(out)
except (Exception) as e:
    print(f"Erro ao executar, favor tentar novamente mais tarde! - Erro: {e}")

sys.stdout.flush()