# Criminal-Records-using-Blockchain
Hello, here is detailed about this project:
**Preresquites**
1. Python (I use 3.11)
2. Flask
3. Python web3
4. Ganache
5. Node.js
6. npm
Step by step:
1. Clone this repository
2. Make virtual environment (venv) on the repository folder. Use python -m venv [name_venv]
3. Activate the venv with /path_to_venv/Scripts/activate
4. Now install Flask and web3 on the venv with CLI: pip install Flask web3
5. Then install truffle and ganache-cli (if u don't want to use Ganache GUI). Use CLI: npm install -g truffle ganache-cli
6. Then run truffle init
7. After that, compile the project using truffle compile.
8. Then, migrate the data to the ganache (testnet) using truffle migrate **or** truffle migrate --network development
9. After that, run the dummy_data.py to add dummy data to the system, change directory to the src (except u already changed it)
10. After you see the confirmation on output log, run the py app.py, still in src path. Make sure the venv is still active.

Here is my screenshot:
