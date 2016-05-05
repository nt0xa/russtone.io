'use strict';

var marked = require('marked');
var hljs = require('highlight.js');
var renderer = new marked.Renderer();

renderer.code = function (code, lang) {
  return '<pre><code class="hljs ' + lang + '">' + hljs.highlight(lang, code).value + '</code></pre>';
};

marked.setOptions({
  renderer: renderer
});

function markedRenderer(data) {
  return marked(data.text);
}

hexo.extend.renderer.register('md', 'html', markedRenderer, true);
