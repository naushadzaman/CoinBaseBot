# CoinBaseBot
Buy / Sell on CoinBase for Bitcoin (BTC) / Ethereum (ETH) / Litecoin (LTC) given an expected price 

Algorithmic trading of Crypto currencies - Bitcoin, Ethereum and Litecoin. 


Provided under MIT License by Naushad UzZaman.

Note: The code is released under the MIT License – please take the following message to heart:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


## Create Trade requests 
Trade request will be in trade_queue.txt file. 

```
trade_queue.txt format
currency, action, gte_or_lte, targer, budget

currency = BTC | ETH | LTC
action = BUY | SELL
gte_or_lte = < | > 
target = target price for the currency
budget = how much money to spend

Example:
BTC, BUY, <, 12000, 100
ETC, SELL, >, 600, 50
```

## Create config file 
$ cp sample_config config 

* Enable API Key here: https://coinbase.com/settings/api

* Update API Key and Secret with your API. No quotations on key and secret. 
```
API Key: afkefmwipwiwigjwpig
API Secret: amfemgijrgirgs
```

## Installation 
With virtualenv, additionally do the following:
```
virtualenv venv
source venv/bin/activate
```

Install requirements
```
pip install -r requirements.txt 

```


## Next ToDO
* As soon as send the notification, remove it from trade queue and add it in history file, which is appended. 
* Predict crypto currency price from other ones, e.g. predict Litecoin price from Bitcoin and Litecoin historic + ETH current and historic + gold current and historic
* If the price is in free falling or continuous upwards 
* Get recent transactions to get a sense of what's going on 