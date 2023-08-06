(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[9928],{23682:(e,t,r)=>{"use strict";function i(e,t){if(t.length<e)throw new TypeError(e+" argument"+(e>1?"s":"")+" required, but only "+t.length+" present")}r.d(t,{Z:()=>i})},90394:(e,t,r)=>{"use strict";function i(e){if(null===e||!0===e||!1===e)return NaN;var t=Number(e);return isNaN(t)?t:t<0?Math.ceil(t):Math.floor(t)}r.d(t,{Z:()=>i})},59699:(e,t,r)=>{"use strict";r.d(t,{Z:()=>a});var i=r(90394),n=r(39244),o=r(23682),s=36e5;function a(e,t){(0,o.Z)(2,arguments);var r=(0,i.Z)(t);return(0,n.Z)(e,r*s)}},39244:(e,t,r)=>{"use strict";r.d(t,{Z:()=>s});var i=r(90394),n=r(34327),o=r(23682);function s(e,t){(0,o.Z)(2,arguments);var r=(0,n.Z)(e).getTime(),s=(0,i.Z)(t);return new Date(r+s)}},93752:(e,t,r)=>{"use strict";r.d(t,{Z:()=>o});var i=r(34327),n=r(23682);function o(e){(0,n.Z)(1,arguments);var t=(0,i.Z)(e);return t.setHours(23,59,59,999),t}},70390:(e,t,r)=>{"use strict";r.d(t,{Z:()=>n});var i=r(93752);function n(){return(0,i.Z)(Date.now())}},61334:(e,t,r)=>{"use strict";function i(){var e=new Date,t=e.getFullYear(),r=e.getMonth(),i=e.getDate(),n=new Date(0);return n.setFullYear(t,r,i-1),n.setHours(23,59,59,999),n}r.d(t,{Z:()=>i})},59429:(e,t,r)=>{"use strict";r.d(t,{Z:()=>o});var i=r(34327),n=r(23682);function o(e){(0,n.Z)(1,arguments);var t=(0,i.Z)(e);return t.setHours(0,0,0,0),t}},27088:(e,t,r)=>{"use strict";r.d(t,{Z:()=>n});var i=r(59429);function n(){return(0,i.Z)(Date.now())}},83008:(e,t,r)=>{"use strict";function i(){var e=new Date,t=e.getFullYear(),r=e.getMonth(),i=e.getDate(),n=new Date(0);return n.setFullYear(t,r,i-1),n.setHours(0,0,0,0),n}r.d(t,{Z:()=>i})},34327:(e,t,r)=>{"use strict";r.d(t,{Z:()=>n});var i=r(23682);function n(e){(0,i.Z)(1,arguments);var t=Object.prototype.toString.call(e);return e instanceof Date||"object"==typeof e&&"[object Date]"===t?new Date(e.getTime()):"number"==typeof e||"[object Number]"===t?new Date(e):("string"!=typeof e&&"[object String]"!==t||"undefined"==typeof console||(console.warn("Starting with v2.0.0-beta.1 date-fns doesn't accept strings as date arguments. Please use `parseISO` to parse strings. See: https://git.io/fjule"),console.warn((new Error).stack)),new Date(NaN))}},11950:(e,t,r)=>{"use strict";r.d(t,{l:()=>i});const i=async(e,t)=>new Promise((r=>{const i=t(e,(e=>{i(),r(e)}))}))},81582:(e,t,r)=>{"use strict";r.d(t,{LZ:()=>i,pB:()=>n,SO:()=>o,iJ:()=>s,Nn:()=>a,Ny:()=>c,T0:()=>l});const i=2143==r.j?["migration_error","setup_error","setup_retry"]:null,n=e=>e.callApi("GET","config/config_entries/entry"),o=(e,t,r)=>e.callWS({type:"config_entries/update",entry_id:t,...r}),s=(e,t)=>e.callApi("DELETE",`config/config_entries/entry/${t}`),a=(e,t)=>e.callApi("POST",`config/config_entries/entry/${t}/reload`),c=(e,t)=>e.callWS({type:"config_entries/disable",entry_id:t,disabled_by:"user"}),l=(e,t)=>e.callWS({type:"config_entries/disable",entry_id:t,disabled_by:null})},55424:(e,t,r)=>{"use strict";r.d(t,{Bm:()=>p,o1:()=>h,iK:()=>m,rl:()=>y,ZC:()=>g,_Z:()=>b,Jj:()=>_,UB:()=>w});var i=r(59699),n=r(27088),o=r(83008),s=r(70390),a=r(61334),c=r(95282),l=r(11950),d=r(81582),u=r(74186),f=r(58763);const p=()=>({stat_energy_from:"",stat_cost:null,entity_energy_from:null,entity_energy_price:null,number_energy_price:null}),h=()=>({stat_energy_to:"",stat_compensation:null,entity_energy_to:null,entity_energy_price:null,number_energy_price:null}),m=()=>({type:"grid",flow_from:[],flow_to:[],cost_adjustment_day:0}),y=()=>({type:"solar",stat_energy_from:"",config_entry_solar_forecast:null}),v=e=>e.callWS({type:"energy/info"}),g=e=>e.callWS({type:"energy/get_prefs"}),b=async(e,t)=>{const r=e.callWS({type:"energy/save_prefs",...t}),i=w(e);return i.clearPrefs(),i._active&&i.refresh(),r},_=e=>{const t={};for(const r of e.energy_sources)r.type in t?t[r.type].push(r):t[r.type]=[r];return t},w=(e,t)=>{if(e.connection._energy)return e.connection._energy;const r=(0,c._)(e.connection,"_energy",(async()=>{if(r.prefs||(r.prefs=await g(e)),r._refreshTimeout&&clearTimeout(r._refreshTimeout),r._active&&(!r.end||r.end>new Date)){const e=new Date;e.getMinutes()>20&&e.setHours(e.getHours()+1),e.setMinutes(20),r._refreshTimeout=window.setTimeout((()=>r.refresh()),e.getTime()-Date.now())}return(async(e,t,r,n)=>{const[o,s,a]=await Promise.all([(0,d.pB)(e),(0,l.l)(e.connection,u.LM),v(e)]),c=o.find((e=>"co2signal"===e.domain));let p;if(c)for(const t of s){if(t.config_entry_id!==c.entry_id)continue;const r=e.states[t.entity_id];if(r&&"%"===r.attributes.unit_of_measurement){p=r.entity_id;break}}const h=[];void 0!==p&&h.push(p);for(const e of t.energy_sources)if("solar"!==e.type){for(const t of e.flow_from)h.push(t.stat_energy_from);for(const t of e.flow_to)h.push(t.stat_energy_to)}else h.push(e.stat_energy_from);return{start:r,end:n,info:a,prefs:t,stats:await(0,f.dL)(e,(0,i.Z)(r,-1),n,h),co2SignalConfigEntry:c,co2SignalEntity:p}})(e,r.prefs,r.start,r.end)})),p=r.subscribe;r.subscribe=e=>{const t=p(e);return r._active++,()=>{r._active--,r._active<1&&(clearTimeout(r._refreshTimeout),r._refreshTimeout=void 0),t()}},r._active=0,r.prefs=t;const h=new Date;r.start=h.getHours()>0?(0,n.Z)():(0,o.Z)(),r.end=h.getHours()>0?(0,s.Z)():(0,a.Z)();const m=()=>{r._updatePeriodTimeout=window.setTimeout((()=>{r.start=(0,n.Z)(),r.end=(0,s.Z)(),m()}),(0,i.Z)((0,s.Z)(),1).getTime()-Date.now())};return m(),r.clearPrefs=()=>{r.prefs=void 0},r.setPeriod=(e,t)=>{var i;r.start=e,r.end=t,r._updatePeriodTimeout&&(clearTimeout(r._updatePeriodTimeout),r._updatePeriodTimeout=void 0),r.start.getTime()===(0,n.Z)().getTime()&&(null===(i=r.end)||void 0===i?void 0:i.getTime())===(0,s.Z)().getTime()&&m()},r}},74186:(e,t,r)=>{"use strict";r.d(t,{eD:()=>s,Mw:()=>a,vA:()=>c,L3:()=>l,Nv:()=>d,z3:()=>u,LM:()=>h});var i=r(95282);if(2143==r.j)var n=r(91741);var o=r(38346);const s=(e,t)=>t.find((t=>e.states[t.entity_id]&&"battery"===e.states[t.entity_id].attributes.device_class)),a=(e,t)=>t.find((t=>e.states[t.entity_id]&&"battery_charging"===e.states[t.entity_id].attributes.device_class)),c=(e,t)=>{if(t.name)return t.name;const r=e.states[t.entity_id];return r?(0,n.C)(r):null},l=(e,t)=>e.callWS({type:"config/entity_registry/get",entity_id:t}),d=(e,t,r)=>e.callWS({type:"config/entity_registry/update",entity_id:t,...r}),u=(e,t)=>e.callWS({type:"config/entity_registry/remove",entity_id:t}),f=e=>e.sendMessagePromise({type:"config/entity_registry/list"}),p=(e,t)=>e.subscribeEvents((0,o.D)((()=>f(e).then((e=>t.setState(e,!0)))),500,!0),"entity_registry_updated"),h=(e,t)=>(0,i.B)("_entityRegistry",f,p,e,t)},58763:(e,t,r)=>{"use strict";r.d(t,{vq:()=>c,_J:()=>l,Nu:()=>u,uR:()=>f,dL:()=>p,Kj:()=>h,q6:()=>m,Nw:()=>y,m2:()=>g});var i=r(29171),n=r(22311),o=r(91741);const s=["climate","humidifier","water_heater"],a=["temperature","current_temperature","target_temp_low","target_temp_high","hvac_action","humidity","mode"],c=(e,t,r,i,n=!1,o,s=!0)=>{let a="history/period";return r&&(a+="/"+r.toISOString()),a+="?filter_entity_id="+t,i&&(a+="&end_time="+i.toISOString()),n&&(a+="&skip_initial_state"),void 0!==o&&(a+=`&significant_changes_only=${Number(o)}`),s&&(a+="&minimal_response"),e.callApi("GET",a)},l=(e,t,r,i)=>e.callApi("GET",`history/period/${t.toISOString()}?end_time=${r.toISOString()}&minimal_response${i?`&filter_entity_id=${i}`:""}`),d=(e,t)=>e.state===t.state&&(!e.attributes||!t.attributes||a.every((r=>e.attributes[r]===t.attributes[r]))),u=(e,t,r)=>{const c={},l=[];if(!t)return{line:[],timeline:[]};t.forEach((t=>{if(0===t.length)return;const s=t.find((e=>e.attributes&&"unit_of_measurement"in e.attributes));let a;a=s?s.attributes.unit_of_measurement:{climate:e.config.unit_system.temperature,counter:"#",humidifier:"%",input_number:"#",number:"#",water_heater:e.config.unit_system.temperature}[(0,n.N)(t[0])],a?a in c?c[a].push(t):c[a]=[t]:l.push(((e,t,r)=>{const n=[],s=r.length-1;for(const o of r)n.length>0&&o.state===n[n.length-1].state||(o.entity_id||(o.attributes=r[s].attributes,o.entity_id=r[s].entity_id),n.push({state_localize:(0,i.D)(e,o,t),state:o.state,last_changed:o.last_changed}));return{name:(0,o.C)(r[0]),entity_id:r[0].entity_id,data:n}})(r,e.locale,t))}));return{line:Object.keys(c).map((e=>((e,t)=>{const r=[];for(const e of t){const t=e[e.length-1],i=(0,n.N)(t),c=[];for(const t of e){let e;if(s.includes(i)){e={state:t.state,last_changed:t.last_updated,attributes:{}};for(const r of a)r in t.attributes&&(e.attributes[r]=t.attributes[r])}else e=t;c.length>1&&d(e,c[c.length-1])&&d(e,c[c.length-2])||c.push(e)}r.push({domain:i,name:(0,o.C)(t),entity_id:t.entity_id,states:c})}return{unit:e,identifier:t.map((e=>e[0].entity_id)).join(""),data:r}})(e,c[e]))),timeline:l}},f=(e,t)=>e.callWS({type:"history/list_statistic_ids",statistic_type:t}),p=(e,t,r,i)=>e.callWS({type:"history/statistics_during_period",start_time:t.toISOString(),end_time:null==r?void 0:r.toISOString(),statistic_ids:i}),h=e=>{if(!e||e.length<2)return null;const t=e[e.length-1].sum;if(null===t)return null;const r=e[0].sum;return null===r?t:t-r},m=(e,t)=>{let r=null;for(const i of t){if(!(i in e))continue;const t=h(e[i]);null!==t&&(null===r?r=t:r+=t)}return r},y=(e,t)=>e.some((e=>null!==e[t])),v=e=>{let t=null,r=null;for(const i of e){if(0===i.length)continue;const e=new Date(i[0].start);null!==t?e<r&&(t=i[0].start,r=e):(t=i[0].start,r=e)}return t},g=(e,t)=>{let r=null;if(0===t.length)return null;const i=(e=>{const t=[],r=e.map((e=>[...e]));for(;r.some((e=>e.length>0));){const e=v(r);let i=0;for(const t of r){if(0===t.length)continue;if(t[0].start!==e)continue;const r=t.shift();r.sum&&(i+=r.sum)}t.push({start:e,sum:i})}return t})(t),n=[...e];let o=null;for(const t of i){if(new Date(t.start)>=new Date(e[0].start))break;o=t.sum}for(;n.length>0;){if(!i.length)return r;if(i[0].start!==n[0].start){new Date(i[0].start)<new Date(n[0].start)?i.shift():n.shift();continue}const e=i.shift(),t=n.shift();if(null!==o){const i=e.sum-o;null===r?r=i*(t.mean/100):r+=i*(t.mean/100)}o=e.sum}return r}},73826:(e,t,r)=>{"use strict";r.d(t,{f:()=>m});var i=r(55358);function n(e,t,r,i){var n=o();if(i)for(var d=0;d<i.length;d++)n=i[d](n);var u=t((function(e){n.initializeInstanceElements(e,f.elements)}),r),f=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(l(o.descriptor)||l(n.descriptor)){if(c(o)||c(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(c(o)){if(c(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}a(o,n)}else t.push(o)}return t}(u.d.map(s)),e);return n.initializeClassElements(u.F,f.elements),n.runClassFinishers(u.F,f.finishers)}function o(){o=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!c(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return f(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?f(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=u(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:d(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=d(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function s(e){var t,r=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function a(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function l(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function d(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function f(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function p(e,t,r){return(p="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=h(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}})(e,t,r||e)}function h(e){return(h=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const m=e=>n(null,(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",key:"__unsubs",value:void 0},{kind:"method",key:"connectedCallback",value:function(){p(h(r.prototype),"connectedCallback",this).call(this),this.__checkSubscribed()}},{kind:"method",key:"disconnectedCallback",value:function(){if(p(h(r.prototype),"disconnectedCallback",this).call(this),this.__unsubs){for(;this.__unsubs.length;){const e=this.__unsubs.pop();e instanceof Promise?e.then((e=>e())):e()}this.__unsubs=void 0}}},{kind:"method",key:"updated",value:function(e){p(h(r.prototype),"updated",this).call(this,e),e.has("hass")&&this.__checkSubscribed()}},{kind:"method",key:"hassSubscribe",value:function(){return[]}},{kind:"method",key:"__checkSubscribed",value:function(){void 0===this.__unsubs&&this.isConnected&&void 0!==this.hass&&(this.__unsubs=this.hassSubscribe())}}]}}),e)},9928:(e,t,r)=>{"use strict";r.r(t);var i=r(50424),n=r(55358),o=r(76666),s=r(82816),a=r(45524),c=(r(22098),r(52039),r(55424)),l=r(58763),d=r(73826);function u(){u=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!h(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);r.push.apply(r,l)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return g(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?g(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=v(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:y(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=y(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function f(e){var t,r=v(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function p(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function m(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function y(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function v(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function g(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}const b=238.76104;!function(e,t,r,i){var n=u();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(m(o.descriptor)||m(n.descriptor)){if(h(o)||h(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(h(o)){if(h(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}p(o,n)}else t.push(o)}return t}(s.d.map(f)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,n.Mo)("hui-energy-distribution-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_data",value:void 0},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"hassSubscribe",value:function(){return[(0,c.UB)(this.hass).subscribe((e=>{this._data=e}))]}},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"render",value:function(){var e,t;if(!this._config)return i.dy``;if(!this._data)return i.dy`Loading…`;const r=this._data.prefs,n=(0,c.Jj)(r),d=void 0!==n.solar,u=n.grid[0].flow_to.length>0,f=null!==(e=(0,l.q6)(this._data.stats,n.grid[0].flow_from.map((e=>e.stat_energy_from))))&&void 0!==e?e:0;let p=null;d&&(p=(0,l.q6)(this._data.stats,n.solar.map((e=>e.stat_energy_from)))||0);let h=null;u&&(h=(0,l.q6)(this._data.stats,n.grid[0].flow_to.map((e=>e.stat_energy_to)))||0);const m=Math.max(0,(p||0)-(h||0)),y=f+m;let v,g,_,w,k;if(d&&(v=b*(m/y)),this._data.co2SignalEntity&&this._data.co2SignalEntity in this._data.stats){const e=(0,l.m2)(this._data.stats[this._data.co2SignalEntity],n.grid[0].flow_from.map((e=>this._data.stats[e.stat_energy_from])).filter(Boolean)),t=this.hass.states[this._data.co2SignalEntity];t&&(k=`https://www.electricitymap.org/zone/${t.attributes.country_code}`),null!==e&&(g=f-e,w=b*(e/y),_=b-(v||0)-w)}return i.dy`
      <ha-card .header=${this._config.title}>
        <div class="card-content">
          ${void 0!==g||d?i.dy`<div class="row">
                ${void 0===g?i.dy`<div class="spacer"></div>`:i.dy`<div class="circle-container low-carbon">
                      <span class="label">Non-fossil</span>
                      <a
                        class="circle"
                        href=${(0,s.o)(k)}
                        target="_blank"
                        rel="noopener no referrer"
                      >
                        <ha-svg-icon .path="${"M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z"}"></ha-svg-icon>
                        ${g?(0,a.u)(g,this.hass.locale,{maximumFractionDigits:1}):"-"}
                        kWh
                      </a>
                      <svg width="80" height="30">
                        <line x1="40" y1="0" x2="40" y2="30"></line>
                      </svg>
                    </div>`}
                ${d?i.dy`<div class="circle-container solar">
                      <span class="label">Solar</span>
                      <div class="circle">
                        <ha-svg-icon .path="${"M11.45,2V5.55L15,3.77L11.45,2M10.45,8L8,10.46L11.75,11.71L10.45,8M2,11.45L3.77,15L5.55,11.45H2M10,2H2V10C2.57,10.17 3.17,10.25 3.77,10.25C7.35,10.26 10.26,7.35 10.27,3.75C10.26,3.16 10.17,2.57 10,2M17,22V16H14L19,7V13H22L17,22Z"}"></ha-svg-icon>
                        ${(0,a.u)(p||0,this.hass.locale,{maximumFractionDigits:1})}
                        kWh
                      </div>
                    </div>`:""}
                <div class="spacer"></div>
              </div>`:""}
          <div class="row">
            <div class="circle-container grid">
              <div class="circle">
                <ha-svg-icon .path="${"M8.28,5.45L6.5,4.55L7.76,2H16.23L17.5,4.55L15.72,5.44L15,4H9L8.28,5.45M18.62,8H14.09L13.3,5H10.7L9.91,8H5.38L4.1,10.55L5.89,11.44L6.62,10H17.38L18.1,11.45L19.89,10.56L18.62,8M17.77,22H15.7L15.46,21.1L12,15.9L8.53,21.1L8.3,22H6.23L9.12,11H11.19L10.83,12.35L12,14.1L13.16,12.35L12.81,11H14.88L17.77,22M11.4,15L10.5,13.65L9.32,18.13L11.4,15M14.68,18.12L13.5,13.64L12.6,15L14.68,18.12Z"}"></ha-svg-icon>
                <span class="consumption">
                  ${u?i.dy`<ha-svg-icon
                        class="small"
                        .path=${"M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"}
                      ></ha-svg-icon>`:""}${(0,a.u)(f,this.hass.locale,{maximumFractionDigits:1})}
                  kWh
                </span>
                ${null!==h?i.dy`<span class="return">
                      <ha-svg-icon
                        class="small"
                        .path=${"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}
                      ></ha-svg-icon
                      >${(0,a.u)(h,this.hass.locale,{maximumFractionDigits:1})}
                      kWh
                    </span>`:""}
              </div>
              <span class="label">Grid</span>
            </div>
            <div class="circle-container home">
              <div
                class="circle ${(0,o.$)({border:void 0===v&&void 0===_})}"
              >
                <ha-svg-icon .path="${"M10,20V14H14V20H19V12H22L12,3L2,12H5V20H10Z"}"></ha-svg-icon>
                ${(0,a.u)(y,this.hass.locale,{maximumFractionDigits:1})}
                kWh
                ${void 0!==v||void 0!==_?i.dy`<svg>
                      ${void 0!==v?i.YP`<circle
                            class="solar"
                            cx="40"
                            cy="40"
                            r="38"
                            stroke-dasharray="${v} ${b-v}"
                            shape-rendering="geometricPrecision"
                            stroke-dashoffset="-${b-v}"
                          />`:""}
                      ${_?i.YP`<circle
                            class="low-carbon"
                            cx="40"
                            cy="40"
                            r="38"
                            stroke-dasharray="${_} ${b-_}"
                            stroke-dashoffset="-${b-_-(v||0)}"
                            shape-rendering="geometricPrecision"
                          />`:""}
                      <circle
                        class="grid"
                        cx="40"
                        cy="40"
                        r="38"
                        stroke-dasharray="${null!==(t=w)&&void 0!==t?t:b-v} ${void 0!==w?b-w:v}"
                        stroke-dashoffset="0"
                        shape-rendering="geometricPrecision"
                      />
                    </svg>`:""}
              </div>
              <span class="label">Home</span>
            </div>
          </div>
          <div class="lines">
            <svg
              viewBox="0 0 100 100"
              xmlns="http://www.w3.org/2000/svg"
              preserveAspectRatio="xMidYMid slice"
            >
              ${u&&d?i.YP`<path
                    id="return"
                    class="return"
                    d="M47,0 v15 c0,40 -10,35 -30,35 h-20"
                    vector-effect="non-scaling-stroke"
                  ></path> `:""}
              ${d?i.YP`<path
                    id="solar"
                    class="solar"
                    d="M${u?53:50},0 v15 c0,40 10,35 30,35 h20"
                    vector-effect="non-scaling-stroke"
                  ></path>`:""}
              <path
                class="grid"
                id="grid"
                d="M0,${d?56:53} H100"
                vector-effect="non-scaling-stroke"
              ></path>
              ${h&&d?i.YP`<circle
                    r="1"
                    class="return"
                    vector-effect="non-scaling-stroke"
                  >
                    <animateMotion
                      dur="${6-h/(f+(p||0))*5}s"
                      repeatCount="indefinite"
                      rotate="auto"
                    >
                      <mpath xlink:href="#return" />
                    </animateMotion>
                  </circle>`:""}
              ${p?i.YP`<circle
                    r="1"
                    class="solar"
                    vector-effect="non-scaling-stroke"
                  >
                    <animateMotion
                      dur="${6-(p-(h||0))/(f+(p||0))*5}s"
                      repeatCount="indefinite"
                      rotate="auto"
                    >
                      <mpath xlink:href="#solar" />
                    </animateMotion>
                  </circle>`:""}
              ${f?i.YP`<circle
                    r="1"
                    class="grid"
                    vector-effect="non-scaling-stroke"
                  >
                    <animateMotion
                      dur="${6-f/(f+(p||0))*5}s"
                      repeatCount="indefinite"
                      rotate="auto"
                    >
                      <mpath xlink:href="#grid" />
                    </animateMotion>
                  </circle>`:""}
            </svg>
          </div>
        </div>
      </ha-card>
    `}},{kind:"field",static:!0,key:"styles",value:()=>i.iv`
    :host {
      --mdc-icon-size: 24px;
    }
    .card-content {
      position: relative;
    }
    .lines {
      position: absolute;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 146px;
      display: flex;
      justify-content: center;
      padding: 0 16px 16px;
      box-sizing: border-box;
    }
    .lines svg {
      width: calc(100% - 160px);
      height: 100%;
      max-width: 340px;
    }
    .row {
      display: flex;
      justify-content: space-between;
      max-width: 500px;
      margin: 0 auto;
    }
    .circle-container {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .circle-container.low-carbon {
      margin-right: 4px;
    }
    .circle-container.solar {
      margin-left: 4px;
      height: 130px;
    }
    .spacer {
      width: 84px;
    }
    .circle {
      width: 80px;
      height: 80px;
      border-radius: 50%;
      box-sizing: border-box;
      border: 2px solid;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      font-size: 12px;
      line-height: 12px;
      position: relative;
      text-decoration: none;
      color: var(--primary-text-color);
    }
    ha-svg-icon {
      padding-bottom: 2px;
    }
    ha-svg-icon.small {
      --mdc-icon-size: 12px;
    }
    .label {
      color: var(--secondary-text-color);
      font-size: 12px;
    }
    line,
    path {
      stroke: var(--primary-text-color);
      stroke-width: 1;
      fill: none;
    }
    .circle svg {
      position: absolute;
      fill: none;
      stroke-width: 4px;
      width: 100%;
      height: 100%;
    }
    .low-carbon line {
      stroke: var(--energy-non-fossil-color);
    }
    .low-carbon .circle {
      border-color: var(--energy-non-fossil-color);
    }
    .low-carbon ha-svg-icon {
      color: var(--energy-non-fossil-color);
    }
    circle.low-carbon {
      stroke: var(--energy-non-fossil-color);
      fill: var(--energy-non-fossil-color);
    }
    .solar .circle {
      border-color: var(--energy-solar-color);
    }
    circle.solar,
    path.solar {
      stroke: var(--energy-solar-color);
    }
    circle.solar {
      stroke-width: 4;
      fill: var(--energy-solar-color);
    }
    path.return,
    circle.return {
      stroke: var(--energy-grid-return-color);
    }
    circle.return {
      stroke-width: 4;
      fill: var(--energy-grid-return-color);
    }
    .return {
      color: var(--energy-grid-return-color);
    }
    .grid .circle {
      border-color: var(--energy-grid-consumption-color);
    }
    .consumption {
      color: var(--energy-grid-consumption-color);
    }
    circle.grid,
    path.grid {
      stroke: var(--energy-grid-consumption-color);
    }
    circle.grid {
      stroke-width: 4;
      fill: var(--energy-grid-consumption-color);
    }
    .home .circle {
      border-width: 0;
      border-color: var(--primary-color);
    }
    .home .circle.border {
      border-width: 2px;
    }
    .circle svg circle {
      animation: rotate-in 0.6s ease-in;
      transition: stroke-dashoffset 0.4s, stroke-dasharray 0.4s;
      fill: none;
    }
    @keyframes rotate-in {
      from {
        stroke-dashoffset: 238.76104;
        stroke-dasharray: 238.76104;
      }
    }
  `}]}}),(0,d.f)(i.oi))}}]);
//# sourceMappingURL=f91ddf2b.js.map