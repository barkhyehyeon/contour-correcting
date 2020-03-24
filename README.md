# contour-smoothing

This is an algorithm to correct the contour of a circular object in an image.
<br>
1. First, it converts the object to its convex hull and find its longest axis.
2. Then, the axis is rotated by 45 degrees to find an intersecting point on the edge of the object.
By repeating this process, eight representative dots are fitted on the edge.
3. Then, it interpolates the dots to create a circular object with a smooth contour.

* This algorithm is tested on more than 1800 IVUS masks predicted by a deep learning model, and was found to enhance the shape of the object while preserving the accuracy(dice coefficient) of the prediction.
* You can check the example run of this algorithm in main.ipynb file. The example image is self created using paint app.
