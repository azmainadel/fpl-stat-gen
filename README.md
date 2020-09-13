
## Prerequisites

1. Python 3.4. Go to [Download Python 3.4.7](https://www.python.org/downloads/)

2. `requests` and `tqdm` library. Run the following on your preferred terminal:

```
pip3 install requests tqdm
```

3. Set Email, Password and League ID in the **python_script** folder.


## Usage

For now, you can get 2 main things out of the python script:

* Distribution of players that are being picked in a Gameweek
* Distribution of players being captained in a Gameweek



### 1. Get stats for a specific GW

Run:

```python3 python_script/getKoraFPLStat.py --gameweek 2 --type classic``` 

or 

```python3 python_script/getKoraFPLStat.py -g 2 -t classic```

If it does not work use `python` instead of `python3`

### 2. Get all stats for every GW

Add execution permission to the bash scripts:
```chmod +x getAll.sh```

Run the command:

```./getAll.sh```



### 3. Get stats for the latest GW

Add execution permission to the bash scripts:
```chmod +x getLastGW.sh```

Run the command:

```./getLastGW.sh```



> Please Note:
 **For first time usage, you have to put your password to validate the payload for getting all players' data. Replace the value of `LOGIN_PASSWORD` in getKoraFPLStat.py**
*(It's not harmful, relax)*

> The outputs here are for Noibeddo FPL league.

