'use strict';

var path       = require('path');
var hljs       = require('highlight.js');
var MarkdownIt = require('markdown-it');
var katex      = require('markdown-it-katex');
var anchor     = require('markdown-it-anchor');
var toc        = require('markdown-it-table-of-contents');
var cheerio    = require('cheerio');

var md = new MarkdownIt({
  highlight: function (code, lang) {
    var langMap = {
      make: 'makefile'
    };
    lang = langMap[lang] || lang;
    return hljs.highlight(lang, code).value;
  }
});

md.use(katex);
md.use(anchor);
md.use(toc, {
  includeLevel: [1, 2, 3, 4]
});

function markdownItRenderer(data, options) {
  var html = md.render(data.text);
  var $ = cheerio.load(html);
  var folder = path.basename(data.path, '.md');

  $('img').each(function (i, el) {
    var src = $(this).attr('src');
    $(this).attr('src', src.replace(folder + '/', ''));
  });

  return $.html();
}

hexo.extend.renderer.register('md', 'html', markdownItRenderer, true);
