'use strict';

const Q = require('q');
const request = require('request').defaults({ encoding: null });
// const vision = require('@google-cloud/vision')();


//For Local dev:
const vision = require('@google-cloud/vision')({
    projectId: 'temporal-clover-122123',
    keyFilename: './config/vision-api-key.json'
});

const food_words = require('./DATA/food_words.json');
const wordSet = new Set(food_words.words);

const cache = {};


function isFood(word) {
    return word.split(' ')
        .map((w) => w.trim().toLowerCase())
        .filter((w) => w.length)
        .some((w) => wordSet.has(w));
}

function filterAnnotations(annotations) {
    return annotations.filter((annotation) => isFood(annotation.description));
}

function labelDetection(data) {
    var deferred = Q.defer();
    if (cache[data]) {
        deferred.resolve(cache[imageUri]);
    } else {
        vision
            .labelDetection({ content: data })
            .then(function (response) {
                if (response && response.length) {
                    cache[data] = filterAnnotations(response[0].labelAnnotations)
                    deferred.resolve(cache[imageUri]);
                } else {
                    deferred.reject('Empty response');
                }
            });
    }
    return deferred.promise;
}

function loadImageAndDetect(imageUri) {
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
                            cache[imageUri] = filterAnnotations(response[0].labelAnnotations)
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
    labelDetection: labelDetection,
    loadImageAndDetect: loadImageAndDetect
};
