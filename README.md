# plaster
Plaster is an adaptable command-line paste-bin client.



install xclip
http://sourceforge.net/projects/xclip/

```
pip install python-magic
pip install pyperclip
```


###Linux

```
git clone https://github.com/ampling/plaster.git
mkdir -p ~/.config/plaster
ln -sr ./plaster/plaster/config ~/.config/plaster/
ln -sr ./plaster/plaster/plugins ~/.config/plaster/
sudo ln -sr ./plaster/plaster/plaster.py /usr/local/bin/plaster
```
