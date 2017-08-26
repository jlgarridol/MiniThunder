# MiniThunder

## Minimize project to production, saving space (Not reversible)

### Python version
It supports html/css/js files
#### Requires
* [jsmin](https://github.com/tikitu/jsmin/) - MIT
* [rcssmin](http://opensource.perlig.de/rcssmin) - APACHE 2.0

#### Use
```
python minithunder.py Folder/proyect Folder/minified
```
---
### Bash version
It supports html/xml,js,css,png and jpg files
#### Requires
* [html-minifier](https://www.npmjs.com/package/html-minifier)
* [clean-css-cli](https://www.npmjs.com/package/clean-css)
* [uglify-js](https://www.npmjs.com/package/uglify-js)
* [optipng](http://optipng.sourceforge.net/) - ZLIB LICENSE (OPEN SOURCE)
* [jpegoptim](http://freecode.com/projects/jpegoptim) - GPL

#### Use
```
bash minithunder.sh Folder/proyect
```

#### Install dependencies in Debian and derivates (All as root)

```
# apt install optipng jpegoptim uglifyjs cleancss npm
# npm install html-minifier -g
```

#### Install dependencies in Archlinux (All as root)
```
# pacman -S optipng jpegoptim npm
# npm install html-minifier clean-css-cli uglify-js -g