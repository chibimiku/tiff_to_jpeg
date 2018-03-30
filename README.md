# tiff_to_jpeg
a simple tool to try best quality in converting tiff to jpg

you can also try magick to slove that problem.

cli is : magick convert *.tif -define jpeg:extent=300kb -set filename:f %t %[filename:f].jpg
