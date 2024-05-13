# nicehash-on-linux
Simple python script to mine using GPU(miniZ)/CPU(xmrig) on linux (nicehash), now with fan speed control.

Tested on arch linux. Install curl and p7zip on your system manually if it is not arch.

Edit config.ini after first start to change options.

To allow Gpu Fan Control set coolbits to 31

sudo nvidia-xconfig -a --cool-bits=31 --allow-empty-initial-configuration


# roadmap
add multi gpu support for fan control

add locking clock, undervolt, pl limits

~~add different algos~~ Added in 1.2

~~add support for other distros~~ Kinda added in 1.2
