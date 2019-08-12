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

We are using sqlmap, nmap, nikto tools  etc. while dealing with cyber security. Sometimes we need to be anonymous when using these tools for testing. We are able to use proxychains for this.But.…<br><br>

<a href="/assets/images/proxychains_1.png" imageanchor="1"><img style="display: block;margin: 0 auto;width: 43em;"  src="/assets/images/proxychains_1.png" /></a><br/>

Damn it! Most likely tor is banned in your country so this method doesn’t work. Let's fix this problem.Solution to use the bridge. We need to make some changes to the /etc/proxychains.conf file for add bridge.<br>

You will see 3 different chain configuration in the file.

• dynamic_chain <br>
• strict_chain <br>
• random_chain <br>

We will use dynamic_chain. Remove the # in front of the dynamic_chain and add the # in front of the strict_chain and random_chain.<br>

Now, we need to make some changes to /etc/tor/torrc. At the bottom of the file we are writing these lines.

<pre class="brush:python">
UseBridges 1
ClientTransportPlugin obfs4 exec /usr/bin/obfs4proxy managed
Bridge obfs4 "bridge info"
Bridge obfs4 "bridge info”
Bridge obfs4 "bridge info"
</pre>

Paste the bridge  get from https://bridges.torproject.org/ to the section "bridge info".<br><br>
It look like this:
<a href="/assets/images/proxychains_2.png" imageanchor="1"><img style="display: block;margin: 0 auto; width: 50em;"  src="/assets/images/proxychains_2.png" /></a><br/>

Now we need to set up a few programs. These are obfs4proxy and tor. After installing the programs, restart the tor service.
<pre class="brush:python">
systemctl restart tor
</pre>
Let's try it again.
<br><br>
<a href="/assets/images/proxychains_3.png" imageanchor="1"><img style="display: block;margin: 0 auto;width: 43em;"  src="/assets/images/proxychains_3.png" /></a><br/>
That's it! There are tor exit nodes at <a href="https://www.dan.me.uk/torlist/">https://www.dan.me.uk/torlist/</a>.
You can be sure that your ip address is using tor by looking at list.