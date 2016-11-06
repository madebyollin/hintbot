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

function base64toRGBA(image) {
    // Frankensteined from http://stackoverflow.com/questions/8751020/how-to-get-a-pixels-x-y-coordinate-color-from-an-image
    var img = document.createElement("img");
    img.src = image;
    var canvas = document.createElement("canvas");
    console.log("image has width " + img.width +" and height " + img.height);
    canvas.width = img.width;
    canvas.height = img.height;
    canvas.getContext('2d').drawImage(img, 0, 0, img.width, img.height);
    var imageData = canvas.getContext('2d').getImageData(0, 0, img.width, img.height);
    console.log("got image data:" + imageData);
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
                var flatrgba =  new Float32Array([].concat.apply([], rgba));
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
                    console.log(JSON.stringify(outputData.output, null, 4));
                }).catch(err => {
                    console.log(err);
                });
            }

            reader.readAsDataURL(this.files[0]);
        }, false);
    });
}
window.onload = init;
