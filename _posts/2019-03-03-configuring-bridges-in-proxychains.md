---
title: Configuring bridges in proxychains
comments: true
layout: post
date: '2019-03-03 21:30:00'
author: furkan önder
categories:
- tor
- proxychains
tags:
- proxychains and bridges
description: Configuring bridges in proxychains
---

We are using sqlmap, nmap, nikto tools  etc. while dealing with cyber security. Sometimes we need to be anonymous when using these tools for testing. We are able to use proxychains for this.But...

<a href="/assets/images/proxychains_1.png" imageanchor="1">
  <img style="display: block;margin: 0 auto;width: 43em;" src="/assets/images/proxychains_1.png"/>
</a>

Damn it! Most likely tor is banned in your country so this method doesn’t work. Let's fix this problem.Solution to use the bridge.

We need to make some changes to the <b>/etc/proxychains.conf</b> file for add bridge.

You will see 3 different chain configuration in the file.

* dynamic_chain
* strict_chain 
* random_chain 

We will use dynamic_chain. Remove the # in front of the dynamic_chain and add the # in front of the strict_chain and random_chain.

Now, we need to make some changes to <b>/etc/tor/torrc</b>. At the bottom of the file we are writing these lines.

```
UseBridges 1
ClientTransportPlugin obfs4 exec /usr/bin/obfs4proxy managed
Bridge obfs4 "bridge info"
Bridge obfs4 "bridge info”
Bridge obfs4 "bridge info"
```

Paste the bridge  get from https://bridges.torproject.org/ to the section "bridge info".
It look like this:

<a href="/assets/images/proxychains_2.png" imageanchor="1">
  <img style="display: block;margin: 0 auto; width: 50em;" src="/assets/images/proxychains_2.png"/>
</a>

Now we need to set up a few programs. These are obfs4proxy and tor. After installing the programs, restart the tor service.

```
systemctl restart tor
```

Let's try it again.

<a href="/assets/images/proxychains_3.png" imageanchor="1">
  <img style="display: block;margin: 0 auto;width: 43em;" src="/assets/images/proxychains_3.png"/>
</a>

That's it! There are tor exit nodes at <a href="https://www.dan.me.uk/torlist/">https://www.dan.me.uk/torlist/</a>.
You can be sure that your ip address is using tor by looking at list.

# References
* https://github.com/haad/proxychains
* https://github.com/Yawning/obfs4