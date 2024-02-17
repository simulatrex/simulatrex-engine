import "ace-builds/src-noconflict/ace";
declare var ace: any;

ace.define(
  "ace/mode/simulatrex_highlight_rules",
  ["require", "exports", "ace/lib/oop", "ace/mode/text_highlight_rules"],
  function (require: any, exports: any) {
    var oop = require("ace/lib/oop");
    var TextHighlightRules =
      require("ace/mode/text_highlight_rules").TextHighlightRules;

    var SimulatrexHighlightRules = function () {
      this.$rules = {
        start: [
          {
            token: "keyword",
            regex: "\\b(?:Agent|Environment|Simulation)\\b",
          },
          {
            token: "string", // single line
            regex: '".*?"',
          },
          {
            token: "comment",
            regex: "//.*$",
          },
          {
            token: "constant.numeric", // float
            regex: "[+-]?\\d+(?:\\.\\d+)?(?:[eE][+-]?\\d+)?",
          },
        ],
      };
    };

    oop.inherits(SimulatrexHighlightRules, TextHighlightRules);

    exports.SimulatrexHighlightRules = SimulatrexHighlightRules;
  }
);

ace.define(
  "ace/mode/simulatrex",
  [
    "require",
    "exports",
    "ace/lib/oop",
    "ace/mode/text",
    "ace/mode/simulatrex_highlight_rules",
  ],
  function (require: any, exports: any) {
    var oop = require("ace/lib/oop");
    var TextMode = require("ace/mode/text").Mode;
    var SimulatrexHighlightRules =
      require("ace/mode/simulatrex_highlight_rules").SimulatrexHighlightRules;

    var Mode = function () {
      this.HighlightRules = SimulatrexHighlightRules;
    };

    oop.inherits(Mode, TextMode);

    (function () {
      this.$id = "ace/mode/simulatrex";
    }).call(Mode.prototype);

    exports.Mode = Mode;
  }
);
