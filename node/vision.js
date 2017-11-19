'use strict';

const Q = require('q');
const request = require('request').defaults({ encoding: null });
const vision = require('@google-cloud/vision')({
    projectId: 'temporal-clover-122123',
    keyFilename: './config/vision-api-key.json'
});

const cache = {}

function labelDetection(imageUri) {
    var deferred = Q.defer();

    var image = {
        source: {
            imageUri: imageUri
        }
    };

    if (cache[imageUri]) {
        deferred.resolve(cache[imageUri]);
    } else {
        request.get(imageUri, function (error, response, body) {
            if (!error && response.statusCode == 200) {
                var data = new Buffer(body).toString('base64');
                vision
                    .labelDetection({ content: data })
                    .then(function (response) {
                        if (response && response.length) {
                            cache[imageUri] = response[0].labelAnnotations
                            deferred.resolve(cache[imageUri]);
                        } else {
                            deferred.reject('Empty response');
                        }
                    });
            } else {
                deferred.reject(error)
            }
        });
    }

    return deferred.promise;
}

module.exports = {
    labelDetection: labelDetection
};
