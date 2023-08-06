# Image to Ascii-Art

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)                 
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)   

## Usage

- Make sure you have Python installed in your system.
- Run Following command in the CMD.
 ```
  pip install PyAscii-Art
  ```

## Example
```
  from PyAsciiArt import AsciiArt
  
  # Path to the image
  image_path = r"image.jpg"
  
  # Create new Ascii-Art
  ascii_art = AsciiArt(image_path)

  ascii_art.generatePixelArray()     # Generate the pixel-array of the image
  ascii_art.trimPixelColors()        # Set the pixel brightness value to match the char list
  ascii_art.generateAsciiImage()     # Generate the image
  ascii_art.writeToFile("image.txt") # Write the image to the image.txt file
  ```