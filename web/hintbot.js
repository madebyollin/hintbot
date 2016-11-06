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

function init() {
    hintbot = loadHintBot();
    hintbot.ready().then(() => {
        document.getElementById("spinner").classList.add("hidden");
        document.getElementById("wrapper").classList.remove("hidden");
        document.getElementById("fileInput").addEventListener("change", function() {
            var reader = new FileReader();
            reader.onload = function() {
                var array = new Uint8Array(this.result),
                console.log(array);

                // input data object keyed by names of the input layers
                // or `input` for Sequential models
                // values are the flattened Float32Array data
                // (input tensor shapes are specified in the model config)
                const inputData = {
                    'input_1': array
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

            reader.readAsArrayBuffer(this.files[0]);
        }, false);
    });
}
window.onload = init;
