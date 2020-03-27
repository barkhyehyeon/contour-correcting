# contour-correcting

This is an algorithm to correct the contour of an object in an image.
<br>
1. Small blobs are removed to leave only the biggest object in the image, then the object is converted to its convex hull.
2. The longest axis of the object(with 'center of the mass' as the center point) is obtained.
3. The axis is rotated by 45 degrees to find an intersecting point on the edge of the object.
By repeating this process, eight dots on the edge are extracted.
4. The dots are interpolated to produce a connected circular object with smooth contour.

* You can change the amount of degrees to rotate at a time(i.e. the number of dots extracted from the edge) to adjust the scale of interpolation.
* The example run of this algorithm is presented in main.ipynb file. The example image is self created using paint app.
