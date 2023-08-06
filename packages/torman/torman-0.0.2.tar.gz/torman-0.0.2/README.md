
# What
This script allows you to initialize multiple TOR instances and proxy to them using an API.

The script automatically refreshes TOR IP's after a number of calls through each TOR Socket.

# Running

To get started with Torman:

- Install with pip: ```$ pip install torman``` 
- Then Start: ```$ torman```

You should see the following output.

```text
,---------.    ,-----.    .-------.    ,---.    ,---.   ____    ,---.   .--. 
\          \ .'  .-,  '.  |  _ _   \   |    \  /    | .'  __ `. |    \  |  | 
 `--.  ,---'/ ,-.|  \ _ \ | ( ' )  |   |  ,  \/  ,  |/   '  \  \|  ,  \ |  | 
    |   \  ;  \  '_ /  | :|(_ o _) /   |  |\_   /|  ||___|  /  ||  |\_ \|  | 
    :_ _:  |  _`,/ \ _/  || (_,_).' __ |  _( )_/ |  |   _.-`   ||  _( )_\  | 
    (_I_)  : (  '\_/ \   ;|  |\ \  |  || (_ o _) |  |.'   _    || (_ o _)  | 
   (_(=)_)  \ `"/  \  ) / |  | \ `'   /|  (_,_)  |  ||  _( )_  ||  (_,_)\  | 
    (_I_)    '. \_/``".'  |  |  \    / |  |      |  |\ (_ o _) /|  |    |  | 
    '---'      '-----'    ''-'   `'-'  '--'      '--' '.(_,_).' '--'    '--' 
    ┌                                   ┐
    │  Manage TOR Proxies like a Boss!  │
    └                                   ┘

2021-12-11 21:13:48 mugendis-beast Torman[53081] INFO Started 4 TOR instances.
2021-12-11 21:13:48 mugendis-beast waitress[53081] INFO Serving on http://0.0.0.0:6930
30

```

This confirms that Torman is ready and runnibng on the *default port* **6930**. Torman is now ready to start taking your requests and you can run the following CURL command.


```sh
curl --request GET \
  --url http://127.0.0.1:6930/ \
  --header 'Content-Type: application/json' \
  --data '{"url" : "https://ipinfo.tw/ip"}'
```

This should return a response showing your current TOR IP address.

```json
{
  "meta": {
    "proxy": "socks5://127.0.0.1:9080",
    "took": "773ms"
  },
  "response": "185.220.101.44"
}
```
This shows the proxy port used, the response as well as how long it took to get the response. Repeat the CURL command and note that the TOR proxies keep getting rotated with each proxy call.

# API
You can pass arguments to fine tune how torman works.

```torman --help``` will show you all the available commands.

- **--refresh-after** Number of requests after which the TOR IP gets refreshed. You must provide a control passwoerd for this to work. Defaults to 50 requests.
- **--control-pass** Your TOR control password. Used to renew TOR IPs when **refresh-after** value has been reached.
- **--server** The port through which Torman listens for REST API requests. Default is 6930
- **--instances** Number of TOR instances to initiate. Default is 4. Torman will allocate requests to these instances randomly.
- **--stop** Stop Torman and all TOR instances.
- **--verbose** Show/Log API requests

## Examples

1. ```torman --verbose```
2. ```torman --refresh-after 10 --control-pass my_pass``` refresh after 10 TOR requests wusing "my_pass" as the control password


# Beware!
1. Stopping Torman using the **--stop** argument stops all running TOR and Torman instances. This includes any TOR processes not initiated by Torman. You might need to manually restart them if any. 





