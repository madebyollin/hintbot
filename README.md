# hintbot
A CNN written in keras to hint icons automatically.

**What is hinting?**

Hinting is the process of adapting the style of icons to be clear at small sizes.  It's a small but significant part of the icon design process.  Here's an example:

![](readme_images/comparison.png)

**How well does hintbot work?**

This project hints icons automatically using a Convolutional Neural Network (CNN).  The model is trained off of thousands of pairs of larger and smaller (hinted) versions of the same image.  Here's how the model performs at present (images shown are from test data; the model hadn't seen them before):

![](readme_images/model_progress.png)

The model output is better than a standard downscale.  However, it still falls short of human performance (for now).  I have several ideas to improve performance, including:

-   Working with HSLA images (since most of the work is done on the LA channels).
-   Switching to a different error metric (MSE can encourage averaged/fuzzy results rather than confident ones)
-   Experimenting with network designs/hyperparameters; right now the choice of model structure was fairly arbitrary, so switching to a more appropriate model structure will almost certainly lead to better performance.

Further ideas are encouraged!

**Is this really an important problem?**

Not really, no.  But it takes me about 30-60 minutes to hint all of the sizes of a single icon, and it's a very dull process, so I'm curious to find out if I can automate it.  The best case scenario is something like https://xkcd.com/1319/; my hope is that tackling simple problems like this first will help me develop the experience to tackle larger ones.