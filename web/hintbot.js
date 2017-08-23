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

function displayImage(image, img, w, h, scale) {
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
    // rescale to desired scale

    var dataUri = canvas.toDataURL();
    img.src = dataUri;
}

function base64toRGBA(image) {
    // Frankensteined from http://stackoverflow.com/questions/8751020/how-to-get-a-pixels-x-y-coordinate-color-from-an-image
    // Bugfix from https://taditdash.wordpress.com/2016/10/04/uncaught-indexsizeerror-failed-to-execute-getimagedata-on-canvasrenderingcontext2d-the-source-width-is-0/
    return new Promise((resolve, reject) => {
        var img = document.createElement("img");
        img.src = image;
        img.onload = () => {
            var canvas = document.createElement("canvas");
            canvas.width = img.width || img.naturalWidth;
            canvas.height = img.height || img.naturalHeight;
            console.log("Canvas size", canvas.width, canvas.height);
            console.log("image", image, "img", img);
            canvas.getContext('2d').drawImage(img, 0, 0, canvas.width, canvas.height);
            var imageData = canvas.getContext('2d').getImageData(0, 0, canvas.width, canvas.height).data;
            resolve(imageData);
        }
    });
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
                var base64 = this.result;
                base64toRGBA(base64).then((rgba) => {
                    var flatrgba = new Float32Array([].concat.apply([], rgba));

                    var original = document.getElementById("original");
                    var hinted = document.getElementById("hinted");

                    displayImage(new Uint8ClampedArray(flatrgba), original, 32, 32, 0.5);

                    const inputData = {
                        'icon_goes_here': flatrgba
                    };
                    hintbot.predict(inputData).then(outputData => {
                        var prediction = new Uint8ClampedArray(getFirstProperty(outputData));
                        displayImage(prediction, hinted, 16, 16, 1.0);
                        show("display");
                    }).catch(err => {
                        console.log(err);
                    });
                });
            }

            reader.readAsDataURL(this.files[0]);
        }, false);
    });
}
window.onload = init;
