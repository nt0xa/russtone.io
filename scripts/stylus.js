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
    .set('compress', true)
    .render(callback);
}

hexo.extend.renderer.register('styl', 'css', stylusRenderer);
