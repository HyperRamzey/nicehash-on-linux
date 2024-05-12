# nicehash-on-linux
Simple python script to mine using GPU(gminer/miniZ)/CPU(xmrig) on linux (nicehash), now with fan speed control.

Run as Sudo if you wish to use xmrig`s msr mod and fan control or miniZ overclocking options

Tested on arch linux. Install gminer and xmrig on your system manually if it is not arch.

Edit config.ini after first start to change options.

To allow Gpu Fan Control set coolbits to 31

sudo nvidia-xconfig -a --cool-bits=31 --allow-empty-initial-configuration


# roadmap
add multi gpu support for fan control

add locking clock, undervolt, pl limits

add different algos

add support for other distros
