note: ripping is bad, don't do it
# WNovelArchiver
A simple python script to easily download and keep up to date raw web-novels on syosetu and kakuyomu  
If you have another WN site (JP/CN/KR/...) which you would like to be usable, feel free to put an issue.  
If your connection isn't stable, the script may (will) crash while downloading.
### Features:
* batch download (1 to max) from the input.txt
* update chapters of all the novels in the /novel_list/ directory
* generate a status file recording for every novel the last chapter ddl-ed
* compressing each novel in a zip of its own (not accessible by commands atm)

### Sites featured:
* Syosetu ncode and novel18
* Kakuyomu
* Wuxiaworld.com


## How to use

Clone or download the repo  <br>
<code>cd WNovelArchiver</code><br>
<code>python archive_updater.py</code><br>
(you might be aksed to download some packages)<br>

## Instructions
##### more details in https://github.com/safirex/WNovelArchiver/wiki
The input.txt is used to give the script the entries to download.  
It should be written in csv style (code;novelname):  
The novel name can be let empty, in this case the script will fetch the novel name from the site  
![r](https://image.prntscr.com/image/8AY0wQWOQfqTNRfqg9Lejg.png)  
With n5947eg being the code of the novel accessed by https://ncode.syosetu.com/n5947eg/

codes:
* syosetsu    : code of the novel
* syosetsu 18+: <code>n18</code>code of the novel
* kakyomu     : code of the novel
* wuxiaworld  : Name-Of-The-Novel
