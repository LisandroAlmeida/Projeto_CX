import os
import subprocess
from flask import Flask

app = Flask(__name__)

@app.route('/')
def run_streamlit():
    # Comando para rodar o Streamlit
    cmd = "streamlit run rox_app.py --server.port=8080 --server.headless=true"
    process = subprocess.Popen(cmd, shell=True)
    return "Streamlit app is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
