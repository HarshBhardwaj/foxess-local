(window["webpackJsonp"] = window["webpackJsonp"] || []).push([
 ["setup"], {
  fd46: function(e, t, a) {
   "use strict";
   a.r(t);
   var l = function() {
     var e = this,
      t = e.$createElement,
      a = e._self._c || t;
     return a("div", {
      staticClass: "content"
     }, [a("el-form", {
      ref: "formModuleSetup",
      staticStyle: {
       width: "700px",
       "margin-left": "50px"
      },
      attrs: {
       model: e.formDataModuleSetup,
       "label-position": "left",
       "label-width": "160px"
      }
     }, [a("el-form-item", {
      attrs: {
       label: e.$t("setupModule.frequency")
      }
     }, [a("el-select", {
      staticStyle: {
       width: "120px"
      },
      model: {
       value: e.formDataModuleSetup.upload_freq,
       callback: function(t) {
        e.$set(e.formDataModuleSetup, "upload_freq", t)
       },
       expression: "formDataModuleSetup.upload_freq"
      }
     }, [a("el-option", {
      attrs: {
       label: "1",
       value: 1
      }
     }), a("el-option", {
      attrs: {
       label: "2",
       value: 2
      }
     }), a("el-option", {
      attrs: {
       label: "3",
       value: 3
      }
     }), a("el-option", {
      attrs: {
       label: "4",
       value: 4
      }
     }), a("el-option", {
      attrs: {
       label: "5",
       value: 5
      }
     }), a("el-option", {
      attrs: {
       label: "6",
       value: 6
      }
     }), a("el-option", {
      attrs: {
       label: "7",
       value: 7
      }
     }), a("el-option", {
      attrs: {
       label: "8",
       value: 8
      }
     }), a("el-option", {
      attrs: {
       label: "9",
       value: 9
      }
     }), a("el-option", {
      attrs: {
       label: "10",
       value: 10
      }
     }), a("el-option", {
      attrs: {
       label: "11",
       value: 11
      }
     }), a("el-option", {
      attrs: {
       label: "12",
       value: 12
      }
     }), a("el-option", {
      attrs: {
       label: "13",
       value: 13
      }
     }), a("el-option", {
      attrs: {
       label: "14",
       value: 14
      }
     }), a("el-option", {
      attrs: {
       label: "15",
       value: 15
      }
     })], 1), e._v(" " + e._s(e.$t("setupModule.unit")) + " ")], 1), a("el-form-item", {
      attrs: {
       label: e.$t("setupModule.domain")
      }
     }, [a("el-select", {
      staticStyle: {
       width: "220px"
      },
      model: {
       value: e.formDataModuleSetup.domain,
       callback: function(t) {
        e.$set(e.formDataModuleSetup, "domain", t)
       },
       expression: "formDataModuleSetup.domain"
      }
     }, [a("el-option", {
      attrs: {
       label: "8.209.116.72",
       value: "8.209.116.72"
      }
     }), a("el-option", {
      attrs: {
       label: "www.maitian-yun.com",
       value: "www.maitian-yun.com"
      }
     }), a("el-option", {
      attrs: {
       label: "test.maitian-yun.com",
       value: "test.maitian-yun.com"
      }
     })], 1)], 1), a("el-form-item", {
      attrs: {
       label: e.$t("setupModule.port")
      }
     }, [a("span", [e._v(e._s(e.formDataModuleSetup.port))])]), a("el-form-item", [a("el-button", {
      attrs: {
       type: "primary",
       size: "mini"
      },
      on: {
       click: e.moduleSetup
      }
     }, [e._v(e._s(e.$t("setupModule.setup")))])], 1)], 1)], 1)
    },
    r = [],
    o = a("1da1"),
    u = a("d4ec"),
    n = a("bee2"),
    i = a("262e"),
    s = a("2caf"),
    p = (a("96cf"), a("9ab4")),
    c = a("1b40"),
    d = a("5c96"),
    m = a("c952"),
    f = function(e) {
     Object(i["a"])(a, e);
     var t = Object(s["a"])(a);

     function a() {
      var e;
      return Object(u["a"])(this, a), e = t.apply(this, arguments), e.formDataModuleSetup = {
       upload_freq: 0,
       domain: "",
       port: 10001
      }, e.moduleModel = "", e.setNetPriority = !1, e
     }
     return Object(n["a"])(a, [{
      key: "created",
      value: function() {
       var e = Object(o["a"])(regeneratorRuntime.mark((function e() {
        var t;
        return regeneratorRuntime.wrap((function(e) {
         while (1) switch (e.prev = e.next) {
          case 0:
           return e.next = 2, Object(m["r"])();
          case 2:
           return t = e.sent, 0 === t.errno && (this.moduleModel = t.data.module, "Smart 4GWiLAN" === this.moduleModel && (this.setNetPriority = !0)), e.next = 6, this.getParam();
          case 6:
          case "end":
           return e.stop()
         }
        }), e, this)
       })));

       function t() {
        return e.apply(this, arguments)
       }
       return t
      }()
     }, {
      key: "getParam",
      value: function() {
       var e = Object(o["a"])(regeneratorRuntime.mark((function e() {
        var t;
        return regeneratorRuntime.wrap((function(e) {
         while (1) switch (e.prev = e.next) {
          case 0:
           return e.next = 2, Object(m["g"])();
          case 2:
           t = e.sent, 0 === t.errno && (this.formDataModuleSetup.upload_freq = t.data.upload_freq, this.formDataModuleSetup.domain = t.data.domain, this.formDataModuleSetup.port = t.data.port);
          case 4:
          case "end":
           return e.stop()
         }
        }), e, this)
       })));

       function t() {
        return e.apply(this, arguments)
       }
       return t
      }()
     }, {
      key: "moduleSetup",
      value: function() {
       var e = Object(o["a"])(regeneratorRuntime.mark((function e() {
        var t, a;
        return regeneratorRuntime.wrap((function(e) {
         while (1) switch (e.prev = e.next) {
          case 0:
           return t = {
            upload_freq: this.formDataModuleSetup.upload_freq,
            domain: this.formDataModuleSetup.domain
           }, e.next = 3, Object(m["q"])(t);
          case 3:
           a = e.sent, 0 === a.errno ? Object(d["Message"])({
            message: "Success",
            type: "success",
            duration: 5e3
           }) : Object(d["Message"])({
            message: "Setup fail",
            type: "error",
            duration: 5e3
           });
          case 5:
          case "end":
           return e.stop()
         }
        }), e, this)
       })));

       function t() {
        return e.apply(this, arguments)
       }
       return t
      }()
     }]), a
    }(c["c"]);
   f = Object(p["a"])([Object(c["a"])({
    name: "moduleSetup"
   })], f);
   var b = f,
    v = b,
    h = a("0c7c"),
    w = Object(h["a"])(v, l, r, !1, null, "5ca6caea", null);
   t["default"] = w.exports
  }
 }
]);