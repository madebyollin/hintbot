# hintbot
A CNN written in keras to hint icons automatically.  Live in-browser at [madebyollin.github.io/hintbot/](https://madebyollin.github.io/hintbot/)

**What is hinting?**

Hinting is the process of making icons crisp at small sizes.  Here's an example:

![](readme_images/comparison.png)

For all of human history, designers have laboriously pushed pixels to hint icons by hand.
<br/>But no longer!

**How well does Hintbot work?**

Here's how Hintbot performs at present (images shown are from test data; the model hadn't seen them before!):

![](readme_images/model_progress.png)

The model output is *substantially* better than a standard downscale.  However, it still falls short of human performance (for now).
This is not an indicator that the human performance is unreachable–rather, it's a sign that this project is still young.

**Wait, how does it work in-browser?**

I've used [keras.js](https://github.com/transcranial/keras-js/) to do the processing client-side.  The size of the model (it's designed around small inputs/outputs and has comparatively few parameters) allows it to render output instantly.

**Is this really an important problem?**

Not really, no!  But it takes me about 30-60 minutes to hint all of the sizes of a single icon, and it's a very mechanical process, so I'd like to have a robot do it.  My hope is that tackling simple problems like this first will help me develop the experience to tackle larger ones.
