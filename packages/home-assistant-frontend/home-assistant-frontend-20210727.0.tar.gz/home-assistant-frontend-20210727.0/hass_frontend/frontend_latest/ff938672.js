(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[9928],{27593:(e,t,i)=>{"use strict";i.d(t,{N:()=>r});const r=(e,t=2)=>Math.round(e*10**t)/10**t},11950:(e,t,i)=>{"use strict";i.d(t,{l:()=>r});const r=async(e,t)=>new Promise((i=>{const r=t(e,(e=>{r(),i(e)}))}))},81582:(e,t,i)=>{"use strict";i.d(t,{LZ:()=>r,pB:()=>n,SO:()=>s,iJ:()=>o,Nn:()=>a,Ny:()=>l,T0:()=>c});const r=2143==i.j?["migration_error","setup_error","setup_retry"]:null,n=e=>e.callApi("GET","config/config_entries/entry"),s=(e,t,i)=>e.callWS({type:"config_entries/update",entry_id:t,...i}),o=(e,t)=>e.callApi("DELETE",`config/config_entries/entry/${t}`),a=(e,t)=>e.callApi("POST",`config/config_entries/entry/${t}/reload`),l=(e,t)=>e.callWS({type:"config_entries/disable",entry_id:t,disabled_by:"user"}),c=(e,t)=>e.callWS({type:"config_entries/disable",entry_id:t,disabled_by:null})},55424:(e,t,i)=>{"use strict";i.d(t,{Bm:()=>r,o1:()=>n,iK:()=>s,rl:()=>o,xZ:()=>a,ZC:()=>l,_Z:()=>c,Jj:()=>d});const r=()=>({stat_energy_from:"",stat_cost:null,entity_energy_from:null,entity_energy_price:null,number_energy_price:null}),n=()=>({stat_energy_to:"",stat_compensation:null,entity_energy_to:null,entity_energy_price:null,number_energy_price:null}),s=()=>({type:"grid",flow_from:[],flow_to:[],cost_adjustment_day:0}),o=()=>({type:"solar",stat_energy_from:"",config_entry_solar_forecast:null}),a=e=>e.callWS({type:"energy/info"}),l=e=>e.callWS({type:"energy/get_prefs"}),c=(e,t)=>e.callWS({type:"energy/save_prefs",...t}),d=e=>{const t={};for(const i of e.energy_sources)i.type in t?t[i.type].push(i):t[i.type]=[i];return t}},74186:(e,t,i)=>{"use strict";i.d(t,{eD:()=>o,Mw:()=>a,vA:()=>l,L3:()=>c,Nv:()=>d,z3:()=>f,LM:()=>h});var r=i(95282);if(2143==i.j)var n=i(91741);var s=i(38346);const o=(e,t)=>t.find((t=>e.states[t.entity_id]&&"battery"===e.states[t.entity_id].attributes.device_class)),a=(e,t)=>t.find((t=>e.states[t.entity_id]&&"battery_charging"===e.states[t.entity_id].attributes.device_class)),l=(e,t)=>{if(t.name)return t.name;const i=e.states[t.entity_id];return i?(0,n.C)(i):null},c=(e,t)=>e.callWS({type:"config/entity_registry/get",entity_id:t}),d=(e,t,i)=>e.callWS({type:"config/entity_registry/update",entity_id:t,...i}),f=(e,t)=>e.callWS({type:"config/entity_registry/remove",entity_id:t}),p=e=>e.sendMessagePromise({type:"config/entity_registry/list"}),u=(e,t)=>e.subscribeEvents((0,s.D)((()=>p(e).then((e=>t.setState(e,!0)))),500,!0),"entity_registry_updated"),h=(e,t)=>(0,r.B)("_entityRegistry",p,u,e,t)},58763:(e,t,i)=>{"use strict";i.d(t,{vq:()=>l,_J:()=>c,Nu:()=>f,uR:()=>p,dL:()=>u,Kj:()=>h,q6:()=>y,Nw:()=>m});var r=i(29171),n=i(22311),s=i(91741);const o=["climate","humidifier","water_heater"],a=["temperature","current_temperature","target_temp_low","target_temp_high","hvac_action","humidity","mode"],l=(e,t,i,r,n=!1,s,o=!0)=>{let a="history/period";return i&&(a+="/"+i.toISOString()),a+="?filter_entity_id="+t,r&&(a+="&end_time="+r.toISOString()),n&&(a+="&skip_initial_state"),void 0!==s&&(a+=`&significant_changes_only=${Number(s)}`),o&&(a+="&minimal_response"),e.callApi("GET",a)},c=(e,t,i,r)=>e.callApi("GET",`history/period/${t.toISOString()}?end_time=${i.toISOString()}&minimal_response${r?`&filter_entity_id=${r}`:""}`),d=(e,t)=>e.state===t.state&&(!e.attributes||!t.attributes||a.every((i=>e.attributes[i]===t.attributes[i]))),f=(e,t,i)=>{const l={},c=[];if(!t)return{line:[],timeline:[]};t.forEach((t=>{if(0===t.length)return;const o=t.find((e=>e.attributes&&"unit_of_measurement"in e.attributes));let a;a=o?o.attributes.unit_of_measurement:{climate:e.config.unit_system.temperature,counter:"#",humidifier:"%",input_number:"#",number:"#",water_heater:e.config.unit_system.temperature}[(0,n.N)(t[0])],a?a in l?l[a].push(t):l[a]=[t]:c.push(((e,t,i)=>{const n=[],o=i.length-1;for(const s of i)n.length>0&&s.state===n[n.length-1].state||(s.entity_id||(s.attributes=i[o].attributes,s.entity_id=i[o].entity_id),n.push({state_localize:(0,r.D)(e,s,t),state:s.state,last_changed:s.last_changed}));return{name:(0,s.C)(i[0]),entity_id:i[0].entity_id,data:n}})(i,e.locale,t))}));return{line:Object.keys(l).map((e=>((e,t)=>{const i=[];for(const e of t){const t=e[e.length-1],r=(0,n.N)(t),l=[];for(const t of e){let e;if(o.includes(r)){e={state:t.state,last_changed:t.last_updated,attributes:{}};for(const i of a)i in t.attributes&&(e.attributes[i]=t.attributes[i])}else e=t;l.length>1&&d(e,l[l.length-1])&&d(e,l[l.length-2])||l.push(e)}i.push({domain:r,name:(0,s.C)(t),entity_id:t.entity_id,states:l})}return{unit:e,identifier:t.map((e=>e[0].entity_id)).join(""),data:i}})(e,l[e]))),timeline:c}},p=(e,t)=>e.callWS({type:"history/list_statistic_ids",statistic_type:t}),u=(e,t,i,r)=>e.callWS({type:"history/statistics_during_period",start_time:t.toISOString(),end_time:null==i?void 0:i.toISOString(),statistic_ids:r}),h=e=>{if(!e||e.length<2)return null;const t=e[e.length-1].sum;if(null===t)return null;const i=e[0].sum;return null===i?t:t-i},y=(e,t)=>{let i=null;for(const r of t){if(!(r in e))continue;const t=h(e[r]);null!==t&&(null===i?i=t:i+=t)}return i},m=(e,t)=>e.some((e=>null!==e[t]))},9928:(e,t,i)=>{"use strict";i.r(t);var r=i(50424),n=i(55358),s=i(76666),o=i(27593),a=i(11950),l=(i(22098),i(52039),i(81582)),c=i(55424),d=i(74186),f=i(58763);function p(){p=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var s="static"===n?e:i;this.defineClassElement(s,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!y(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var s=this.decorateConstructor(i,t);return r.push.apply(r,s.finishers),s.finishers=r,s},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,s=n.length-1;s>=0;s--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[s])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==s.finisher&&i.push(s.finisher),void 0!==s.elements){e=s.elements;for(var o=0;o<e.length-1;o++)for(var a=o+1;a<e.length;a++)if(e[o].key===e[a].key&&e[o].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return _(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?_(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=v(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:g(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=g(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function u(e){var t,i=v(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function h(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function y(e){return e.decorators&&e.decorators.length}function m(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function g(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function v(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function _(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function b(e,t,i){return(b="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=w(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function w(e){return(w=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const k=238.76104;!function(e,t,i,r){var n=p();if(r)for(var s=0;s<r.length;s++)n=r[s](n);var o=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},r=0;r<e.length;r++){var n,s=e[r];if("method"===s.kind&&(n=t.find(i)))if(m(s.descriptor)||m(n.descriptor)){if(y(s)||y(n))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");n.descriptor=s.descriptor}else{if(y(s)){if(y(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");n.decorators=s.decorators}h(s,n)}else t.push(s)}return t}(o.d.map(u)),e);n.initializeClassElements(o.F,a.elements),n.runClassFinishers(o.F,a.finishers)}([(0,n.Mo)("hui-energy-distribution-card")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_stats",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_co2SignalEntity",value:void 0},{kind:"field",key:"_fetching",value:()=>!1},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"willUpdate",value:function(e){b(w(i.prototype),"willUpdate",this).call(this,e),this._fetching||this._stats||(this._fetching=!0,Promise.all([this._getStatistics(),this._fetchCO2SignalEntity()]).then((()=>{this._fetching=!1})))}},{kind:"method",key:"render",value:function(){var e,t;if(!this._config)return r.dy``;if(!this._stats)return r.dy`Loading…`;const i=this._config.prefs,n=(0,c.Jj)(i),a=void 0!==n.solar,l=n.grid[0].flow_to.length>0,d=null!==(e=(0,f.q6)(this._stats,n.grid[0].flow_from.map((e=>e.stat_energy_from))))&&void 0!==e?e:0;let p=null;a&&(p=(0,f.q6)(this._stats,n.solar.map((e=>e.stat_energy_from))));let u,h=null;if(l&&(h=(0,f.q6)(this._stats,n.grid[0].flow_to.map((e=>e.stat_energy_to)))),this._co2SignalEntity){const e=this.hass.states[this._co2SignalEntity];e&&(u=Number(e.state),isNaN(u)&&(u=void 0))}const y=d+(p||0)-(h||0);let m,g,v,_;if(a){m=k*(((p||0)-(h||0))/y)}if(void 0!==u){const e=u/100;g=d-d*e;_=k*(e*d/y),v=k-(m||0)-_}return r.dy`
      <ha-card .header=${this._config.title}>
        <div class="card-content">
          ${void 0!==g||a?r.dy`<div class="row">
                ${void 0===g?r.dy`<div class="spacer"></div>`:r.dy`
                      <div class="circle-container low-carbon">
                        <span class="label">Non-fossil</span>
                        <div class="circle">
                          <ha-svg-icon .path="${"M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z"}"></ha-svg-icon>
                          ${(0,o.N)(g,1)} kWh
                        </div>
                        <svg width="80" height="30">
                          <line x1="40" y1="0" x2="40" y2="30"></line>
                        </svg>
                      </div>
                    `}
                ${a?r.dy`<div class="circle-container solar">
                      <span class="label">Solar</span>
                      <div class="circle">
                        <ha-svg-icon .path="${"M11.45,2V5.55L15,3.77L11.45,2M10.45,8L8,10.46L11.75,11.71L10.45,8M2,11.45L3.77,15L5.55,11.45H2M10,2H2V10C2.57,10.17 3.17,10.25 3.77,10.25C7.35,10.26 10.26,7.35 10.27,3.75C10.26,3.16 10.17,2.57 10,2M17,22V16H14L19,7V13H22L17,22Z"}"></ha-svg-icon>
                        ${(0,o.N)(p||0,1)} kWh
                      </div>
                    </div>`:""}
                <div class="spacer"></div>
              </div>`:""}
          <div class="row">
            <div class="circle-container grid">
              <div class="circle">
                <ha-svg-icon .path="${"M8.28,5.45L6.5,4.55L7.76,2H16.23L17.5,4.55L15.72,5.44L15,4H9L8.28,5.45M18.62,8H14.09L13.3,5H10.7L9.91,8H5.38L4.1,10.55L5.89,11.44L6.62,10H17.38L18.1,11.45L19.89,10.56L18.62,8M17.77,22H15.7L15.46,21.1L12,15.9L8.53,21.1L8.3,22H6.23L9.12,11H11.19L10.83,12.35L12,14.1L13.16,12.35L12.81,11H14.88L17.77,22M11.4,15L10.5,13.65L9.32,18.13L11.4,15M14.68,18.12L13.5,13.64L12.6,15L14.68,18.12Z"}"></ha-svg-icon>
                <span class="consumption">
                  ${l?r.dy`<ha-svg-icon
                        class="small"
                        .path=${"M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"}
                      ></ha-svg-icon>`:""}${(0,o.N)(d,1)}
                  kWh
                </span>
                ${h?r.dy`<span class="return">
                      <ha-svg-icon
                        class="small"
                        .path=${"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}
                      ></ha-svg-icon
                      >${(0,o.N)(h,1)} kWh
                    </span>`:""}
              </div>
              <span class="label">Grid</span>
            </div>
            <div class="circle-container home">
              <div
                class="circle ${(0,s.$)({border:void 0===m&&void 0===v})}"
              >
                <ha-svg-icon .path="${"M10,20V14H14V20H19V12H22L12,3L2,12H5V20H10Z"}"></ha-svg-icon>
                ${(0,o.N)(y,1)} kWh
                ${void 0!==m||void 0!==v?r.dy`<svg>
                      ${void 0!==m?r.YP`
              <circle
                  class="solar"
                  cx="40"
                  cy="40"
                  r="38"
                  stroke-dasharray="${m} ${k-m}"
                  shape-rendering="geometricPrecision"
                  stroke-dashoffset="0"
                />`:""}
                      ${_?r.YP`
                <circle
                  class="low-carbon"
                  cx="40"
                  cy="40"
                  r="38"
                  stroke-dasharray="${v} ${k-v}"
                  stroke-dashoffset="${-1*((m||0)+_)}"
                  shape-rendering="geometricPrecision"
                />`:""}
                      <circle
                        class="grid"
                        cx="40"
                        cy="40"
                        r="38"
                        stroke-dasharray="${null!==(t=_)&&void 0!==t?t:k-m} ${_?k-_:m}"
                        stroke-dashoffset="${-1*(m||0)}"
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
              preserveAspectRatio="none"
            >
              ${h&&a?r.YP`<path
                class="return"
                d="M50,0 v20 c0,40 -10,35 -65,35 h20"
                vector-effect="non-scaling-stroke"
              ></path>`:""}
              ${p?r.YP`<path
                    class="solar"
                    d="M50,0 v20 c0,40 10,35 65,35 h20"
                    vector-effect="non-scaling-stroke"
                  ></path>`:""}
              ${d?r.YP`<path
                class="grid"
                d="M0,55 H100"
                vector-effect="non-scaling-stroke"
              ></path>`:""}
            </svg>
          </div>
        </div>
      </ha-card>
    `}},{kind:"method",key:"_fetchCO2SignalEntity",value:async function(){const[e,t]=await Promise.all([(0,l.pB)(this.hass),(0,a.l)(this.hass.connection,d.LM)]),i=e.find((e=>"co2signal"===e.domain));if(i)for(const e of t){if(e.config_entry_id!==i.entry_id)continue;const t=this.hass.states[e.entity_id];if(t&&"%"===t.attributes.unit_of_measurement){this._co2SignalEntity=t.entity_id;break}}}},{kind:"method",key:"_getStatistics",value:async function(){const e=new Date;e.setHours(0,0,0,0),e.setTime(e.getTime()-36e5);const t=[],i=this._config.prefs;for(const e of i.energy_sources)if("solar"!==e.type){for(const i of e.flow_from)t.push(i.stat_energy_from);for(const i of e.flow_to)t.push(i.stat_energy_to)}else t.push(e.stat_energy_from);this._stats=await(0,f.dL)(this.hass,e,void 0,t)}},{kind:"field",static:!0,key:"styles",value:()=>r.iv`
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
    .circle-container.solar {
      height: 130px;
    }
    .spacer {
      width: 80px;
      height: 30px;
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
    .circle svg circle {
      animation: rotate-in 0.2s ease-in;
    }
    .low-carbon line {
      stroke: #0f9d58;
    }
    .low-carbon .circle {
      border-color: #0f9d58;
    }
    .low-carbon ha-svg-icon {
      color: #0f9d58;
    }
    .solar .circle {
      border-color: #ff9800;
    }
    path.solar,
    circle.solar {
      stroke: #ff9800;
    }
    circle.low-carbon {
      stroke: #0f9d58;
    }
    circle.return,
    path.return {
      stroke: #673ab7;
    }
    .return {
      color: #673ab7;
    }
    .grid .circle {
      border-color: #126a9a;
    }
    .consumption {
      color: #126a9a;
    }
    circle.grid,
    path.grid {
      stroke: #126a9a;
    }
    .home .circle {
      border: none;
    }
    .home .circle.border {
      border-color: var(--primary-color);
    }
    @keyframes rotate-in {
      from {
        stroke-dashoffset: 0;
      }
    }
  `}]}}),r.oi)}}]);
//# sourceMappingURL=ff938672.js.map