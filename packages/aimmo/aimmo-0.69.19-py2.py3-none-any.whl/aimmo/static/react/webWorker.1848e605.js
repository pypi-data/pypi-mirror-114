parcelRequire=function(e,r,t,n){var i,o="function"==typeof parcelRequire&&parcelRequire,u="function"==typeof require&&require;function f(t,n){if(!r[t]){if(!e[t]){var i="function"==typeof parcelRequire&&parcelRequire;if(!n&&i)return i(t,!0);if(o)return o(t,!0);if(u&&"string"==typeof t)return u(t);var c=new Error("Cannot find module '"+t+"'");throw c.code="MODULE_NOT_FOUND",c}p.resolve=function(r){return e[t][1][r]||r},p.cache={};var l=r[t]=new f.Module(t);e[t][0].call(l.exports,p,l,l.exports,this)}return r[t].exports;function p(e){return f(p.resolve(e))}}f.isParcelRequire=!0,f.Module=function(e){this.id=e,this.bundle=f,this.exports={}},f.modules=e,f.cache=r,f.parent=o,f.register=function(r,t){e[r]=[function(e,r){r.exports=t},{}]};for(var c=0;c<t.length;c++)try{f(t[c])}catch(e){i||(i=e)}if(t.length){var l=f(t[t.length-1]);"object"==typeof exports&&"undefined"!=typeof module?module.exports=l:"function"==typeof define&&define.amd?define(function(){return l}):n&&(this[n]=l)}if(parcelRequire=f,i)throw i;return f}({"JZ8d":[function(require,module,exports) {
"use strict";function e(e){var o,r=e.Symbol;return"function"==typeof r?r.observable?o=r.observable:(o=r("observable"),r.observable=o):o="@@observable",o}Object.defineProperty(exports,"__esModule",{value:!0}),exports.default=e;
},{}],"LkZ7":[function(require,module,exports) {
var global = arguments[3];
var e=arguments[3];Object.defineProperty(exports,"__esModule",{value:!0}),exports.default=void 0;var d,o=t(require("./ponyfill.js"));function t(e){return e&&e.__esModule?e:{default:e}}d="undefined"!=typeof self?self:"undefined"!=typeof window?window:void 0!==e?e:"undefined"!=typeof module?module:Function("return this")();var u=(0,o.default)(d),n=u;exports.default=n;
},{"./ponyfill.js":"JZ8d"}],"UALh":[function(require,module,exports) {
"use strict";const e=require("symbol-observable").default;module.exports=(o=>Boolean(o&&o[e]&&o===o[e]()));
},{"symbol-observable":"LkZ7"}],"huOx":[function(require,module,exports) {
"use strict";function e(e,r){const i=e.deserialize.bind(e),a=e.serialize.bind(e);return{deserialize:e=>r.deserialize(e,i),serialize:e=>r.serialize(e,a)}}Object.defineProperty(exports,"__esModule",{value:!0}),exports.DefaultSerializer=exports.extendSerializer=void 0,exports.extendSerializer=e;const r={deserialize:e=>Object.assign(Error(e.message),{name:e.name,stack:e.stack}),serialize:e=>({__error_marker:"$$error",message:e.message,name:e.name,stack:e.stack})},i=e=>e&&"object"==typeof e&&"__error_marker"in e&&"$$error"===e.__error_marker;exports.DefaultSerializer={deserialize:e=>i(e)?r.deserialize(e):e,serialize:e=>e instanceof Error?r.serialize(e):e};
},{}],"ujDW":[function(require,module,exports) {
"use strict";Object.defineProperty(exports,"__esModule",{value:!0}),exports.serialize=exports.deserialize=exports.registerSerializer=void 0;const e=require("./serializers");let r=e.DefaultSerializer;function i(i){r=e.extendSerializer(r,i)}function t(e){return r.deserialize(e)}function s(e){return r.serialize(e)}exports.registerSerializer=i,exports.deserialize=t,exports.serialize=s;
},{"./serializers":"huOx"}],"NcLz":[function(require,module,exports) {
"use strict";Object.defineProperty(exports,"__esModule",{value:!0}),exports.$worker=exports.$transferable=exports.$terminate=exports.$events=exports.$errors=void 0,exports.$errors=Symbol("thread.errors"),exports.$events=Symbol("thread.events"),exports.$terminate=Symbol("thread.terminate"),exports.$transferable=Symbol("thread.transferable"),exports.$worker=Symbol("thread.worker");
},{}],"HnZs":[function(require,module,exports) {
"use strict";Object.defineProperty(exports,"__esModule",{value:!0}),exports.Transfer=exports.isTransferDescriptor=void 0;const r=require("./symbols");function e(r){return!(!r||"object"!=typeof r)}function t(e){return e&&"object"==typeof e&&e[r.$transferable]}function s(t,s){if(!s){if(!e(t))throw Error();s=[t]}return{[r.$transferable]:!0,send:t,transferables:s}}exports.isTransferDescriptor=t,exports.Transfer=s;
},{"./symbols":"NcLz"}],"No47":[function(require,module,exports) {
"use strict";var e,r;Object.defineProperty(exports,"__esModule",{value:!0}),exports.WorkerMessageType=exports.MasterMessageType=void 0,function(e){e.cancel="cancel",e.run="run"}(e=exports.MasterMessageType||(exports.MasterMessageType={})),function(e){e.error="error",e.init="init",e.result="result",e.running="running",e.uncaughtError="uncaughtError"}(r=exports.WorkerMessageType||(exports.WorkerMessageType={}));
},{}],"Oz27":[function(require,module,exports) {
"use strict";Object.defineProperty(exports,"__esModule",{value:!0});const e=function(){const e="undefined"!=typeof self&&"undefined"!=typeof Window&&self instanceof Window;return!("undefined"==typeof self||!self.postMessage||e)},s=function(e,s){self.postMessage(e,s)},t=function(e){const s=s=>{e(s.data)};return self.addEventListener("message",s),()=>{self.removeEventListener("message",s)}};exports.default={isWorkerRuntime:e,postMessageToMaster:s,subscribeToMasterMessages:t};
},{}],"pBGv":[function(require,module,exports) {

var t,e,n=module.exports={};function r(){throw new Error("setTimeout has not been defined")}function o(){throw new Error("clearTimeout has not been defined")}function i(e){if(t===setTimeout)return setTimeout(e,0);if((t===r||!t)&&setTimeout)return t=setTimeout,setTimeout(e,0);try{return t(e,0)}catch(n){try{return t.call(null,e,0)}catch(n){return t.call(this,e,0)}}}function u(t){if(e===clearTimeout)return clearTimeout(t);if((e===o||!e)&&clearTimeout)return e=clearTimeout,clearTimeout(t);try{return e(t)}catch(n){try{return e.call(null,t)}catch(n){return e.call(this,t)}}}!function(){try{t="function"==typeof setTimeout?setTimeout:r}catch(n){t=r}try{e="function"==typeof clearTimeout?clearTimeout:o}catch(n){e=o}}();var c,s=[],l=!1,a=-1;function f(){l&&c&&(l=!1,c.length?s=c.concat(s):a=-1,s.length&&h())}function h(){if(!l){var t=i(f);l=!0;for(var e=s.length;e;){for(c=s,s=[];++a<e;)c&&c[a].run();a=-1,e=s.length}c=null,l=!1,u(t)}}function m(t,e){this.fun=t,this.array=e}function p(){}n.nextTick=function(t){var e=new Array(arguments.length-1);if(arguments.length>1)for(var n=1;n<arguments.length;n++)e[n-1]=arguments[n];s.push(new m(t,e)),1!==s.length||l||i(h)},m.prototype.run=function(){this.fun.apply(null,this.array)},n.title="browser",n.env={},n.argv=[],n.version="",n.versions={},n.on=p,n.addListener=p,n.once=p,n.off=p,n.removeListener=p,n.removeAllListeners=p,n.emit=p,n.prependListener=p,n.prependOnceListener=p,n.listeners=function(t){return[]},n.binding=function(t){throw new Error("process.binding is not supported")},n.cwd=function(){return"/"},n.chdir=function(t){throw new Error("process.chdir is not supported")},n.umask=function(){return 0};
},{}],"DwFB":[function(require,module,exports) {
var process = require("process");
var e=require("process"),t=this&&this.__awaiter||function(e,t,r,s){return new(r||(r=Promise))(function(o,n){function i(e){try{u(s.next(e))}catch(t){n(t)}}function a(e){try{u(s.throw(e))}catch(t){n(t)}}function u(e){var t;e.done?o(e.value):(t=e.value,t instanceof r?t:new r(function(e){e(t)})).then(i,a)}u((s=s.apply(e,t||[])).next())})},r=this&&this.__importDefault||function(e){return e&&e.__esModule?e:{default:e}};Object.defineProperty(exports,"__esModule",{value:!0}),exports.expose=exports.isWorkerRuntime=void 0;const s=r(require("is-observable")),o=require("../common"),n=require("../transferable"),i=require("../types/messages"),a=r(require("./implementation"));var u=require("../common");Object.defineProperty(exports,"registerSerializer",{enumerable:!0,get:function(){return u.registerSerializer}});var c=require("../transferable");Object.defineProperty(exports,"Transfer",{enumerable:!0,get:function(){return c.Transfer}}),exports.isWorkerRuntime=a.default.isWorkerRuntime;let f=!1;const l=new Map,p=e=>e&&e.type===i.MasterMessageType.cancel,d=e=>e&&e.type===i.MasterMessageType.run,y=e=>s.default(e)||g(e);function g(e){return e&&"object"==typeof e&&"function"==typeof e.subscribe}function m(e){return n.isTransferDescriptor(e)?{payload:e.send,transferables:e.transferables}:{payload:e,transferables:void 0}}function b(){const e={type:i.WorkerMessageType.init,exposed:{type:"function"}};a.default.postMessageToMaster(e)}function h(e){const t={type:i.WorkerMessageType.init,exposed:{type:"module",methods:e}};a.default.postMessageToMaster(t)}function M(e,t){const{payload:r,transferables:s}=m(t),n={type:i.WorkerMessageType.error,uid:e,error:o.serialize(r)};a.default.postMessageToMaster(n,s)}function T(e,t,r){const{payload:s,transferables:o}=m(r),n={type:i.WorkerMessageType.result,uid:e,complete:!!t||void 0,payload:s};a.default.postMessageToMaster(n,o)}function x(e,t){const r={type:i.WorkerMessageType.running,uid:e,resultType:t};a.default.postMessageToMaster(r)}function v(e){try{const r={type:i.WorkerMessageType.uncaughtError,error:o.serialize(e)};a.default.postMessageToMaster(r)}catch(t){console.error("Not reporting uncaught error back to master thread as it occured while reporting an uncaught error already.\nLatest error:",t,"\nOriginal error:",e)}}function k(e,r,s){return t(this,void 0,void 0,function*(){let t;try{t=r(...s)}catch(i){return M(e,i)}const n=y(t)?"observable":"promise";if(x(e,n),y(t)){const r=t.subscribe(t=>T(e,!1,o.serialize(t)),t=>{M(e,o.serialize(t)),l.delete(e)},()=>{T(e,!0),l.delete(e)});l.set(e,r)}else try{const r=yield t;T(e,!0,o.serialize(r))}catch(i){M(e,o.serialize(i))}})}function W(e){if(!a.default.isWorkerRuntime())throw Error("expose() called in the master thread.");if(f)throw Error("expose() called more than once. This is not possible. Pass an object to expose() if you want to expose multiple functions.");if(f=!0,"function"==typeof e)a.default.subscribeToMasterMessages(t=>{d(t)&&!t.method&&k(t.uid,e,t.args.map(o.deserialize))}),b();else{if("object"!=typeof e||!e)throw Error(`Invalid argument passed to expose(). Expected a function or an object, got: ${e}`);a.default.subscribeToMasterMessages(t=>{d(t)&&t.method&&k(t.uid,e[t.method],t.args.map(o.deserialize))}),h(Object.keys(e).filter(t=>"function"==typeof e[t]))}a.default.subscribeToMasterMessages(e=>{if(p(e)){const t=e.uid,r=l.get(t);r&&(r.unsubscribe(),l.delete(t))}})}exports.expose=W,"undefined"!=typeof self&&"function"==typeof self.addEventListener&&a.default.isWorkerRuntime()&&(self.addEventListener("error",e=>{setTimeout(()=>v(e.error||e),250)}),self.addEventListener("unhandledrejection",e=>{const t=e.reason;t&&"string"==typeof t.message&&setTimeout(()=>v(t),250)})),void 0!==e&&"function"==typeof e.on&&a.default.isWorkerRuntime()&&(e.on("uncaughtException",e=>{setTimeout(()=>v(e),250)}),e.on("unhandledRejection",e=>{e&&"string"==typeof e.message&&setTimeout(()=>v(e),250)}));
},{"is-observable":"UALh","../common":"ujDW","../transferable":"HnZs","../types/messages":"No47","./implementation":"Oz27","process":"pBGv"}],"g6uu":[function(require,module,exports) {
module.exports=require("./dist/worker/index");
},{"./dist/worker/index":"DwFB"}],"rgp3":[function(require,module,exports) {
"use strict";Object.defineProperty(exports,"__esModule",{value:!0}),exports.simplifyErrorMessageInLog=e,exports.updateAvatarCode=i;var t=require("threads/worker");function n(t,n){return t.players.find(t=>t.id===n)}async function o(){self.languagePluginUrl="https://pyodide-cdn2.iodide.io/v0.15.0/full/",importScripts("https://pyodide-cdn2.iodide.io/v0.15.0/full/pyodide.js"),await languagePluginLoader,await pyodide.loadPackage(["micropip"]),await pyodide.runPythonAsync(`\nimport micropip\n\nmicropip.install("${self.location.origin}/static/worker/aimmo_game_worker-0.0.0-py3-none-any.whl")\n  `),await pyodide.runPythonAsync('\nfrom simulation import direction\nfrom simulation import location\nfrom simulation.action import MoveAction, PickupAction, WaitAction, MoveTowardsAction\nfrom simulation.world_map import WorldMapCreator\nfrom simulation.avatar_state import create_avatar_state\nfrom io import StringIO\nimport contextlib\n\n\n@contextlib.contextmanager\ndef capture_output(stdout=None, stderr=None):\n  """Temporarily switches stdout and stderr to stringIO objects or variable."""\n  old_out = sys.stdout\n  old_err = sys.stderr\n\n  if stdout is None:\n      stdout = StringIO()\n  if stderr is None:\n      stderr = StringIO()\n  sys.stdout = stdout\n  sys.stderr = stderr\n  yield stdout, stderr\n\n  sys.stdout = old_out\n  sys.stderr = old_err\n')}async function r(t,o){const r=n(t,o);try{return await pyodide.runPythonAsync(`\ngame_state = ${JSON.stringify(t)}\nworld_map = WorldMapCreator.generate_world_map_from_game_state(game_state)\navatar_state = create_avatar_state(${JSON.stringify(r)})\nserialized_action = {"action_type": "wait"}\nwith capture_output() as output:\n    action = next_turn(world_map, avatar_state)\n    if action is None:\n        raise Exception("Make sure you are returning an action")\n    serialized_action = action.serialise()\nstdout, stderr = output\nlogs = stdout.getvalue() + stderr.getvalue()\n{"action": serialized_action, "log": logs, "turnCount": game_state["turnCount"] + 1}\n    `)}catch(i){return Promise.resolve({action:{action_type:"wait"},log:e(i.toString()),turnCount:t.turnCount+1})}}function e(t){const n=t.match(/.*line (\d+), in next_turn\n((?:.|\n)*)/);return(null==n?void 0:null==n?void 0:n.length)>=2?`Uh oh! Something isn't correct on line ${n[1]}. Here's the error we got:\n${n[2]}`:t.split("\n").slice(-2).join("\n")}async function i(t,n,o=0){let i=0;n&&(i=n.turnCount+1);try{return await pyodide.runPythonAsync(t),n?r(n,o):Promise.resolve({action:{action_type:"wait"},log:"",turnCount:i})}catch(s){return await a(),Promise.resolve({action:{action_type:"wait"},log:e(s.toString()),turnCount:i})}}async function a(){await pyodide.runPythonAsync("def next_turn(world_map, avatar_state):\n    return WaitAction()")}const s={initializePyodide:o,computeNextAction:r,updateAvatarCode:i};(0,t.expose)(s);
},{"threads/worker":"g6uu"}]},{},["rgp3"], null)
//# sourceMappingURL=/static/react/webWorker.1848e605.js.map