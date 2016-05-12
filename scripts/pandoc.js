'use strict';

var pdc = require('pdc');

function pandocRenderer(data, options, callback) {
  var args = [];
  return pdc(data.text, 'markdown', 'html', args, callback);
}

hexo.extend.renderer.register('md', 'html', pandocRenderer);
