## Automatic crop and resizer tool with stiching abilities

#### This tool is designed to take a folder containing different images, cropping them to the same aspect ration then resizing them to the same size squares

Limitations:
* Will only work with .jpg and .png without some editing
* Will only make squares of a resolution divisible by 100X100 pixels at the moment.
* Doesn't currently have the ability to specify any details regarding the images.


#### There is additional capabilitied to then stitch all the images together into a larger square image 

* The amount of pictures must have a whole real number as it's square root, otherwise the large image wont be created properly.

* The image will be saved as a higher quality .jpeg file.

// TODO:

* Implement more options for user input and customizability.

* Add better error handeling and features.

* Allow for different patterns to be stiched together, allowing for different image sizes and styles.

* Give the ability to overlay a single large image over the top of the smaller ones, creating a large image out of smaller images.
