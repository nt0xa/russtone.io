'use strict';

var pug = require('pug');

function pugRenderer(data, locals) {
  var result = pug.renderFile(data.path, locals);
  return result;
}

hexo.extend.renderer.register('pug', 'html', pugRenderer, true);
