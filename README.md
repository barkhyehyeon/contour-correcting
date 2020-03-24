# contour-correcting

This is an algorithm to correct the contour of a circular object in an image.
<br>
1. Small blobs are cleaned except the one biggest object in the image, then the object is converted to its convex hull
2. The longest axis of the object(with center of the mass as a center point) is obtained.
3. The axis is rotated by 45 degrees to find an intersecting point on the edge of the object.
By repeating this process, eight representative dots are fitted on the edge.
4. Then, the dots are interpolated to create a connected circular object with a smooth contour.

* This algorithm is tested on more than 1800 IVUS masks predicted by a deep learning model, and was found to enhance the shape of the object while preserving the accuracy(dice coefficient) of the prediction.
* You can adjust the amount of degrees to rotate at a time(i.e. the number of dots extracted from the edge) as you want.
* You can check the example run of this algorithm in main.ipynb file. The example image is self created using paint app.
