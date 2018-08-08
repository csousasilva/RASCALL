{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf400
{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 \
\
For mac: (install homebrew\
\
brew install python2)\
\
\
pip install virtualenv (install virtualenv)\
\
virtualenv pythonenv (create virtualenv)\
\
. pythonenv/bin/activate (activate virtualenv)\
\
pip install -r requirements.txt (install the requirements for atoms to run)\
\
IT SHOULD RUN BUT MIGHT NOT PLOT (in Macs it should be fine if you used home-brew which already has a matplotlib backend)\
\
Otherwise, install matplotlib backend which is system dependent:\
\
linux/debian -  sudo apt install python-dev python-virtualenv python-tk\
\
}