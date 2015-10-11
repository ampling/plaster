# plaster
Plaster is an adaptable command-line paste-bin client.



```
pip install python-magic
pip install pyperclip
```


```
git clone https://github.com/ampling/plaster.git

```
### Linux

```
mkdir -p ~/.config/plaster
ln -sr ./plaster/plaster/config ~/.config/plaster/
ln -sr ./plaster/plaster/plugins ~/.config/plaster/
sudo ln -sr ./plaster/plaster/plaster.py /usr/local/bin/plaster
```
Note: pyperclip for linux will require xclip or xsel.
