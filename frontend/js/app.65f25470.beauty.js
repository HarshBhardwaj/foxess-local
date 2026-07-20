(window["webpackJsonp"] = window["webpackJsonp"] || []).push([
 ["app"], {
  0: function(e, t, a) {
   e.exports = a("cd49")
  },
  "023d": function(e, t, a) {
   "use strict";
   a("0374")
  },
  "0374": function(e, t, a) {
   e.exports = {
    menuBg: "#304156",
    menuText: "#bfcbd9",
    menuActiveText: "#409eff"
   }
  },
  "0613": function(e, t, a) {
   "use strict";
   var r = a("2b0e"),
    n = a("2f62");
   r["default"].use(n["a"]), t["a"] = new n["a"].Store({
    state: {},
    getters: {},
    mutations: {},
    actions: {},
    modules: {}
   })
  },
  "0ff5": function(e, t, a) {
   "use strict";
   a("db8d")
  },
  1: function(e, t) {},
  10: function(e, t) {},
  1302: function(e, t, a) {},
  1497: function(e, t, a) {
   e.exports = {
    menuBg: "#304156",
    menuText: "#bfcbd9",
    menuActiveText: "#409eff"
   }
  },
  2: function(e, t) {},
  "20c1": function(e, t, a) {
   "use strict";
   a("35e0")
  },
  "232e": function(e, t, a) {},
  "24ab": function(e, t, a) {
   e.exports = {
    menuBg: "#304156",
    menuText: "#bfcbd9",
    menuActiveText: "#409eff",
    theme: "#1890ff"
   }
  },
  2769: function(e, t, a) {
   "use strict";
   a("2b41")
  },
  "2b41": function(e, t, a) {},
  "2d92": function(e, t, a) {
   "use strict";
   a("caad")
  },
  3: function(e, t) {},
  3308: function(e, t, a) {
   "use strict";
   a("455a")
  },
  "35e0": function(e, t, a) {},
  4: function(e, t) {},
  "455a": function(e, t, a) {},
  "4f20": function(e, t, a) {
   e.exports = {
    menuBg: "#304156",
    menuText: "#bfcbd9",
    menuActiveText: "#409eff"
   }
  },
  5: function(e, t) {},
  5581: function(e, t, a) {
   "use strict";
   a.d(t, "b", (function() {
    return c
   })), a.d(t, "f", (function() {
    return o
   })), a.d(t, "a", (function() {
    return u
   })), a.d(t, "e", (function() {
    return l
   })), a.d(t, "c", (function() {
    return h
   })), a.d(t, "g", (function() {
    return p
   })), a.d(t, "d", (function() {
    return v
   }));
   var r = a("a78e"),
    n = a.n(r),
    i = "sidebar_status",
    c = function() {
     return n.a.get(i)
    },
    o = function(e) {
     return n.a.set(i, e)
    },
    s = "language",
    u = function() {
     return n.a.get(s)
    },
    l = function(e) {
     return n.a.set(s, e)
    },
    d = "fox_energy_username",
    h = function() {
     return n.a.get(d)
    },
    p = function(e) {
     return n.a.set(d, e)
    },
    v = function() {
     return n.a.remove(d)
    }
  },
  "5c0b": function(e, t, a) {
   "use strict";
   a("1497")
  },
  6: function(e, t) {},
  "6ebf": function(e, t, a) {
   "use strict";
   a.d(t, "b", (function() {
    return v
   }));
   var r = a("5530"),
    n = (a("b64b"), a("2b0e")),
    i = a("a925"),
    c = a("5581"),
    o = a("b2d6"),
    s = a.n(o),
    u = a("f0d9"),
    l = a.n(u),
    d = {
     route: {
      sunspec: "Device Monitoring",
      config: "Config",
      configWifi: "Network",
      moduleSetup: "Setup",
      maintain: "Maintain",
      upgradeModule: "Module Upgrade",
      upgradeDevice: "Firmware Upgrade",
      upgradeWebserver: "Webserver Upgrade",
      deviceLog: "Device Log",
      downloadContent: "Download Content",
      systemInfo: "System Info",
      resetPassword: "Reset Password",
      about: "About",
      system: "System",
      device: "Device",
      inverterLog: "Inverter Log",
      faultRecorder: "Fault Record",
      overview: "Overview",
      currentAlarms: "Current Alarms"
     },
     login: {
      title: "Smart WiLAN",
      username: "username",
      password: "password",
      loginError: "Username or password error",
      login: "Login"
     },
     navbar: {
      changePassword: "Change password",
      logOut: "Logout"
     },
     common: {
      edit: "Edit",
      upload: "Upload",
      reload: "Reload",
      download: "Download",
      uploadWarning: "DO NOT RELOAD PAGE WHEN UPGRADING!!!"
     },
     table: {
      field: "Field",
      data: "Data",
      operation: "Opertation",
      dateTime: "Time",
      addr: "Address",
      errorCode: "Error Code",
      faultResume: "Fault / Resume",
      no: "No."
     },
     errorWaitSetting: "Waiting for previous setting finished. Try again later.",
     configNet: {
      title: "Config Station",
      netType: "Net Type",
      lan: "LAN",
      wifi: "WiFi",
      g4: "4G",
      setNetPriorityTitle: "Set Net Priority",
      netPriority: "Net Priority"
     },
     configWifi: {
      ssid: "SSID",
      psk: "password",
      ssidPlaceholder: "Please select the SSID",
      rssi: "RSSI",
      submitButton: "Config",
      mac: "MAC"
     },
     configIp: {
      dhcp: "DHCP",
      ip: "IP",
      submitButton: "Config"
     },
     configAp: {
      title: "Config AP",
      ssid: "SSID",
      psk: "Password",
      submitButton: "Config"
     },
     config4g: {
      title: "Config 4G",
      apnIPv: "IPv",
      apnName: "APN",
      apnUserId: "APN Username",
      apnPasswd: "APN Password",
      apnAuth: "APN Auth",
      submitButton: "Config",
      sim_ccid: "SIM CCID"
     },
     setupModule: {
      frequency: "Report frequency",
      unit: "min",
      domain: "Report domain",
      port: "Report port",
      setup: "Setup"
     },
     uploadModule: {
      uploadTip: "Please upload the module upgrade firmware file",
      startUpgrade: "Start upgrade module...",
      uploadSuccess: "Upgrade module success",
      uploadError: "Upgrade module error"
     },
     uploadWeb: {
      uploadTip: "Please upload the webserver upgrade firmware file",
      startUpgrade: "Start upgrade webserver...",
      uploadSuccess: "Upgrade webserver success",
      uploadError: "Upgrade webserver error"
     },
     uploadDevice: {
      uploadTip: "Please upload the device upgrade file",
      startUpgrade: "Start upload device upgrade file...",
      uploadSuccess: "Upload device upgrade file success",
      uploadError: "Upload device upgrade file error",
      upgradeFile: "Upgrade file: ",
      upgradeFileSuccess: " success",
      unzipFile: "Processing upload file...",
      unzipFail: "Process upload file error"
     },
     password: {
      oldPassword: "Old",
      newPassword: "New",
      confirmPassword: "Confirm",
      changePassword: "Change",
      adminPassword: "Admin Password",
      resetPassword: "Reset",
      resetUser: "Reset User"
     },
     about: {
      about: "About"
     }
    },
    h = {
     route: {
      sunspec: "Sunspec"
     }
    };
   n["default"].use(i["a"]);
   var p = {
     en: Object(r["a"])(Object(r["a"])({}, d), s.a),
     zh: Object(r["a"])(Object(r["a"])({}, h), l.a)
    },
    v = function() {
     var e = Object(c["a"])();
     if (e) return document.documentElement.lang = e, e;
     if (!e) return "en";
     for (var t = navigator.language.toLowerCase(), a = Object.keys(p), r = 0, n = a; r < n.length; r++) {
      var i = n[r];
      if (t.indexOf(i) > -1) return document.documentElement.lang = i, i
     }
     return "en"
    },
    m = new i["a"]({
     locale: v(),
     messages: p
    });
   t["a"] = m
  },
  7: function(e, t) {},
  8: function(e, t) {},
  9: function(e, t) {},
  9448: function(e, t, a) {
   "use strict";
   a("1302")
  },
  "9dba": function(e, t, a) {
   "use strict";
   a.d(t, "a", (function() {
    return f
   }));
   var r = a("1da1"),
    n = a("d4ec"),
    i = a("bee2"),
    c = a("262e"),
    o = a("2caf"),
    s = (a("96cf"), a("b0c0"), a("498a"), a("9ab4")),
    u = a("6fc5"),
    l = a("c952"),
    d = a("d257"),
    h = a("5581"),
    p = a("0613"),
    v = a("5c96"),
    m = function(e) {
     Object(c["a"])(a, e);
     var t = Object(o["a"])(a);

     function a() {
      var e;
      return Object(n["a"])(this, a), e = t.apply(this, arguments), e.name = Object(h["c"])() || "", e.avatar = "", e.roles = ["admin"], e
     }
     return Object(i["a"])(a, [{
      key: "SET_NAME",
      value: function(e) {
       this.name = e
      }
     }, {
      key: "Login",
      value: function() {
       var e = Object(r["a"])(regeneratorRuntime.mark((function e(t) {
        var a, r, n, i;
        return regeneratorRuntime.wrap((function(e) {
         while (1) switch (e.prev = e.next) {
          case 0:
           return a = t.username, r = t.password, a = a.trim(), n = Object(d["b"])(r), e.next = 5, Object(l["k"])({
            username: a,
            password: n
           });
          case 5:
           if (i = e.sent, console.log(i), 0 === i.errno && 0 === i.data.result) {
            e.next = 10;
            break
           }
           return Object(v["Message"])({
            message: "Username or password error",
            type: "error",
            duration: 5e3
           }), e.abrupt("return");
          case 10:
           Object(h["g"])(a), this.SET_NAME(a);
          case 12:
          case "end":
           return e.stop()
         }
        }), e, this)
       })));

       function t(t) {
        return e.apply(this, arguments)
       }
       return t
      }()
     }, {
      key: "SetName",
      value: function(e) {
       this.SET_NAME(e)
      }
     }, {
      key: "GetUserInfo",
      value: function() {
       var e = Object(r["a"])(regeneratorRuntime.mark((function e() {
        var t, a;
        return regeneratorRuntime.wrap((function(e) {
         while (1) switch (e.prev = e.next) {
          case 0:
           if (t = {
             name: "admin"
            }, t) {
            e.next = 3;
            break
           }
           throw Error("Verification failed, please Login again.");
          case 3:
           a = Object(h["c"])(), console.log(a), this.SET_NAME(a);
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
      key: "LogOut",
      value: function() {
       var e = Object(r["a"])(regeneratorRuntime.mark((function e() {
        return regeneratorRuntime.wrap((function(e) {
         while (1) switch (e.prev = e.next) {
          case 0:
           Object(h["d"])(), this.SET_NAME("");
          case 2:
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
    }(u["d"]);
   Object(s["a"])([u["c"]], m.prototype, "SET_NAME", null), Object(s["a"])([u["a"]], m.prototype, "Login", null), Object(s["a"])([u["a"]], m.prototype, "SetName", null), Object(s["a"])([u["a"]], m.prototype, "GetUserInfo", null), Object(s["a"])([u["a"]], m.prototype, "LogOut", null), m = Object(s["a"])([Object(u["b"])({
    dynamic: !0,
    store: p["a"],
    name: "user"
   })], m);
   var f = Object(u["e"])(m)
  },
  a1de: function(e, t, a) {
   e.exports = {
    menuBg: "#304156",
    menuText: "#bfcbd9",
    menuActiveText: "#409eff"
   }
  },
  adc6: function(e, t, a) {
   "use strict";
   a("232e")
  },
  b20f: function(e, t, a) {
   e.exports = {
    menuBg: "#304156",
    menuText: "#bfcbd9",
    menuActiveText: "#409eff"
   }
  },
  ba54: function(e, t, a) {
   "use strict";
   a("f749")
  },
  c952: function(e, t, a) {
   "use strict";
   a.d(t, "d", (function() {
    return u
   })), a.d(t, "c", (function() {
    return l
   })), a.d(t, "l", (function() {
    return d
   })), a.d(t, "p", (function() {
    return h
   })), a.d(t, "m", (function() {
    return p
   })), a.d(t, "i", (function() {
    return v
   })), a.d(t, "g", (function() {
    return m
   })), a.d(t, "q", (function() {
    return f
   })), a.d(t, "n", (function() {
    return g
   })), a.d(t, "j", (function() {
    return b
   })), a.d(t, "a", (function() {
    return w
   })), a.d(t, "r", (function() {
    return O
   })), a.d(t, "h", (function() {
    return z
   })), a.d(t, "k", (function() {
    return j
   })), a.d(t, "b", (function() {
    return H
   })), a.d(t, "o", (function() {
    return y
   })), a.d(t, "e", (function() {
    return M
   })), a.d(t, "f", (function() {
    return x
   }));
   var r = a("1da1"),
    n = (a("96cf"), a("99af"), a("d3b7"), a("bc3a")),
    i = a.n(n),
    c = a("5c96"),
    o = i.a.create({
     baseURL: "/api/v1/",
     timeout: 1e4
    });
   o.interceptors.response.use((function(e) {
    var t = e.data;
    return 0 !== t.errno ? (Object(c["Message"])({
     message: t.errmsg || t.message || "Error",
     type: "error",
     duration: 5e3
    }), 50008 !== t.code && 50012 !== t.code && 50014 !== t.code || c["MessageBox"].confirm("你已被登出，可以取消继续留在该页面，或者重新登录", "确定登出", {
     confirmButtonText: "重新登录",
     cancelButtonText: "取消",
     type: "warning"
    }).then((function() {
     location.reload()
    })), Promise.reject(new Error(t.message || "Error"))) : e.data
   }), (function(e) {
    return Object(c["Message"])({
     message: e.message,
     type: "error",
     duration: 5e3
    }), Promise.reject(e)
   }));
   var s = o,
    u = function() {
     return s({
      url: "/sunspec/devlist",
      method: "get"
     })
    },
    l = function(e) {
     return s({
      url: "/sunspec/data?addr=".concat(e.addr, "&id=").concat(e.id),
      method: "get"
     })
    },
    d = function(e) {
     return s({
      url: "/sunspec/modbus_rw",
      method: "post",
      data: e
     })
    },
    h = function() {
     var e = Object(r["a"])(regeneratorRuntime.mark((function e() {
      return regeneratorRuntime.wrap((function(e) {
       while (1) switch (e.prev = e.next) {
        case 0:
         return e.abrupt("return", s({
          url: "/sunspec/scanlist",
          method: "get"
         }));
        case 1:
        case "end":
         return e.stop()
       }
      }), e)
     })));
     return function() {
      return e.apply(this, arguments)
     }
    }(),
    p = function() {
     var e = Object(r["a"])(regeneratorRuntime.mark((function e(t) {
      return regeneratorRuntime.wrap((function(e) {
       while (1) switch (e.prev = e.next) {
        case 0:
         return e.abrupt("return", s({
          url: "/sunspec/net_config",
          method: "post",
          data: t
         }));
        case 1:
        case "end":
         return e.stop()
       }
      }), e)
     })));
     return function(t) {
      return e.apply(this, arguments)
     }
    }(),
    v = function() {
     var e = Object(r["a"])(regeneratorRuntime.mark((function e() {
      return regeneratorRuntime.wrap((function(e) {
       while (1) switch (e.prev = e.next) {
        case 0:
         return e.abrupt("return", s({
          url: "/sunspec/inv_upgrade_status",
          method: "get"
         }));
        case 1:
        case "end":
         return e.stop()
       }
      }), e)
     })));
     return function() {
      return e.apply(this, arguments)
     }
    }(),
    m = function() {
     var e = Object(r["a"])(regeneratorRuntime.mark((function e() {
      return regeneratorRuntime.wrap((function(e) {
       while (1) switch (e.prev = e.next) {
        case 0:
         return e.abrupt("return", s({
          url: "/sunspec/param_get",
          method: "get"
         }));
        case 1:
        case "end":
         return e.stop()
       }
      }), e)
     })));
     return function() {
      return e.apply(this, arguments)
     }
    }(),
    f = function() {
     var e = Object(r["a"])(regeneratorRuntime.mark((function e(t) {
      return regeneratorRuntime.wrap((function(e) {
       while (1) switch (e.prev = e.next) {
        case 0:
         return e.abrupt("return", s({
          url: "/sunspec/param_set",
          method: "post",
          data: t
         }));
        case 1:
        case "end":
         return e.stop()
       }
      }), e)
     })));
     return function(t) {
      return e.apply(this, arguments)
     }
    }(),
    g = function() {
     var e = Object(r["a"])(regeneratorRuntime.mark((function e() {
      return regeneratorRuntime.wrap((function(e) {
       while (1) switch (e.prev = e.next) {
        case 0:
         return e.abrupt("return", s({
          url: "/sunspec/net_status",
          method: "get"
         }));
        case 1:
        case "end":
         return e.stop()
       }
      }), e)
     })));
     return function() {
      return e.apply(this, arguments)
     }
    }(),
    b = function() {
     var e = Object(r["a"])(regeneratorRuntime.mark((function e(t) {
      return regeneratorRuntime.wrap((function(e) {
       while (1) switch (e.prev = e.next) {
        case 0:
         return e.abrupt("return", s({
          url: "/sunspec/ip_config",
          method: "post",
          data: t
         }));
        case 1:
        case "end":
         return e.stop()
       }
      }), e)
     })));
     return function(t) {
      return e.apply(this, arguments)
     }
    }(),
    w = function() {
     var e = Object(r["a"])(regeneratorRuntime.mark((function e(t) {
      return regeneratorRuntime.wrap((function(e) {
       while (1) switch (e.prev = e.next) {
        case 0:
         return e.abrupt("return", s({
          url: "/sunspec/ap_config",
          method: "post",
          data: t
         }));
        case 1:
        case "end":
         return e.stop()
       }
      }), e)
     })));
     return function(t) {
      return e.apply(this, arguments)
     }
    }(),
    O = function() {
     var e = Object(r["a"])(regeneratorRuntime.mark((function e() {
      return regeneratorRuntime.wrap((function(e) {
       while (1) switch (e.prev = e.next) {
        case 0:
         return e.abrupt("return", s({
          url: "/sunspec/sys_info",
          method: "get"
         }));
        case 1:
        case "end":
         return e.stop()
       }
      }), e)
     })));
     return function() {
      return e.apply(this, arguments)
     }
    }(),
    z = function() {
     var e = Object(r["a"])(regeneratorRuntime.mark((function e() {
      return regeneratorRuntime.wrap((function(e) {
       while (1) switch (e.prev = e.next) {
        case 0:
         return e.abrupt("return", s({
          url: "/sunspec/inv_file_list",
          method: "get"
         }));
        case 1:
        case "end":
         return e.stop()
       }
      }), e)
     })));
     return function() {
      return e.apply(this, arguments)
     }
    }(),
    j = function() {
     var e = Object(r["a"])(regeneratorRuntime.mark((function e(t) {
      return regeneratorRuntime.wrap((function(e) {
       while (1) switch (e.prev = e.next) {
        case 0:
         return e.abrupt("return", s({
          url: "/sunspec/login",
          method: "post",
          data: t
         }));
        case 1:
        case "end":
         return e.stop()
       }
      }), e)
     })));
     return function(t) {
      return e.apply(this, arguments)
     }
    }(),
    H = function() {
     var e = Object(r["a"])(regeneratorRuntime.mark((function e(t) {
      return regeneratorRuntime.wrap((function(e) {
       while (1) switch (e.prev = e.next) {
        case 0:
         return e.abrupt("return", s({
          url: "/sunspec/change_password",
          method: "post",
          data: t
         }));
        case 1:
        case "end":
         return e.stop()
       }
      }), e)
     })));
     return function(t) {
      return e.apply(this, arguments)
     }
    }(),
    y = function() {
     var e = Object(r["a"])(regeneratorRuntime.mark((function e(t) {
      return regeneratorRuntime.wrap((function(e) {
       while (1) switch (e.prev = e.next) {
        case 0:
         return e.abrupt("return", s({
          url: "/sunspec/reset_password",
          method: "post",
          data: t
         }));
        case 1:
        case "end":
         return e.stop()
       }
      }), e)
     })));
     return function(t) {
      return e.apply(this, arguments)
     }
    }(),
    M = function() {
     var e = Object(r["a"])(regeneratorRuntime.mark((function e(t) {
      return regeneratorRuntime.wrap((function(e) {
       while (1) switch (e.prev = e.next) {
        case 0:
         return e.abrupt("return", s({
          url: "/sunspec/log?addr=".concat(t.addr, "&type=3"),
          method: "get"
         }));
        case 1:
        case "end":
         return e.stop()
       }
      }), e)
     })));
     return function(t) {
      return e.apply(this, arguments)
     }
    }(),
    x = function() {
     var e = Object(r["a"])(regeneratorRuntime.mark((function e(t) {
      return regeneratorRuntime.wrap((function(e) {
       while (1) switch (e.prev = e.next) {
        case 0:
         return e.abrupt("return", s({
          url: "/sunspec/log?addr=".concat(t.addr, "&type=2"),
          method: "get"
         }));
        case 1:
        case "end":
         return e.stop()
       }
      }), e)
     })));
     return function(t) {
      return e.apply(this, arguments)
     }
    }()
  },
  caad: function(e, t, a) {},
  cd49: function(e, t, a) {
   "use strict";
   a.r(t);
   a("e260"), a("e6cf"), a("cca6"), a("a79d");
   var r = a("2b0e"),
    n = a("5c96"),
    i = a.n(n),
    c = a("038a"),
    o = a.n(c),
    s = (a("f5df1"), a("24ab"), a("b20f"), function() {
     var e = this,
      t = e.$createElement,
      a = e._self._c || t;
     return a("div", {
      attrs: {
       id: "app"
      }
     }, [a("router-view"), a("service-worker-update-popup")], 1)
    }),
    u = [],
    l = a("d4ec"),
    d = a("262e"),
    h = a("2caf"),
    p = a("9ab4"),
    v = a("1b40"),
    m = a("bee2"),
    f = function(e) {
     Object(d["a"])(a, e);
     var t = Object(h["a"])(a);

     function a() {
      var e;
      return Object(l["a"])(this, a), e = t.apply(this, arguments), e.refreshing = !1, e.notificationText = "系统更新了，请刷新GET新功能", e.refreshButtonText = "刷新", e.registration = null, e
     }
     return Object(m["a"])(a, [{
      key: "created",
      value: function() {
       var e = this;
       document.addEventListener("swUpdated", this.showRefreshUI, {
        once: !0
       }), navigator.serviceWorker.addEventListener("controllerchange", (function() {
        e.refreshing || (e.refreshing = !0, window.location.reload())
       }))
      }
     }, {
      key: "render",
      value: function() {}
     }, {
      key: "showRefreshUI",
      value: function(e) {
       var t = this,
        a = this.$createElement;
       this.registration = e.detail, this.$notify.info({
        title: "系统已更新",
        message: a("div", {
         class: "sw-update-popup"
        }, [this.notificationText, a("br"), a("button", {
         on: {
          click: function(e) {
           e.preventDefault(), t.refreshApp()
          }
         }
        }, this.refreshButtonText)]),
        position: "bottom-right",
        duration: 0
       })
      }
     }, {
      key: "refreshApp",
      value: function() {
       this.registration && this.registration.waiting && this.registration.waiting.postMessage("skipWaiting")
      }
     }]), a
    }(v["c"]);
   f = Object(p["a"])([Object(v["a"])({
    name: "ServiceWorkerUpdatePopup"
   })], f);
   var g, b, w = f,
    O = w,
    z = (a("9448"), a("0c7c")),
    j = Object(z["a"])(O, g, b, !1, null, "772d0b9a", null),
    H = j.exports,
    y = function(e) {
     Object(d["a"])(a, e);
     var t = Object(h["a"])(a);

     function a() {
      return Object(l["a"])(this, a), t.apply(this, arguments)
     }
     return a
    }(v["c"]);
   y = Object(p["a"])([Object(v["a"])({
    name: "App",
    components: {
     ServiceWorkerUpdatePopup: H
    }
   })], y);
   var M = y,
    x = M,
    V = (a("5c0b"), Object(z["a"])(x, s, u, !1, null, null, null)),
    k = V.exports,
    L = a("9483");
   Object(L["a"])("".concat("/", "service-worker.js"), {
    ready: function() {
     console.log("App is being served from cache by a service worker.\nFor more details, visit https://goo.gl/AFskqB")
    },
    registered: function() {
     console.log("Service worker has been registered.")
    },
    cached: function() {
     console.log("Content has been cached for offline use.")
    },
    updatefound: function() {
     console.log("New content is downloading.")
    },
    updated: function(e) {
     console.log("New content is available; please refresh."), document.dispatchEvent(new CustomEvent("swUpdated", {
      detail: e
     }))
    },
    offline: function() {
     console.log("No internet connection found. App is running in offline mode.")
    },
    error: function(e) {
     console.error("Error during service worker registration:", e)
    }
   });
   a("d3b7"), a("3ca3"), a("ddb0");
   var C = a("8c4f"),
    S = function() {
     var e = this,
      t = e.$createElement,
      a = e._self._c || t;
     return a("div", {
      staticClass: "app-wrapper",
      class: e.classObj
     }, [e.classObj.mobile && e.sidebar.opened ? a("div", {
      staticClass: "drawer-bg",
      on: {
       click: e.handleClickOutside
      }
     }) : e._e(), a("sidebar", {
      staticClass: "sidebar-container"
     }), a("div", {
      staticClass: "main-container"
     }, [a("div", [a("navbar")], 1), a("app-main", {
      staticStyle: {
       height: "calc(100% - 50px)"
      }
     })], 1)], 1)
    },
    A = [],
    B = a("2fe1"),
    E = function() {
     var e = this,
      t = e.$createElement,
      a = e._self._c || t;
     return a("section", {
      staticClass: "app-main"
     }, [a("transition", {
      attrs: {
       name: "fade-transform",
       mode: "out-in"
      }
     }, [a("keep-alive", [a("router-view", {
      key: e.key
     })], 1)], 1)], 1)
    },
    _ = [],
    R = function(e) {
     Object(d["a"])(a, e);
     var t = Object(h["a"])(a);

     function a() {
      return Object(l["a"])(this, a), t.apply(this, arguments)
     }
     return Object(m["a"])(a, [{
      key: "key",
      get: function() {
       return this.$route.path
      }
     }]), a
    }(v["c"]);
   R = Object(p["a"])([Object(v["a"])({
    name: "AppMain"
   })], R);
   var T, P = R,
    N = P,
    D = (a("20c1"), Object(z["a"])(N, E, _, !1, null, "39862ad2", null)),
    U = D.exports,
    I = function() {
     var e = this,
      t = e.$createElement,
      a = e._self._c || t;
     return a("div", {
      staticClass: "navbar"
     }, [a("hamburger", {
      staticClass: "hamburger-container",
      attrs: {
       id: "hamburger-container",
       "is-active": e.sidebar.opened
      },
      on: {
       "toggle-click": e.toggleSideBar
      }
     }), a("div", {
      staticClass: "right-menu"
     }, [a("el-dropdown", {
      staticClass: "avatar-container right-menu-item hover-effect",
      attrs: {
       trigger: "click"
      }
     }, [a("div", {
      staticClass: "avatar-wrapper"
     }, [a("i", {
      staticClass: "el-icon-user-solid"
     }), e._v(" " + e._s(e.userName) + " "), a("i", {
      staticClass: "el-icon-caret-bottom"
     })]), a("el-dropdown-menu", {
      attrs: {
       slot: "dropdown"
      },
      slot: "dropdown"
     }, [a("router-link", {
      attrs: {
       to: "/user/changepassword"
      }
     }, [a("el-dropdown-item", [e._v(" " + e._s(e.$t("navbar.changePassword")) + " ")])], 1), a("el-dropdown-item", {
      attrs: {
       divided: ""
      },
      nativeOn: {
       click: function(t) {
        return e.logout(t)
       }
      }
     }, [a("span", {
      staticStyle: {
       display: "block"
      }
     }, [e._v(" " + e._s(e.$t("navbar.logOut")) + " ")])])], 1)], 1)], 1)], 1)
    },
    G = [],
    W = a("1da1"),
    $ = (a("96cf"), a("b0c0"), a("6fc5")),
    q = a("5581"),
    F = a("6ebf"),
    J = a("0613");
   (function(e) {
    e[e["Mobile"] = 0] = "Mobile", e[e["Desktop"] = 1] = "Desktop"
   })(T || (T = {}));
   var K = function(e) {
    Object(d["a"])(a, e);
    var t = Object(h["a"])(a);

    function a() {
     var e;
     return Object(l["a"])(this, a), e = t.apply(this, arguments), e.sidebar = {
      opened: "closed" !== Object(q["b"])(),
      withoutAnimation: !1
     }, e.device = T.Desktop, e.language = Object(F["b"])(), e
    }
    return Object(m["a"])(a, [{
     key: "TOGGLE_SIDEBAR",
     value: function(e) {
      this.sidebar.opened = !this.sidebar.opened, this.sidebar.withoutAnimation = e, this.sidebar.opened ? Object(q["f"])("opened") : Object(q["f"])("closed")
     }
    }, {
     key: "CLOSE_SIDEBAR",
     value: function(e) {
      this.sidebar.opened = !1, this.sidebar.withoutAnimation = e, Object(q["f"])("closed")
     }
    }, {
     key: "TOGGLE_DEVICE",
     value: function(e) {
      this.device = e
     }
    }, {
     key: "SET_LANGUAGE",
     value: function(e) {
      this.language = e, Object(q["e"])(this.language)
     }
    }, {
     key: "ToggleSideBar",
     value: function(e) {
      this.TOGGLE_SIDEBAR(e)
     }
    }, {
     key: "CloseSideBar",
     value: function(e) {
      this.CLOSE_SIDEBAR(e)
     }
    }, {
     key: "ToggleDevice",
     value: function(e) {
      this.TOGGLE_DEVICE(e)
     }
    }, {
     key: "SetLanguage",
     value: function(e) {
      this.SET_LANGUAGE(e)
     }
    }]), a
   }($["d"]);
   Object(p["a"])([$["c"]], K.prototype, "TOGGLE_SIDEBAR", null), Object(p["a"])([$["c"]], K.prototype, "CLOSE_SIDEBAR", null), Object(p["a"])([$["c"]], K.prototype, "TOGGLE_DEVICE", null), Object(p["a"])([$["c"]], K.prototype, "SET_LANGUAGE", null), Object(p["a"])([$["a"]], K.prototype, "ToggleSideBar", null), Object(p["a"])([$["a"]], K.prototype, "CloseSideBar", null), Object(p["a"])([$["a"]], K.prototype, "ToggleDevice", null), Object(p["a"])([$["a"]], K.prototype, "SetLanguage", null), K = Object(p["a"])([Object($["b"])({
    dynamic: !0,
    store: J["a"],
    name: "app"
   })], K);
   var Q = Object($["e"])(K),
    X = a("9dba"),
    Y = function() {
     var e = this,
      t = e.$createElement,
      a = e._self._c || t;
     return a("div", {
      class: [{
       "is-active": e.isActive
      }],
      on: {
       click: e.toggleClick
      }
     }, [a("svg-icon", {
      attrs: {
       name: "hamburger",
       width: "20",
       height: "20"
      }
     })], 1)
    },
    Z = [],
    ee = function(e) {
     Object(d["a"])(a, e);
     var t = Object(h["a"])(a);

     function a() {
      return Object(l["a"])(this, a), t.apply(this, arguments)
     }
     return Object(m["a"])(a, [{
      key: "toggleClick",
      value: function() {
       this.$emit("toggle-click")
      }
     }]), a
    }(v["c"]);
   Object(p["a"])([Object(v["b"])({
    default: !1
   })], ee.prototype, "isActive", void 0), ee = Object(p["a"])([Object(v["a"])({
    name: "Hamburger"
   })], ee);
   var te = ee,
    ae = te,
    re = (a("adc6"), Object(z["a"])(ae, Y, Z, !1, null, "715ce9d0", null)),
    ne = re.exports,
    ie = function(e) {
     Object(d["a"])(a, e);
     var t = Object(h["a"])(a);

     function a() {
      return Object(l["a"])(this, a), t.apply(this, arguments)
     }
     return Object(m["a"])(a, [{
      key: "userName",
      get: function() {
       return X["a"].name
      }
     }, {
      key: "sidebar",
      get: function() {
       return Q.sidebar
      }
     }, {
      key: "toggleSideBar",
      value: function() {
       Q.ToggleSideBar(!1)
      }
     }, {
      key: "logout",
      value: function() {
       var e = Object(W["a"])(regeneratorRuntime.mark((function e() {
        return regeneratorRuntime.wrap((function(e) {
         while (1) switch (e.prev = e.next) {
          case 0:
           return e.next = 2, X["a"].LogOut();
          case 2:
           this.$router.push("/login").catch((function(e) {
            console.warn(e)
           }));
          case 3:
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
    }(v["c"]);
   ie = Object(p["a"])([Object(v["a"])({
    name: "Navbar",
    components: {
     Hamburger: ne
    }
   })], ie);
   var ce = ie,
    oe = ce,
    se = (a("0ff5"), Object(z["a"])(oe, I, G, !1, null, "08d7385a", null)),
    ue = se.exports,
    le = function() {
     var e = this,
      t = e.$createElement,
      a = e._self._c || t;
     return a("div", {
      class: {
       "has-logo": e.showLogo
      }
     }, [e.showLogo ? a("sidebar-logo", {
      attrs: {
       collapse: e.isCollapse
      }
     }) : e._e(), a("el-scrollbar", {
      attrs: {
       "wrap-class": "scrollbar-wrapper"
      }
     }, [a("el-menu", {
      attrs: {
       "default-active": e.activeMenu,
       collapse: e.isCollapse,
       "background-color": e.variables.menuBg,
       "text-color": e.variables.menuText,
       "unique-opened": !0,
       "collapse-transition": !1,
       mode: "vertical"
      }
     }, e._l(e.routes, (function(t) {
      return a("sidebar-item", {
       key: t.path,
       attrs: {
        item: t,
        "base-path": t.path,
        "is-collapse": e.isCollapse
       }
      })
     })), 1)], 1)], 1)
    },
    de = [],
    he = function() {
     var e = this,
      t = e.$createElement,
      a = e._self._c || t;
     return e.item.meta && e.item.meta.hidden ? e._e() : a("div", {
      class: [e.isCollapse ? "simple-mode" : "full-mode", {
       "first-level": e.isFirstLevel
      }]
     }, [e.alwaysShowRootMenu || !e.theOnlyOneChild || e.theOnlyOneChild.children ? a("el-submenu", {
      attrs: {
       index: e.resolvePath(e.item.path),
       "popper-append-to-body": ""
      }
     }, [a("template", {
      slot: "title"
     }, [e.item.meta && e.item.meta.icon ? a("svg-icon", {
      attrs: {
       name: e.item.meta.icon
      }
     }) : e._e(), e.item.meta && e.item.meta.title ? a("span", {
      attrs: {
       slot: "title"
      },
      slot: "title"
     }, [e._v(e._s(e.$t("route." + e.item.meta.title)))]) : e._e()], 1), e.item.children ? e._l(e.item.children, (function(t) {
      return a("sidebar-item", {
       key: t.path,
       staticClass: "nest-menu",
       attrs: {
        item: t,
        "is-collapse": e.isCollapse,
        "is-first-level": !1,
        "base-path": e.resolvePath(t.path)
       }
      })
     })) : e._e()], 2) : [e.theOnlyOneChild.meta ? a("sidebar-item-link", {
      attrs: {
       to: e.resolvePath(e.theOnlyOneChild.path)
      }
     }, [a("el-menu-item", {
      class: {
       "submenu-title-noDropdown": e.isFirstLevel
      },
      attrs: {
       index: e.resolvePath(e.theOnlyOneChild.path)
      }
     }, [e.theOnlyOneChild.meta.icon ? a("svg-icon", {
      attrs: {
       name: e.theOnlyOneChild.meta.icon
      }
     }) : e._e(), e.theOnlyOneChild.meta.title ? a("span", {
      attrs: {
       slot: "title"
      },
      slot: "title"
     }, [e._v(e._s(e.$t("route." + e.theOnlyOneChild.meta.title)))]) : e._e()], 1)], 1) : e._e()]], 2)
    },
    pe = [],
    ve = a("5530"),
    me = a("b85c"),
    fe = (a("4de4"), a("df7c")),
    ge = a.n(fe),
    be = (a("498a"), function(e) {
     return /^(https?:|mailto:|tel:)/.test(e)
    }),
    we = function() {
     var e = this,
      t = e.$createElement,
      a = e._self._c || t;
     return e.isExternal(e.to) ? a("a", {
      attrs: {
       href: e.to,
       target: "_blank",
       rel: "noopener"
      }
     }, [e._t("default")], 2) : a("router-link", {
      attrs: {
       to: e.to
      }
     }, [e._t("default")], 2)
    },
    Oe = [],
    ze = function(e) {
     Object(d["a"])(a, e);
     var t = Object(h["a"])(a);

     function a() {
      var e;
      return Object(l["a"])(this, a), e = t.apply(this, arguments), e.isExternal = be, e
     }
     return a
    }(v["c"]);
   Object(p["a"])([Object(v["b"])({
    required: !0
   })], ze.prototype, "to", void 0), ze = Object(p["a"])([Object(v["a"])({
    name: "SidebarItemLink"
   })], ze);
   var je = ze,
    He = je,
    ye = Object(z["a"])(He, we, Oe, !1, null, null, null),
    Me = ye.exports,
    xe = function(e) {
     Object(d["a"])(a, e);
     var t = Object(h["a"])(a);

     function a() {
      return Object(l["a"])(this, a), t.apply(this, arguments)
     }
     return Object(m["a"])(a, [{
      key: "alwaysShowRootMenu",
      get: function() {
       return !(!this.item.meta || !this.item.meta.alwaysShow)
      }
     }, {
      key: "showingChildNumber",
      get: function() {
       if (this.item.children) {
        var e = this.item.children.filter((function(e) {
         return !e.meta || !e.meta.hidden
        }));
        return e.length
       }
       return 0
      }
     }, {
      key: "theOnlyOneChild",
      get: function() {
       if (this.showingChildNumber > 1) return null;
       if (this.item.children) {
        var e, t = Object(me["a"])(this.item.children);
        try {
         for (t.s(); !(e = t.n()).done;) {
          var a = e.value;
          if (!a.meta || !a.meta.hidden) return a
         }
        } catch (r) {
         t.e(r)
        } finally {
         t.f()
        }
       }
       return Object(ve["a"])(Object(ve["a"])({}, this.item), {}, {
        path: ""
       })
      }
     }, {
      key: "resolvePath",
      value: function(e) {
       return be(e) ? e : be(this.basePath) ? this.basePath : ge.a.resolve(this.basePath, e)
      }
     }]), a
    }(v["c"]);
   Object(p["a"])([Object(v["b"])({
    required: !0
   })], xe.prototype, "item", void 0), Object(p["a"])([Object(v["b"])({
    default: !1
   })], xe.prototype, "isCollapse", void 0), Object(p["a"])([Object(v["b"])({
    default: !0
   })], xe.prototype, "isFirstLevel", void 0), Object(p["a"])([Object(v["b"])({
    default: ""
   })], xe.prototype, "basePath", void 0), xe = Object(p["a"])([Object(v["a"])({
    name: "SidebarItem",
    components: {
     SidebarItemLink: Me
    }
   })], xe);
   var Ve = xe,
    ke = Ve,
    Le = (a("d729"), a("2d92"), Object(z["a"])(ke, he, pe, !1, null, "65fc5612", null)),
    Ce = Le.exports,
    Se = function() {
     var e = this,
      t = e.$createElement,
      a = e._self._c || t;
     return a("div", {
      staticClass: "sidebar-logo-container",
      class: {
       collapse: e.collapse
      }
     }, [a("transition", {
      attrs: {
       name: "sidebarLogoFade"
      }
     }, [e.collapse ? a("router-link", {
      key: "collapse",
      staticClass: "sidebar-logo-link",
      attrs: {
       to: "/"
      }
     }, [a("img", {
      staticClass: "sidebar-logo",
      attrs: {
       src: "/img/foxess.png"
      }
     })]) : a("router-link", {
      key: "expand",
      staticClass: "sidebar-logo-link",
      attrs: {
       to: "/"
      }
     }, [a("img", {
      staticClass: "sidebar-logo",
      attrs: {
       src: "/img/foxess.png"
      }
     }), a("h1", {
      staticClass: "sidebar-title"
     }, [e._v(" " + e._s(e.title) + " ")])])], 1)], 1)
    },
    Ae = [],
    Be = function(e) {
     Object(d["a"])(a, e);
     var t = Object(h["a"])(a);

     function a() {
      var e;
      return Object(l["a"])(this, a), e = t.apply(this, arguments), e.title = "FoxEss", e
     }
     return a
    }(v["c"]);
   Object(p["a"])([Object(v["b"])({
    required: !0
   })], Be.prototype, "collapse", void 0), Be = Object(p["a"])([Object(v["a"])({
    name: "SidebarLogo"
   })], Be);
   var Ee = Be,
    _e = Ee,
    Re = (a("3308"), Object(z["a"])(_e, Se, Ae, !1, null, "30e3607e", null)),
    Te = Re.exports,
    Pe = a("a1de"),
    Ne = a.n(Pe),
    De = (a("caad6"), a("2532"), a("159b"), function(e, t) {
     return !t.meta || !t.meta.roles || t.meta.roles.includes(e)
    }),
    Ue = function e(t, a) {
     var r = [];
     return t.forEach((function(t) {
      var n = Object(ve["a"])({}, t);
      De(a, n) && (n.children && (n.children = e(n.children, a)), r.push(n))
     })), r
    },
    Ie = function(e) {
     Object(d["a"])(a, e);
     var t = Object(h["a"])(a);

     function a() {
      var e;
      return Object(l["a"])(this, a), e = t.apply(this, arguments), e.routes = [], e
     }
     return Object(m["a"])(a, [{
      key: "SET_ROUTES",
      value: function(e) {
       this.routes = e
      }
     }, {
      key: "GenerateRoutes",
      value: function(e) {
       var t;
       t = "admin" === e ? rt : Ue(rt, e), this.SET_ROUTES(t)
      }
     }]), a
    }($["d"]);
   Object(p["a"])([$["c"]], Ie.prototype, "SET_ROUTES", null), Object(p["a"])([$["a"]], Ie.prototype, "GenerateRoutes", null), Ie = Object(p["a"])([Object($["b"])({
    dynamic: !0,
    store: J["a"],
    name: "permission"
   })], Ie);
   var Ge = Object($["e"])(Ie),
    We = function(e) {
     Object(d["a"])(a, e);
     var t = Object(h["a"])(a);

     function a() {
      var e;
      return Object(l["a"])(this, a), e = t.apply(this, arguments), e.showLogo = !1, e.activeTextColor = !0, e
     }
     return Object(m["a"])(a, [{
      key: "sidebar",
      get: function() {
       return Q.sidebar
      }
     }, {
      key: "routes",
      get: function() {
       return Ge.routes
      }
     }, {
      key: "variables",
      get: function() {
       return Ne.a
      }
     }, {
      key: "activeMenu",
      get: function() {
       var e = this.$route,
        t = e.meta,
        a = e.path;
       return null !== t && void 0 !== t && t.activeMenu ? t.activeMenu : a
      }
     }, {
      key: "isCollapse",
      get: function() {
       return !this.sidebar.opened
      }
     }]), a
    }(v["c"]);
   We = Object(p["a"])([Object(v["a"])({
    name: "SideBar",
    components: {
     SidebarItem: Ce,
     SidebarLogo: Te
    }
   })], We);
   var $e = We,
    qe = $e,
    Fe = (a("023d"), a("2769"), Object(z["a"])(qe, le, de, !1, null, "bb300160", null)),
    Je = Fe.exports,
    Ke = 992,
    Qe = function(e) {
     Object(d["a"])(a, e);
     var t = Object(h["a"])(a);

     function a() {
      return Object(l["a"])(this, a), t.apply(this, arguments)
     }
     return Object(m["a"])(a, [{
      key: "device",
      get: function() {
       return Q.device
      }
     }, {
      key: "sidebar",
      get: function() {
       return Q.sidebar
      }
     }, {
      key: "onRouteChange",
      value: function() {
       this.device === T.Mobile && this.sidebar.opened && Q.CloseSideBar(!1)
      }
     }, {
      key: "beforeMount",
      value: function() {
       window.addEventListener("resize", this.resizeHandler)
      }
     }, {
      key: "mounted",
      value: function() {
       var e = this.isMobile();
       e && (Q.ToggleDevice(T.Mobile), Q.CloseSideBar(!0))
      }
     }, {
      key: "beforeDestroy",
      value: function() {
       window.removeEventListener("resize", this.resizeHandler)
      }
     }, {
      key: "isMobile",
      value: function() {
       var e = document.body.getBoundingClientRect();
       return e.width - 1 < Ke
      }
     }, {
      key: "resizeHandler",
      value: function() {
       if (!document.hidden) {
        var e = this.isMobile();
        Q.ToggleDevice(e ? T.Mobile : T.Desktop), e && Q.CloseSideBar(!0)
       }
      }
     }]), a
    }(v["c"]);
   Object(p["a"])([Object(v["d"])("$route")], Qe.prototype, "onRouteChange", null), Qe = Object(p["a"])([Object(v["a"])({
    name: "ResizeMixin"
   })], Qe);
   var Xe = Qe,
    Ye = function(e) {
     Object(d["a"])(a, e);
     var t = Object(h["a"])(a);

     function a() {
      return Object(l["a"])(this, a), t.apply(this, arguments)
     }
     return Object(m["a"])(a, [{
      key: "classObj",
      get: function() {
       return {
        hideSidebar: !this.sidebar.opened,
        openSidebar: this.sidebar.opened,
        withoutAnimation: this.sidebar.withoutAnimation
       }
      }
     }]), a
    }(Object(B["c"])(Xe));
   Ye = Object(p["a"])([Object(v["a"])({
    name: "Layout",
    components: {
     AppMain: U,
     Navbar: ue,
     Sidebar: Je
    }
   })], Ye);
   var Ze = Ye,
    et = Ze,
    tt = (a("ba54"), Object(z["a"])(et, S, A, !1, null, "1ed8e595", null)),
    at = tt.exports;
   r["default"].use(C["a"]);
   var rt = [{
     path: "/login",
     component: function() {
      return a.e("login").then(a.bind(null, "9ed6"))
     },
     meta: {
      hidden: !0
     }
    }, {
     path: "/user",
     name: "user",
     component: at,
     meta: {
      hidden: !0
     },
     children: [{
      path: "/user/changepassword",
      component: function() {
       return a.e("change").then(a.bind(null, "c242"))
      },
      meta: {
       hidden: !0
      }
     }]
    }, {
     path: "/overview",
     name: "overview",
     component: at,
     redirect: "/overview/current-alarms",
     meta: {
      title: "overview",
      roles: ["admin", "user"],
      icon: "documentation",
      alwaysShow: !0
     },
     children: [{
      path: "current-alarms",
      component: function() {
       return a.e("err-info").then(a.bind(null, "ffcb"))
      },
      name: "currentAlarms",
      meta: {
       title: "currentAlarms",
       roles: ["admin", "user"]
      }
     }]
    }, {
     path: "/",
     name: "home",
     component: at,
     redirect: "/device/sunspec",
     children: [{
      path: "/device/sunspec",
      component: function() {
       return Promise.all([a.e("vendors~sunspec"), a.e("sunspec")]).then(a.bind(null, "e23f"))
      },
      meta: {
       title: "sunspec",
       icon: "table",
       roles: ["admin", "user"],
       alwaysShow: !0
      }
     }]
    }, {
     path: "/device",
     name: "device",
     component: at,
     redirect: "/device/upgade-device",
     meta: {
      title: "device",
      roles: ["admin", "user"],
      icon: "skill",
      alwaysShow: !0
     },
     children: [{
      path: "upgrade-device",
      component: function() {
       return a.e("up-device").then(a.bind(null, "eecf"))
      },
      name: "upgradeDevice",
      meta: {
       title: "upgradeDevice",
       roles: ["admin"]
      }
     }, {
      path: "download",
      component: function() {
       return a.e("download").then(a.bind(null, "648c"))
      },
      name: "downloadContent",
      meta: {
       title: "inverterLog",
       roles: ["admin"]
      }
     }, {
      path: "fault-recorder",
      component: function() {
       return a.e("err-log").then(a.bind(null, "2874"))
      },
      name: "faultRecorder",
      meta: {
       title: "faultRecorder",
       roles: ["admin", "user"]
      }
     }]
    }, {
     path: "/system",
     name: "system",
     component: at,
     redirect: "/system/module",
     meta: {
      title: "system",
      icon: "tree-table",
      roles: ["admin", "user"],
      alwaysShow: !0
     },
     children: [{
      path: "module",
      component: function() {
       return a.e("up-module").then(a.bind(null, "f2eb"))
      },
      name: "upgradeModule",
      meta: {
       title: "upgradeModule",
       roles: ["admin"]
      }
     }, {
      path: "webserver",
      component: function() {
       return a.e("up-webserver").then(a.bind(null, "8f02"))
      },
      name: "upgradeWebserver",
      meta: {
       title: "upgradeWebserver",
       roles: ["admin"]
      }
     }, {
      path: "network",
      component: function() {
       return a.e("wifi").then(a.bind(null, "4cca"))
      },
      name: "configWifi",
      meta: {
       title: "configWifi",
       roles: ["admin", "user"]
      }
     }, {
      path: "setup",
      component: function() {
       return a.e("setup").then(a.bind(null, "fd46"))
      },
      name: "moduleSetup",
      meta: {
       title: "moduleSetup",
       roles: ["admin"]
      }
     }, {
      path: "resetpassword",
      component: function() {
       return a.e("reset").then(a.bind(null, "c1bd"))
      },
      meta: {
       title: "resetPassword",
       roles: ["admin"]
      }
     }]
    }, {
     path: "/about",
     name: "about",
     component: at,
     redirect: "/about/about",
     children: [{
      path: "about",
      component: function() {
       return a.e("wifi").then(a.bind(null, "53bc"))
      },
      name: "about",
      meta: {
       title: "about",
       alwaysShow: !0,
       icon: "message",
       roles: ["admin", "user"]
      }
     }]
    }],
    nt = new C["a"]({
     base: "/",
     routes: rt
    }),
    it = nt;
   o.a.register({
    404: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M121.7 73.3v10c4-7.7 6.2-16.1 6.2-25C128 26 99.3 0 64 0S0 26 0 58.2v1.2l23-26h13.3L16.6 60.8H23v-7l13.7-19.4v49.4H23V73.3H2.2a61.6 61.6 0 0 0 46 41.4c-1.5 3.3-5.7 11.2-12.6 12.6-8.6 1.8 23.3.5 46.2-13.1a63 63 0 0 0 39.7-30.5H108V73.3H85V59.5l23-26h13l-19.4 27.2h6.4v-7.5l13.7-19.4v39.5zM43.5 76a10.5 10.5 0 0 1-1-4.5v-27c0-1.7.3-3.2 1-4.6a11.7 11.7 0 0 1 2.7-3.7 13 13 0 0 1 9-3.3h11.3a13.6 13.6 0 0 1 9 3.3L63.2 52.6v-3a2 2 0 0 0-.7-1.4c-.4-.4-1-.6-1.6-.6-.7 0-1.2.2-1.7.6a2 2 0 0 0-.6 1.5v9l-14.2 19a10.6 10.6 0 0 1-1-1.6zm35.7-4.5c0 1.6-.3 3-1 4.5a11.7 11.7 0 0 1-2.7 3.7 13 13 0 0 1-9 3.4H55.2a13.6 13.6 0 0 1-9-3.4 12.5 12.5 0 0 1-1.4-1.5L58.5 60v6.4c0 .6.2 1.1.7 1.5.4.4 1 .6 1.6.6.7 0 1.2-.2 1.7-.6a2 2 0 0 0 .7-1.5V54L76 37a10.5 10.5 0 0 1 3.2 7.7v27z"/>'
    }
   }), o.a.register({
    "back-top": {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M85.516 108.161a6.773 6.93 0 0 1-6.753 6.896H38.078a6.746 6.903 0 0 1-6.752-6.903V59.606H10.973c-7.45 0-9.211-4.387-3.915-9.814L53.643 2.124a6.793 6.951 0 0 1 9.563 0l46.584 47.682c5.297 5.406 3.543 9.807-3.928 9.807H85.516V108.161z"/>'
    }
   }), o.a.register({
    bug: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M127.9 73.1a5 5 0 0 1-1.5 3.7c-1 1-2.2 1.6-3.6 1.6h-18c0 9.3-1.7 17.1-5.3 23.6l16.6 17a5 5 0 0 1 1.6 3.7 5 5 0 0 1-1.6 3.7c-1 1-2.1 1.5-3.6 1.5-1.4 0-2.6-.5-3.5-1.5l-15.9-16a15.5 15.5 0 0 1-1.2 1l-3.3 2.3a50.1 50.1 0 0 1-5.2 3 36.4 36.4 0 0 1-14.3 3.4v-73H59v73a32.2 32.2 0 0 1-15-3.8 66.8 66.8 0 0 1-5.3-3.2c-1.6-1-2.8-2-3.5-2.6l-1.2-1.2-14.6 17a5.1 5.1 0 0 1-7.3.4c-1-1-1.5-2.3-1.6-3.7 0-1.4.3-2.7 1.2-3.8l16.2-18.5C24.7 94.5 23 87 23 78.4H5.2c-1.3 0-2.5-.6-3.6-1.6S.1 74.5.1 73.1a5 5 0 0 1 1.5-3.6c1-1 2.3-1.6 3.6-1.6h18V44l-14-14a5 5 0 0 1-1.5-3.7 5 5 0 0 1 1.5-3.7c1-1 2.2-1.6 3.6-1.6s2.6.6 3.6 1.6l13.8 14.1h67.4l13.8-14.1a4.9 4.9 0 0 1 7.2 0 5 5 0 0 1 1.5 3.7 5 5 0 0 1-1.5 3.6L104.9 44v24h17.9c1.4 0 2.6.5 3.6 1.6a5 5 0 0 1 1.5 3.6zm-38.3-47H38.4C38.4 19 41 12.9 46 7.8 51 2.7 57 .1 64 .1s13.1 2.5 18 7.6c5 5 7.6 11.2 7.6 18.5z"/>'
    }
   }), o.a.register({
    chart: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M0 54.9h36.6V128H0V54.9zm91.4-27.5H128V128H91.4V27.4zM45.7 0h36.6v128H45.7V0z"/>'
    }
   }), o.a.register({
    clipboard: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M54.9 118.9h64V73H89c-1.9 0-3.5-.6-4.8-2-1.3-1.3-2-3-2-4.8V36.6H54.9v82.3zM73 16v-4.6a2.2 2.2 0 0 0-.6-1.6 2.2 2.2 0 0 0-1.6-.7H20.6c-.7 0-1.2.3-1.6.7a2.2 2.2 0 0 0-.7 1.6V16a2.2 2.2 0 0 0 .7 1.6c.4.5 1 .7 1.6.7h50.3c.6 0 1.1-.2 1.6-.7.4-.4.6-1 .6-1.6zm18.3 48h21.4L91.4 42.6V64zm36.6 9.1v48c0 2-.7 3.6-2 4.9-1.3 1.3-3 2-4.9 2H52.6c-2 0-3.6-.7-4.9-2-1.3-1.3-2-3-2-4.9v-11.4H7c-2 0-3.6-.7-4.9-2-1.3-1.3-2-3-2-4.8v-96C0 4.9.7 3.3 2 2 3.3.7 5 0 6.9 0h77.7c1.9 0 3.5.7 4.8 2 1.4 1.3 2 3 2 4.9v23.4c1 .6 1.9 1.3 2.6 2l29.1 29.1c1.4 1.4 2.5 3.2 3.5 5.5s1.4 4.4 1.4 6.3z"/>'
    }
   }), o.a.register({
    component: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M0 0h54.9v54.9H0V0zm0 73.1h54.9V128H0V73.1zm73.1 0H128V128H73.1V73.1zM100.6 55a27.4 27.4 0 1 0 0-54.9 27.4 27.4 0 0 0 0 54.9z"/>'
    }
   }), o.a.register({
    dashboard: {
     width: 128,
     height: 100,
     viewBox: "0 0 128 100",
     data: '<path pid="0" d="M27.4 63.6c0-2.5-.9-4.6-2.6-6.4a8.8 8.8 0 0 0-6.5-2.6c-2.5 0-4.7.8-6.5 2.6a8.7 8.7 0 0 0-2.7 6.4c0 2.5 1 4.7 2.7 6.5 1.8 1.7 4 2.6 6.5 2.6s4.7-.9 6.5-2.6c1.7-1.8 2.6-4 2.6-6.5zm13.7-31.8c0-2.5-.9-4.6-2.6-6.4a8.8 8.8 0 0 0-6.5-2.6c-2.5 0-4.7.8-6.5 2.6a8.7 8.7 0 0 0-2.6 6.4c0 2.5.9 4.7 2.6 6.5 1.8 1.7 4 2.6 6.5 2.6s4.7-.9 6.5-2.6c1.7-1.8 2.6-4 2.6-6.5zM71.7 66L79 38.9c.3-1.3.1-2.4-.5-3.5a4.5 4.5 0 0 0-8.3 1.2L63 63.7a13.6 13.6 0 1 0 8 25.4 13 13 0 0 0 6.4-8.4A13.5 13.5 0 0 0 71.7 66zm47.2-2.4c0-2.5-1-4.6-2.7-6.4a8.8 8.8 0 0 0-6.5-2.6c-2.5 0-4.7.8-6.5 2.6a8.7 8.7 0 0 0-2.6 6.4c0 2.5.9 4.7 2.7 6.5 1.7 1.7 3.9 2.6 6.4 2.6 2.5 0 4.7-.9 6.5-2.6 1.8-1.8 2.7-4 2.7-6.5zM73 18.2c0-2.5-.8-4.6-2.6-6.4A8.8 8.8 0 0 0 64 9c-2.5 0-4.7 1-6.5 2.7a8.7 8.7 0 0 0-2.6 6.4c0 2.5.9 4.7 2.6 6.4 1.8 1.8 4 2.7 6.5 2.7s4.7-.9 6.5-2.7c1.7-1.7 2.6-3.9 2.6-6.4zm32 13.6c0-2.5-.8-4.6-2.6-6.4a8.8 8.8 0 0 0-6.5-2.6c-2.5 0-4.7.8-6.5 2.6a8.7 8.7 0 0 0-2.6 6.4c0 2.5.8 4.7 2.6 6.5 1.8 1.7 4 2.6 6.5 2.6s4.7-.9 6.5-2.6c1.7-1.8 2.6-4 2.6-6.5zm23 31.8c0 12.4-3.4 23.8-10 34.3-1 1.4-2.3 2-4 2H14c-1.7 0-3-.6-4-2a62.2 62.2 0 0 1-5-59 63.9 63.9 0 0 1 123 24.7z"/>'
    }
   }), o.a.register({
    documentation: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M72 44.8h43.9l-44-35.2v35.2zM16 0h64l47.9 38.4v76.8c0 3.4-1.7 6.6-4.7 9-3 2.4-7 3.7-11.3 3.7H16.1c-4.2 0-8.3-1.3-11.3-3.7-3-2.4-4.7-5.6-4.7-9V12.8C.1 5.8 7.2 0 16.1 0zm72 102.4V89.6H16v12.8h72zm24-25.6V64H16v12.8h96z"/>'
    }
   }), o.a.register({
    drag: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M73.1 29H64h29.7L64 0 34.4 29h20.5v27.1H27.2v18H55v27.1h18V74.1h27.4V56H73.1V29zM64 128l27.5-26.8H36.6l27.3 26.7zM0 65l27.2 27V38.2L0 65zm100.5-26.8V92L128 65l-27.5-26.8z"/>'
    }
   }), o.a.register({
    edit: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M106.1 67.2a4.8 4.8 0 0 0-4.8 4.8v46.4H9.6V26.7h50.1a4.8 4.8 0 1 0 0-9.6H9.6A9.6 9.6 0 0 0 0 26.7v91.7c0 5.3 4.3 9.6 9.6 9.6h91.7c5.3 0 9.6-4.3 9.6-9.6V72c0-2.7-2.1-4.8-4.8-4.8z"/><path pid="1" d="M125.2 13.4L114.6 2.8a9.6 9.6 0 0 0-13.6 0l-53 53a4.3 4.3 0 0 0-.9 1.3L33.8 88.5a4.2 4.2 0 0 0 1 4.7c1 1.2 2.8 1.7 4.6 1l31.4-13.4c.5-.2 1-.5 1.4-.9l53-53a9.6 9.6 0 0 0 0-13.5zm-59 59l-18.4 7.8 7.7-18.4 37.2-37.1 10.6 10.5L66 72.4zm52.1-52.2l-8.2 8.2L99.5 18l8.3-8.3L118.4 20z"/>'
    }
   }), o.a.register({
    education: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M88.9 119.6c-7.3 0-19.5 2.5-21.4 8.2v.1c-4.2.2-5.2 0-7 0-2-5.7-14.1-8.2-21.4-8.2H0V0h42.5C51.7 0 59.6 5.5 64 13.6 68.4 5.5 76.3 0 85.5 0H128v119.6H88.9zM60.4 24.8c0-9.7-9-16.5-17.7-16.5H7v103.1h32c7-.1 18.2.1 21.3 6.2V24.8zM121 8.2H85.3c-8.8 0-17.7 6.9-17.7 16.5v92.7c3.1-6 14.2-6.2 21.3-6h32V8.1z"/>'
    }
   }), o.a.register({
    email: {
     width: 128,
     height: 96,
     viewBox: "0 0 128 96",
     data: '<path pid="0" d="M64.1 57l56-56a12.5 12.5 0 0 0-4.6-1h-103C10.9 0 9.4.3 8 .8L64 57z"/><path pid="1" d="M64.1 68.3L1.8 6A12.4 12.4 0 0 0 0 12.5v71C0 90.4 5.6 96 12.5 96h103c6.9 0 12.5-5.6 12.5-12.5v-71a12.5 12.5 0 0 0-1.7-6.3L64 68.2z"/>'
    }
   }), o.a.register({
    example: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M96.3 57.5h31.4A64.2 64.2 0 0 0 70.3 0v31.4a32.9 32.9 0 0 1 26 26zm-38.8-26V0A64.2 64.2 0 0 0 0 57.5h31.4a32.9 32.9 0 0 1 26-26zm12.8 64.8v31.4A64.5 64.5 0 0 0 128 70H96.6a33.6 33.6 0 0 1-26.3 26.3zm-38.8-26H0A64.5 64.5 0 0 0 57.8 128V96.6a33.6 33.6 0 0 1-26.3-26.3z"/>'
    }
   }), o.a.register({
    excel: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M78.2 16.6V25H117v5.3H78.2V39H117v5.4H78.2V53H117v5.4H78.2v8.5H117v5.4H78.2V81H117v5.4H78.2v8.5H117v5.4H78.2v11.1H128V16.6H78.2zM0 114.4L72.1 128V0L0 13.6v100.8z"/><path pid="1" d="M28.7 82.6H17.5L32.3 59 18.2 36.5h11.5l8.2 15 8.4-15h11.2L43.4 58.7l15 23.9H46.7l-8.8-15.7z"/>'
    }
   }), o.a.register({
    "exit-fullscreen": {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M49.2 41.3l-.1-35.2c0-2.7-2.3-4.4-5-4.4h-3.7a4.8 4.8 0 0 0-4.8 5l.2 19.2L11.6 2a6.7 6.7 0 0 0-9.5 0 6.8 6.8 0 0 0 0 9.5l24 23.7H7.6A5.5 5.5 0 0 0 2 40.5V44c0 2.7 2.3 5 5 5l35-.2h2.6a4.6 4.6 0 0 0 3.4-1.3c1-.9 1.2-2.1 1.2-3.5l-.3-2.4.2-.2zm52.5 51.2h18.4c2.7 0 5.2-1.6 5.6-4.8v-3.5c0-2.7-2.3-5-5-5l-34.6.2H86l-2.5-.1a4.6 4.6 0 0 0-3.4 1.4c-1 .8-1.2 2-1.2 3.4l.3 2.5-.2.1.1 34.7c0 2.7 2.3 4.4 5 4.4h3.5c2.7 0 4.9-2.3 4.8-5l-.2-18.8 24.2 24a6.7 6.7 0 0 0 9.5 0 6.7 6.7 0 0 0 0-9.5l-24.2-24zM48.1 80.7a4.6 4.6 0 0 0-3.4-1.4h-2.6l-35-.1c-2.7 0-5 2.3-5 5v3.5c.4 3.2 2.9 4.8 5.6 4.8h18.5l-24.1 24a6.8 6.8 0 0 0 0 9.5 6.7 6.7 0 0 0 9.5 0l24.2-23.8-.2 18.9c0 2.7 2 5 4.8 5H44c2.8 0 5-1.7 5-4.4l.2-35-.2-.1.3-2.5c0-1.3-.3-2.6-1.2-3.4zm32-33.3a4.6 4.6 0 0 0 3.4 1.4H86l.1-.1 35.1.2c2.7 0 5-2.3 5-5v-3.5c-.4-3.2-3-5-5.6-5H102l23.9-23.8a6.7 6.7 0 0 0 0-9.5 6.7 6.7 0 0 0-9.5 0L92.3 26l.1-19.4c0-2.7-2-5-4.8-5h-3.4c-2.8 0-5 1.7-5 4.4L79 41.3l.2.2-.3 2.4c0 1.4.3 2.6 1.2 3.5z"/>'
    }
   }), o.a.register({
    "eye-off": {
     width: 128,
     height: 64,
     viewBox: "0 0 128 64",
     data: '<path pid="0" d="M127 8c1.4-2.2 1-5.2-.8-6.9-2.1-1.7-4.8-1.2-6.4 1-.3.3-25.6 32.4-55.8 32.4C34.8 34.5 8.3 2 8 1.9a4.4 4.4 0 0 0-6.3-.5 5.2 5.2 0 0 0-.5 6.8c.5.8 6 7.4 14.6 14.8L4.2 36a5 5 0 0 0 .2 6.8c.5 1 1.6 1.5 2.7 1.5s2.3-.5 3.2-1.5l12.6-14a87 87 0 0 0 20.8 11.6l-4.8 17.4c-.7 2.7.7 5.4 3.2 6.1h1.4c2 0 3.8-1.4 4.3-3.7l4.8-17.4a58.3 58.3 0 0 0 22.8 0L80.2 60a4.7 4.7 0 0 0 4.4 3.7c.4 0 .9 0 1.1-.3 2.5-.7 4-3.4 3.2-6.1l-4.8-17.2A87 87 0 0 0 105 28.6l12.3 13.7c1 1 2.1 1.5 3.2 1.5s2.3-.5 3.2-1.5c1.9-2 1.9-4.9.3-6.8l-11.7-13C121.6 15 127.1 8 127.1 8z"/>'
    }
   }), o.a.register({
    "eye-on": {
     width: 128,
     height: 128,
     viewBox: "0 0 1024 1024",
     data: '<defs/><path pid="0" d="M512 128q69.7 0 135.5 21.2t115.5 55 93.5 74.8 73.7 82 51.6 74.8 32.2 54.9l10 21.3-6.3 13.5q-4 8.5-18.8 34.7t-31.7 51.6-44.3 60-56.9 64.4-69.5 60.1-82.3 51.5-94.9 34.7T512 896q-69.7 0-135.5-21.2T261 820t-93.5-74.3-73.7-81.5-51.6-74.5-32.2-55l-10-21 6.3-13.5q4-8.5 18.8-34.8t31.7-51.8 44.3-60.4 56.9-64.6 69.5-60.4 82.3-51.8 94.9-34.8T512 128zm0 85.3q-46.7 0-91.6 12.4t-81.2 31.8-70.7 47.1-59.6 54.5-48.9 57.7-37.6 52.8-26.4 44q12.4 21.7 26.4 43.5t37.6 52.4 48.9 57 59.6 53.8 70.7 46.7 81.2 31.5 91.6 12.2 91.6-12.4 81.2-31.6 70.7-46.9 59.6-54.2 48.9-57.3 37.6-52.7T928 512q-12.4-21.7-26.4-43.6T864 415.7t-49-57.3-59.6-54.2-70.7-46.9-81.2-31.6-91.6-12.4zm0 128q70.7 0 120.7 50t50 120.7-50 120.7-120.7 50-120.7-50-50-120.7 50-120.7 120.7-50zm0 85.4q-35.3 0-60.3 25t-25 60.3 25 60.3 60.3 25 60.3-25 25-60.3-25-60.3-60.3-25z"/>'
    }
   }), o.a.register({
    form: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M84 23.8c-1 0-1.8-.3-2.5-1a8.6 8.6 0 0 1-1.7-2.2 11.5 11.5 0 0 1-1-2.6c-.3-1-.4-1.7-.4-2.3V0h.2c.9 0 1.7 0 2.4.3.8.1 1.7.5 2.7 1.2l4 2.7a211.6 211.6 0 0 1 11.7 9.7c1.4 1.4 2.6 2.6 3.4 3.6.8 1 1.2 1.8 1.4 2.4l.3 1.8v2H84.1zM127.4 84c.3.7.5 1.5.6 2.6 0 1-.4 2-1.4 3a30.4 30.4 0 0 0-2.3 2 6.7 6.7 0 0 1-1 .9l-11.7-10.8a44.3 44.3 0 0 0 1.8-1.5 31 31 0 0 1 1.8-1.4c1-1 2.3-1.4 3.6-1.2a9 9 0 0 1 6.2 3c1 1 1.8 2.2 2.4 3.4zM78.3 96c2 0 3.7-.5 5-1.5l-26.9 25.8H18c-1.7 0-3.6-.5-5.7-1.4a24.5 24.5 0 0 1-5.9-3.7 21.4 21.4 0 0 1-4.5-5.3c-1.2-2-1.8-4-1.8-6.2V16.5c0-1.8.4-3.7 1.3-5.6A18.4 18.4 0 0 1 5 5.6a21.8 21.8 0 0 1 5.3-4c1.9-1 4-1.6 6-1.6h53.3v16c0 1.6.3 3.4.8 5.2a16.7 16.7 0 0 0 2.6 5.2A13.2 13.2 0 0 0 84.2 32h20.3v42.3l-19 18.2c1-1.4 1.5-3 1.5-4.5 0-2.2-.9-4.1-2.6-5.7a8.8 8.8 0 0 0-6.2-2.4H26.1c-2.4 0-4.4.8-6.1 2.4a7.6 7.6 0 0 0-2.5 5.7c0 2.2.8 4 2.5 5.6a8.7 8.7 0 0 0 6.1 2.3h52.1zM26 47.9c-2.4 0-4.4.8-6.1 2.4a7.6 7.6 0 0 0-2.5 5.7c0 2.2.8 4.1 2.5 5.6A8.7 8.7 0 0 0 26 64h52.1a9 9 0 0 0 6.2-2.3A7.3 7.3 0 0 0 87 56c0-2.2-.9-4.1-2.6-5.7a8.8 8.8 0 0 0-6.2-2.3H26.1zM78.5 112l1.8-1.6 3.5-3.2a479.8 479.8 0 0 0 4.6-4.3 500.8 500.8 0 0 1 5-4.7l13.5-12.3 11.6 10.8-13.4 12.4-5 4.6-4.6 4.2a179.5 179.5 0 0 0-3.3 3l-1.5 1.5a62.2 62.2 0 0 1-3.2 2l-2.5 1a83.5 83.5 0 0 1-3.6 1 72.2 72.2 0 0 1-3.4 1l-2.6.5c-1 .1-1.8 0-2.2-.4-.3-.4-.4-1.2-.3-2.2a30 30 0 0 1 1.6-5.4l1-3 .8-2a10.2 10.2 0 0 1 2.2-2.9z"/>'
    }
   }), o.a.register({
    fullscreen: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M38.5 52L52 38.5 28.4 14.8 43.2 0H0v43.1l14.8-14.8L38.5 52zm74.7 47.7L89.5 76 76 89.5l23.6 23.7L84.8 128H128V84.9l-14.8 14.8zM89.5 52l23.7-23.6L128 43.2V0H84.9l14.8 14.8L76 38.5 89.5 52zm-51 24L14.8 99.7 0 84.7V128h43.1l-14.8-14.8L52 89.5 38.5 76z"/>'
    }
   }), o.a.register({
    "guide-2": {
     width: 1e3,
     height: 1e3,
     viewBox: "0 0 1000 1000",
     data: '<path pid="0" d="M11.6 547.9l282.8 126.4L703.7 291l137-128.3-479.5 551.5L724 860.6a16.8 16.8 0 0 0 21.9-10.7v-.6l254-849L10.4 514.7c-8.7 4.7-11.8 15.3-8 24.7 2.4 4 5.5 7.3 9.3 8.6zm349 451.7L501.7 838l-141-61.2v222.8z"/>'
    }
   }), o.a.register({
    guide: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M1.5 70.1l36.2 16.2 70-65.5-61.5 70.6 46.5 18.8c1 .4 2.4-.2 2.8-1.4L128 0 1.3 66c-1.1.6-1.5 2-1 3.1.3.5.7 1 1.2 1.1zM46.2 128l18-20.7-18-7.9V128z"/>'
    }
   }), o.a.register({
    hamburger: {
     width: 64,
     height: 64,
     viewBox: "0 0 1024 1024",
     data: '<path pid="0" d="M408 442h480a8 8 0 0 0 8-8v-56a8 8 0 0 0-8-8H408a8 8 0 0 0-8 8v56a8 8 0 0 0 8 8zm-8 204a8 8 0 0 0 8 8h480a8 8 0 0 0 8-8v-56a8 8 0 0 0-8-8H408a8 8 0 0 0-8 8v56zm504-486H120a8 8 0 0 0-8 8v56a8 8 0 0 0 8 8h784a8 8 0 0 0 8-8v-56a8 8 0 0 0-8-8zm0 632H120a8 8 0 0 0-8 8v56a8 8 0 0 0 8 8h784a8 8 0 0 0 8-8v-56a8 8 0 0 0-8-8zM142.4 642.1L298.7 519a8.8 8.8 0 0 0 0-13.9L142.4 381.9a8.9 8.9 0 0 0-14.4 6.9v246.3a8.9 8.9 0 0 0 14.4 7z"/>'
    }
   }), o.a.register({
    icon: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M115.1 0a13 13 0 0 1 5 1c1.5.6 2.9 1.5 4 2.7a13.1 13.1 0 0 1 2.8 4c.7 1.6 1 3.3 1 5.2v102.3c0 3.6-1.2 6.7-3.5 9.1a12 12 0 0 1-9 3.6H13c-3.9 0-7-1.2-9.4-3.7a13.2 13.2 0 0 1-3.5-9.5v-102c0-3.4 1.1-6.3 3.4-8.9A12 12 0 0 1 12.8.1h102.3zM81.4 109c1.8 0 3-.4 3.8-1.2.8-.8 1.2-1.9 1.2-3.3 0-1.2-.4-2.3-1.2-3.2-.8-.8-2-1.3-3.8-1.3h-8.8l.1-.8V27h9c1.8 0 3-.4 3.7-1.3.6-.9 1-2 1-3.2a5 5 0 0 0-1-3.2c-.7-.9-2-1.3-3.7-1.3H46.3c-1.8 0-3 .4-3.7 1.3-.6.9-1 2-1 3.2a5 5 0 0 0 1 3.2c.7.9 2 1.3 3.7 1.3h8.1v72.5l.2.4h-8c-1.8 0-3 .5-3.8 1.3-.8 1-1.2 2-1.2 3.2 0 1.4.4 2.5 1.2 3.3.8.8 2 1.2 3.8 1.2h34.8z"/>'
    }
   }), o.a.register({
    international: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M83.3 103a85 85 0 0 0-15.5-19.5c-2.3-2.5-2.1-4.3-1.3-9.9V73c.6-3.8 1.5-6 14.3-8.1 6.5-1 8.2 1.5 10.6 5.2l.8 1.1a12.6 12.6 0 0 0 6.4 5.3c1.2.5 2.5 1.1 4.4 2.2 4.6 2.5 4.6 5.4 4.6 11.7v.8a27 27 0 0 1-5.1 17.4 59 59 0 0 1-19 11c3.4-6.5.7-14.3 0-16.5h-.2zM64 5.1A58.5 58.5 0 0 1 89.5 11a54.3 54.3 0 0 0-12.9 10.4l-2.4 3.5c-2.5 3.7-3.7 5.4-5.9 5.7a25.1 25.1 0 0 1-4.2 0c-4.3-.3-10-.7-12 4.4-1.1 3.2-1.3 12 2.5 16.5a4 4 0 0 1 .3 3.6 7 7 0 0 1-2 3.2 19 19 0 0 1-3-3 19 19 0 0 0-8.3-6.5l-4-1c-3.7-.7-8-1.6-9-3.8a14.9 14.9 0 0 1-.7-5.8 22 22 0 0 0-1.4-9.2 8.9 8.9 0 0 0-5.6-5A58.7 58.7 0 0 1 64 5.1zM0 64a64 64 0 1 0 128 0A64 64 0 0 0 0 64z"/>'
    }
   }), o.a.register({
    language: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M84.7 36.8A44 44 0 0 0 96 55.2c4.8-4.8 8-11.2 10.4-18.4H84.7zM32 76.8h20.8l-10.4-28-10.4 28z"/><path pid="1" d="M112 0H16A16 16 0 0 0 0 16v96a16 16 0 0 0 16 16h96a16 16 0 0 0 15.9-16V16c0-8.8-6.4-16-16-16zM72.7 103.2c-1.6 1.6-3.2 1.6-4.8 1.6-.8 0-2.4 0-3.2-.8-.8-.8-1.6 0-1.6-.8s-.8-1.6-1.6-3.2-.8-2.4-1.6-4l-3.2-8.8h-28L25.6 96c-1.6 3.2-2.4 5.6-3.2 7.2-.8 1.6-2.4 1.6-4.8 1.6-1.6 0-3.2-.8-4.8-1.6-1.6-1.6-2.4-2.4-2.4-4 0-.8 0-1.6.8-3.2s.8-2.4 1.6-4l17.6-44.8c.8-1.6.8-3.2 1.6-4.8.8-1.6 1.6-3.2 2.4-4 .8-.8 1.6-2.4 3.2-3.2 1.6-.8 3.2-.8 4.8-.8 1.6 0 3.2 0 4.8.8 1.6.8 2.4 1.6 3.2 3.2a39 39 0 0 1 4.8 9.6l17.6 44c1.6 3.2 2.4 5.6 2.4 7.2-.8.8-1.6 2.4-2.4 4zm44-31.2a64.6 64.6 0 0 1-20.9-12 47.5 47.5 0 0 1-21.5 12L72 68c8.7-2.4 16-5.6 21.5-11.2a42.1 42.1 0 0 1-12-20.8h-8v-3.2h21.6c-1.6-2.4-3.2-5.6-4.8-8l2.4-.8c1.6 2.4 4 5.6 5.6 8.8h20v4h-8c-2.4 8-6.4 15.2-11.2 20 5.6 4.8 12 8.8 20.8 11.2l-3.2 4z"/>'
    }
   }), o.a.register({
    like: {
     width: 24,
     height: 24,
     viewBox: "0 0 24 24",
     data: '<path pid="0" d="M12 21.6C6.4 16 1 11.3 1 7.2 1 3.4 4 2 6.3 2c1.3 0 4.1.5 5.7 4.5 1.6-4 4.5-4.5 5.7-4.5C20.3 2 23 3.6 23 7.2c0 4-5.1 8.6-11 14.4M17.7 1c-2.2 0-4.4 1-5.7 3.2A6.5 6.5 0 0 0 6.3 1C3 1 0 3.2 0 7.2c0 4.7 5.6 9.4 12 15.8 6.4-6.4 12-11.1 12-15.8 0-4-3.1-6.2-6.3-6.2"/>'
    }
   }), o.a.register({
    link: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M115.6 128H.1V12.3h57.7v12.3H12.4v90.9h90.9V70.2h12.3z"/><path pid="1" d="M116.4 2.8l8.8 8.8-56.8 56.7-8.7-8.7z"/><path pid="2" d="M127.9 38h-12.4V12.4H88.7V0H128z"/>'
    }
   }), o.a.register({
    list: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M1.6 12c0 6.7 4 12 8.9 12s8.8-5.3 8.8-12c0-6.5-4-11.9-8.8-11.9-5 0-9 5.4-9 12zM125.9.2H35.6c-1.3 0-2.1 1.4-2.1 2.9v18.2c0 1.7 1 2.9 2.1 2.9H126c1.2 0 2-1.5 2-2.9V3c0-1.8-1-2.9-2-2.9zM0 63c0 6.6 4 12 8.9 12s8.9-5.4 8.9-12c0-6.7-4-12-9-12C4 51 0 56.3 0 63zm124-12H34c-1.2 0-2 1.4-2 2.8V72c0 1.7 1 2.8 2 2.8h90.3c1.2 0 2-1.4 2-2.8V53.7c0-1.4-.8-2.8-2-2.8zM0 116c0 6.6 4 12 8.9 12s8.9-5.4 8.9-12-4-12-9-12C4 104 0 109.4 0 116zm124-12H34c-1.2 0-2 1.5-2 2.9V125c0 1.8 1 2.9 2 2.9h90.3c1.2 0 2-1.4 2-2.9v-18.2c0-1.4-.8-2.9-2-2.9z"/>'
    }
   }), o.a.register({
    lock: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M119.9 49.7h-8V39.5C111.9 17.7 90.4.1 64 .1 37.5 0 16.1 17.7 16.1 39.5v10.2h-8c-4.4 0-8 3-8 6.6v65c0 3.7 3.6 6.7 8 6.7H120c4.4 0 8-3 8-6.6V56.3c0-3.7-3.6-6.6-8-6.6zm-24 0H32.1V39.5C32 25 46.4 13.2 64 13.2c17.6 0 32 11.8 32 26.3v10.2z"/>'
    }
   }), o.a.register({
    message: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M0 21v59.6c0 11.5 8.5 21 19 21h28.7l1 26.4 28.1-26.5h32.1c10.6 0 19.1-9.4 19.1-21V21c0-11.6-8.5-21-19-21H19C8.6 0 0 9.4 0 21zm82.3 33c0-5.5 4-9.9 9-9.9s9.1 4.4 9.1 10c0 5.5-4 9.9-9 9.9s-9-4.4-9-10zm-27.6 0c0-5.5 4-9.9 9-9.9s9 4.4 9 10c0 5.5-4 9.9-9 9.9s-9-4.4-9-10zm-27 0c0-5.5 4-9.9 9-9.9s9 4.4 9 10c0 5.5-4 9.9-9 9.9s-9-4.4-9-10z"/>'
    }
   }), o.a.register({
    money: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M54.1 127.9V99.2H7.5v-12h46.6V75H7.5V62h38L.1 0h22.6l32.6 45c3.6 5.2 6.4 9.7 8.4 13.5 1.8-3.1 5-7.8 9.3-14.2L104 0h24L82.3 62h38.3v13H74.3v12.4h46.4v12H74.3V128H54.1z"/>'
    }
   }), o.a.register({
    nested: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M0 9.2c0 5 3.6 9.1 8 9.1s8-4 8-9.1c0-5-3.6-9.1-8-9.1S0 4 0 9.2zM32 .1h96v18.2H32V.1zm0 45.6c0 5 3.6 9.2 8 9.2s8-4.1 8-9.2c0-3.2-1.5-6.2-4-7.9a7.2 7.2 0 0 0-8 0 9.4 9.4 0 0 0-4 8zm32-9.1h64v18.3H64V36.6zm-32 82.2c0 5 3.6 9.1 8 9.1s8-4 8-9.1c0-5-3.6-9.1-8-9.1s-8 4-8 9.1zm32-9.1h64v18.2H64v-18.2zm0-27.4c0 5 3.6 9.1 8 9.1s8-4 8-9.1c0-3.3-1.5-6.3-4-8a7.1 7.1 0 0 0-8 0 9.4 9.4 0 0 0-4 8zM96 73h32v18.3H96V73.1z"/>'
    }
   }), o.a.register({
    password: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M108.8 44.3H89.6V39c0-9-3.3-24.2-25.6-24.2-23.1 0-25.6 16.9-25.6 24.2v5.3H19.2V39C19.2 15.3 36.8 0 64 0c27.2 0 44.8 15.3 44.8 39v5.3zm-32 39.4c0-5.5-5.8-9.9-12.8-9.9-7 0-12.8 4.4-12.8 9.9 0 3.7 2.6 6.8 6.4 8.5v11.2c0 2.7 2.9 5 6.4 5 3.5 0 6.4-2.3 6.4-5V92.2c3.8-1.7 6.4-4.8 6.4-8.5zM128 64v49.2c0 8.2-8.6 14.8-19.2 14.8H19.2C8.7 128 0 121.4 0 113.2V64c0-8.2 8.6-14.8 19.2-14.8h89.6c10.6 0 19.2 6.6 19.2 14.8z"/>'
    }
   }), o.a.register({
    pdf: {
     width: 128,
     height: 128,
     viewBox: "0 0 1024 1024",
     data: '<path pid="0" d="M869 277.3H657.2v-212l212 212zm-238.2 26.3V65.3H154.3v417h714.8V303.5H630.8zM295 664c-5-3-11-5-17.6-6.2a132 132 0 0 0-20.8-1.6h-48.8V742h48.8c7.2 0 14.1-.5 20.8-1.6 6.7-1 12.5-3.1 17.6-6.2 5-3 9.1-7.4 12.2-13 3-5.6 4.6-13 4.6-22 0-9.1-1.5-16.4-4.6-22-3-5.6-7.1-10-12.2-13zM35.8 541.8v417h952.4v-417H35.8zM367.2 733a79 79 0 0 1-47.8 50 119 119 0 0 1-45.6 7.8h-66v102.5h-62.9V607.5h128.9c17.9 0 33 2.6 45.6 7.8a79.3 79.3 0 0 1 47.8 49.8 108.1 108.1 0 0 1 0 67.9zM645 806.4a127 127 0 0 1-24.2 45.6 113.5 113.5 0 0 1-40.4 30.3c-16.2 7.3-35.2 11-57 11H400V607.5h123.2c18.4 0 35.6 3 51.5 8.8a111.6 111.6 0 0 1 41.2 26.4 122 122 0 0 1 27.2 44c6.5 17.7 9.8 38.3 9.8 62 0 20.9-2.7 40.1-8 57.7zm245.4-146H752.2v66h119.7v48.8H752.2v118h-62.8V607.6h200.9v52.8zM572 686a61.3 61.3 0 0 0-25.5-19 101.5 101.5 0 0 0-39-6.7h-44.8v180.1h56c9.1 0 18-1.4 26.4-4.4 8.6-2.9 16.2-7.8 22.9-14.6 6.6-6.8 12-15.6 16-26.6 4-11 6-24.3 6-40 0-14.4-1.4-27.4-4.2-39A77.9 77.9 0 0 0 572 686zm0 0"/>'
    }
   }), o.a.register({
    people: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M104.2 95.3A38.6 38.6 0 0 1 117 128h-10.7c.2-1.5.4-3 .4-4.5 0-9-4.4-17-11.5-23.2a73.5 73.5 0 0 1-62.4 0 30.7 30.7 0 0 0-11.5 23.2c0 1.6.2 3 .4 4.5H11a35.4 35.4 0 0 1-.3-4.5c0-10.8 5-20.7 13.1-28.3A50.7 50.7 0 0 1 0 53.6C0 24 28.7 0 64 0s64 24 64 53.6c0 16.8-9.3 31.8-23.8 41.7zM64 36.9c-29.5 0-53.3-10.1-53.3 15.3s23.8 46 53.3 46c29.5 0 53.3-20.6 53.3-46S93.5 37 64 37zm24.9 25.6c-4 0-7.1-2.7-7.1-6 0-3.2 3.2-5.9 7-5.9 4 0 7.2 2.7 7.2 6s-3.2 6-7.1 6zM85.3 79c0 4-9.5 7.4-21.3 7.4S42.7 83 42.7 79c0-1 .6-2 1.8-3 3.3 2.6 10.8 4.5 19.5 4.5s16.2-1.9 19.5-4.5c1.2 1 1.8 2 1.8 3zM39.1 62.5c-4 0-7.1-2.7-7.1-6 0-3.2 3.2-5.9 7.1-5.9 4 0 7.1 2.7 7.1 6s-3.2 6-7 6z"/>'
    }
   }), o.a.register({
    peoples: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M95.6 118.8c0 5-3.5 9-8 9H8c-4.4 0-8-4-8-9 0-18.3 15.4-35.3 31.2-42a37.8 37.8 0 0 1-15.3-31v-9.2C16 16.5 30.2.1 48 .1s31.8 16.4 31.8 36.5v9.2c0 13-6.1 24.5-15.2 31 15.7 6.7 31.1 23.7 31.1 42z"/><path pid="1" d="M106 118.3h16c3.4 0 6.1-3.2 6.1-7 0-14-11.8-27-23.8-32.1 7-5 11.6-13.7 11.6-23.7v-7c0-15.4-11-28-24.4-28-1.6 0-3.3.2-4.9.6 2 4.7 3 10 3 15.5v9.2c0 13-3 23-11 31 14.8 4.4 27.3 23.4 27.5 41.5z"/>'
    }
   }), o.a.register({
    qq: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M18.4 57.5l-.2-.7-.2-1-.1-.5v-2.2l.2-.8.2-1 .4-.9.4-1 .6-1.2.7-1v-.8l.1-.8.2-1 .3-1 .3-1.2.3-.6.2-.5.4-.6.4-.4v-2.7l.3-1.4.2-1.7.4-2 .6-2 .4-1 .4-1.3.5-1.1.6-1.2.5-1.4.7-1.2.7-1.4 1-1.3.4-.7.4-.7 1-1.4 1-1.4L33 15l1.3-1.4 1.3-1.4 1.4-1.4 1.7-1.6 1.1-.9 1.3-1 1.4-.9 1.4-.9 1.4-.7 1.6-.6 1.7-.8 1.6-.6 1.7-.5 1.8-.6 1.7-.4 2-.3L59 .7l2-.3 1.8-.2 2-.1h5.9l2 .2 2 .3 2 .2 1.8.4 2 .4 1.9.5 2 .5 1.9.7 1.8.7 1.9.8 1.7.8 1.7 1 1.6 1 1.5 1 .6.5.7.4 1.3 1.1 1.2 1.1 1 1.1 1.2 1.2.8 1.2 1.1 1.2.8 1.3.7 1.2.8 1.3.7 1.2 1 2.5.6 1.3.4 1.2.5 1.3.4 1.2.2 1 .4 1.3.6 2.2.4 1.9.2 1.9.2 1.5.4 2.2v.4l.3.4.8 1.2.4.8.5.8.5 1 .5 1 .3 1 .3 1.3.3 1.2v.6l.2.8v.6l-.1.6v.8l-.2.8-.4 1.5-.4.8-.3.8v.2l.2.3.4.6 1.7 2.6 1.4 1.9.7 1.2.8 1.4.8 1.5 1 1.7.8 1.8 1 2 .6 1.3.5 1.3.4 1.3.5 1.1.3 1.3.4 1.1.4 2.3.3 2.3.3 2v3l-.2 1-.2 1.7-.3 1.6-.5 1.5-.2.6-.3.7-.3.5-.4.6-.3.4-.4.5-.4.4-.4.3-.5.2-.4.2-.4.1h-.9l-.6-.4-.3-.2-.3-.2-.4-.4-.3-.3-.6-.6-.7-1-.5-.8-.6-.8-.5-.8-.7-1.5-.9-1.6h-.2l-.3.2-.2.4-.4.5-.5 1.5-.9 2.2-1 2.6-1 1.4-.8 1.3-1 1.6-1 1.5-.6.6-.7.8-1.6 1.5.2.1.2.2.7.5 3.3 1.5 1.4.8 1.3.7 1.4 1 1.2 1 .5.4.5.5.4.6.4.7.2.5.2.6.1.6.1.6v.9l-.2.5-.2.4-.1.3-.2.4-.6.8-.6.6-.4.5-.3.3-1 .7-1 .5-1 .5-1.2.6-1.3.5-.7.2-.6.1-1.5.4-1.5.3-1.6.3-1.6.3H100l-1.8.3h-5.5l-2-.1-1.9-.2-2-.3-2-.2-2-.3-2-.5-2-.3-2-.6-2-.7-2-.6-1-.3-1-.4-.6-.2-.6-.1H68l-2-.1-.9-.1-1.2-.2-.8.7-1.1.7-1.5.7-1.6.9-1 .5-1 .3-2.3 1-1.2.3-1.3.3-1.9.3-1 .1-1.3.1-1.2.2H36l-3.3-.4-1.6-.2-1.6-.2-1.6-.2-1.5-.3-1.5-.5-1.4-.3-1.3-.5-1.2-.5-1.2-.5-1-.6-1-.7-.3-.4-.4-.4-.3-.4-.3-.4-.3-.4-.2-.4-.3-.9-.1-.5-.2-.5v-.4l.2-.6v-2.1l.1-.6.3-.6.2-.7.4-.7.3-.3.2-.4.6-.7.5-.4.5-.3.4-.3.7-.2.5-.3.7-.4.8-.2.7-.2 1-.2.8-.1 1-.2h1l.4-.1.2-.2-.2-.4-.6-.2-1.5-1.3-1-.7-1-1-1.2-1-1.2-1.5L19 101l-.6-.9-.6-.8-.6-1-.5-1.1-.7-1-.5-1.3-.5-1.2-.6-1.3L14 91l-.4-1.5v-.1h-.2v-.1H13l-.2.1h-.1l-.2.3v.3l-.2.3-.2.5-.6 1.2-.4.7-.5.6-.6.7-.6.8-.7.8-.8.7-.7.6-.9.5-.9.6-.8.3-1 .3H2.2l-.1-.4-.3-.2-.4-1-.3-.4-.2-.7-.2-.8-.1-.7-.3-1.6-.2-1v-3.2l.2-2.4.2-1.2.2-1.2.2-1.4.4-1.2.4-1.5.4-1.4.6-1.4.5-1.4L4 74l.7-1.5.8-1.5 1-1.5 1-1.4 1.1-1.5 1-1 1-1.3L12 63l.5-.5.7-.7 1-.8 1-.9 1.7-1.4 1.2-1z"/>'
    }
   }), o.a.register({
    search: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M124.9 109.8L94.3 79.2l-1.2-1a50.4 50.4 0 0 0 8.2-27.5 50.6 50.6 0 1 0-23 42.4c.2.4.5.8.9 1.1l30.6 30.7a10.6 10.6 0 0 0 7.5 3.1 10.7 10.7 0 0 0 7.6-18.2M50.7 85.3a34.7 34.7 0 1 1 0-69.4 34.7 34.7 0 0 1 0 69.4"/>'
    }
   }), o.a.register({
    shopping: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M43 101.4c1.6 0 3.1.3 4.6 1a12.3 12.3 0 0 1 3.9 2.7c1 1.2 2 2.6 2.6 4.2a14.4 14.4 0 0 1-2.6 14.5 13.3 13.3 0 0 1-4 2.8 10.6 10.6 0 0 1-4.6 1c-1.7 0-3.3-.3-4.7-1a13.6 13.6 0 0 1-3.8-2.8c-1.2-1.2-2-2.6-2.6-4.2a14.4 14.4 0 0 1-1-5.2c0-1.8.4-3.5 1-5 .6-1.7 1.4-3 2.6-4.3a12.5 12.5 0 0 1 3.8-2.7c1.4-.7 3-1 4.7-1zm53.8.2c1.7 0 3.3.4 4.8 1a11.4 11.4 0 0 1 3.9 2.8 13.8 13.8 0 0 1 2.6 14.4c-.7 1.7-1.6 3-2.6 4.2a12.3 12.3 0 0 1-4 2.9 11 11 0 0 1-4.7 1 10.6 10.6 0 0 1-4.6-1 12.5 12.5 0 0 1-3.8-2.9c-1.1-1.1-2-2.5-2.6-4.2a13.6 13.6 0 0 1-1-5 13.6 13.6 0 0 1 3.6-9.4 11.6 11.6 0 0 1 3.8-2.8 11.2 11.2 0 0 1 4.6-1zM118.6 21c2.4 0 4.3.4 5.7 1 1.3.8 2.3 1.7 2.8 2.7a6.4 6.4 0 0 1 .8 3.3c0 1.2-.2 2.2-.5 3l-1.6 5.4A589.3 589.3 0 0 1 123 45a1236.4 1236.4 0 0 0-3 9.4l-2.3 7.4a16.4 16.4 0 0 1-4.3 8 9.5 9.5 0 0 1-6.3 2.1H39l2 12.8h65.3c4.2 0 6.2 2 6.2 5.9 0 1.9-.4 3.5-1.2 4.9-.8 1.3-2.4 2-4.9 2H38.5c-1.7 0-3.2-.4-4.3-1.3-1.2-.8-2.2-2-3-3.3a21.3 21.3 0 0 1-1.8-4.5 44.1 44.1 0 0 1-1.1-4.5A233.5 233.5 0 0 0 26 71.6l-1.9-11a6273.2 6273.2 0 0 1-7.6-44.1H6.9a5 5 0 0 1-3.3-1 9 9 0 0 1-2.1-2.6A10.4 10.4 0 0 1 .3 9.7 17 17 0 0 1 0 6.5c0-1.9.6-3.4 1.8-4.7A6.2 6.2 0 0 1 6.5 0h13c1.8 0 3.2.3 4.2.9 1 .5 1.9 1.2 2.5 2a8.5 8.5 0 0 1 1.3 2.8L28 8l.6 3.2a1032.4 1032.4 0 0 1 1.2 9.6h88.7z"/>'
    }
   }), o.a.register({
    size: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M0 54.9h54.8V73H36.5v55H18.3V73.1H0V55zm127.9-36.6h-36V128H72.5V18.3h-36V0H128v18.3z"/>'
    }
   }), o.a.register({
    skill: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M31.7 93.2H65a41 41 0 0 0 5 6.8H31.7v-6.7zm0-10.6h28.9a44.8 44.8 0 0 1-1.3-6.7H31.7v6.7zm0-17.2h27.7c.3-2.3.7-4.6 1.3-6.7h-29v6.7zm53.9 44.8v5.8c0 2.8-2.1 5.1-4.7 5.1h-70c-2.6 0-4.7-2.3-4.7-5V31.2l23.2-21v22.3H17.2v6.6h18.4V6.7h45.3c2.6 0 4.7 2.3 4.7 5v20c2-.6 4-1 6.1-1.4V11.8C91.7 5.3 87 0 81 0H31.1L0 28.1v88c0 6.4 4.9 11.7 10.8 11.7H81c6 0 10.8-5.3 10.8-11.8v-4.4c-2-.3-4.1-.7-6.1-1.4zM23.3 58.7h-8v6.7h8v-6.7zm-8 41.2h8v-6.7h-8v6.7zm8-24h-8v6.7h8V76zM113 61l-4.9-4-12.4 17.5-11.2-9.3-3.8 5.3 16 13.4 16.3-23zm15 10c0-18.6-14-33.7-31.1-33.7-17.2 0-31.2 15.2-31.2 33.8 0 18.6 14 33.8 31.2 33.8C114 104.8 128 89.6 128 71zm-6.2 0c0 15-11.2 27.2-25 27.2-13.7 0-25-12.2-25-27.1 0-15 11.3-27.1 25-27.1 13.8 0 25 12.1 25 27z"/>'
    }
   }), o.a.register({
    star: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M70.7 4.3l14 29.7c1 2.3 3.1 3.9 5.6 4.3l31.3 4.7c6.1 1 8.5 8.8 4.1 13.3l-22.7 23a8 8 0 0 0-2 7l5.3 32.6c1 6.3-5.4 11.2-10.8 8.2l-28-15.4a7.1 7.1 0 0 0-7 0l-28 15.4c-5.4 3-11.8-1.9-10.8-8.2l5.4-32.6a8 8 0 0 0-2.2-7l-22.6-23C-2.1 51.8.3 44 6.3 43l31.4-4.7c2.4-.4 4.5-2 5.6-4.3l14-29.7a7.3 7.3 0 0 1 13.4 0z"/>'
    }
   }), o.a.register({
    tab: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M79 0H49c-1.7 0-3 1.8-3 3.6v6.7c0 1.8 1.6 3.4 3.2 3.4H79c1.9 0 3.2-1.6 3.2-3.4V3.5C82.4 1.6 80.8.1 79 .1zm45.5 0H94.6a3.5 3.5 0 0 0-3.4 3.5v6.7c0 1.8 1.6 3.4 3.4 3.4h29.9c1.8-.2 3.4-1.6 3.4-3.4V3.5c0-1.8-1.6-3.4-3.4-3.4zm0 22.4H40a3.5 3.5 0 0 1-3.4-3.4V3.5C36.6 1.7 35 .1 33 .1H3.5A3.5 3.5 0 0 0 .1 3.5v121.3c0 1.5 1.6 3.1 3.4 3.1h121c1.8 0 3.4-1.6 3.4-3.4V25.9c0-1.9-1.6-3.5-3.4-3.5z"/>'
    }
   }), o.a.register({
    table: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M0 0h128v31.2H0V0zm0 38h38.4v41.6H0V38zm0 48.5h38.4v41.4H0V86.5zM44.8 38h38.4v41.5H44.8V38zm0 48.4h38.4v41.4H44.8V86.5zM89.6 38H128v41.5H89.6zm0 48.4H128v41.4H89.6z"/><path pid="1" d="M0 0h128v31.2H0V0zm0 38h38.4v41.6H0V38zm0 48.5h38.4v41.4H0V86.5zM44.8 38h38.4v41.5H44.8V38zm0 48.4h38.4v41.4H44.8V86.5zM89.6 38H128v41.5H89.6zm0 48.4H128v41.4H89.6z"/>'
    }
   }), o.a.register({
    theme: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M125.5 37L95.3 2.8a8 8 0 0 0-6-2.8 8 8 0 0 0-6 2.8l-3.8 4.3a8 8 0 0 1-6 2.8h-19a8 8 0 0 1-6-2.8l-3.8-4.3a8 8 0 0 0-6-2.8 8 8 0 0 0-6 2.8L2.5 37A10.3 10.3 0 0 0 0 43.8c0 2.6.9 5 2.5 6.8l12 13.7a7.8 7.8 0 0 0 8.4 2.5c1.3-.5 2.7.5 2.7 2.1v49.4c0 5.4 3.8 9.7 8.5 9.7H94c4.7 0 8.5-4.3 8.5-9.7V69c0-1.6 1.4-2.6 2.7-2.1 3 1 6.2 0 8.3-2.5l12.1-13.7c1.6-1.8 2.5-4.2 2.5-6.8 0-2.5-.9-5-2.5-6.8z"/>'
    }
   }), o.a.register({
    "tree-table": {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M44.8 0h79.5c2.5 0 3.7 1.4 3.7 4.3v23.4c0 2.9-1.2 4.3-3.7 4.3H44.8c-2.4 0-3.7-1.4-3.7-4.3V4.3c0-2.9 1.3-4.3 3.7-4.3zm22.9 48h56.6c2.5 0 3.7 1.4 3.7 4.3v23.4c0 2.9-1.2 4.3-3.7 4.3H67.7c-2.5 0-3.7-1.4-3.7-4.3V52.3c0-2.9 1.2-4.3 3.7-4.3zm0 48h56.6c2.5 0 3.7 1.4 3.7 4.3v23.4c0 2.9-1.2 4.3-3.7 4.3H67.7c-2.5 0-3.7-1.4-3.7-4.3v-23.4c0-2.9 1.2-4.3 3.7-4.3zM50.3 68.3c2 0 3.6-2 3.6-4.3 0-2.4-1.6-4.3-3.6-4.3h-33V32h6.5c2 0 3.6-2 3.6-4.3V4.3c0-2.4-1.6-4.3-3.6-4.3H3.7C1.7 0 0 2 0 4.3v23.4C0 30.1 1.6 32 3.7 32H10v80c0 2.4 1.6 4.3 3.6 4.3h36.6c2 0 3.6-2 3.6-4.3 0-2.4-1.6-4.3-3.6-4.3h-33V68.3h33z"/>'
    }
   }), o.a.register({
    tree: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M126.7 90a5 5 0 0 1 1.3 3.5V123a5 5 0 0 1-1.3 3.6c-.8.9-1.9 1.3-3.1 1.3H97.8a4 4 0 0 1-3-1.3 5 5 0 0 1-1.3-3.6V93.5c0-1 .2-1.7.6-2.5.4-.8 1-1.4 1.6-1.8a3.8 3.8 0 0 1 2.1-.7h9.7V69a3.8 3.8 0 0 0-.4-1.8 3.6 3.6 0 0 0-1.1-1.3 2.7 2.7 0 0 0-1.6-.5H67.9v23.1h9.8c1.1 0 2.1.5 3 1.5a5 5 0 0 1 1.2 3.5V123c0 .9-.1 1.7-.5 2.5s-1 1.4-1.6 1.8a3.8 3.8 0 0 1-2.1.6H51.9a3.8 3.8 0 0 1-2.1-.6 5 5 0 0 1-1.7-1.8 5 5 0 0 1-.6-2.5V93.5a5 5 0 0 1 1.3-3.5 4 4 0 0 1 3.1-1.5h9.6V65.4H23.6a3 3 0 0 0-2.4 1c-.6.8-.9 1.6-.9 2.6v19.5H30c1.3 0 2.3.5 3.1 1.5.8 1 1.2 2.2 1.2 3.5V123c0 1.4-.4 2.6-1.2 3.6-.8.9-1.8 1.3-3 1.3H4.2c-.5 0-1 0-1.4-.2a4.1 4.1 0 0 1-1.1-.7 4.7 4.7 0 0 1-1-1 5.2 5.2 0 0 1-.6-1.4A5.6 5.6 0 0 1 0 123V93.5l.1-1.3A4 4 0 0 1 .6 91 6.4 6.4 0 0 1 2 89.2a3 3 0 0 1 1-.5l1.2-.2H14V61.6c0-1 .3-1.8 1-2.5.6-.7 1.3-1 2.2-1h44.3V39.5h-9.6a4 4 0 0 1-3.1-1.5 5 5 0 0 1-1.3-3.4V5c0-1.4.4-2.6 1.3-3.6A4 4 0 0 1 51.9.1h25.8c.7 0 1.4.2 2.1.7a5.2 5.2 0 0 1 1.6 1.9c.4.7.5 1.6.5 2.4v29.6a5 5 0 0 1-1.2 3.4c-.9 1-1.9 1.5-3 1.5h-9.8V58h42.8c1 0 1.7.4 2.4 1 .6.8.9 1.6.9 2.6v27h9.6a4 4 0 0 1 3.1 1.4z"/>'
    }
   }), o.a.register({
    user: {
     width: 130,
     height: 130,
     viewBox: "0 0 130 130",
     data: '<path pid="0" d="M63.4 65c20.7 0 37.4-14.3 37.4-32 0-17.6-16.7-32-37.4-32-20.6 0-37.3 14.4-37.3 32 0 17.7 16.7 32 37.3 32zm17.2 10.7H49.4C22.8 75.7 1.2 94 1.2 116.9v2.7c0 9.3 21.6 9.3 48.2 9.3h31.2c26.6 0 48.2-.3 48.2-9.3v-2.7c0-22.8-21.6-41.2-48.2-41.2z" _stroke="#979797"/>'
    }
   }), o.a.register({
    wechat: {
     width: 128,
     height: 110,
     viewBox: "0 0 128 110",
     data: '<path pid="0" d="M86.6 33.3c1.5 0 3 .1 4.4.3C87 14.4 67.6.1 45.3.1 20.4.1.1 18 .1 40.7c0 13 6.7 23.8 18 32.2l-4.5 14.3L29.5 79c5.6 1.2 10.2 2.4 15.8 2.4 1.4 0 2.9 0 4.2-.2a38 38 0 0 1 37-47.8zM62.3 20.4c3.4 0 5.7 2.4 5.7 6 0 3.5-2.3 6-5.7 6-3.4 0-6.8-2.5-6.8-6 0-3.6 3.4-6 6.8-6zm-31.7 12c-3.4 0-6.8-2.5-6.8-6 0-3.6 3.4-6 6.8-6s5.7 2.4 5.7 6c0 3.5-2.3 6-5.7 6z"/><path pid="1" d="M128 70.5c0-19-18.2-34.6-38.5-34.6C68 35.9 51 51.4 51 70.5s17 34.6 38.5 34.6c4.5 0 9-1.2 13.6-2.4l12.4 7.2-3.4-12c9-7 15.8-16.6 15.8-27.4zm-51-6c-2.2 0-4.5-2.3-4.5-4.7 0-2.4 2.3-4.8 4.5-4.8 3.4 0 5.7 2.4 5.7 4.8s-2.3 4.8-5.7 4.8zm25 0c-2.3 0-4.6-2.3-4.6-4.7 0-2.4 2.3-4.8 4.5-4.8 3.4 0 5.7 2.4 5.7 4.8s-2.3 4.8-5.7 4.8z"/>'
    }
   }), o.a.register({
    zip: {
     width: 128,
     height: 128,
     viewBox: "0 0 128 128",
     data: '<path pid="0" d="M78.5 116.8h40.8c4.7 0 8.5-3.7 8.5-8.2V19c0-4.5-3.8-8.2-8.5-8.2H78.5V0L0 10v107.5l78.5 10.3v-11zm0-101.4h40.8c2 0 3.6 1.6 3.6 3.5v89.7c0 2-1.6 3.5-3.6 3.5H78.5V15.4zM30.3 75.8l-18.8-.5v-3l11.3-16.6v-.2l-10.2.2v-4.5l17.5-.4V54L18.7 70.8v.1l11.6.2v4.7zm9.4.2l-5.8-.2V50.7l5.8-.2V76zm22.2-11.6c-2.1 1.9-5.3 2.7-9 2.7l-2-.1v9.3l-6-.2V50.7A52 52 0 0 1 53 50c3.9-.1 6.6.5 8.5 2 1.8 1.2 3 3.4 3 6s-.9 4.9-2.6 6.4zm-8.5-10c-.9 0-1.7.1-2.6.3v7.7l2 .2c3.4 0 5.4-1.7 5.4-4.4 0-2.4-1.7-3.8-4.8-3.7zm39.8-37h9.6v3.8h-9.6v-3.8zM83.6 23h9.6v3.8h-9.6V23zm9.6 6.2h9.6V33h-9.6v-3.8zm0 12h9.6V45h-9.6v-3.8zm-9.6-6.1h9.6V39h-9.6v-3.8zm9.5 47c2.5 0 5-1 6.7-2.6a9 9 0 0 0 2.8-6.5l-1.8-15c0-5-2.5-9.1-7.7-9.1s-7.7 4-7.7 9l-1.8 15.3a9 9 0 0 0 2.8 6.5 9.7 9.7 0 0 0 6.7 2.6zM90 65.5h6.2v12.7H90V65.5z"/>'
    }
   });
   a("99af"), a("a5d8");
   var ct = {
     title: "Fox Ess Smart WiLAN",
     showSettings: !1,
     showTagsView: !1,
     fixedHeader: !1,
     showSidebarLogo: !1,
     errorLog: ["production"],
     sidebarTextTheme: !0,
     devServerPort: 9527,
     mockServerPort: 9528
    },
    ot = ct,
    st = ["/login", "/auth-redirect"],
    ut = function(e) {
     var t = F["a"].te("route.".concat(e));
     if (t) {
      var a = F["a"].t("route.".concat(e));
      return "".concat(a, " - ").concat(ot.title)
     }
     return "".concat(ot.title)
    };
   it.beforeEach(function() {
    var e = Object(W["a"])(regeneratorRuntime.mark((function e(t, a, r) {
     return regeneratorRuntime.wrap((function(e) {
      while (1) switch (e.prev = e.next) {
       case 0:
        if (!X["a"].name) {
         e.next = 22;
         break
        }
        if ("/login" !== t.path) {
         e.next = 5;
         break
        }
        r({
         path: "/"
        }), e.next = 20;
        break;
       case 5:
        if (Ge.GenerateRoutes(X["a"].name), 0 !== X["a"].roles.length) {
         e.next = 19;
         break
        }
        return e.prev = 7, e.next = 10, X["a"].GetUserInfo();
       case 10:
        Ge.GenerateRoutes(X["a"].name), r(Object(ve["a"])(Object(ve["a"])({}, t), {}, {
         replace: !0
        })), e.next = 17;
        break;
       case 14:
        e.prev = 14, e.t0 = e["catch"](7), r("/login?redirect=".concat(t.path));
       case 17:
        e.next = 20;
        break;
       case 19:
        r();
       case 20:
        e.next = 23;
        break;
       case 22:
        -1 !== st.indexOf(t.path) ? r() : r("/login?redirect=".concat(t.path));
       case 23:
       case "end":
        return e.stop()
      }
     }), e, null, [
      [7, 14]
     ])
    })));
    return function(t, a, r) {
     return e.apply(this, arguments)
    }
   }()), it.afterEach((function(e) {
    document.title = ut(e.meta.title)
   })), r["default"].use(i.a, {
    i18n: function(e, t) {
     return F["a"].t(e, t)
    }
   }), r["default"].use(o.a, {
    tagName: "svg-icon",
    defaultWidth: "1em",
    defaultHeight: "1em"
   }), r["default"].config.productionTip = !1, new r["default"]({
    router: it,
    store: J["a"],
    i18n: F["a"],
    render: function(e) {
     return e(k)
    }
   }).$mount("#app")
  },
  d257: function(e, t, a) {
   "use strict";
   a.d(t, "b", (function() {
    return i
   })), a.d(t, "a", (function() {
    return c
   }));
   var r = a("b85c"),
    n = (a("53ca"), a("ac1f"), a("5319"), a("d3b7"), a("25f0"), a("4d90"), a("d81d"), a("466d"), a("4d63"), a("1c46")),
    i = (a("5a0c"), function(e) {
     var t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : "utf8";
     return Object(n["createHash"])("md5").update(e, t).digest("hex")
    }),
    c = function(e, t, a, n) {
     try {
      var i, c = Object(r["a"])(e);
      try {
       for (c.s(); !(i = c.n()).done;) {
        var o = i.value;
        if (o[t] === n) return a ? o[a] : o
       }
      } catch (s) {
       c.e(s)
      } finally {
       c.f()
      }
      return !1
     } catch (u) {
      return !1
     }
    }
  },
  d729: function(e, t, a) {
   "use strict";
   a("4f20")
  },
  db8d: function(e, t, a) {},
  f749: function(e, t, a) {}
 },
 [
  [0, "runtime", "chunk-elementUI", "chunk-libs"]
 ]
]);