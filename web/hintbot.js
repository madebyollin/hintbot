function loadHintBot() {
    return new KerasJS.Model({
        filepaths: {
            model: 'web/hintbot.json',
            weights: 'web/hintbot_weights.buf',
            metadata: 'web/hintbot_metadata.json'
        },
        gpu: true
    })
}

function displayImage(image) {
    // Frankensteined from http://stackoverflow.com/questions/22823752/creating-image-from-array-in-javascript-and-html5
    var canvas = document.createElement('canvas');
    var ctx = canvas.getContext('2d');

    canvas.width = 16;
    canvas.height = 16;

    // create imageData object
    var idata = ctx.createImageData(16, 16);

    // set our buffer as source
    idata.data.set(image);

    // update canvas with new data
    ctx.putImageData(idata, 0, 0);
    var dataUri = canvas.toDataURL();
    var img = document.createElement("img");
    img.src = dataUri;
    document.getElementById("display").appendChild(img);
}

function base64toRGBA(image) {
    // Frankensteined from http://stackoverflow.com/questions/8751020/how-to-get-a-pixels-x-y-coordinate-color-from-an-image
    var img = document.createElement("img");
    img.src = image;
    var canvas = document.createElement("canvas");
    console.log("image has width " + img.width + " and height " + img.height);
    canvas.width = img.width;
    canvas.height = img.height;
    canvas.getContext('2d').drawImage(img, 0, 0, img.width, img.height);
    var imageData = canvas.getContext('2d').getImageData(0, 0, img.width, img.height).data;
    console.log("got image data:" + JSON.stringify(imageData, null, 4));
    return imageData;
}

function init() {
    hintbot = loadHintBot();
    hintbot.ready().then(() => {
        document.getElementById("spinner").classList.add("hidden");
        document.getElementById("wrapper").classList.remove("hidden");
        document.getElementById("fileInput").addEventListener("change", function() {
            var reader = new FileReader();
            reader.onload = function() {
                var base64 = this.result;
                var rgba = base64toRGBA(base64);
                var flatrgba = new Float32Array([].concat.apply([], rgba));
                // input data object keyed by names of the input layers
                // or `input` for Sequential models
                // values are the flattened Float32Array data
                // (input tensor shapes are specified in the model config)
                console.log("flatrgba:" + flatrgba);
                const inputData = {
                    'input_1': flatrgba
                }

                // make predictions
                // outputData is an object keyed by names of the output layers
                // or `output` for Sequential models
                hintbot.predict(inputData).then(outputData => {
                    // e.g.,
                    // outputData['fc1000']
                    console.log("Model output:");
                    console.log(JSON.stringify(outputData, null, 4));
                    var raw = outputData.convolution2d_7;
                    var clean = new Uint8ClampedArray(raw);
                    displayImage(clean);
                }).catch(err => {
                    console.log(err);
                });
            }

            reader.readAsDataURL(this.files[0]);
        }, false);
    });
}
window.onload = init;
