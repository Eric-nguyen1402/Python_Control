# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import pymysql
import os

time.sleep(3)

class Neo_pixel:
    def __init__(self):

        # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
        # NeoPixels must be connected to D10, D12, D18 or D21 to work.
        self.pixel_pin = board.D18
        # The number of pixels
        self.num_pixels = 8
        self.brightness = 0.2
        self.auto_write = False
        # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
        # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
        ORDER = neopixel.GRB
        self.pixel_order = ORDER
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness = self.brightness, auto_write = self.auto_write, pixel_order = self.pixel_order)

    def wheel(self, val):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if val < 0 or val > 255:
            r = g = b = 0
        elif val < 85:
            r = int(val * 3)
            g = int(255 - val * 3)
            b = 0
        elif val < 170:
            val -= 85
            r = int(255 - val * 3)
            g = 0
            b = int(val * 3)
        else:
            val -= 170
            r = 0
            g = int(val * 3)
            b = int(255 - val * 3)
        return (r, g, b) if self.pixel_order in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.num_pixels):
                pixel_index = (i * 256 // self.num_pixels) + j
                self.pixels[i] = self.wheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(wait)


    def action(self):
        try:
        # queries for retrievint all rows
            self.connection = pymysql.connect(
                host="localhost", user="root", passwd="raspberry", database="tanker")
            self.cursor = self.connection.cursor()
            retrive = "Select * from move_control;"
            # executing the quires
            self.cursor.execute(retrive)
            rows = self.cursor.fetchall()
            
            if rows[0][10] != 0:
                self.pixels.fill((255, 255, 255))
                # Uncomment this line if you have RGBW/GRBW NeoPixels
                # pixels.fill((255, 0, 0, 0))
                self.pixels.show()
            else:
                # Comment this line out if you have RGBW/GRBW NeoPixels
                self.pixels.fill((255, 0, 0))
                # Uncomment this line if you have RGBW/GRBW NeoPixels
                # pixels.fill((255, 0, 0, 0))
                self.pixels.show()
                time.sleep(1)

                # Comment this line out if you have RGBW/GRBW NeoPixels
                self.pixels.fill((0, 255, 0))
                # Uncomment this line if you have RGBW/GRBW NeoPixels
                # pixels.fill((0, 255, 0, 0))
                self.pixels.show()
                time.sleep(1)

                # Comment this line out if you have RGBW/GRBW NeoPixels
                self.pixels.fill((0, 0, 255))
                # Uncomment this line if you have RGBW/GRBW NeoPixels
                # pixels.fill((0, 0, 255, 0))
                self.pixels.show()
                time.sleep(1)

                self.rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step
        except KeyError:
            print("Something went wrong")


def main():
    Led_pixel = Neo_pixel()
    while True:
        Led_pixel.action()    
        
if __name__ == '__main__':
    main()