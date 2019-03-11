# rm-exif
Remove exif data and transform them so that they display the same everywhere


## A command line utility to remove exif data from an image and transform it so that it doesn't appear rotated everywhere.

### requirements
```
pip install Pillow
```

### usage
``` 
rm-exif -s ./file.jpg -d ./out.jpg
```
or
```
rm-exif -s ./in-directory/* -d ./out-directory/*
```
