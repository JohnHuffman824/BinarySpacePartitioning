Jack Huffman, Nathaniel Li
Eric Alexander
CS 252 Algorithms
6-5-2023

This library contains out primary code file 'partition.py' and a csv file points.csv which is used to illustrate the algorithm in action. We also include the graphics library graphics.py to help visualize the algorithm. You will need numpy to run to code.

By default, our test code generates a BSP once which renders the doom logo, there are several test data sets which can be uncommented to see simpler test scenarios.

Within the main function there are a couple global variables which are important to understand the code.
    scale_factor - A variable which is used to assist rendering. It increases sizes when displayed so we can define points at a lower scale but have them displayed visibly. It can be increased or decreased to change rendering sizes
    sleep_time - A variable which changes how long the sleep time is between rendering edges. Increase sleep_time to increase duration between edges being rendered
    click_through - A boolean which enables you to click through the rendering rather than having it render at set intervals

Our test files only have one value per line which represents an x or y coordinate. You can think of these as coming in pairs of 4, where the first two lines represent one point and second two lines represent another point. Together these 4 values represent a single edges.
File formatting format:
    x1
    y1
    x2
    y2
Which represents edge from (x1, y1) to (x2, y2)



