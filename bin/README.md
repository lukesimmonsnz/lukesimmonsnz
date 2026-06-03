# bin/

Process control scripts. Each `cd /d "%~dp0\.."` first so they always
operate against the repo root regardless of where they're invoked from.

| Script | Purpose | Logs | PID |
|---|---|---|---|
| `start.bat` | Launch Flask on `:5000` (no reloader, hidden window) | `logs/server.log`, `logs/server.err` | `instance/.server.pid` |
| `stop.bat`  | Stop Flask via PID, falling back to port-5000 sweep | — | clears `instance/.server.pid` |
| `start-ml.bat` | Launch ML daemon on `:5001` via `.venv-ml` | `logs/ml-daemon.log`, `logs/ml-daemon.err` | `instance/.ml-daemon.pid` |
| `stop-ml.bat`  | Stop ML daemon | — | clears `instance/.ml-daemon.pid` |
