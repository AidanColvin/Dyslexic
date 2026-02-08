import sys; sys.path.append('backend'); from backend.app import app; print('Starting NeuroRead...'); app.run(host='0.0.0.0', port=5000)
