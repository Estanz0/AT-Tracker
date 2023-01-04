-- Start venv:
	- AT-Bus$ source server_py/.venv/bin/activate

-- Start Backend:
	- AT-Bus$ uvicorn --app-dir=server_py main:app

-- Update DB:
	- AT-Bus/server_py$ python update/updater_static.py
	- AT-Bus/server_py$ python update/updater_realtime.py

-- Start Frontend
	- AT-Bus/client$ npm start