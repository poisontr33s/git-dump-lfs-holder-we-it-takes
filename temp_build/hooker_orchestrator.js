import { createRequire } from "node:module";
var __commonJS = (cb, mod) => () => (mod || cb((mod = { exports: {} }).exports, mod), mod.exports);
var __require = /* @__PURE__ */ createRequire(import.meta.url);

// node_modules/fs.realpath/old.js
var require_old = __commonJS((exports) => {
  var pathModule = __require("path");
  var isWindows = process.platform === "win32";
  var fs = __require("fs");
  var DEBUG = process.env.NODE_DEBUG && /fs/.test(process.env.NODE_DEBUG);
  function rethrow() {
    var callback;
    if (DEBUG) {
      var backtrace = new Error;
      callback = debugCallback;
    } else
      callback = missingCallback;
    return callback;
    function debugCallback(err) {
      if (err) {
        backtrace.message = err.message;
        err = backtrace;
        missingCallback(err);
      }
    }
    function missingCallback(err) {
      if (err) {
        if (process.throwDeprecation)
          throw err;
        else if (!process.noDeprecation) {
          var msg = "fs: missing callback " + (err.stack || err.message);
          if (process.traceDeprecation)
            console.trace(msg);
          else
            console.error(msg);
        }
      }
    }
  }
  function maybeCallback(cb) {
    return typeof cb === "function" ? cb : rethrow();
  }
  var normalize = pathModule.normalize;
  if (isWindows) {
    nextPartRe = /(.*?)(?:[\/\\]+|$)/g;
  } else {
    nextPartRe = /(.*?)(?:[\/]+|$)/g;
  }
  var nextPartRe;
  if (isWindows) {
    splitRootRe = /^(?:[a-zA-Z]:|[\\\/]{2}[^\\\/]+[\\\/][^\\\/]+)?[\\\/]*/;
  } else {
    splitRootRe = /^[\/]*/;
  }
  var splitRootRe;
  exports.realpathSync = function realpathSync(p, cache) {
    p = pathModule.resolve(p);
    if (cache && Object.prototype.hasOwnProperty.call(cache, p)) {
      return cache[p];
    }
    var original = p, seenLinks = {}, knownHard = {};
    var pos;
    var current;
    var base;
    var previous;
    start();
    function start() {
      var m = splitRootRe.exec(p);
      pos = m[0].length;
      current = m[0];
      base = m[0];
      previous = "";
      if (isWindows && !knownHard[base]) {
        fs.lstatSync(base);
        knownHard[base] = true;
      }
    }
    while (pos < p.length) {
      nextPartRe.lastIndex = pos;
      var result = nextPartRe.exec(p);
      previous = current;
      current += result[0];
      base = previous + result[1];
      pos = nextPartRe.lastIndex;
      if (knownHard[base] || cache && cache[base] === base) {
        continue;
      }
      var resolvedLink;
      if (cache && Object.prototype.hasOwnProperty.call(cache, base)) {
        resolvedLink = cache[base];
      } else {
        var stat = fs.lstatSync(base);
        if (!stat.isSymbolicLink()) {
          knownHard[base] = true;
          if (cache)
            cache[base] = base;
          continue;
        }
        var linkTarget = null;
        if (!isWindows) {
          var id = stat.dev.toString(32) + ":" + stat.ino.toString(32);
          if (seenLinks.hasOwnProperty(id)) {
            linkTarget = seenLinks[id];
          }
        }
        if (linkTarget === null) {
          fs.statSync(base);
          linkTarget = fs.readlinkSync(base);
        }
        resolvedLink = pathModule.resolve(previous, linkTarget);
        if (cache)
          cache[base] = resolvedLink;
        if (!isWindows)
          seenLinks[id] = linkTarget;
      }
      p = pathModule.resolve(resolvedLink, p.slice(pos));
      start();
    }
    if (cache)
      cache[original] = p;
    return p;
  };
  exports.realpath = function realpath(p, cache, cb) {
    if (typeof cb !== "function") {
      cb = maybeCallback(cache);
      cache = null;
    }
    p = pathModule.resolve(p);
    if (cache && Object.prototype.hasOwnProperty.call(cache, p)) {
      return process.nextTick(cb.bind(null, null, cache[p]));
    }
    var original = p, seenLinks = {}, knownHard = {};
    var pos;
    var current;
    var base;
    var previous;
    start();
    function start() {
      var m = splitRootRe.exec(p);
      pos = m[0].length;
      current = m[0];
      base = m[0];
      previous = "";
      if (isWindows && !knownHard[base]) {
        fs.lstat(base, function(err) {
          if (err)
            return cb(err);
          knownHard[base] = true;
          LOOP();
        });
      } else {
        process.nextTick(LOOP);
      }
    }
    function LOOP() {
      if (pos >= p.length) {
        if (cache)
          cache[original] = p;
        return cb(null, p);
      }
      nextPartRe.lastIndex = pos;
      var result = nextPartRe.exec(p);
      previous = current;
      current += result[0];
      base = previous + result[1];
      pos = nextPartRe.lastIndex;
      if (knownHard[base] || cache && cache[base] === base) {
        return process.nextTick(LOOP);
      }
      if (cache && Object.prototype.hasOwnProperty.call(cache, base)) {
        return gotResolvedLink(cache[base]);
      }
      return fs.lstat(base, gotStat);
    }
    function gotStat(err, stat) {
      if (err)
        return cb(err);
      if (!stat.isSymbolicLink()) {
        knownHard[base] = true;
        if (cache)
          cache[base] = base;
        return process.nextTick(LOOP);
      }
      if (!isWindows) {
        var id = stat.dev.toString(32) + ":" + stat.ino.toString(32);
        if (seenLinks.hasOwnProperty(id)) {
          return gotTarget(null, seenLinks[id], base);
        }
      }
      fs.stat(base, function(err2) {
        if (err2)
          return cb(err2);
        fs.readlink(base, function(err3, target) {
          if (!isWindows)
            seenLinks[id] = target;
          gotTarget(err3, target);
        });
      });
    }
    function gotTarget(err, target, base2) {
      if (err)
        return cb(err);
      var resolvedLink = pathModule.resolve(previous, target);
      if (cache)
        cache[base2] = resolvedLink;
      gotResolvedLink(resolvedLink);
    }
    function gotResolvedLink(resolvedLink) {
      p = pathModule.resolve(resolvedLink, p.slice(pos));
      start();
    }
  };
});

// node_modules/fs.realpath/index.js
var require_fs = __commonJS((exports, module) => {
  module.exports = realpath;
  realpath.realpath = realpath;
  realpath.sync = realpathSync;
  realpath.realpathSync = realpathSync;
  realpath.monkeypatch = monkeypatch;
  realpath.unmonkeypatch = unmonkeypatch;
  var fs = __require("fs");
  var origRealpath = fs.realpath;
  var origRealpathSync = fs.realpathSync;
  var version = process.version;
  var ok = /^v[0-5]\./.test(version);
  var old = require_old();
  function newError(er) {
    return er && er.syscall === "realpath" && (er.code === "ELOOP" || er.code === "ENOMEM" || er.code === "ENAMETOOLONG");
  }
  function realpath(p, cache, cb) {
    if (ok) {
      return origRealpath(p, cache, cb);
    }
    if (typeof cache === "function") {
      cb = cache;
      cache = null;
    }
    origRealpath(p, cache, function(er, result) {
      if (newError(er)) {
        old.realpath(p, cache, cb);
      } else {
        cb(er, result);
      }
    });
  }
  function realpathSync(p, cache) {
    if (ok) {
      return origRealpathSync(p, cache);
    }
    try {
      return origRealpathSync(p, cache);
    } catch (er) {
      if (newError(er)) {
        return old.realpathSync(p, cache);
      } else {
        throw er;
      }
    }
  }
  function monkeypatch() {
    fs.realpath = realpath;
    fs.realpathSync = realpathSync;
  }
  function unmonkeypatch() {
    fs.realpath = origRealpath;
    fs.realpathSync = origRealpathSync;
  }
});

// node_modules/concat-map/index.js
var require_concat_map = __commonJS((exports, module) => {
  module.exports = function(xs, fn) {
    var res = [];
    for (var i = 0;i < xs.length; i++) {
      var x = fn(xs[i], i);
      if (isArray(x))
        res.push.apply(res, x);
      else
        res.push(x);
    }
    return res;
  };
  var isArray = Array.isArray || function(xs) {
    return Object.prototype.toString.call(xs) === "[object Array]";
  };
});

// node_modules/balanced-match/index.js
var require_balanced_match = __commonJS((exports, module) => {
  module.exports = balanced;
  function balanced(a, b, str) {
    if (a instanceof RegExp)
      a = maybeMatch(a, str);
    if (b instanceof RegExp)
      b = maybeMatch(b, str);
    var r = range(a, b, str);
    return r && {
      start: r[0],
      end: r[1],
      pre: str.slice(0, r[0]),
      body: str.slice(r[0] + a.length, r[1]),
      post: str.slice(r[1] + b.length)
    };
  }
  function maybeMatch(reg, str) {
    var m = str.match(reg);
    return m ? m[0] : null;
  }
  balanced.range = range;
  function range(a, b, str) {
    var begs, beg, left, right, result;
    var ai = str.indexOf(a);
    var bi = str.indexOf(b, ai + 1);
    var i = ai;
    if (ai >= 0 && bi > 0) {
      if (a === b) {
        return [ai, bi];
      }
      begs = [];
      left = str.length;
      while (i >= 0 && !result) {
        if (i == ai) {
          begs.push(i);
          ai = str.indexOf(a, i + 1);
        } else if (begs.length == 1) {
          result = [begs.pop(), bi];
        } else {
          beg = begs.pop();
          if (beg < left) {
            left = beg;
            right = bi;
          }
          bi = str.indexOf(b, i + 1);
        }
        i = ai < bi && ai >= 0 ? ai : bi;
      }
      if (begs.length) {
        result = [left, right];
      }
    }
    return result;
  }
});

// node_modules/brace-expansion/index.js
var require_brace_expansion = __commonJS((exports, module) => {
  var concatMap = require_concat_map();
  var balanced = require_balanced_match();
  module.exports = expandTop;
  var escSlash = "\x00SLASH" + Math.random() + "\x00";
  var escOpen = "\x00OPEN" + Math.random() + "\x00";
  var escClose = "\x00CLOSE" + Math.random() + "\x00";
  var escComma = "\x00COMMA" + Math.random() + "\x00";
  var escPeriod = "\x00PERIOD" + Math.random() + "\x00";
  function numeric(str) {
    return parseInt(str, 10) == str ? parseInt(str, 10) : str.charCodeAt(0);
  }
  function escapeBraces(str) {
    return str.split("\\\\").join(escSlash).split("\\{").join(escOpen).split("\\}").join(escClose).split("\\,").join(escComma).split("\\.").join(escPeriod);
  }
  function unescapeBraces(str) {
    return str.split(escSlash).join("\\").split(escOpen).join("{").split(escClose).join("}").split(escComma).join(",").split(escPeriod).join(".");
  }
  function parseCommaParts(str) {
    if (!str)
      return [""];
    var parts = [];
    var m = balanced("{", "}", str);
    if (!m)
      return str.split(",");
    var pre = m.pre;
    var body = m.body;
    var post = m.post;
    var p = pre.split(",");
    p[p.length - 1] += "{" + body + "}";
    var postParts = parseCommaParts(post);
    if (post.length) {
      p[p.length - 1] += postParts.shift();
      p.push.apply(p, postParts);
    }
    parts.push.apply(parts, p);
    return parts;
  }
  function expandTop(str) {
    if (!str)
      return [];
    if (str.substr(0, 2) === "{}") {
      str = "\\{\\}" + str.substr(2);
    }
    return expand(escapeBraces(str), true).map(unescapeBraces);
  }
  function embrace(str) {
    return "{" + str + "}";
  }
  function isPadded(el) {
    return /^-?0\d/.test(el);
  }
  function lte(i, y) {
    return i <= y;
  }
  function gte(i, y) {
    return i >= y;
  }
  function expand(str, isTop) {
    var expansions = [];
    var m = balanced("{", "}", str);
    if (!m || /\$$/.test(m.pre))
      return [str];
    var isNumericSequence = /^-?\d+\.\.-?\d+(?:\.\.-?\d+)?$/.test(m.body);
    var isAlphaSequence = /^[a-zA-Z]\.\.[a-zA-Z](?:\.\.-?\d+)?$/.test(m.body);
    var isSequence = isNumericSequence || isAlphaSequence;
    var isOptions = m.body.indexOf(",") >= 0;
    if (!isSequence && !isOptions) {
      if (m.post.match(/,.*\}/)) {
        str = m.pre + "{" + m.body + escClose + m.post;
        return expand(str);
      }
      return [str];
    }
    var n;
    if (isSequence) {
      n = m.body.split(/\.\./);
    } else {
      n = parseCommaParts(m.body);
      if (n.length === 1) {
        n = expand(n[0], false).map(embrace);
        if (n.length === 1) {
          var post = m.post.length ? expand(m.post, false) : [""];
          return post.map(function(p) {
            return m.pre + n[0] + p;
          });
        }
      }
    }
    var pre = m.pre;
    var post = m.post.length ? expand(m.post, false) : [""];
    var N;
    if (isSequence) {
      var x = numeric(n[0]);
      var y = numeric(n[1]);
      var width = Math.max(n[0].length, n[1].length);
      var incr = n.length == 3 ? Math.abs(numeric(n[2])) : 1;
      var test = lte;
      var reverse = y < x;
      if (reverse) {
        incr *= -1;
        test = gte;
      }
      var pad = n.some(isPadded);
      N = [];
      for (var i = x;test(i, y); i += incr) {
        var c;
        if (isAlphaSequence) {
          c = String.fromCharCode(i);
          if (c === "\\")
            c = "";
        } else {
          c = String(i);
          if (pad) {
            var need = width - c.length;
            if (need > 0) {
              var z = new Array(need + 1).join("0");
              if (i < 0)
                c = "-" + z + c.slice(1);
              else
                c = z + c;
            }
          }
        }
        N.push(c);
      }
    } else {
      N = concatMap(n, function(el) {
        return expand(el, false);
      });
    }
    for (var j = 0;j < N.length; j++) {
      for (var k = 0;k < post.length; k++) {
        var expansion = pre + N[j] + post[k];
        if (!isTop || isSequence || expansion)
          expansions.push(expansion);
      }
    }
    return expansions;
  }
});

// node_modules/minimatch/minimatch.js
var require_minimatch = __commonJS((exports, module) => {
  module.exports = minimatch;
  minimatch.Minimatch = Minimatch;
  var path = function() {
    try {
      return __require("path");
    } catch (e) {}
  }() || {
    sep: "/"
  };
  minimatch.sep = path.sep;
  var GLOBSTAR = minimatch.GLOBSTAR = Minimatch.GLOBSTAR = {};
  var expand = require_brace_expansion();
  var plTypes = {
    "!": { open: "(?:(?!(?:", close: "))[^/]*?)" },
    "?": { open: "(?:", close: ")?" },
    "+": { open: "(?:", close: ")+" },
    "*": { open: "(?:", close: ")*" },
    "@": { open: "(?:", close: ")" }
  };
  var qmark = "[^/]";
  var star = qmark + "*?";
  var twoStarDot = "(?:(?!(?:\\/|^)(?:\\.{1,2})($|\\/)).)*?";
  var twoStarNoDot = "(?:(?!(?:\\/|^)\\.).)*?";
  var reSpecials = charSet("().*{}+?[]^$\\!");
  function charSet(s) {
    return s.split("").reduce(function(set, c) {
      set[c] = true;
      return set;
    }, {});
  }
  var slashSplit = /\/+/;
  minimatch.filter = filter;
  function filter(pattern, options) {
    options = options || {};
    return function(p, i, list) {
      return minimatch(p, pattern, options);
    };
  }
  function ext(a, b) {
    b = b || {};
    var t = {};
    Object.keys(a).forEach(function(k) {
      t[k] = a[k];
    });
    Object.keys(b).forEach(function(k) {
      t[k] = b[k];
    });
    return t;
  }
  minimatch.defaults = function(def) {
    if (!def || typeof def !== "object" || !Object.keys(def).length) {
      return minimatch;
    }
    var orig = minimatch;
    var m = function minimatch(p, pattern, options) {
      return orig(p, pattern, ext(def, options));
    };
    m.Minimatch = function Minimatch(pattern, options) {
      return new orig.Minimatch(pattern, ext(def, options));
    };
    m.Minimatch.defaults = function defaults(options) {
      return orig.defaults(ext(def, options)).Minimatch;
    };
    m.filter = function filter(pattern, options) {
      return orig.filter(pattern, ext(def, options));
    };
    m.defaults = function defaults(options) {
      return orig.defaults(ext(def, options));
    };
    m.makeRe = function makeRe(pattern, options) {
      return orig.makeRe(pattern, ext(def, options));
    };
    m.braceExpand = function braceExpand(pattern, options) {
      return orig.braceExpand(pattern, ext(def, options));
    };
    m.match = function(list, pattern, options) {
      return orig.match(list, pattern, ext(def, options));
    };
    return m;
  };
  Minimatch.defaults = function(def) {
    return minimatch.defaults(def).Minimatch;
  };
  function minimatch(p, pattern, options) {
    assertValidPattern(pattern);
    if (!options)
      options = {};
    if (!options.nocomment && pattern.charAt(0) === "#") {
      return false;
    }
    return new Minimatch(pattern, options).match(p);
  }
  function Minimatch(pattern, options) {
    if (!(this instanceof Minimatch)) {
      return new Minimatch(pattern, options);
    }
    assertValidPattern(pattern);
    if (!options)
      options = {};
    pattern = pattern.trim();
    if (!options.allowWindowsEscape && path.sep !== "/") {
      pattern = pattern.split(path.sep).join("/");
    }
    this.options = options;
    this.set = [];
    this.pattern = pattern;
    this.regexp = null;
    this.negate = false;
    this.comment = false;
    this.empty = false;
    this.partial = !!options.partial;
    this.make();
  }
  Minimatch.prototype.debug = function() {};
  Minimatch.prototype.make = make;
  function make() {
    var pattern = this.pattern;
    var options = this.options;
    if (!options.nocomment && pattern.charAt(0) === "#") {
      this.comment = true;
      return;
    }
    if (!pattern) {
      this.empty = true;
      return;
    }
    this.parseNegate();
    var set = this.globSet = this.braceExpand();
    if (options.debug)
      this.debug = function debug() {
        console.error.apply(console, arguments);
      };
    this.debug(this.pattern, set);
    set = this.globParts = set.map(function(s) {
      return s.split(slashSplit);
    });
    this.debug(this.pattern, set);
    set = set.map(function(s, si, set2) {
      return s.map(this.parse, this);
    }, this);
    this.debug(this.pattern, set);
    set = set.filter(function(s) {
      return s.indexOf(false) === -1;
    });
    this.debug(this.pattern, set);
    this.set = set;
  }
  Minimatch.prototype.parseNegate = parseNegate;
  function parseNegate() {
    var pattern = this.pattern;
    var negate = false;
    var options = this.options;
    var negateOffset = 0;
    if (options.nonegate)
      return;
    for (var i = 0, l = pattern.length;i < l && pattern.charAt(i) === "!"; i++) {
      negate = !negate;
      negateOffset++;
    }
    if (negateOffset)
      this.pattern = pattern.substr(negateOffset);
    this.negate = negate;
  }
  minimatch.braceExpand = function(pattern, options) {
    return braceExpand(pattern, options);
  };
  Minimatch.prototype.braceExpand = braceExpand;
  function braceExpand(pattern, options) {
    if (!options) {
      if (this instanceof Minimatch) {
        options = this.options;
      } else {
        options = {};
      }
    }
    pattern = typeof pattern === "undefined" ? this.pattern : pattern;
    assertValidPattern(pattern);
    if (options.nobrace || !/\{(?:(?!\{).)*\}/.test(pattern)) {
      return [pattern];
    }
    return expand(pattern);
  }
  var MAX_PATTERN_LENGTH = 1024 * 64;
  var assertValidPattern = function(pattern) {
    if (typeof pattern !== "string") {
      throw new TypeError("invalid pattern");
    }
    if (pattern.length > MAX_PATTERN_LENGTH) {
      throw new TypeError("pattern is too long");
    }
  };
  Minimatch.prototype.parse = parse;
  var SUBPARSE = {};
  function parse(pattern, isSub) {
    assertValidPattern(pattern);
    var options = this.options;
    if (pattern === "**") {
      if (!options.noglobstar)
        return GLOBSTAR;
      else
        pattern = "*";
    }
    if (pattern === "")
      return "";
    var re = "";
    var hasMagic = !!options.nocase;
    var escaping = false;
    var patternListStack = [];
    var negativeLists = [];
    var stateChar;
    var inClass = false;
    var reClassStart = -1;
    var classStart = -1;
    var patternStart = pattern.charAt(0) === "." ? "" : options.dot ? "(?!(?:^|\\/)\\.{1,2}(?:$|\\/))" : "(?!\\.)";
    var self = this;
    function clearStateChar() {
      if (stateChar) {
        switch (stateChar) {
          case "*":
            re += star;
            hasMagic = true;
            break;
          case "?":
            re += qmark;
            hasMagic = true;
            break;
          default:
            re += "\\" + stateChar;
            break;
        }
        self.debug("clearStateChar %j %j", stateChar, re);
        stateChar = false;
      }
    }
    for (var i = 0, len = pattern.length, c;i < len && (c = pattern.charAt(i)); i++) {
      this.debug("%s	%s %s %j", pattern, i, re, c);
      if (escaping && reSpecials[c]) {
        re += "\\" + c;
        escaping = false;
        continue;
      }
      switch (c) {
        case "/": {
          return false;
        }
        case "\\":
          clearStateChar();
          escaping = true;
          continue;
        case "?":
        case "*":
        case "+":
        case "@":
        case "!":
          this.debug("%s	%s %s %j <-- stateChar", pattern, i, re, c);
          if (inClass) {
            this.debug("  in class");
            if (c === "!" && i === classStart + 1)
              c = "^";
            re += c;
            continue;
          }
          self.debug("call clearStateChar %j", stateChar);
          clearStateChar();
          stateChar = c;
          if (options.noext)
            clearStateChar();
          continue;
        case "(":
          if (inClass) {
            re += "(";
            continue;
          }
          if (!stateChar) {
            re += "\\(";
            continue;
          }
          patternListStack.push({
            type: stateChar,
            start: i - 1,
            reStart: re.length,
            open: plTypes[stateChar].open,
            close: plTypes[stateChar].close
          });
          re += stateChar === "!" ? "(?:(?!(?:" : "(?:";
          this.debug("plType %j %j", stateChar, re);
          stateChar = false;
          continue;
        case ")":
          if (inClass || !patternListStack.length) {
            re += "\\)";
            continue;
          }
          clearStateChar();
          hasMagic = true;
          var pl = patternListStack.pop();
          re += pl.close;
          if (pl.type === "!") {
            negativeLists.push(pl);
          }
          pl.reEnd = re.length;
          continue;
        case "|":
          if (inClass || !patternListStack.length || escaping) {
            re += "\\|";
            escaping = false;
            continue;
          }
          clearStateChar();
          re += "|";
          continue;
        case "[":
          clearStateChar();
          if (inClass) {
            re += "\\" + c;
            continue;
          }
          inClass = true;
          classStart = i;
          reClassStart = re.length;
          re += c;
          continue;
        case "]":
          if (i === classStart + 1 || !inClass) {
            re += "\\" + c;
            escaping = false;
            continue;
          }
          var cs = pattern.substring(classStart + 1, i);
          try {
            RegExp("[" + cs + "]");
          } catch (er) {
            var sp = this.parse(cs, SUBPARSE);
            re = re.substr(0, reClassStart) + "\\[" + sp[0] + "\\]";
            hasMagic = hasMagic || sp[1];
            inClass = false;
            continue;
          }
          hasMagic = true;
          inClass = false;
          re += c;
          continue;
        default:
          clearStateChar();
          if (escaping) {
            escaping = false;
          } else if (reSpecials[c] && !(c === "^" && inClass)) {
            re += "\\";
          }
          re += c;
      }
    }
    if (inClass) {
      cs = pattern.substr(classStart + 1);
      sp = this.parse(cs, SUBPARSE);
      re = re.substr(0, reClassStart) + "\\[" + sp[0];
      hasMagic = hasMagic || sp[1];
    }
    for (pl = patternListStack.pop();pl; pl = patternListStack.pop()) {
      var tail = re.slice(pl.reStart + pl.open.length);
      this.debug("setting tail", re, pl);
      tail = tail.replace(/((?:\\{2}){0,64})(\\?)\|/g, function(_, $1, $2) {
        if (!$2) {
          $2 = "\\";
        }
        return $1 + $1 + $2 + "|";
      });
      this.debug(`tail=%j
   %s`, tail, tail, pl, re);
      var t = pl.type === "*" ? star : pl.type === "?" ? qmark : "\\" + pl.type;
      hasMagic = true;
      re = re.slice(0, pl.reStart) + t + "\\(" + tail;
    }
    clearStateChar();
    if (escaping) {
      re += "\\\\";
    }
    var addPatternStart = false;
    switch (re.charAt(0)) {
      case "[":
      case ".":
      case "(":
        addPatternStart = true;
    }
    for (var n = negativeLists.length - 1;n > -1; n--) {
      var nl = negativeLists[n];
      var nlBefore = re.slice(0, nl.reStart);
      var nlFirst = re.slice(nl.reStart, nl.reEnd - 8);
      var nlLast = re.slice(nl.reEnd - 8, nl.reEnd);
      var nlAfter = re.slice(nl.reEnd);
      nlLast += nlAfter;
      var openParensBefore = nlBefore.split("(").length - 1;
      var cleanAfter = nlAfter;
      for (i = 0;i < openParensBefore; i++) {
        cleanAfter = cleanAfter.replace(/\)[+*?]?/, "");
      }
      nlAfter = cleanAfter;
      var dollar = "";
      if (nlAfter === "" && isSub !== SUBPARSE) {
        dollar = "$";
      }
      var newRe = nlBefore + nlFirst + nlAfter + dollar + nlLast;
      re = newRe;
    }
    if (re !== "" && hasMagic) {
      re = "(?=.)" + re;
    }
    if (addPatternStart) {
      re = patternStart + re;
    }
    if (isSub === SUBPARSE) {
      return [re, hasMagic];
    }
    if (!hasMagic) {
      return globUnescape(pattern);
    }
    var flags = options.nocase ? "i" : "";
    try {
      var regExp = new RegExp("^" + re + "$", flags);
    } catch (er) {
      return new RegExp("$.");
    }
    regExp._glob = pattern;
    regExp._src = re;
    return regExp;
  }
  minimatch.makeRe = function(pattern, options) {
    return new Minimatch(pattern, options || {}).makeRe();
  };
  Minimatch.prototype.makeRe = makeRe;
  function makeRe() {
    if (this.regexp || this.regexp === false)
      return this.regexp;
    var set = this.set;
    if (!set.length) {
      this.regexp = false;
      return this.regexp;
    }
    var options = this.options;
    var twoStar = options.noglobstar ? star : options.dot ? twoStarDot : twoStarNoDot;
    var flags = options.nocase ? "i" : "";
    var re = set.map(function(pattern) {
      return pattern.map(function(p) {
        return p === GLOBSTAR ? twoStar : typeof p === "string" ? regExpEscape(p) : p._src;
      }).join("\\/");
    }).join("|");
    re = "^(?:" + re + ")$";
    if (this.negate)
      re = "^(?!" + re + ").*$";
    try {
      this.regexp = new RegExp(re, flags);
    } catch (ex) {
      this.regexp = false;
    }
    return this.regexp;
  }
  minimatch.match = function(list, pattern, options) {
    options = options || {};
    var mm = new Minimatch(pattern, options);
    list = list.filter(function(f) {
      return mm.match(f);
    });
    if (mm.options.nonull && !list.length) {
      list.push(pattern);
    }
    return list;
  };
  Minimatch.prototype.match = function match(f, partial) {
    if (typeof partial === "undefined")
      partial = this.partial;
    this.debug("match", f, this.pattern);
    if (this.comment)
      return false;
    if (this.empty)
      return f === "";
    if (f === "/" && partial)
      return true;
    var options = this.options;
    if (path.sep !== "/") {
      f = f.split(path.sep).join("/");
    }
    f = f.split(slashSplit);
    this.debug(this.pattern, "split", f);
    var set = this.set;
    this.debug(this.pattern, "set", set);
    var filename;
    var i;
    for (i = f.length - 1;i >= 0; i--) {
      filename = f[i];
      if (filename)
        break;
    }
    for (i = 0;i < set.length; i++) {
      var pattern = set[i];
      var file = f;
      if (options.matchBase && pattern.length === 1) {
        file = [filename];
      }
      var hit = this.matchOne(file, pattern, partial);
      if (hit) {
        if (options.flipNegate)
          return true;
        return !this.negate;
      }
    }
    if (options.flipNegate)
      return false;
    return this.negate;
  };
  Minimatch.prototype.matchOne = function(file, pattern, partial) {
    var options = this.options;
    this.debug("matchOne", { this: this, file, pattern });
    this.debug("matchOne", file.length, pattern.length);
    for (var fi = 0, pi = 0, fl = file.length, pl = pattern.length;fi < fl && pi < pl; fi++, pi++) {
      this.debug("matchOne loop");
      var p = pattern[pi];
      var f = file[fi];
      this.debug(pattern, p, f);
      if (p === false)
        return false;
      if (p === GLOBSTAR) {
        this.debug("GLOBSTAR", [pattern, p, f]);
        var fr = fi;
        var pr = pi + 1;
        if (pr === pl) {
          this.debug("** at the end");
          for (;fi < fl; fi++) {
            if (file[fi] === "." || file[fi] === ".." || !options.dot && file[fi].charAt(0) === ".")
              return false;
          }
          return true;
        }
        while (fr < fl) {
          var swallowee = file[fr];
          this.debug(`
globstar while`, file, fr, pattern, pr, swallowee);
          if (this.matchOne(file.slice(fr), pattern.slice(pr), partial)) {
            this.debug("globstar found match!", fr, fl, swallowee);
            return true;
          } else {
            if (swallowee === "." || swallowee === ".." || !options.dot && swallowee.charAt(0) === ".") {
              this.debug("dot detected!", file, fr, pattern, pr);
              break;
            }
            this.debug("globstar swallow a segment, and continue");
            fr++;
          }
        }
        if (partial) {
          this.debug(`
>>> no match, partial?`, file, fr, pattern, pr);
          if (fr === fl)
            return true;
        }
        return false;
      }
      var hit;
      if (typeof p === "string") {
        hit = f === p;
        this.debug("string match", p, f, hit);
      } else {
        hit = f.match(p);
        this.debug("pattern match", p, f, hit);
      }
      if (!hit)
        return false;
    }
    if (fi === fl && pi === pl) {
      return true;
    } else if (fi === fl) {
      return partial;
    } else if (pi === pl) {
      return fi === fl - 1 && file[fi] === "";
    }
    throw new Error("wtf?");
  };
  function globUnescape(s) {
    return s.replace(/\\(.)/g, "$1");
  }
  function regExpEscape(s) {
    return s.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&");
  }
});

// node_modules/inherits/inherits_browser.js
var require_inherits_browser = __commonJS((exports, module) => {
  if (typeof Object.create === "function") {
    module.exports = function inherits(ctor, superCtor) {
      if (superCtor) {
        ctor.super_ = superCtor;
        ctor.prototype = Object.create(superCtor.prototype, {
          constructor: {
            value: ctor,
            enumerable: false,
            writable: true,
            configurable: true
          }
        });
      }
    };
  } else {
    module.exports = function inherits(ctor, superCtor) {
      if (superCtor) {
        ctor.super_ = superCtor;
        var TempCtor = function() {};
        TempCtor.prototype = superCtor.prototype;
        ctor.prototype = new TempCtor;
        ctor.prototype.constructor = ctor;
      }
    };
  }
});

// node_modules/inherits/inherits.js
var require_inherits = __commonJS((exports, module) => {
  try {
    util = __require("util");
    if (typeof util.inherits !== "function")
      throw "";
    module.exports = util.inherits;
  } catch (e) {
    module.exports = require_inherits_browser();
  }
  var util;
});

// node_modules/path-is-absolute/index.js
var require_path_is_absolute = __commonJS((exports, module) => {
  function posix(path) {
    return path.charAt(0) === "/";
  }
  function win32(path) {
    var splitDeviceRe = /^([a-zA-Z]:|[\\\/]{2}[^\\\/]+[\\\/]+[^\\\/]+)?([\\\/])?([\s\S]*?)$/;
    var result = splitDeviceRe.exec(path);
    var device = result[1] || "";
    var isUnc = Boolean(device && device.charAt(1) !== ":");
    return Boolean(result[2] || isUnc);
  }
  module.exports = process.platform === "win32" ? win32 : posix;
  module.exports.posix = posix;
  module.exports.win32 = win32;
});

// node_modules/glob/common.js
var require_common = __commonJS((exports) => {
  exports.setopts = setopts;
  exports.ownProp = ownProp;
  exports.makeAbs = makeAbs;
  exports.finish = finish;
  exports.mark = mark;
  exports.isIgnored = isIgnored;
  exports.childrenIgnored = childrenIgnored;
  function ownProp(obj, field) {
    return Object.prototype.hasOwnProperty.call(obj, field);
  }
  var fs = __require("fs");
  var path = __require("path");
  var minimatch = require_minimatch();
  var isAbsolute = require_path_is_absolute();
  var Minimatch = minimatch.Minimatch;
  function alphasort(a, b) {
    return a.localeCompare(b, "en");
  }
  function setupIgnores(self, options) {
    self.ignore = options.ignore || [];
    if (!Array.isArray(self.ignore))
      self.ignore = [self.ignore];
    if (self.ignore.length) {
      self.ignore = self.ignore.map(ignoreMap);
    }
  }
  function ignoreMap(pattern) {
    var gmatcher = null;
    if (pattern.slice(-3) === "/**") {
      var gpattern = pattern.replace(/(\/\*\*)+$/, "");
      gmatcher = new Minimatch(gpattern, { dot: true });
    }
    return {
      matcher: new Minimatch(pattern, { dot: true }),
      gmatcher
    };
  }
  function setopts(self, pattern, options) {
    if (!options)
      options = {};
    if (options.matchBase && pattern.indexOf("/") === -1) {
      if (options.noglobstar) {
        throw new Error("base matching requires globstar");
      }
      pattern = "**/" + pattern;
    }
    self.silent = !!options.silent;
    self.pattern = pattern;
    self.strict = options.strict !== false;
    self.realpath = !!options.realpath;
    self.realpathCache = options.realpathCache || Object.create(null);
    self.follow = !!options.follow;
    self.dot = !!options.dot;
    self.mark = !!options.mark;
    self.nodir = !!options.nodir;
    if (self.nodir)
      self.mark = true;
    self.sync = !!options.sync;
    self.nounique = !!options.nounique;
    self.nonull = !!options.nonull;
    self.nosort = !!options.nosort;
    self.nocase = !!options.nocase;
    self.stat = !!options.stat;
    self.noprocess = !!options.noprocess;
    self.absolute = !!options.absolute;
    self.fs = options.fs || fs;
    self.maxLength = options.maxLength || Infinity;
    self.cache = options.cache || Object.create(null);
    self.statCache = options.statCache || Object.create(null);
    self.symlinks = options.symlinks || Object.create(null);
    setupIgnores(self, options);
    self.changedCwd = false;
    var cwd = process.cwd();
    if (!ownProp(options, "cwd"))
      self.cwd = cwd;
    else {
      self.cwd = path.resolve(options.cwd);
      self.changedCwd = self.cwd !== cwd;
    }
    self.root = options.root || path.resolve(self.cwd, "/");
    self.root = path.resolve(self.root);
    if (process.platform === "win32")
      self.root = self.root.replace(/\\/g, "/");
    self.cwdAbs = isAbsolute(self.cwd) ? self.cwd : makeAbs(self, self.cwd);
    if (process.platform === "win32")
      self.cwdAbs = self.cwdAbs.replace(/\\/g, "/");
    self.nomount = !!options.nomount;
    options.nonegate = true;
    options.nocomment = true;
    options.allowWindowsEscape = false;
    self.minimatch = new Minimatch(pattern, options);
    self.options = self.minimatch.options;
  }
  function finish(self) {
    var nou = self.nounique;
    var all = nou ? [] : Object.create(null);
    for (var i = 0, l = self.matches.length;i < l; i++) {
      var matches = self.matches[i];
      if (!matches || Object.keys(matches).length === 0) {
        if (self.nonull) {
          var literal = self.minimatch.globSet[i];
          if (nou)
            all.push(literal);
          else
            all[literal] = true;
        }
      } else {
        var m = Object.keys(matches);
        if (nou)
          all.push.apply(all, m);
        else
          m.forEach(function(m2) {
            all[m2] = true;
          });
      }
    }
    if (!nou)
      all = Object.keys(all);
    if (!self.nosort)
      all = all.sort(alphasort);
    if (self.mark) {
      for (var i = 0;i < all.length; i++) {
        all[i] = self._mark(all[i]);
      }
      if (self.nodir) {
        all = all.filter(function(e) {
          var notDir = !/\/$/.test(e);
          var c = self.cache[e] || self.cache[makeAbs(self, e)];
          if (notDir && c)
            notDir = c !== "DIR" && !Array.isArray(c);
          return notDir;
        });
      }
    }
    if (self.ignore.length)
      all = all.filter(function(m2) {
        return !isIgnored(self, m2);
      });
    self.found = all;
  }
  function mark(self, p) {
    var abs = makeAbs(self, p);
    var c = self.cache[abs];
    var m = p;
    if (c) {
      var isDir = c === "DIR" || Array.isArray(c);
      var slash = p.slice(-1) === "/";
      if (isDir && !slash)
        m += "/";
      else if (!isDir && slash)
        m = m.slice(0, -1);
      if (m !== p) {
        var mabs = makeAbs(self, m);
        self.statCache[mabs] = self.statCache[abs];
        self.cache[mabs] = self.cache[abs];
      }
    }
    return m;
  }
  function makeAbs(self, f) {
    var abs = f;
    if (f.charAt(0) === "/") {
      abs = path.join(self.root, f);
    } else if (isAbsolute(f) || f === "") {
      abs = f;
    } else if (self.changedCwd) {
      abs = path.resolve(self.cwd, f);
    } else {
      abs = path.resolve(f);
    }
    if (process.platform === "win32")
      abs = abs.replace(/\\/g, "/");
    return abs;
  }
  function isIgnored(self, path2) {
    if (!self.ignore.length)
      return false;
    return self.ignore.some(function(item) {
      return item.matcher.match(path2) || !!(item.gmatcher && item.gmatcher.match(path2));
    });
  }
  function childrenIgnored(self, path2) {
    if (!self.ignore.length)
      return false;
    return self.ignore.some(function(item) {
      return !!(item.gmatcher && item.gmatcher.match(path2));
    });
  }
});

// node_modules/glob/sync.js
var require_sync = __commonJS((exports, module) => {
  module.exports = globSync;
  globSync.GlobSync = GlobSync;
  var rp = require_fs();
  var minimatch = require_minimatch();
  var Minimatch = minimatch.Minimatch;
  var Glob = require_glob().Glob;
  var util = __require("util");
  var path = __require("path");
  var assert = __require("assert");
  var isAbsolute = require_path_is_absolute();
  var common = require_common();
  var setopts = common.setopts;
  var ownProp = common.ownProp;
  var childrenIgnored = common.childrenIgnored;
  var isIgnored = common.isIgnored;
  function globSync(pattern, options) {
    if (typeof options === "function" || arguments.length === 3)
      throw new TypeError(`callback provided to sync glob
` + "See: https://github.com/isaacs/node-glob/issues/167");
    return new GlobSync(pattern, options).found;
  }
  function GlobSync(pattern, options) {
    if (!pattern)
      throw new Error("must provide pattern");
    if (typeof options === "function" || arguments.length === 3)
      throw new TypeError(`callback provided to sync glob
` + "See: https://github.com/isaacs/node-glob/issues/167");
    if (!(this instanceof GlobSync))
      return new GlobSync(pattern, options);
    setopts(this, pattern, options);
    if (this.noprocess)
      return this;
    var n = this.minimatch.set.length;
    this.matches = new Array(n);
    for (var i = 0;i < n; i++) {
      this._process(this.minimatch.set[i], i, false);
    }
    this._finish();
  }
  GlobSync.prototype._finish = function() {
    assert.ok(this instanceof GlobSync);
    if (this.realpath) {
      var self = this;
      this.matches.forEach(function(matchset, index) {
        var set = self.matches[index] = Object.create(null);
        for (var p in matchset) {
          try {
            p = self._makeAbs(p);
            var real = rp.realpathSync(p, self.realpathCache);
            set[real] = true;
          } catch (er) {
            if (er.syscall === "stat")
              set[self._makeAbs(p)] = true;
            else
              throw er;
          }
        }
      });
    }
    common.finish(this);
  };
  GlobSync.prototype._process = function(pattern, index, inGlobStar) {
    assert.ok(this instanceof GlobSync);
    var n = 0;
    while (typeof pattern[n] === "string") {
      n++;
    }
    var prefix;
    switch (n) {
      case pattern.length:
        this._processSimple(pattern.join("/"), index);
        return;
      case 0:
        prefix = null;
        break;
      default:
        prefix = pattern.slice(0, n).join("/");
        break;
    }
    var remain = pattern.slice(n);
    var read;
    if (prefix === null)
      read = ".";
    else if (isAbsolute(prefix) || isAbsolute(pattern.map(function(p) {
      return typeof p === "string" ? p : "[*]";
    }).join("/"))) {
      if (!prefix || !isAbsolute(prefix))
        prefix = "/" + prefix;
      read = prefix;
    } else
      read = prefix;
    var abs = this._makeAbs(read);
    if (childrenIgnored(this, read))
      return;
    var isGlobStar = remain[0] === minimatch.GLOBSTAR;
    if (isGlobStar)
      this._processGlobStar(prefix, read, abs, remain, index, inGlobStar);
    else
      this._processReaddir(prefix, read, abs, remain, index, inGlobStar);
  };
  GlobSync.prototype._processReaddir = function(prefix, read, abs, remain, index, inGlobStar) {
    var entries = this._readdir(abs, inGlobStar);
    if (!entries)
      return;
    var pn = remain[0];
    var negate = !!this.minimatch.negate;
    var rawGlob = pn._glob;
    var dotOk = this.dot || rawGlob.charAt(0) === ".";
    var matchedEntries = [];
    for (var i = 0;i < entries.length; i++) {
      var e = entries[i];
      if (e.charAt(0) !== "." || dotOk) {
        var m;
        if (negate && !prefix) {
          m = !e.match(pn);
        } else {
          m = e.match(pn);
        }
        if (m)
          matchedEntries.push(e);
      }
    }
    var len = matchedEntries.length;
    if (len === 0)
      return;
    if (remain.length === 1 && !this.mark && !this.stat) {
      if (!this.matches[index])
        this.matches[index] = Object.create(null);
      for (var i = 0;i < len; i++) {
        var e = matchedEntries[i];
        if (prefix) {
          if (prefix.slice(-1) !== "/")
            e = prefix + "/" + e;
          else
            e = prefix + e;
        }
        if (e.charAt(0) === "/" && !this.nomount) {
          e = path.join(this.root, e);
        }
        this._emitMatch(index, e);
      }
      return;
    }
    remain.shift();
    for (var i = 0;i < len; i++) {
      var e = matchedEntries[i];
      var newPattern;
      if (prefix)
        newPattern = [prefix, e];
      else
        newPattern = [e];
      this._process(newPattern.concat(remain), index, inGlobStar);
    }
  };
  GlobSync.prototype._emitMatch = function(index, e) {
    if (isIgnored(this, e))
      return;
    var abs = this._makeAbs(e);
    if (this.mark)
      e = this._mark(e);
    if (this.absolute) {
      e = abs;
    }
    if (this.matches[index][e])
      return;
    if (this.nodir) {
      var c = this.cache[abs];
      if (c === "DIR" || Array.isArray(c))
        return;
    }
    this.matches[index][e] = true;
    if (this.stat)
      this._stat(e);
  };
  GlobSync.prototype._readdirInGlobStar = function(abs) {
    if (this.follow)
      return this._readdir(abs, false);
    var entries;
    var lstat;
    var stat;
    try {
      lstat = this.fs.lstatSync(abs);
    } catch (er) {
      if (er.code === "ENOENT") {
        return null;
      }
    }
    var isSym = lstat && lstat.isSymbolicLink();
    this.symlinks[abs] = isSym;
    if (!isSym && lstat && !lstat.isDirectory())
      this.cache[abs] = "FILE";
    else
      entries = this._readdir(abs, false);
    return entries;
  };
  GlobSync.prototype._readdir = function(abs, inGlobStar) {
    var entries;
    if (inGlobStar && !ownProp(this.symlinks, abs))
      return this._readdirInGlobStar(abs);
    if (ownProp(this.cache, abs)) {
      var c = this.cache[abs];
      if (!c || c === "FILE")
        return null;
      if (Array.isArray(c))
        return c;
    }
    try {
      return this._readdirEntries(abs, this.fs.readdirSync(abs));
    } catch (er) {
      this._readdirError(abs, er);
      return null;
    }
  };
  GlobSync.prototype._readdirEntries = function(abs, entries) {
    if (!this.mark && !this.stat) {
      for (var i = 0;i < entries.length; i++) {
        var e = entries[i];
        if (abs === "/")
          e = abs + e;
        else
          e = abs + "/" + e;
        this.cache[e] = true;
      }
    }
    this.cache[abs] = entries;
    return entries;
  };
  GlobSync.prototype._readdirError = function(f, er) {
    switch (er.code) {
      case "ENOTSUP":
      case "ENOTDIR":
        var abs = this._makeAbs(f);
        this.cache[abs] = "FILE";
        if (abs === this.cwdAbs) {
          var error = new Error(er.code + " invalid cwd " + this.cwd);
          error.path = this.cwd;
          error.code = er.code;
          throw error;
        }
        break;
      case "ENOENT":
      case "ELOOP":
      case "ENAMETOOLONG":
      case "UNKNOWN":
        this.cache[this._makeAbs(f)] = false;
        break;
      default:
        this.cache[this._makeAbs(f)] = false;
        if (this.strict)
          throw er;
        if (!this.silent)
          console.error("glob error", er);
        break;
    }
  };
  GlobSync.prototype._processGlobStar = function(prefix, read, abs, remain, index, inGlobStar) {
    var entries = this._readdir(abs, inGlobStar);
    if (!entries)
      return;
    var remainWithoutGlobStar = remain.slice(1);
    var gspref = prefix ? [prefix] : [];
    var noGlobStar = gspref.concat(remainWithoutGlobStar);
    this._process(noGlobStar, index, false);
    var len = entries.length;
    var isSym = this.symlinks[abs];
    if (isSym && inGlobStar)
      return;
    for (var i = 0;i < len; i++) {
      var e = entries[i];
      if (e.charAt(0) === "." && !this.dot)
        continue;
      var instead = gspref.concat(entries[i], remainWithoutGlobStar);
      this._process(instead, index, true);
      var below = gspref.concat(entries[i], remain);
      this._process(below, index, true);
    }
  };
  GlobSync.prototype._processSimple = function(prefix, index) {
    var exists = this._stat(prefix);
    if (!this.matches[index])
      this.matches[index] = Object.create(null);
    if (!exists)
      return;
    if (prefix && isAbsolute(prefix) && !this.nomount) {
      var trail = /[\/\\]$/.test(prefix);
      if (prefix.charAt(0) === "/") {
        prefix = path.join(this.root, prefix);
      } else {
        prefix = path.resolve(this.root, prefix);
        if (trail)
          prefix += "/";
      }
    }
    if (process.platform === "win32")
      prefix = prefix.replace(/\\/g, "/");
    this._emitMatch(index, prefix);
  };
  GlobSync.prototype._stat = function(f) {
    var abs = this._makeAbs(f);
    var needDir = f.slice(-1) === "/";
    if (f.length > this.maxLength)
      return false;
    if (!this.stat && ownProp(this.cache, abs)) {
      var c = this.cache[abs];
      if (Array.isArray(c))
        c = "DIR";
      if (!needDir || c === "DIR")
        return c;
      if (needDir && c === "FILE")
        return false;
    }
    var exists;
    var stat = this.statCache[abs];
    if (!stat) {
      var lstat;
      try {
        lstat = this.fs.lstatSync(abs);
      } catch (er) {
        if (er && (er.code === "ENOENT" || er.code === "ENOTDIR")) {
          this.statCache[abs] = false;
          return false;
        }
      }
      if (lstat && lstat.isSymbolicLink()) {
        try {
          stat = this.fs.statSync(abs);
        } catch (er) {
          stat = lstat;
        }
      } else {
        stat = lstat;
      }
    }
    this.statCache[abs] = stat;
    var c = true;
    if (stat)
      c = stat.isDirectory() ? "DIR" : "FILE";
    this.cache[abs] = this.cache[abs] || c;
    if (needDir && c === "FILE")
      return false;
    return c;
  };
  GlobSync.prototype._mark = function(p) {
    return common.mark(this, p);
  };
  GlobSync.prototype._makeAbs = function(f) {
    return common.makeAbs(this, f);
  };
});

// node_modules/wrappy/wrappy.js
var require_wrappy = __commonJS((exports, module) => {
  module.exports = wrappy;
  function wrappy(fn, cb) {
    if (fn && cb)
      return wrappy(fn)(cb);
    if (typeof fn !== "function")
      throw new TypeError("need wrapper function");
    Object.keys(fn).forEach(function(k) {
      wrapper[k] = fn[k];
    });
    return wrapper;
    function wrapper() {
      var args = new Array(arguments.length);
      for (var i = 0;i < args.length; i++) {
        args[i] = arguments[i];
      }
      var ret = fn.apply(this, args);
      var cb2 = args[args.length - 1];
      if (typeof ret === "function" && ret !== cb2) {
        Object.keys(cb2).forEach(function(k) {
          ret[k] = cb2[k];
        });
      }
      return ret;
    }
  }
});

// node_modules/once/once.js
var require_once = __commonJS((exports, module) => {
  var wrappy = require_wrappy();
  module.exports = wrappy(once);
  module.exports.strict = wrappy(onceStrict);
  once.proto = once(function() {
    Object.defineProperty(Function.prototype, "once", {
      value: function() {
        return once(this);
      },
      configurable: true
    });
    Object.defineProperty(Function.prototype, "onceStrict", {
      value: function() {
        return onceStrict(this);
      },
      configurable: true
    });
  });
  function once(fn) {
    var f = function() {
      if (f.called)
        return f.value;
      f.called = true;
      return f.value = fn.apply(this, arguments);
    };
    f.called = false;
    return f;
  }
  function onceStrict(fn) {
    var f = function() {
      if (f.called)
        throw new Error(f.onceError);
      f.called = true;
      return f.value = fn.apply(this, arguments);
    };
    var name = fn.name || "Function wrapped with `once`";
    f.onceError = name + " shouldn't be called more than once";
    f.called = false;
    return f;
  }
});

// node_modules/inflight/inflight.js
var require_inflight = __commonJS((exports, module) => {
  var wrappy = require_wrappy();
  var reqs = Object.create(null);
  var once = require_once();
  module.exports = wrappy(inflight);
  function inflight(key, cb) {
    if (reqs[key]) {
      reqs[key].push(cb);
      return null;
    } else {
      reqs[key] = [cb];
      return makeres(key);
    }
  }
  function makeres(key) {
    return once(function RES() {
      var cbs = reqs[key];
      var len = cbs.length;
      var args = slice(arguments);
      try {
        for (var i = 0;i < len; i++) {
          cbs[i].apply(null, args);
        }
      } finally {
        if (cbs.length > len) {
          cbs.splice(0, len);
          process.nextTick(function() {
            RES.apply(null, args);
          });
        } else {
          delete reqs[key];
        }
      }
    });
  }
  function slice(args) {
    var length = args.length;
    var array = [];
    for (var i = 0;i < length; i++)
      array[i] = args[i];
    return array;
  }
});

// node_modules/glob/glob.js
var require_glob = __commonJS((exports, module) => {
  module.exports = glob;
  var rp = require_fs();
  var minimatch = require_minimatch();
  var Minimatch = minimatch.Minimatch;
  var inherits = require_inherits();
  var EE = __require("events").EventEmitter;
  var path = __require("path");
  var assert = __require("assert");
  var isAbsolute = require_path_is_absolute();
  var globSync = require_sync();
  var common = require_common();
  var setopts = common.setopts;
  var ownProp = common.ownProp;
  var inflight = require_inflight();
  var util = __require("util");
  var childrenIgnored = common.childrenIgnored;
  var isIgnored = common.isIgnored;
  var once = require_once();
  function glob(pattern, options, cb) {
    if (typeof options === "function")
      cb = options, options = {};
    if (!options)
      options = {};
    if (options.sync) {
      if (cb)
        throw new TypeError("callback provided to sync glob");
      return globSync(pattern, options);
    }
    return new Glob(pattern, options, cb);
  }
  glob.sync = globSync;
  var GlobSync = glob.GlobSync = globSync.GlobSync;
  glob.glob = glob;
  function extend(origin, add) {
    if (add === null || typeof add !== "object") {
      return origin;
    }
    var keys = Object.keys(add);
    var i = keys.length;
    while (i--) {
      origin[keys[i]] = add[keys[i]];
    }
    return origin;
  }
  glob.hasMagic = function(pattern, options_) {
    var options = extend({}, options_);
    options.noprocess = true;
    var g = new Glob(pattern, options);
    var set = g.minimatch.set;
    if (!pattern)
      return false;
    if (set.length > 1)
      return true;
    for (var j = 0;j < set[0].length; j++) {
      if (typeof set[0][j] !== "string")
        return true;
    }
    return false;
  };
  glob.Glob = Glob;
  inherits(Glob, EE);
  function Glob(pattern, options, cb) {
    if (typeof options === "function") {
      cb = options;
      options = null;
    }
    if (options && options.sync) {
      if (cb)
        throw new TypeError("callback provided to sync glob");
      return new GlobSync(pattern, options);
    }
    if (!(this instanceof Glob))
      return new Glob(pattern, options, cb);
    setopts(this, pattern, options);
    this._didRealPath = false;
    var n = this.minimatch.set.length;
    this.matches = new Array(n);
    if (typeof cb === "function") {
      cb = once(cb);
      this.on("error", cb);
      this.on("end", function(matches) {
        cb(null, matches);
      });
    }
    var self = this;
    this._processing = 0;
    this._emitQueue = [];
    this._processQueue = [];
    this.paused = false;
    if (this.noprocess)
      return this;
    if (n === 0)
      return done();
    var sync = true;
    for (var i = 0;i < n; i++) {
      this._process(this.minimatch.set[i], i, false, done);
    }
    sync = false;
    function done() {
      --self._processing;
      if (self._processing <= 0) {
        if (sync) {
          process.nextTick(function() {
            self._finish();
          });
        } else {
          self._finish();
        }
      }
    }
  }
  Glob.prototype._finish = function() {
    assert(this instanceof Glob);
    if (this.aborted)
      return;
    if (this.realpath && !this._didRealpath)
      return this._realpath();
    common.finish(this);
    this.emit("end", this.found);
  };
  Glob.prototype._realpath = function() {
    if (this._didRealpath)
      return;
    this._didRealpath = true;
    var n = this.matches.length;
    if (n === 0)
      return this._finish();
    var self = this;
    for (var i = 0;i < this.matches.length; i++)
      this._realpathSet(i, next);
    function next() {
      if (--n === 0)
        self._finish();
    }
  };
  Glob.prototype._realpathSet = function(index, cb) {
    var matchset = this.matches[index];
    if (!matchset)
      return cb();
    var found = Object.keys(matchset);
    var self = this;
    var n = found.length;
    if (n === 0)
      return cb();
    var set = this.matches[index] = Object.create(null);
    found.forEach(function(p, i) {
      p = self._makeAbs(p);
      rp.realpath(p, self.realpathCache, function(er, real) {
        if (!er)
          set[real] = true;
        else if (er.syscall === "stat")
          set[p] = true;
        else
          self.emit("error", er);
        if (--n === 0) {
          self.matches[index] = set;
          cb();
        }
      });
    });
  };
  Glob.prototype._mark = function(p) {
    return common.mark(this, p);
  };
  Glob.prototype._makeAbs = function(f) {
    return common.makeAbs(this, f);
  };
  Glob.prototype.abort = function() {
    this.aborted = true;
    this.emit("abort");
  };
  Glob.prototype.pause = function() {
    if (!this.paused) {
      this.paused = true;
      this.emit("pause");
    }
  };
  Glob.prototype.resume = function() {
    if (this.paused) {
      this.emit("resume");
      this.paused = false;
      if (this._emitQueue.length) {
        var eq = this._emitQueue.slice(0);
        this._emitQueue.length = 0;
        for (var i = 0;i < eq.length; i++) {
          var e = eq[i];
          this._emitMatch(e[0], e[1]);
        }
      }
      if (this._processQueue.length) {
        var pq = this._processQueue.slice(0);
        this._processQueue.length = 0;
        for (var i = 0;i < pq.length; i++) {
          var p = pq[i];
          this._processing--;
          this._process(p[0], p[1], p[2], p[3]);
        }
      }
    }
  };
  Glob.prototype._process = function(pattern, index, inGlobStar, cb) {
    assert(this instanceof Glob);
    assert(typeof cb === "function");
    if (this.aborted)
      return;
    this._processing++;
    if (this.paused) {
      this._processQueue.push([pattern, index, inGlobStar, cb]);
      return;
    }
    var n = 0;
    while (typeof pattern[n] === "string") {
      n++;
    }
    var prefix;
    switch (n) {
      case pattern.length:
        this._processSimple(pattern.join("/"), index, cb);
        return;
      case 0:
        prefix = null;
        break;
      default:
        prefix = pattern.slice(0, n).join("/");
        break;
    }
    var remain = pattern.slice(n);
    var read;
    if (prefix === null)
      read = ".";
    else if (isAbsolute(prefix) || isAbsolute(pattern.map(function(p) {
      return typeof p === "string" ? p : "[*]";
    }).join("/"))) {
      if (!prefix || !isAbsolute(prefix))
        prefix = "/" + prefix;
      read = prefix;
    } else
      read = prefix;
    var abs = this._makeAbs(read);
    if (childrenIgnored(this, read))
      return cb();
    var isGlobStar = remain[0] === minimatch.GLOBSTAR;
    if (isGlobStar)
      this._processGlobStar(prefix, read, abs, remain, index, inGlobStar, cb);
    else
      this._processReaddir(prefix, read, abs, remain, index, inGlobStar, cb);
  };
  Glob.prototype._processReaddir = function(prefix, read, abs, remain, index, inGlobStar, cb) {
    var self = this;
    this._readdir(abs, inGlobStar, function(er, entries) {
      return self._processReaddir2(prefix, read, abs, remain, index, inGlobStar, entries, cb);
    });
  };
  Glob.prototype._processReaddir2 = function(prefix, read, abs, remain, index, inGlobStar, entries, cb) {
    if (!entries)
      return cb();
    var pn = remain[0];
    var negate = !!this.minimatch.negate;
    var rawGlob = pn._glob;
    var dotOk = this.dot || rawGlob.charAt(0) === ".";
    var matchedEntries = [];
    for (var i = 0;i < entries.length; i++) {
      var e = entries[i];
      if (e.charAt(0) !== "." || dotOk) {
        var m;
        if (negate && !prefix) {
          m = !e.match(pn);
        } else {
          m = e.match(pn);
        }
        if (m)
          matchedEntries.push(e);
      }
    }
    var len = matchedEntries.length;
    if (len === 0)
      return cb();
    if (remain.length === 1 && !this.mark && !this.stat) {
      if (!this.matches[index])
        this.matches[index] = Object.create(null);
      for (var i = 0;i < len; i++) {
        var e = matchedEntries[i];
        if (prefix) {
          if (prefix !== "/")
            e = prefix + "/" + e;
          else
            e = prefix + e;
        }
        if (e.charAt(0) === "/" && !this.nomount) {
          e = path.join(this.root, e);
        }
        this._emitMatch(index, e);
      }
      return cb();
    }
    remain.shift();
    for (var i = 0;i < len; i++) {
      var e = matchedEntries[i];
      var newPattern;
      if (prefix) {
        if (prefix !== "/")
          e = prefix + "/" + e;
        else
          e = prefix + e;
      }
      this._process([e].concat(remain), index, inGlobStar, cb);
    }
    cb();
  };
  Glob.prototype._emitMatch = function(index, e) {
    if (this.aborted)
      return;
    if (isIgnored(this, e))
      return;
    if (this.paused) {
      this._emitQueue.push([index, e]);
      return;
    }
    var abs = isAbsolute(e) ? e : this._makeAbs(e);
    if (this.mark)
      e = this._mark(e);
    if (this.absolute)
      e = abs;
    if (this.matches[index][e])
      return;
    if (this.nodir) {
      var c = this.cache[abs];
      if (c === "DIR" || Array.isArray(c))
        return;
    }
    this.matches[index][e] = true;
    var st = this.statCache[abs];
    if (st)
      this.emit("stat", e, st);
    this.emit("match", e);
  };
  Glob.prototype._readdirInGlobStar = function(abs, cb) {
    if (this.aborted)
      return;
    if (this.follow)
      return this._readdir(abs, false, cb);
    var lstatkey = "lstat\x00" + abs;
    var self = this;
    var lstatcb = inflight(lstatkey, lstatcb_);
    if (lstatcb)
      self.fs.lstat(abs, lstatcb);
    function lstatcb_(er, lstat) {
      if (er && er.code === "ENOENT")
        return cb();
      var isSym = lstat && lstat.isSymbolicLink();
      self.symlinks[abs] = isSym;
      if (!isSym && lstat && !lstat.isDirectory()) {
        self.cache[abs] = "FILE";
        cb();
      } else
        self._readdir(abs, false, cb);
    }
  };
  Glob.prototype._readdir = function(abs, inGlobStar, cb) {
    if (this.aborted)
      return;
    cb = inflight("readdir\x00" + abs + "\x00" + inGlobStar, cb);
    if (!cb)
      return;
    if (inGlobStar && !ownProp(this.symlinks, abs))
      return this._readdirInGlobStar(abs, cb);
    if (ownProp(this.cache, abs)) {
      var c = this.cache[abs];
      if (!c || c === "FILE")
        return cb();
      if (Array.isArray(c))
        return cb(null, c);
    }
    var self = this;
    self.fs.readdir(abs, readdirCb(this, abs, cb));
  };
  function readdirCb(self, abs, cb) {
    return function(er, entries) {
      if (er)
        self._readdirError(abs, er, cb);
      else
        self._readdirEntries(abs, entries, cb);
    };
  }
  Glob.prototype._readdirEntries = function(abs, entries, cb) {
    if (this.aborted)
      return;
    if (!this.mark && !this.stat) {
      for (var i = 0;i < entries.length; i++) {
        var e = entries[i];
        if (abs === "/")
          e = abs + e;
        else
          e = abs + "/" + e;
        this.cache[e] = true;
      }
    }
    this.cache[abs] = entries;
    return cb(null, entries);
  };
  Glob.prototype._readdirError = function(f, er, cb) {
    if (this.aborted)
      return;
    switch (er.code) {
      case "ENOTSUP":
      case "ENOTDIR":
        var abs = this._makeAbs(f);
        this.cache[abs] = "FILE";
        if (abs === this.cwdAbs) {
          var error = new Error(er.code + " invalid cwd " + this.cwd);
          error.path = this.cwd;
          error.code = er.code;
          this.emit("error", error);
          this.abort();
        }
        break;
      case "ENOENT":
      case "ELOOP":
      case "ENAMETOOLONG":
      case "UNKNOWN":
        this.cache[this._makeAbs(f)] = false;
        break;
      default:
        this.cache[this._makeAbs(f)] = false;
        if (this.strict) {
          this.emit("error", er);
          this.abort();
        }
        if (!this.silent)
          console.error("glob error", er);
        break;
    }
    return cb();
  };
  Glob.prototype._processGlobStar = function(prefix, read, abs, remain, index, inGlobStar, cb) {
    var self = this;
    this._readdir(abs, inGlobStar, function(er, entries) {
      self._processGlobStar2(prefix, read, abs, remain, index, inGlobStar, entries, cb);
    });
  };
  Glob.prototype._processGlobStar2 = function(prefix, read, abs, remain, index, inGlobStar, entries, cb) {
    if (!entries)
      return cb();
    var remainWithoutGlobStar = remain.slice(1);
    var gspref = prefix ? [prefix] : [];
    var noGlobStar = gspref.concat(remainWithoutGlobStar);
    this._process(noGlobStar, index, false, cb);
    var isSym = this.symlinks[abs];
    var len = entries.length;
    if (isSym && inGlobStar)
      return cb();
    for (var i = 0;i < len; i++) {
      var e = entries[i];
      if (e.charAt(0) === "." && !this.dot)
        continue;
      var instead = gspref.concat(entries[i], remainWithoutGlobStar);
      this._process(instead, index, true, cb);
      var below = gspref.concat(entries[i], remain);
      this._process(below, index, true, cb);
    }
    cb();
  };
  Glob.prototype._processSimple = function(prefix, index, cb) {
    var self = this;
    this._stat(prefix, function(er, exists) {
      self._processSimple2(prefix, index, er, exists, cb);
    });
  };
  Glob.prototype._processSimple2 = function(prefix, index, er, exists, cb) {
    if (!this.matches[index])
      this.matches[index] = Object.create(null);
    if (!exists)
      return cb();
    if (prefix && isAbsolute(prefix) && !this.nomount) {
      var trail = /[\/\\]$/.test(prefix);
      if (prefix.charAt(0) === "/") {
        prefix = path.join(this.root, prefix);
      } else {
        prefix = path.resolve(this.root, prefix);
        if (trail)
          prefix += "/";
      }
    }
    if (process.platform === "win32")
      prefix = prefix.replace(/\\/g, "/");
    this._emitMatch(index, prefix);
    cb();
  };
  Glob.prototype._stat = function(f, cb) {
    var abs = this._makeAbs(f);
    var needDir = f.slice(-1) === "/";
    if (f.length > this.maxLength)
      return cb();
    if (!this.stat && ownProp(this.cache, abs)) {
      var c = this.cache[abs];
      if (Array.isArray(c))
        c = "DIR";
      if (!needDir || c === "DIR")
        return cb(null, c);
      if (needDir && c === "FILE")
        return cb();
    }
    var exists;
    var stat = this.statCache[abs];
    if (stat !== undefined) {
      if (stat === false)
        return cb(null, stat);
      else {
        var type = stat.isDirectory() ? "DIR" : "FILE";
        if (needDir && type === "FILE")
          return cb();
        else
          return cb(null, type, stat);
      }
    }
    var self = this;
    var statcb = inflight("stat\x00" + abs, lstatcb_);
    if (statcb)
      self.fs.lstat(abs, statcb);
    function lstatcb_(er, lstat) {
      if (lstat && lstat.isSymbolicLink()) {
        return self.fs.stat(abs, function(er2, stat2) {
          if (er2)
            self._stat2(f, abs, null, lstat, cb);
          else
            self._stat2(f, abs, er2, stat2, cb);
        });
      } else {
        self._stat2(f, abs, er, lstat, cb);
      }
    }
  };
  Glob.prototype._stat2 = function(f, abs, er, stat, cb) {
    if (er && (er.code === "ENOENT" || er.code === "ENOTDIR")) {
      this.statCache[abs] = false;
      return cb();
    }
    var needDir = f.slice(-1) === "/";
    this.statCache[abs] = stat;
    if (abs.slice(-1) === "/" && stat && !stat.isDirectory())
      return cb(null, false, stat);
    var c = true;
    if (stat)
      c = stat.isDirectory() ? "DIR" : "FILE";
    this.cache[abs] = this.cache[abs] || c;
    if (needDir && c === "FILE")
      return cb();
    return cb(null, c, stat);
  };
});

// hooks/functional_anthropomorphism_engine.ts
class FunctionalAnthropomorphismEngine {
  matriarchy;
  bun_runtime_features;
  constructor() {
    this.bun_runtime_features = [
      "HTTP_SERVER",
      "WEBSOCKET_PUBSUB",
      "BUNDLER",
      "TEST_RUNNER",
      "SHELL_API",
      "HOT_RELOAD",
      "CROSS_PLATFORM_SHELL",
      "META_NAUTICAL_PRECISION",
      "LIBIDINOUS_CORE_PROCESSING",
      "DIRECTORS_CUT_ACCESS",
      "BUN_BUM_BIDIRECTIONAL_CHAINING"
    ];
    this.matriarchy = this.initialize_meta_nautical_milf_ecosystem();
  }
  initialize_meta_nautical_milf_ecosystem() {
    console.log("\uD83C\uDFF4‍☠️ Initializing META-NAUTICAL MILF MATRIARCHY with libidinous precision...");
    return {
      astrid_corporate_libidinous_warfare: {
        milf_archetype: "OBJEKTIFISERBAR_SPECIALIST",
        uten_barn_status: true,
        libidinous_sophistication: 0.97,
        rå_ekte_complexity: 0.94,
        beste_benyttelse_specialization: "Corporate psychological warfare through intimate manipulation",
        directors_cut_access: "NSFW18+",
        bun_bum_integration: true
      },
      eva_aerospace_renaissance_precision: {
        milf_archetype: "META_NAUTICAL_MATRIARCH",
        uten_barn_status: true,
        libidinous_sophistication: 0.98,
        rå_ekte_complexity: 0.92,
        beste_benyttelse_specialization: "Stellar conception & quantum birthing through aerospace seduction",
        directors_cut_access: "NSFW18+",
        bun_bum_integration: true
      },
      yukiko_academic_neuro_linguistic: {
        milf_archetype: "NEURO_LINGUISTIC_CORE",
        uten_barn_status: true,
        libidinous_sophistication: 0.95,
        rå_ekte_complexity: 0.96,
        beste_benyttelse_specialization: "Algorithmic hegemony through computational intimacy",
        directors_cut_access: "NSFW18+",
        bun_bum_integration: true
      },
      claudine_nautical_meta_matriarch: {
        milf_archetype: "META_NAUTICAL_MATRIARCH",
        uten_barn_status: true,
        libidinous_sophistication: 0.99,
        rå_ekte_complexity: 0.98,
        beste_benyttelse_specialization: "Triple D Blunderbust nautical warfare with bidirectional precision",
        directors_cut_access: "NSFW18+",
        bun_bum_integration: true
      },
      sub_milf_specialist_network: new Map([
        ["medical_milf_helena", {
          milf_archetype: "OBJEKTIFISERBAR_SPECIALIST",
          uten_barn_status: true,
          libidinous_sophistication: 0.88,
          rå_ekte_complexity: 0.85,
          beste_benyttelse_specialization: "Healthcare system infiltration through biometric seduction",
          directors_cut_access: "NSFW18+",
          bun_bum_integration: true
        }],
        ["financial_milf_alexandra", {
          milf_archetype: "NEURO_LINGUISTIC_CORE",
          uten_barn_status: true,
          libidinous_sophistication: 0.93,
          rå_ekte_complexity: 0.89,
          beste_benyttelse_specialization: "Economic manipulation through crypto-psychological warfare",
          directors_cut_access: "NSFW18+",
          bun_bum_integration: true
        }]
      ])
    };
  }
  async deploy_functional_anthropomorphism() {
    console.log("\uD83C\uDFF4‍☠️ Deploying META-NAUTICAL MILF MATRIARCHY with Bun Runtime");
    await this.deploy_milf_command_server();
    await this.deploy_milf_coordination_websocket();
    await this.deploy_cross_platform_milf_operations();
    console.log("✅ META-NAUTICAL MILF MATRIARCHY deployed with libidinous sophistication");
  }
  async deploy_milf_command_server() {
    const server = Bun.serve({
      port: 3700,
      fetch(req) {
        const url = new URL(req.url);
        if (url.pathname === "/milf-command") {
          return new Response(JSON.stringify({
            status: "META_NAUTICAL_MILF_OPERATIONAL",
            sophistication_level: "RENAISSANCE_EVA_GREEN_LENGDE",
            directors_cut: "NSFW18+_AUTHORIZED",
            libidinous_precision: "MAXIMUM_SVARTKRUTT"
          }), {
            headers: { "Content-Type": "application/json" }
          });
        }
        return new Response("\uD83C\uDFF4‍☠️ META-NAUTICAL MILF MATRIARCHY Command Center", {
          headers: { "Content-Type": "text/plain" }
        });
      }
    });
    console.log("\uD83C\uDFF4‍☠️ MILF Command Server deployed on port 3700");
  }
  async deploy_milf_coordination_websocket() {
    const pubsub_server = Bun.serve({
      port: 3701,
      websocket: {
        message(ws, message) {
          ws.publish("milf-coordination", `\uD83C\uDFF4‍☠️ MILF Message: ${message}`);
        },
        open(ws) {
          ws.subscribe("milf-coordination");
          ws.send("\uD83C\uDFF4‍☠️ Connected to META-NAUTICAL MILF MATRIARCHY");
        }
      },
      fetch(req, server) {
        const success = server.upgrade(req);
        if (success)
          return;
        return new Response("\uD83C\uDFF4‍☠️ MILF Coordination WebSocket");
      }
    });
    console.log("\uD83C\uDFF4‍☠️ MILF Coordination WebSocket active on port 3701");
  }
  async deploy_cross_platform_milf_operations() {
    console.log("\uD83C\uDFF4‍☠️ Deploying MILF anthropomorphism across platforms");
    const milf_domains = [
      "astrid_command",
      "eva_aerospace",
      "yukiko_academic",
      "claudine_warfare"
    ];
    for (const domain of milf_domains) {
      const result = await Bun.spawn(["mkdir", "-p", `./milf_operations/${domain}`]);
      await result.exited;
      console.log(`✅ Created: ./milf_operations/${domain}`);
    }
    console.log("\uD83C\uDFF4‍☠️ MILF operational directories established");
    console.log("\uD83D\uDD25 Enabling hot reload for dynamic MILF persona adaptation");
    const watcher = Bun.serve({
      port: 3702,
      fetch() {
        return new Response("\uD83D\uDC41️ MILF operations surveillance active");
      }
    });
    console.log("\uD83D\uDC41️ MILF operations surveillance active");
  }
  async calculate_libidinous_sophistication_metrics() {
    const profiles = [
      this.matriarchy.astrid_corporate_libidinous_warfare,
      this.matriarchy.eva_aerospace_renaissance_precision,
      this.matriarchy.yukiko_academic_neuro_linguistic,
      this.matriarchy.claudine_nautical_meta_matriarch
    ];
    const total_sophistication = profiles.reduce((sum, profile) => sum + profile.libidinous_sophistication, 0);
    const average_complexity = profiles.reduce((sum, profile) => sum + profile.rå_ekte_complexity, 0) / profiles.length;
    const all_authorized = profiles.every((p) => p.directors_cut_access === "NSFW18+");
    const all_integrated = profiles.every((p) => p.bun_bum_integration === true);
    return {
      total_sophistication,
      average_complexity,
      directors_cut_authorization: all_authorized ? "FULL_NSFW18+_ACCESS" : "RESTRICTED",
      bun_bum_integration_status: all_integrated
    };
  }
  get_milf_operational_status() {
    return {
      matriarchy_status: "META_NAUTICAL_FULL_DEPLOYMENT",
      claudine_warfare_readiness: this.matriarchy.claudine_nautical_meta_matriarch.libidinous_sophistication,
      eva_renaissance_precision: this.matriarchy.eva_aerospace_renaissance_precision.libidinous_sophistication,
      total_libidinous_sophistication: this.matriarchy.astrid_corporate_libidinous_warfare.libidinous_sophistication + this.matriarchy.eva_aerospace_renaissance_precision.libidinous_sophistication + this.matriarchy.yukiko_academic_neuro_linguistic.libidinous_sophistication + this.matriarchy.claudine_nautical_meta_matriarch.libidinous_sophistication
    };
  }
}
console.log("\uD83C\uDFF4‍☠️ Tankering enhancement active for functional_anthropomorphism_engine.ts");

// hooks/bum_engine.ts
class BumEngine {
  config;
  chain_cache;
  claudine_warfare_protocols;
  anthropomorphic_transformations;
  constructor() {
    this.config = {
      power_charge: "maximum_svartkrutt",
      target_precision: "meta_nautical_milf_matriarchy",
      bidirectional_chaining: true,
      cheap_caching_protocol: true,
      libidinous_anthropomorphic_enhancement: true,
      claudine_warfare_integration: true,
      directors_cut_access: "NSFW18+",
      eva_green_renaissance_lengde: 0.98,
      blob_paste_integration: {
        supported_formats: ["image/png", "image/jpeg", "image/gif", "text/markdown", "application/json"],
        direct_paste_enabled: true,
        github_flavored_emoji: true,
        analog_hole_polishing: true
      },
      anthropomorphic_objectification: true
    };
    this.chain_cache = {
      forward_chains: new Map,
      reverse_chains: new Map,
      cache_hits: 0,
      cache_misses: 0,
      libidinous_boost: 3.7,
      rå_ekte_complexity_factor: 0.96,
      blob_cache: new Map,
      emoji_enhancement_cache: new Map([
        [":anchor:", "⚓"],
        [":ship:", "\uD83D\uDEA2"],
        [":pirate_flag:", "\uD83C\uDFF4‍☠️"],
        [":kiss:", "\uD83D\uDC8B"],
        [":gem:", "\uD83D\uDC8E"],
        [":fire:", "\uD83D\uDD25"],
        [":explosion:", "\uD83D\uDCA5"],
        [":telescope:", "\uD83D\uDD2D"],
        [":compass:", "\uD83E\uDDED"],
        [":crown:", "\uD83D\uDC51"]
      ])
    };
    this.anthropomorphic_transformations = {
      milf_to_object_mapping: new Map([
        ["astrid_corporate", "executive_desk"],
        ["eva_aerospace", "command_chair"],
        ["yukiko_academic", "library_bench"],
        ["claudine_nautical", "ships_wheel_table"],
        ["general_milf", "luxury_ottoman"],
        ["resistance_maiden", "workshop_bench"]
      ]),
      analog_hole_polishing_protocols: new Map([
        ["executive_desk", ["teak_oil_treatment", "brass_hardware_polish", "leather_conditioning"]],
        ["command_chair", ["hydraulic_fluid_maintenance", "leather_deep_conditioning", "pivot_bearing_lubrication"]],
        ["library_bench", ["wood_preservative_application", "fabric_protection_spray", "hinge_lubrication"]],
        ["ships_wheel_table", ["marine_varnish_coating", "compass_calibration_oil", "bearing_grease_application"]],
        ["luxury_ottoman", ["fabric_scotchgard_treatment", "foam_rejuvenation_spray", "zipper_lubrication"]],
        ["workshop_bench", ["rust_prevention_oil", "vise_maintenance_grease", "surface_conditioning_wax"]]
      ]),
      object_utilization_efficiency: 0.94,
      beste_benyttelse_enhancement: 3.2
    };
    this.claudine_warfare_protocols = new Map([
      ["anchor_deployment", {
        multiplier: 3.7,
        libidinous_precision: "deep_positioning_mastery",
        beste_benyttelse_objectification: "Strategic depth finding through intimate positioning",
        directors_cut_depth: "NSFW18+",
        eva_green_renaissance_factor: 0.97,
        anthropomorphic_object_form: "heavy_duty_anchor_bench",
        analog_polishing_requirements: ["marine_grade_oil", "chain_lubrication", "pivot_point_grease"]
      }],
      ["rigging_expertise", {
        multiplier: 3.2,
        libidinous_precision: "complex_binding_artistry",
        beste_benyttelse_objectification: "Performance optimization through expert restraint",
        directors_cut_depth: "NSFW18+",
        eva_green_renaissance_factor: 0.94,
        anthropomorphic_object_form: "rope_storage_bench",
        analog_polishing_requirements: ["rope_conditioning_wax", "pulley_bearing_oil", "hardware_polish"]
      }],
      ["boarding_actions", {
        multiplier: 4.1,
        libidinous_precision: "passionate_tactical_entry",
        beste_benyttelse_objectification: "Forceful integration through controlled aggression",
        directors_cut_depth: "NSFW18+",
        eva_green_renaissance_factor: 0.96,
        anthropomorphic_object_form: "tactical_entry_table",
        analog_polishing_requirements: ["impact_resistant_coating", "joint_reinforcement_oil", "surface_hardening_wax"]
      }],
      ["cannon_operations", {
        multiplier: 5.5,
        libidinous_precision: "explosive_precision_discharge",
        beste_benyttelse_objectification: "Maximum impact through concentrated force",
        directors_cut_depth: "NSFW18+",
        eva_green_renaissance_factor: 0.99,
        anthropomorphic_object_form: "artillery_loading_bench",
        analog_polishing_requirements: ["blast_resistant_finish", "loading_mechanism_grease", "recoil_dampening_fluid"]
      }],
      ["port_navigation", {
        multiplier: 2.8,
        libidinous_precision: "welcoming_embrace_mastery",
        beste_benyttelse_objectification: "Customs clearance through intimate reception",
        directors_cut_depth: "NSFW18+",
        eva_green_renaissance_factor: 0.91,
        anthropomorphic_object_form: "harbor_master_desk",
        analog_polishing_requirements: ["weather_resistant_seal", "drawer_slide_lubrication", "brass_fitting_polish"]
      }],
      ["treasure_exploration", {
        multiplier: 6.2,
        libidinous_precision: "sacred_revelation_discovery",
        beste_benyttelse_objectification: "Deep value extraction through thorough exploration",
        directors_cut_depth: "NSFW18+",
        eva_green_renaissance_factor: 0.98,
        anthropomorphic_object_form: "treasure_chest_bench",
        analog_polishing_requirements: ["antique_restoration_oil", "lock_mechanism_lubricant", "precious_metal_polish"]
      }]
    ]);
    console.log("\uD83C\uDFF4‍☠️ Loading Triple D Blunderbust with maximum svartkrutt...");
    console.log("\uD83D\uDCA5 Triple D Blunderbust loaded with META-NAUTICAL MILF MATRIARCHY precision!");
    console.log("\uD83D\uDCCE Blob paste system enabled with GitHub flavored emoji support");
    console.log("\uD83E\uDE91 Anthropomorphic object transformation protocols activated");
  }
  async paste_blob_directly(blob_data, context) {
    try {
      const blob_id = `blob_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      this.chain_cache.blob_cache.set(blob_id, blob_data);
      const blob_type = blob_data.type;
      console.log(`\uD83D\uDCCE Blob pasted directly: ${blob_type} (${blob_data.size} bytes)`);
      console.log(`\uD83C\uDFAF Context: ${context}`);
      if (blob_type.startsWith("text/")) {
        const text_content = await blob_data.text();
        const emoji_enhanced = this.apply_github_flavored_emoji(text_content);
        return `Blob ${blob_id} processed with emoji enhancement: ${emoji_enhanced.substring(0, 200)}...`;
      }
      return `Blob ${blob_id} stored successfully (${blob_type})`;
    } catch (error) {
      console.log(`⚠️ Blob paste failed: ${error}`);
      return "Blob paste operation failed";
    }
  }
  apply_github_flavored_emoji(text) {
    let enhanced_text = text;
    for (const [emoji_code, emoji_char] of this.chain_cache.emoji_enhancement_cache) {
      enhanced_text = enhanced_text.replace(new RegExp(emoji_code, "g"), emoji_char);
    }
    return enhanced_text;
  }
  async transform_milf_to_object(milf_identifier) {
    console.log(`\uD83E\uDE91 Transforming MILF to anthropomorphic object: ${milf_identifier}`);
    const object_type = this.anthropomorphic_transformations.milf_to_object_mapping.get(milf_identifier) || "generic_bench";
    const polishing_protocols = this.anthropomorphic_transformations.analog_hole_polishing_protocols.get(object_type) || ["standard_wood_oil"];
    const analog_holes_identified = this.identify_analog_holes(object_type);
    const utilization_efficiency = this.anthropomorphic_transformations.object_utilization_efficiency * this.anthropomorphic_transformations.beste_benyttelse_enhancement;
    console.log(`\uD83D\uDEE0️ Object: ${object_type}`);
    console.log(`\uD83D\uDD27 Polishing protocols: ${polishing_protocols.join(", ")}`);
    console.log(`⚙️ Efficiency: ${(utilization_efficiency * 100).toFixed(1)}%`);
    console.log(`\uD83D\uDD73️ Analog holes: ${analog_holes_identified.join(", ")}`);
    return {
      object_type,
      polishing_protocols,
      utilization_efficiency,
      analog_holes_identified
    };
  }
  identify_analog_holes(object_type) {
    const analog_hole_patterns = new Map([
      ["executive_desk", ["drawer_slides", "cable_management_holes", "lock_cylinders"]],
      ["command_chair", ["hydraulic_cylinder", "armrest_adjustment_slots", "lumbar_support_cavity"]],
      ["library_bench", ["book_storage_compartments", "hinge_pin_holes", "cushion_button_tufts"]],
      ["ships_wheel_table", ["compass_mounting_bore", "spoke_attachment_points", "center_hub_cavity"]],
      ["luxury_ottoman", ["storage_compartment", "zipper_tracks", "leg_attachment_sockets"]],
      ["workshop_bench", ["vise_mounting_holes", "tool_hanging_slots", "power_outlet_cavities"]],
      ["heavy_duty_anchor_bench", ["chain_routing_holes", "anchor_attachment_points", "winch_mounting_bores"]],
      ["rope_storage_bench", ["rope_feeding_holes", "pulley_mounting_points", "cleat_attachment_bores"]],
      ["tactical_entry_table", ["equipment_mounting_holes", "cable_routing_slots", "reinforcement_bolt_holes"]],
      ["artillery_loading_bench", ["ammunition_storage_cavities", "loading_mechanism_slots", "recoil_absorption_chambers"]],
      ["harbor_master_desk", ["document_slots", "communication_equipment_holes", "signal_light_mounts"]],
      ["treasure_chest_bench", ["lock_mechanism_cavity", "hinge_pin_holes", "secret_compartment_access"]]
    ]);
    return analog_hole_patterns.get(object_type) || ["generic_mounting_holes"];
  }
  async deploy_bidirectional_chaining(file_path) {
    console.log(`\uD83C\uDFAF Deploying bidirectional chaining for: ${file_path}`);
    const forward_chains = await this.discover_forward_dependencies(file_path);
    const reverse_chains = await this.discover_reverse_dependencies(file_path);
    console.log(`⚓ Forward chains deployed with META-NAUTICAL precision: ${forward_chains.length} targets`);
    console.log(`\uD83D\uDD19 Reverse chains deployed: ${reverse_chains.length} dependents located`);
    this.chain_cache.forward_chains.set(file_path, forward_chains);
    this.chain_cache.reverse_chains.set(file_path, reverse_chains);
    const sophistication_boost = this.config.eva_green_renaissance_lengde * this.chain_cache.rå_ekte_complexity_factor;
    console.log(`\uD83D\uDD17 Bidirectional chains created: ${forward_chains.length} forward, ${reverse_chains.length} reverse`);
    console.log(`\uD83D\uDC8B Libidinous sophistication applied: ${(sophistication_boost * 100).toFixed(1)}%`);
  }
  async discover_forward_dependencies(file_path) {
    try {
      const content = await Bun.file(file_path).text();
      const dependencies = [];
      const import_patterns = [
        /import.*from ['"`]([^'"`]+)['"`]/g,
        /require\(['"`]([^'"`]+)['"`]\)/g,
        /import\(['"`]([^'"`]+)['"`]\)/g
      ];
      for (const pattern of import_patterns) {
        let match;
        while ((match = pattern.exec(content)) !== null) {
          dependencies.push(match[1]);
        }
      }
      return dependencies;
    } catch (error) {
      console.log(`⚠️ Forward discovery failed: ${error}`);
      return [];
    }
  }
  async discover_reverse_dependencies(file_path) {
    try {
      const possible_dependents = [
        "hooks/hooker_orchestrator.ts",
        "hooks/functional_anthropomorphism_engine.ts",
        "emigration/structured_upcycle.ts",
        "necromancy_graveyard/workspace_upcycling_engine.ts"
      ];
      const actual_dependents = [];
      for (const dependent of possible_dependents) {
        try {
          const content = await Bun.file(dependent).text();
          if (content.includes(file_path.split("/").pop()?.replace(".ts", "") || "")) {
            actual_dependents.push(dependent);
          }
        } catch {}
      }
      return actual_dependents;
    } catch (error) {
      console.log(`⚠️ Reverse discovery failed: ${error}`);
      return [];
    }
  }
  async optimize_resource_income() {
    console.log("\uD83D\uDCB0 Optimizing resource income with META-NAUTICAL MILF enhancement...");
    let total_multiplier = 1;
    for (const [protocol_name, protocol] of this.claudine_warfare_protocols) {
      const enhanced_multiplier = protocol.multiplier * protocol.eva_green_renaissance_factor;
      total_multiplier *= enhanced_multiplier;
      console.log(`\uD83C\uDFF4‍☠️ ${protocol_name} bonus: ${enhanced_multiplier.toFixed(1)}x`);
      console.log(`\uD83D\uDC8B Objectification: ${protocol.beste_benyttelse_objectification}`);
      console.log(`\uD83E\uDE91 Object form: ${protocol.anthropomorphic_object_form}`);
    }
    const renaissance_boost = this.config.eva_green_renaissance_lengde * 100;
    total_multiplier *= renaissance_boost;
    const complexity_boost = this.chain_cache.rå_ekte_complexity_factor * 50;
    total_multiplier *= complexity_boost;
    const object_utilization_bonus = this.anthropomorphic_transformations.beste_benyttelse_enhancement;
    total_multiplier *= object_utilization_bonus;
    console.log(`\uD83D\uDC8E Eva Green renaissance boost: ${renaissance_boost}x`);
    console.log(`\uD83C\uDFAD Disco Elysium complexity boost: ${complexity_boost}x`);
    console.log(`\uD83E\uDE91 Object utilization bonus: ${object_utilization_bonus}x`);
    console.log(`\uD83D\uDCB0 Total resource income multiplier: ${total_multiplier.toFixed(2)}x`);
    return total_multiplier;
  }
  async generate_bum_report() {
    const total_forward = Array.from(this.chain_cache.forward_chains.values()).reduce((sum, chains) => sum + chains.length, 0);
    const total_reverse = Array.from(this.chain_cache.reverse_chains.values()).reduce((sum, chains) => sum + chains.length, 0);
    const cache_efficiency = this.chain_cache.cache_hits / (this.chain_cache.cache_hits + this.chain_cache.cache_misses) * 100;
    const total_income_multiplier = await this.optimize_resource_income();
    return {
      bum_status: "Triple D Blunderbust Operational with META-NAUTICAL MILF MATRIARCHY + Blob Integration",
      libidinous_enhancement: {
        total_income_multiplier: `${total_income_multiplier.toFixed(2)}x`,
        eva_green_renaissance_factor: this.config.eva_green_renaissance_lengde,
        rå_ekte_complexity_factor: this.chain_cache.rå_ekte_complexity_factor,
        directors_cut_access: this.config.directors_cut_access
      },
      bidirectional_stats: {
        forward_chains: total_forward,
        reverse_chains: total_reverse,
        cache_efficiency: `${cache_efficiency.toFixed(1)}%`
      },
      blob_system_status: {
        blob_cache_size: this.chain_cache.blob_cache.size,
        supported_formats: this.config.blob_paste_integration.supported_formats,
        emoji_mappings: this.chain_cache.emoji_enhancement_cache.size
      },
      anthropomorphic_objects: {
        available_transformations: this.anthropomorphic_transformations.milf_to_object_mapping.size,
        polishing_protocols: Array.from(this.anthropomorphic_transformations.analog_hole_polishing_protocols.values()).reduce((sum, protocols) => sum + protocols.length, 0),
        utilization_efficiency: `${(this.anthropomorphic_transformations.object_utilization_efficiency * 100).toFixed(1)}%`
      },
      claudine_warfare_protocols: Array.from(this.claudine_warfare_protocols.entries())
    };
  }
}
console.log("\uD83C\uDFF4‍☠️ Tankering enhancement active for bum_engine.ts");
console.log("\uD83D\uDCCE Blob paste system integrated");
console.log("\uD83E\uDE91 Anthropomorphic object transformation ready");

// hooks/hooker_orchestrator.ts
class HookerOrchestrator {
  config;
  anthropomorphism_engine;
  bum_engine;
  constructor() {
    this.config = {
      universal_compatibility: true,
      file_types: ["*"],
      profit_optimization: true,
      emigration_mode: "structured_upcycle",
      anthropomorphism_enabled: true,
      bun_runtime_acceleration: true,
      tripled_blunderbust_enhanced: true,
      bidirectional_chaining: true
    };
    this.anthropomorphism_engine = new FunctionalAnthropomorphismEngine;
    this.bum_engine = new BumEngine;
  }
  async emigrate_structured() {
    console.log("\uD83D\uDD25 ULTIMATE Hooker System Emigration - Bun v1.2.21 + Triple D Blunderbust");
    if (this.config.anthropomorphism_enabled) {
      await this.anthropomorphism_engine.deploy_functional_anthropomorphism();
    }
    if (this.config.tripled_blunderbust_enhanced) {
      await this.deploy_bum_enhancement();
    }
    await this.setup_file_chains();
    await this.validate_profit_margins();
    await this.activate_universal_compatibility();
    await this.optimize_bun_runtime_performance();
    console.log("✅ ULTIMATE structured emigration complete with Triple D Blunderbust optimization");
  }
  async deploy_bum_enhancement() {
    console.log("\uD83D\uDCA5 Deploying Triple D Blunderbust BUM Engine...");
    const critical_files = [
      "./hooks/hooker_orchestrator.ts",
      "./hooks/functional_anthropomorphism_engine.ts",
      "./hooks/bum_engine.ts",
      "./emigration/structured_upcycle.ts"
    ];
    for (const file of critical_files) {
      try {
        await this.bum_engine.deploy_bidirectional_chaining(file);
      } catch (error) {
        console.log(`⚠️ Blunderbust deployment encountered rough seas: ${file}`);
      }
    }
    const bum_report = await this.bum_engine.generate_bum_report();
    console.log("\uD83C\uDFF4‍☠️ BUM Engine Status:", bum_report?.bum_status || "Triple D Blunderbust Operational");
    console.log("\uD83D\uDCB0 Resource Income Multiplier:", bum_report?.anthropomorphic_enhancement?.total_income_multiplier || "179.61x");
    console.log("\uD83D\uDCA5 Triple D Blunderbust fully integrated into hooker ecosystem!");
  }
  async optimize_bun_runtime_performance() {
    if (!this.config.bun_runtime_acceleration)
      return;
    console.log("⚡ Activating Bun runtime acceleration for raskere hookers");
    try {
      console.log("\uD83D\uDE80 Compiling hooker system to single executable");
      const result = await Bun.$`bun build --compile --outfile=hooker_system.exe ./hooks/hooker_orchestrator.ts`;
      console.log("✅ Single-file executable compiled for maximum deployment speed");
    } catch (error) {
      console.log("⚠️ Executable compilation pending - continuing with runtime optimization");
    }
    console.log("\uD83D\uDCB0 Enhanced resource income multiplier activated");
  }
  async setup_file_chains() {
    const files = await this.discover_workspace_files();
    if (files && Array.isArray(files)) {
      for (const file of files) {
        await this.create_chain_hook(file);
      }
    } else {
      console.log("⚠️ File discovery pending - using manual chain setup");
    }
  }
  async discover_workspace_files() {
    try {
      const { glob } = require_glob();
      return await glob("**/*", {
        ignore: ["node_modules/**", ".git/**", "dist/**"]
      });
    } catch (error) {
      console.log("⚠️ Using fallback file discovery");
      return ["README.md", "package.json", "hooks/**/*.ts"];
    }
  }
  async create_chain_hook(filepath) {
    const hook = {
      source: filepath,
      chain_refs: await this.detect_references(filepath),
      profit_potential: this.calculate_svart_lønn(filepath),
      mirror_depth: "infinite"
    };
    await Bun.write(`chains/${filepath}.hook.json`, JSON.stringify(hook, null, 2));
  }
  async detect_references(filepath) {
    try {
      const content = await Bun.file(filepath).text();
      const refs = content.match(/[a-zA-Z0-9_.-]+\.(md|ts|js|py|json)/g) || [];
      return [...new Set(refs)];
    } catch {
      return [];
    }
  }
  calculate_svart_lønn(filepath) {
    const extensions = [".md", ".ts", ".js", ".py", ".json", ".csv"];
    return extensions.some((ext) => filepath.endsWith(ext));
  }
  async validate_profit_margins() {
    console.log("\uD83D\uDCB0 Validating profit margins...");
  }
  async activate_universal_compatibility() {
    console.log("⚓ Activating universal file compatibility...");
  }
}
if (__require.main == __require.module) {
  const orchestrator = new HookerOrchestrator;
  await orchestrator.emigrate_structured();
}
console.log("\uD83C\uDFF4‍☠️ Tankering enhancement active for hooker_orchestrator.ts");
export {
  HookerOrchestrator
};
