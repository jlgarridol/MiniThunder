#!/bin/bash
## Mini thunder (Bash edition)
version="0.9"
## It minifies a folder of files preparing it for production using less space
## It supports html/xml,css,js,jpg and png files.

# First, see if user has all the deps installed (Only check one time, $2 knows that)
if [[ -z $2 ]];then
	which html-minifier > /dev/null 2> /dev/null
	if [[ $? -ne 0 ]];then
		echo "Error. html-minifier not installed."
		echo "You can install it using npm if you have it 'sudo npm install html-minifier -g' or using your distro package manager"
		notdeps=1
	fi
	which cleancss > /dev/null 2> /dev/null
	if [[ $? -ne 0 ]];then
		echo "Error. cleancss not installed."
		echo "You can install it using npm if you have it 'sudo npm install clean-css-cli -g' or using your distro package manager using clean-css"
		notdeps=1
	fi
	which uglifyjs > /dev/null 2> /dev/null
	if [[ $? -ne 0 ]];then
		echo "Error. uglifyjs not installed."
		echo "You can install it using npm if you have it 'sudo npm install uglify-js -g' or using your distro package manager"
		notdeps=1
	fi
	which optipng > /dev/null 2> /dev/null
	if [[ $? -ne 0 ]];then
		echo "Error. optipng not installed."
		echo "You can install it using your distro package manager"
		notdeps=1
	fi
	which jpegoptim > /dev/null 2> /dev/null
	if [[ $? -ne 0 ]];then
		echo "Error. jpegoptim not installed."
		echo "You can install it using your distro package manager"
		notdeps=1
	fi
	# If not all deps are satisfied
	if [[ ! -z $notdeps ]];then
		echo "Some dependencies are not installed, if you continue, you will have errors for files that use this programs"
		echo "You can use the final folder anyways, but it may not be fully minified"
		echo "Press any key to continue, CTRL+C to exit"
		read
	fi
fi

# Start

# See it folder especified

if [[ -z "$1" || "$1" = "-h" ]];then
	echo "Minithunder Bash Edition version $version"
	echo "Usage: minithunder pathOfProject"
	echo "It creates a new 'minified' folder with all files minified inside"
    echo "------------------------------------------------------"
    echo "-h:                                          show this help"
    echo "-v:                                          show version"
	exit 1
fi

if [[ "$1" = "-v" ]];then
	echo "Version: $version"
	exit 0
fi

if [[ ! -d "$1" ]];then
	echo "The path specified is not a valid directory, make sure it's there"
	exit 2
fi

# Copy all folder to minimize it, only where are in root ($2 is null), if I'm in a subfolder, make var $folder with path.
if [[ -z "$2" ]];then
	cd "$1"
	origfolder="$(pwd)" # For counting at finish, and knowing absolute root path
	mkdir ../minified
	cp -r "$origfolder" "${origfolder}/../minified"
	cd "${origfolder}/../minified"
	folder="$(pwd)" # Production folder now
else
	folder="$1"
fi

cd "$folder" # Go to folder

# Run at all files searching files to minify
for j in *
do
	if [ -d "$j" ] ; then # Folder encountered
		"$0" "$folder/$j" 1 # Run script ($0) in a subfolder (The '1' is for making program know it's not root folder)
	elif [ -f "$j" ]; then # File encountered
		case ${j: -4} in # (Extension)
		".htm"|"html"|"twig"|".xml")
			html-minifier --minify-css=true --minify-js=true --collapse-whitespace --conservative-collapse --remove-comments "$j" -o "$j"
			echo "File $j minified"
			;;
		".css")
			cleancss "$j" -o "$j"
			echo "File $j minified"
			;;
		*".js")
			uglifyjs "$j" -o "$j"
			echo "File $j minified"
			;;
		".png")
			optipng -quiet -o7 "$j"
			echo "File $j minified"
			;;
		".jpg"|"jpeg")
			jpegoptim -q --strip-all -o "$j"
			echo "File $j minified"
			;;
		*)
			echo "File $j not minified, format not supported";;
		esac
	fi
done

# Summary (Only original program)
if [[ -z "$2" ]];then
	echo "Files minified in $folder"
	echo "Savings"
	echo "Before: $(du -hs --apparent-size "$origfolder" | cut -f1) ($(du -bs "$origfolder" | cut -f1) bytes)"
	echo "After:  $(du -hs --apparent-size "$folder" | cut -f1) ($(du -bs "$folder" | cut -f1) bytes)"
fi