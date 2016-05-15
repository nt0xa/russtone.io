'use strict';

var stylus      = require('stylus');
var nib         = require('nib');
var jeet        = require('jeet');
var rupture     = require('rupture');
var typographic = require('typographic');

function stylusRenderer(data, options, callback) {
  var config = this.config.stylus || {};

  stylus(data.text)
    .use(nib())
    .use(jeet())
    .use(rupture())
    .use(typographic())
    .set('filename', data.path)
    .set('sourcemap', config.sourcemaps)
    .set('compress', config.compress)
    .render(callback);
}

hexo.extend.renderer.register('styl', 'css', stylusRenderer);
