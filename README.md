
### Prerequisities

1. Python 3.4. Go to [Download Python 3.4.7](https://www.python.org/downloads/)

2. `requests` library. Run the following on your terminal:

```
pip3 install requests
```

### Usage

For now, you can get 2 main things out of the python script:

* Distribution of players that are being picked in a GameWeek
* Distribution of players being captained in a GameWeek

`python3 getKoraFPLStat.py --gameweek 2 --type classic` or `python3 getKoraFPLStat.py -g 2 -t classic`

> Please Note:
 **For first time usage, you have to put your password to validate the payload for getting all players' data. Replace the value of `LOGIN_PASSWORD` in getKoraFPLStat.py**
*(It's not harmful, relax)*
