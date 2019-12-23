## Recommended Browser

The recommended browser for Scratch3 OneGPIO extensions is **Google Chrome**.

### If You Wish To Use Firefox
You may use FireFox, but you will need to configure it to do so.

The OneGPIO extensions use a WebSocket connection between the browser
and the WebSocket Gateway that is part of each extension server.

By default, Firefox does not allow connections to a WebSocket server. To
enable Firefox to allow WebSocket connections, open the following URL

``` 
about:config
```

You should see a warning screen similar to that below.

 <img src="../images/ff_warning.png" > </br>

Click on the *I accept the risk!* button.

Scroll down until you find the
*network.websocket.allowInsecureFromHTTPS* entry and double click false
to change its state to true.

Close FireFox and reopen. Scratch 3 OneGPIO should now function
properly.

### Trouble Shooting
If, after loading an extension, it is not behaving as expected, while
the browser is open, press the F12 key on your keyboard to expose the
browser console. If you see any errors reported, and are still not sure
how to solve the issue,
[create an issue against the s3-extend distribution](https://github.com/MrYsLab/s3-extend/issues)
pasting any error output into the issue comment.

<br> <br> <br>


Copyright (C) 2019 Alan Yorinks All Rights Reserved
