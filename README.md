# paline
This code uses cv2 to read raw rgb images and it executes all of its actions by doing so
The image callback contains all of the functionality of this program, it cycles through constantly
the pid updates the angular velocities and reads a slice of the masked image. Images hold their data in 
a list of lists, each row is the length of one list inside the main list and the height is the number of lists inside of the list
I use a for loop to turn all of the values except for a selected strip to 0
