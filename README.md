-- Start venv:
	- AT-Bus/server_py$ source .venv/bin/activate


-- Start Backend:
	- AT-Bus/server_py$ uvicorn main:app

-- Update DB:
	- AT-Bus/server_py$ python update/updater_static.py

-- Start Frontend
	- AT-Bus/client$ npm start