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

function displayImage(image, img, w, h) {
    // Frankensteined from http://stackoverflow.com/questions/22823752/creating-image-from-array-in-javascript-and-html5
    var canvas = document.createElement('canvas');
    var ctx = canvas.getContext('2d');

    canvas.width = w;
    canvas.height = h;

    // create imageData object
    var idata = ctx.createImageData(w, h);

    // set our buffer as source
    idata.data.set(image);

    // update canvas with new data
    ctx.putImageData(idata, 0, 0);
    var dataUri = canvas.toDataURL();
    img.src = dataUri;
}

function fitInsideSquare(width, height, maxsize) {
    var result = {
        "height": maxsize,
        "width": maxsize,
        "offset": {
            "x": 0,
            "y": 0
        }
    }
    if (width < height) {
        result.width = Math.round(width / height * maxsize);
        result.offset.x = Math.round((maxsize - result.width) / 2);
    } else if (height < width) {
        result.height = Math.round(height / width * maxsize);
        result.offset.y = Math.round((maxsize - result.height) / 2);
    }
    return result;
}

function largestPowerOfTwoLessThan(x) {
    if (x < 32) {
        throw "Image is too small";
    }
    var y = 32;
    while (y < x) {
        y *= 2;
    }
    y /= 2;
    return y;
}

function base64toRGBA(image, maxsize) {
    // Frankensteined from http://stackoverflow.com/questions/8751020/how-to-get-a-pixels-x-y-coordinate-color-from-an-image
    var img = document.createElement("img");
    img.src = image;
    var maxsize = largestPowerOfTwoLessThan(Math.min(img.width, img.height, maxsize));
    var dim = fitInsideSquare(img.width, img.height, maxsize);

    var canvas = document.createElement("canvas");
    canvas.width = maxsize;
    canvas.height = maxsize;
    canvas.getContext('2d').drawImage(img, dim.offset.x, dim.offset.y, dim.width, dim.height);
    var imageData = canvas.getContext('2d').getImageData(0, 0, maxsize, maxsize).data;
    return imageData;
}

function hide(id) {
    document.getElementById(id).classList.add("hidden");
}

function show(id) {
    document.getElementById(id).classList.remove("hidden");
}

function getFirstProperty(obj) {
    for (var i in obj) {
        return obj[i];
    }
}

function createSizes(initial) {
    var sizes = [];
    var measure = initial;
    var display = document.getElementById("display");
    while (measure > 16) {
        measure /= 2;
        var img = document.createElement("img");
        img.alt = "icon_" + measure + "x" + measure;
        display.appendChild(img);
        var size = {
            measure,
            img
        }
        sizes.push(size);
    }
    return sizes;
}

function init() {
    hintbot = loadHintBot();
    hintbot.ready().then(() => {
        // Show file upload button
        hide("spinner");
        show("fileInputWrapper");
        show("description");
        // Enable file uploads
        document.getElementById("fileInput").addEventListener("change", function() {
            var reader = new FileReader();
            reader.onload = function() {
                // Load the image into an appropriately sized rgba master
                var base64 = this.result;
                var rgba = base64toRGBA(base64, 256);
                // Create the list of sizes we need to hint to
                var sizes = createSizes(Math.sqrt(rgba.length));
                console.log("Created sizes:" + JSON.stringify(sizes, null, 4));
                // Flatten image and start the hinting process
                var currentImageData = new Float32Array(rgba);
                for (var i = 0; i < 1; i++) {
                    var size = sizes[i];
                    // Run through the network
                    console.log("Attempting to input image at size " + JSON.stringify(size) + " with data.length " + currentImageData.length);
                    var inputData = {'input_1': currentImageData};
                    hintbot.predict(inputData).then(outputData => {
                        var prediction = new Uint8ClampedArray(getFirstProperty(outputData));
                        displayImage(prediction, size.img, size.measure, size.measure);
                        currentImageData = prediction;
                        if (i == size.length) {
                            show("display");
                        }
                    }).catch(err => {
                        console.log(err);
                    });
                }
            }

            reader.readAsDataURL(this.files[0]);
        }, false);
    });
}
window.onload = init;
