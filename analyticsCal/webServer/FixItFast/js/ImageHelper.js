/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
 * Copyright (c) 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
define(['jquery', 'knockout'], function($, ko) {
  function loadImageUsingCanvas(imageLocalUrl) {
    return new Promise(function(resolve, reject) {
      var $img = $('<img/>');
      $img.attr('src', imageLocalUrl);
      $img.css({position: 'absolute', left: '0px', top: '-999999em', maxWidth: 'none', width: 'auto', height: 'auto'});
      $img.bind('load', function() {
        var canvas = document.createElement("canvas");
        canvas.width = $img[0].width;
        canvas.height = $img[0].height;
        var ctx = canvas.getContext('2d');
        ctx.drawImage($img[0], 0, 0);
        resolve(canvas.toDataURL('image/jpeg'));
      });
    });
  }

  function loadImageUsingFilePlugin(imageLocalUrl) {
    return new Promise(function(resolve, reject) {
      window.resolveLocalFileSystemURL(imageLocalUrl, function(fileEntry) {
        fileEntry.file(function (file) {
          var reader = new FileReader();
          reader.onloadend = function(evt) {
            resolve(evt.target.result);
          };
          reader.readAsDataURL(file);
        });
      });
    });
  }

  function isFile(image) {
    return image.indexOf('file:///') > -1 || image.indexOf('content://') > -1
  }

  function isBase64Encoded(image) {
    return image.indexOf('data:image/') > -1;
  }

  function loadImage(imageLocalUrl) {
    var image = ko.isObservable(imageLocalUrl) ? imageLocalUrl() : imageLocalUrl
    if (!image) {
      oj.Logger.info('Image URL passed is empty or undefined. Returning empty image.');
      return Promise.resolve('')
    }

    if (isBase64Encoded(image)) {
      oj.Logger.info('Image URL passed is already base64 encoded. Returning same image.');
      return Promise.resolve(image);
    }


    if (!isFile(image)) {
      oj.Logger.warn('Invalid image format to load. Image should either be a base64 encoded string or a local file URL. Returning empty image.')
      return Promise.resolve('');
    }

    oj.Logger.info('Loading image from file and returning.');
    return cordova.file ? loadImageUsingFilePlugin(image)
                        : loadImageUsingCanvas(image);
  }

  function captureImage(event, imgHolder) {
    // Get a reference to the taken picture or chosen file
    var files = event.target.files;
    var file;

    if (files && files.length > 0) {
      file = files[0];
      try {
        var fileReader = new FileReader();
        fileReader.onload = function (evt) {
          imgHolder(evt.target.result);
        };
        fileReader.readAsDataURL(file);
      } catch (e) {
        oj.Logger.error(e);
      }
    }
  };

  function registerImageListeners(app, id, imgObs, viewModel, imageLaunch) {
    document.getElementById(id).addEventListener('change',
      function(event) {
        captureImage(event, imgObs);
      }
    );
    viewModel[imageLaunch] = function() {
      if (!navigator.camera)
        document.getElementById(id).click();
      else
        app.openBottomDrawer(imgObs);
    };
  }

  return {
    loadImage: loadImage,
    registerImageListeners: registerImageListeners
  }
});
