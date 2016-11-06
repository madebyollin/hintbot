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
        document.getElementById("spinner").addClass("hidden");
        document.getElementById("wrapper").removeClass("hidden");
        // input data object keyed by names of the input layers
        // or `input` for Sequential models
        // values are the flattened Float32Array data
        // (input tensor shapes are specified in the model config)
        const inputData = {
            'input_1': new Float32Array(data)
        }

        // make predictions
        // outputData is an object keyed by names of the output layers
        // or `output` for Sequential models
        model.predict(inputData).then(outputData => {
            // e.g.,
            // outputData['fc1000']
        }).catch(err => {
            // handle error
        });
    });
}
window.onload = init;
