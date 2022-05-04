# adabin
Adaptive binning algorithm for 2D maps

In order to recover as many spatial pixels as possible, we use an adaptive binning scheme. For independent, identically distributed data we expect the S/N of binned data to increase in proportion to the square root of the number of binned pixels. This increase is paid for by a corresponding decrease in spatial resolution, and thus we only want to bin pixels where we are required to do so for S/N reasons. We therefore carry out the following steps:

(1) First we create a series of maps which cover the same area as our data, which we denote map_1, map_2, map_4, map_8, and so forth, where map_N is a map where we have binned each group of N^2 adjacent pixels in our data together. Therefore map_1 is our original data, while in map_2 we have averaged together every 2 times 2 set of pixels into a single pixel; thus map_2 has half the resolution and 4 times fewer pixels than map_1, but each pixel has 2 times the S/N of the original data. Similarly, in map_4 we bin together every set of 4 times 4 pixels from the original map to create a map with 16 times fewer pixels but 4 times the S/N, and so forth.

(2)We then generate an output map with the same size as map_1. For each pixel in the output map, we first locate the corresponding pixel in map_1, and ask if its S/N ratio is above some specified threshold. If so, we set the value of the pixel in the output map to the value of the pixel in map_1. If the S/N does not reach our threshold, we then examine the pixel in map_2 that covers the same area, and use its value instead if the S/N ratio is high enough. If not, we proceed to map_4, and so forth. We fill in every pixel in the output map in this manner.
\end{enumerate}

We illustrate this process in the figure below. The left panel shows the original data, with pixels below a S/N ratio of 3 masked. The middle panel shows the value N of the map_N for which the S/N reaches the target S/N of 3. As is clear from the figure, the algorithm uses high-resolution data in high S/N regions, and degrades smoothly to more and more binned data in regions of weak signal. The right panel then shows the final output, adaptively binned map. Again, we see that high-resolution information has been preserved where possible, but now none of the map area is masked.

![recon_SN2011hb](https://user-images.githubusercontent.com/25077804/166636783-e98767fb-9378-4dc0-b4b9-8d53509584ae.png)


The details can be found in Li et al. (2022) in preparation.
