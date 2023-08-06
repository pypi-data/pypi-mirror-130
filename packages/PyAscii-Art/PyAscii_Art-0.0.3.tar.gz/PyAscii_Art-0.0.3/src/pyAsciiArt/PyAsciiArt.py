from PIL import Image


class AsciiArt:
    simple_char_set = "@%#*+=-:. "

    image = Image.Image
    ascii_chars_black_to_white = r'$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^' + r"`'. "
    ascii_color_table = {}
    pixels = []
    scaled_pixels = []
    spacerX = 2
    spacerY = 0

    ascii_image = ""

    def __init__(self, path, white_on_black=False, divider=2.0, ascii_chars_black_to_white="", spacerX=2, spacerY=0):
        img = Image.open(path)
        img = img.resize((round(img.width / divider), round(img.height / divider)))
        img = img.convert("L")

        self.image = img
        self.spacerX = spacerX
        self.spacerY = spacerY

        if ascii_chars_black_to_white != "":
            self.ascii_chars_black_to_white = ascii_chars_black_to_white

        self.generateColorTable(self.ascii_chars_black_to_white, white_on_black)

    def generateColorTable(self, ascii_chars_black_to_white, white_on_black):
        for i in range(len(ascii_chars_black_to_white)):
            color_value = i
            if white_on_black:
                color_value = len(ascii_chars_black_to_white) - i - 1
            self.ascii_color_table.update({color_value: ascii_chars_black_to_white[i]})

    def showImage(self):
        self.image.show()

    def generatePixelArray(self):
        self.pixels = []
        for height in range(self.image.height):
            row = []
            for width in range(self.image.width):
                row.append(self.image.getpixel((width, height)))
            self.pixels.append(row)

    def printPixelArray(self):
        for row in self.pixels:
            print(row)

    def trimPixelColors(self):
        scaled_pixels = []

        for row in self.pixels:
            scaled_pixel_row = []
            for value in row:
                scaled_value = round((value / 255) * (len(self.ascii_color_table) - 1))
                scaled_pixel_row.append(scaled_value)
            scaled_pixels.append(scaled_pixel_row)

        self.scaled_pixels = scaled_pixels

    def generateAsciiImage(self):
        rows = []
        for i in range(len(self.scaled_pixels)):
            spaces = self.spacerX

            ascii_row = ""
            for j in range(len(self.scaled_pixels[i])):
                row = self.scaled_pixels[i]
                filler_pos = round((row[(j - 1) % len(row)] + row[(j + 1) % len(row)]) / 2)
                filler = self.ascii_color_table.get(filler_pos)

                if row[j] > len(self.ascii_color_table) - 1 or row[j] < 0:
                    print("Error")
                ascii_row += self.ascii_color_table.get(row[j]) + (filler * spaces)

            rows.append(ascii_row)

        for i in range(len(rows)):
            self.ascii_image += rows[i] + "\n"
            for j in range(self.spacerY):
                self.ascii_image += self.getSpacerRow(rows[(i - 1) % len(rows)], rows[(i + 1) % len(rows)]) + "\n"

    def getSpacerRow(self, row_before, row_after):
        if len(row_before) != len(row_after):
            return ""

        row = ""
        for i in range(len(row_before)):
            rB_value = self.get_key(row_before[i])
            rA_value = self.get_key(row_after[i])
            row += self.ascii_color_table.get(round((rB_value + rA_value) / 2))

        return row

    def get_key(self, val):
        for key, value in self.ascii_color_table.items():
            if val == value:
                return key

        return 0

    def writeToFile(self, path):
        file = open(path, "w")
        file.flush()
        file.write(self.ascii_image)
