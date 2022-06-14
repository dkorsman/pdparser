#!/bin/bash

echo 'Creating folders and cloning projects.'
echo 'This will take a while, and a few gigabytes of disk space...'
echo

mkdir ../TEST-PDPARSER
mkdir ../RES-TEST-PDPARSER

cp -r test/ ../TEST-PDPARSER/

cd ../TEST-PDPARSER

git clone https://github.com/aseprite/aseprite -n && git -C aseprite/ checkout -q 7cc9ea08ba4515dbc7d47ec25f24c0d4a272358c
git clone https://github.com/sobotka/blender -n && git -C blender/ checkout -q 2055ef107a7cb4e5aeeffb5ccc8a2908a59cd7d0
git clone https://git.busybox.net/busybox/ -n && git -C busybox/ checkout -q 836b79211df3aeaba1b8b65c6db5ee6193172cc0
git clone https://github.com/electron/electron -n && git -C electron/ checkout -q 5592652504e9e46e84aa85c3bb0404211cc9e581
git clone https://github.com/emacs-mirror/emacs -n && git -C emacs/ checkout -q 8785d70601c5ef02f20604dc3cd85d6c73d7aef7
git clone https://gitlab.gnome.org/GNOME/gimp -n && git -C gimp/ checkout -q dbed5477c4f0ca6444c5025abfb88c8d1e9b6ddd
git clone https://gitlab.gnome.org/GNOME/gnumeric -n && git -C gnumeric/ checkout -q abfa0655a02fac63e09721f1985598040a4c911b
git clone https://github.com/gnuplot/gnuplot -n && git -C gnuplot/ checkout -q 85e18e837fba2a7f414ecd3d39bac8f2ce056025
git clone https://github.com/apache/httpd -n && git -C httpd/ checkout -q 045f98d8d2df10c43ba52ebafc4f26b9d8c52f67
git clone https://github.com/irssi/irssi -n && git -C irssi/ checkout -q e31d42b381dd38f41d132ce1455a8cedb089b78a
git clone https://gitlab.gnome.org/GNOME/libxml2 -n && git -C libxml2/ checkout -q dea91c97debeac7c1aaf9c19f79029809e23a353
git clone https://git.lighttpd.net/lighttpd/lighttpd1.4.git/ -n && git -C lighttpd/ checkout -q a067d99fa0e94e348b9173bce6dd6ba2c2c7c925
git clone https://github.com/torvalds/linux -n && git -C linux/ checkout -q 1fc596a56b334f4d593a2b49e5ff55af6aaa0816
git clone https://github.com/ARMmbed/mbedtls -n && git -C mbedtls/ checkout -q 2bb5e9c973cf7a37eacb50a65537c921b60f2fac
git clone https://github.com/robol/MPSolve -n && git -C MPSolve/ checkout -q 2545de499edb272dbe7c4b03861d13e022d8b5d2
git clone https://github.com/netdata/netdata -n && git -C netdata/ checkout -q 882bc018f3f128a3f825ce537e00952f84e013e6
git clone https://github.com/nginx/nginx -n && git -C nginx/ checkout -q 3253b346fb8b067d68a79ae72e08a376f234b0b3
git clone https://github.com/opencv/opencv -n && git -C opencv/ checkout -q 244ba1a61a8a514dbd6014766dc17dfde4560487
git clone https://github.com/openssl/openssl -n && git -C openssl/ checkout -q 73970cb91fdf8e7b4b434d479b875a47a0aa0dbc
git clone https://github.com/OpenVPN/openvpn -n && git -C openvpn/ checkout -q dd73b620f2bbb4ad9d3b9d43e5124911e48256f1
git clone https://github.com/parrot/parrot -n && git -C parrot/ checkout -q f89a111c06ad0367817c52fda6ff5c24165c005b
git clone https://github.com/microsoft/PowerToys -n && git -C PowerToys/ checkout -q 6269aa63980c43ea47fe18965c64ef00a53f5ebc
git clone https://github.com/protocolbuffers/protobuf -n && git -C protobuf/ checkout -q 65852d6e9cdb3d6e1120ef6af044968cbbaff733
git clone https://github.com/pytorch/pytorch -n && git -C pytorch/ checkout -q 1ec732bc46c448dc922f5ccde506100cbb9506f1
git clone https://github.com/redis/redis -n && git -C redis/ checkout -q 24b67d5520ca062d2c0ed432112fd3c26ceb3daa
git clone https://github.com/sqlite/sqlite -n && git -C sqlite/ checkout -q 16a8f28e492507523c6b0b9d0bc0d9fd43c253a7
git clone https://github.com/apple/swift -n && git -C swift/ checkout -q 78cb09435ceab7c78210338b0d6592794558e468
git clone https://github.com/tensorflow/tensorflow -n && git -C tensorflow/ checkout -q a91435160c8b4f4cc8f417ec85874133a7af7574
git clone https://github.com/microsoft/terminal -n && git -C terminal/ checkout -q 02ac246807993e57dd5b6061bee1385f186ae20d
git clone https://gogs.waldemar-brodkorb.de/oss/uclibc-ng -n && git -C uclibc-ng/ checkout -q 98680eec548b921abecc641b70246587ffbbdc0a
git clone https://github.com/vim/vim -n && git -C vim/ checkout -q accf4ed352c07ffe59022377c42d36e12dd6d461
git clone https://github.com/terrycavanagh/VVVVVV -n && git -C VVVVVV/ checkout -q 449526bb4f54cd6d14df0d0cae0b728fabd8bf0c 

echo 'Please also download axTLS from https://sourceforge.net/projects/axtls/files/2.1.5/ and extract it in a folder in TEST-PDPARSER/'
