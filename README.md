# pricecheck

Checks TF2 community market items for lowest prices.


Best being run from systemd timer/cron periodically.


Will check item price via json steam api and store lowest price if it encounters price lower than before.


Needs api_key file filled with pushbullet api key.
Needs items.txt with each line being accurate TF2 item name.