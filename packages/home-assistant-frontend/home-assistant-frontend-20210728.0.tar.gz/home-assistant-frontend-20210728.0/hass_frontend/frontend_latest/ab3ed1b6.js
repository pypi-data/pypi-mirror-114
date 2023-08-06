(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[9928],{27593:(t,e,r)=>{"use strict";r.d(e,{N:()=>i});const i=(t,e=2)=>Math.round(t*10**e)/10**e},11950:(t,e,r)=>{"use strict";r.d(e,{l:()=>i});const i=async(t,e)=>new Promise((r=>{const i=e(t,(t=>{i(),r(t)}))}))},81582:(t,e,r)=>{"use strict";r.d(e,{LZ:()=>i,pB:()=>n,SO:()=>s,iJ:()=>o,Nn:()=>a,Ny:()=>l,T0:()=>c});const i=2143==r.j?["migration_error","setup_error","setup_retry"]:null,n=t=>t.callApi("GET","config/config_entries/entry"),s=(t,e,r)=>t.callWS({type:"config_entries/update",entry_id:e,...r}),o=(t,e)=>t.callApi("DELETE",`config/config_entries/entry/${e}`),a=(t,e)=>t.callApi("POST",`config/config_entries/entry/${e}/reload`),l=(t,e)=>t.callWS({type:"config_entries/disable",entry_id:e,disabled_by:"user"}),c=(t,e)=>t.callWS({type:"config_entries/disable",entry_id:e,disabled_by:null})},55424:(t,e,r)=>{"use strict";r.d(e,{Bm:()=>i,o1:()=>n,iK:()=>s,rl:()=>o,xZ:()=>a,ZC:()=>l,_Z:()=>c,Jj:()=>d});const i=()=>({stat_energy_from:"",stat_cost:null,entity_energy_from:null,entity_energy_price:null,number_energy_price:null}),n=()=>({stat_energy_to:"",stat_compensation:null,entity_energy_to:null,entity_energy_price:null,number_energy_price:null}),s=()=>({type:"grid",flow_from:[],flow_to:[],cost_adjustment_day:0}),o=()=>({type:"solar",stat_energy_from:"",config_entry_solar_forecast:null}),a=t=>t.callWS({type:"energy/info"}),l=t=>t.callWS({type:"energy/get_prefs"}),c=(t,e)=>t.callWS({type:"energy/save_prefs",...e}),d=t=>{const e={};for(const r of t.energy_sources)r.type in e?e[r.type].push(r):e[r.type]=[r];return e}},74186:(t,e,r)=>{"use strict";r.d(e,{eD:()=>o,Mw:()=>a,vA:()=>l,L3:()=>c,Nv:()=>d,z3:()=>f,LM:()=>h});var i=r(95282);if(2143==r.j)var n=r(91741);var s=r(38346);const o=(t,e)=>e.find((e=>t.states[e.entity_id]&&"battery"===t.states[e.entity_id].attributes.device_class)),a=(t,e)=>e.find((e=>t.states[e.entity_id]&&"battery_charging"===t.states[e.entity_id].attributes.device_class)),l=(t,e)=>{if(e.name)return e.name;const r=t.states[e.entity_id];return r?(0,n.C)(r):null},c=(t,e)=>t.callWS({type:"config/entity_registry/get",entity_id:e}),d=(t,e,r)=>t.callWS({type:"config/entity_registry/update",entity_id:e,...r}),f=(t,e)=>t.callWS({type:"config/entity_registry/remove",entity_id:e}),u=t=>t.sendMessagePromise({type:"config/entity_registry/list"}),p=(t,e)=>t.subscribeEvents((0,s.D)((()=>u(t).then((t=>e.setState(t,!0)))),500,!0),"entity_registry_updated"),h=(t,e)=>(0,i.B)("_entityRegistry",u,p,t,e)},58763:(t,e,r)=>{"use strict";r.d(e,{vq:()=>l,_J:()=>c,Nu:()=>f,uR:()=>u,dL:()=>p,Kj:()=>h,q6:()=>y,Nw:()=>m,m2:()=>v});var i=r(29171),n=r(22311),s=r(91741);const o=["climate","humidifier","water_heater"],a=["temperature","current_temperature","target_temp_low","target_temp_high","hvac_action","humidity","mode"],l=(t,e,r,i,n=!1,s,o=!0)=>{let a="history/period";return r&&(a+="/"+r.toISOString()),a+="?filter_entity_id="+e,i&&(a+="&end_time="+i.toISOString()),n&&(a+="&skip_initial_state"),void 0!==s&&(a+=`&significant_changes_only=${Number(s)}`),o&&(a+="&minimal_response"),t.callApi("GET",a)},c=(t,e,r,i)=>t.callApi("GET",`history/period/${e.toISOString()}?end_time=${r.toISOString()}&minimal_response${i?`&filter_entity_id=${i}`:""}`),d=(t,e)=>t.state===e.state&&(!t.attributes||!e.attributes||a.every((r=>t.attributes[r]===e.attributes[r]))),f=(t,e,r)=>{const l={},c=[];if(!e)return{line:[],timeline:[]};e.forEach((e=>{if(0===e.length)return;const o=e.find((t=>t.attributes&&"unit_of_measurement"in t.attributes));let a;a=o?o.attributes.unit_of_measurement:{climate:t.config.unit_system.temperature,counter:"#",humidifier:"%",input_number:"#",number:"#",water_heater:t.config.unit_system.temperature}[(0,n.N)(e[0])],a?a in l?l[a].push(e):l[a]=[e]:c.push(((t,e,r)=>{const n=[],o=r.length-1;for(const s of r)n.length>0&&s.state===n[n.length-1].state||(s.entity_id||(s.attributes=r[o].attributes,s.entity_id=r[o].entity_id),n.push({state_localize:(0,i.D)(t,s,e),state:s.state,last_changed:s.last_changed}));return{name:(0,s.C)(r[0]),entity_id:r[0].entity_id,data:n}})(r,t.locale,e))}));return{line:Object.keys(l).map((t=>((t,e)=>{const r=[];for(const t of e){const e=t[t.length-1],i=(0,n.N)(e),l=[];for(const e of t){let t;if(o.includes(i)){t={state:e.state,last_changed:e.last_updated,attributes:{}};for(const r of a)r in e.attributes&&(t.attributes[r]=e.attributes[r])}else t=e;l.length>1&&d(t,l[l.length-1])&&d(t,l[l.length-2])||l.push(t)}r.push({domain:i,name:(0,s.C)(e),entity_id:e.entity_id,states:l})}return{unit:t,identifier:e.map((t=>t[0].entity_id)).join(""),data:r}})(t,l[t]))),timeline:c}},u=(t,e)=>t.callWS({type:"history/list_statistic_ids",statistic_type:e}),p=(t,e,r,i)=>t.callWS({type:"history/statistics_during_period",start_time:e.toISOString(),end_time:null==r?void 0:r.toISOString(),statistic_ids:i}),h=t=>{if(!t||t.length<2)return null;const e=t[t.length-1].sum;if(null===e)return null;const r=t[0].sum;return null===r?e:e-r},y=(t,e)=>{let r=null;for(const i of e){if(!(i in t))continue;const e=h(t[i]);null!==e&&(null===r?r=e:r+=e)}return r},m=(t,e)=>t.some((t=>null!==t[e])),g=t=>{let e=null,r=null;for(const i of t){if(0===i.length)continue;const t=new Date(i[0].start);null!==e?t<r&&(e=i[0].start,r=t):(e=i[0].start,r=t)}return e},v=(t,e)=>{let r=null;if(0===e.length)return null;const i=(t=>{const e=[],r=t.map((t=>[...t]));for(;r.some((t=>t.length>0));){const t=g(r);let i=0;for(const e of r){if(0===e.length)continue;if(e[0].start!==t)continue;const r=e.shift();r.sum&&(i+=r.sum)}e.push({start:t,sum:i})}return e})(e),n=[...t];let s=null;for(const e of i){if(new Date(e.start)>=new Date(t[0].start))break;s=e.sum}for(;n.length>0;){if(!i.length)return r;if(i[0].start!==n[0].start){new Date(i[0].start)<new Date(n[0].start)?i.shift():n.shift();continue}const t=i.shift(),e=n.shift();if(null!==s){const i=t.sum-s;null===r?r=i*(e.mean/100):r+=i*(e.mean/100)}s=t.sum}return r}},9928:(t,e,r)=>{"use strict";r.r(e);var i=r(50424),n=r(55358),s=r(76666),o=r(82816),a=r(27593),l=r(11950),c=(r(22098),r(52039),r(81582)),d=r(55424),f=r(74186),u=r(58763);function p(){p=function(){return t};var t={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(t,e){["method","field"].forEach((function(r){e.forEach((function(e){e.kind===r&&"own"===e.placement&&this.defineClassElement(t,e)}),this)}),this)},initializeClassElements:function(t,e){var r=t.prototype;["method","field"].forEach((function(i){e.forEach((function(e){var n=e.placement;if(e.kind===i&&("static"===n||"prototype"===n)){var s="static"===n?t:r;this.defineClassElement(s,e)}}),this)}),this)},defineClassElement:function(t,e){var r=e.descriptor;if("field"===e.kind){var i=e.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(t)}}Object.defineProperty(t,e.key,r)},decorateClass:function(t,e){var r=[],i=[],n={static:[],prototype:[],own:[]};if(t.forEach((function(t){this.addElementPlacement(t,n)}),this),t.forEach((function(t){if(!m(t))return r.push(t);var e=this.decorateElement(t,n);r.push(e.element),r.push.apply(r,e.extras),i.push.apply(i,e.finishers)}),this),!e)return{elements:r,finishers:i};var s=this.decorateConstructor(r,e);return i.push.apply(i,s.finishers),s.finishers=i,s},addElementPlacement:function(t,e,r){var i=e[t.placement];if(!r&&-1!==i.indexOf(t.key))throw new TypeError("Duplicated element ("+t.key+")");i.push(t.key)},decorateElement:function(t,e){for(var r=[],i=[],n=t.decorators,s=n.length-1;s>=0;s--){var o=e[t.placement];o.splice(o.indexOf(t.key),1);var a=this.fromElementDescriptor(t),l=this.toElementFinisherExtras((0,n[s])(a)||a);t=l.element,this.addElementPlacement(t,e),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],e);r.push.apply(r,c)}}return{element:t,finishers:i,extras:r}},decorateConstructor:function(t,e){for(var r=[],i=e.length-1;i>=0;i--){var n=this.fromClassDescriptor(t),s=this.toClassDescriptor((0,e[i])(n)||n);if(void 0!==s.finisher&&r.push(s.finisher),void 0!==s.elements){t=s.elements;for(var o=0;o<t.length-1;o++)for(var a=o+1;a<t.length;a++)if(t[o].key===t[a].key&&t[o].placement===t[a].placement)throw new TypeError("Duplicated element ("+t[o].key+")")}}return{elements:t,finishers:r}},fromElementDescriptor:function(t){var e={kind:t.kind,key:t.key,placement:t.placement,descriptor:t.descriptor};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===t.kind&&(e.initializer=t.initializer),e},toElementDescriptors:function(t){var e;if(void 0!==t)return(e=t,function(t){if(Array.isArray(t))return t}(e)||function(t){if("undefined"!=typeof Symbol&&null!=t[Symbol.iterator]||null!=t["@@iterator"])return Array.from(t)}(e)||function(t,e){if(t){if("string"==typeof t)return b(t,e);var r=Object.prototype.toString.call(t).slice(8,-1);return"Object"===r&&t.constructor&&(r=t.constructor.name),"Map"===r||"Set"===r?Array.from(t):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?b(t,e):void 0}}(e)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(t){var e=this.toElementDescriptor(t);return this.disallowProperty(t,"finisher","An element descriptor"),this.disallowProperty(t,"extras","An element descriptor"),e}),this)},toElementDescriptor:function(t){var e=String(t.kind);if("method"!==e&&"field"!==e)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+e+'"');var r=_(t.key),i=String(t.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=t.descriptor;this.disallowProperty(t,"elements","An element descriptor");var s={kind:e,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==e?this.disallowProperty(t,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),s.initializer=t.initializer),s},toElementFinisherExtras:function(t){return{element:this.toElementDescriptor(t),finisher:v(t,"finisher"),extras:this.toElementDescriptors(t.extras)}},fromClassDescriptor:function(t){var e={kind:"class",elements:t.map(this.fromElementDescriptor,this)};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),e},toClassDescriptor:function(t){var e=String(t.kind);if("class"!==e)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+e+'"');this.disallowProperty(t,"key","A class descriptor"),this.disallowProperty(t,"placement","A class descriptor"),this.disallowProperty(t,"descriptor","A class descriptor"),this.disallowProperty(t,"initializer","A class descriptor"),this.disallowProperty(t,"extras","A class descriptor");var r=v(t,"finisher");return{elements:this.toElementDescriptors(t.elements),finisher:r}},runClassFinishers:function(t,e){for(var r=0;r<e.length;r++){var i=(0,e[r])(t);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");t=i}}return t},disallowProperty:function(t,e,r){if(void 0!==t[e])throw new TypeError(r+" can't have a ."+e+" property.")}};return t}function h(t){var e,r=_(t.key);"method"===t.kind?e={value:t.value,writable:!0,configurable:!0,enumerable:!1}:"get"===t.kind?e={get:t.value,configurable:!0,enumerable:!1}:"set"===t.kind?e={set:t.value,configurable:!0,enumerable:!1}:"field"===t.kind&&(e={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===t.kind?"field":"method",key:r,placement:t.static?"static":"field"===t.kind?"own":"prototype",descriptor:e};return t.decorators&&(i.decorators=t.decorators),"field"===t.kind&&(i.initializer=t.value),i}function y(t,e){void 0!==t.descriptor.get?e.descriptor.get=t.descriptor.get:e.descriptor.set=t.descriptor.set}function m(t){return t.decorators&&t.decorators.length}function g(t){return void 0!==t&&!(void 0===t.value&&void 0===t.writable)}function v(t,e){var r=t[e];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+e+"' to be a function");return r}function _(t){var e=function(t,e){if("object"!=typeof t||null===t)return t;var r=t[Symbol.toPrimitive];if(void 0!==r){var i=r.call(t,e||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===e?String:Number)(t)}(t,"string");return"symbol"==typeof e?e:String(e)}function b(t,e){(null==e||e>t.length)&&(e=t.length);for(var r=0,i=new Array(e);r<e;r++)i[r]=t[r];return i}function w(t,e,r){return(w="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(t,e,r){var i=function(t,e){for(;!Object.prototype.hasOwnProperty.call(t,e)&&null!==(t=k(t)););return t}(t,e);if(i){var n=Object.getOwnPropertyDescriptor(i,e);return n.get?n.get.call(r):n.value}})(t,e,r||t)}function k(t){return(k=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)})(t)}const L=238.76104;!function(t,e,r,i){var n=p();if(i)for(var s=0;s<i.length;s++)n=i[s](n);var o=e((function(t){n.initializeInstanceElements(t,a.elements)}),r),a=n.decorateClass(function(t){for(var e=[],r=function(t){return"method"===t.kind&&t.key===s.key&&t.placement===s.placement},i=0;i<t.length;i++){var n,s=t[i];if("method"===s.kind&&(n=e.find(r)))if(g(s.descriptor)||g(n.descriptor)){if(m(s)||m(n))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");n.descriptor=s.descriptor}else{if(m(s)){if(m(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");n.decorators=s.decorators}y(s,n)}else e.push(s)}return e}(o.d.map(h)),t);n.initializeClassElements(o.F,a.elements),n.runClassFinishers(o.F,a.finishers)}([(0,n.Mo)("hui-energy-distribution-card")],(function(t,e){class r extends e{constructor(...e){super(...e),t(this)}}return{F:r,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_stats",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_co2SignalEntity",value:void 0},{kind:"field",key:"_fetching",value:()=>!1},{kind:"method",key:"setConfig",value:function(t){this._config=t}},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"willUpdate",value:function(t){w(k(r.prototype),"willUpdate",this).call(this,t),this._fetching||this._stats||(this._fetching=!0,this._getStatistics().then((()=>{this._fetching=!1})))}},{kind:"method",key:"render",value:function(){var t,e;if(!this._config)return i.dy``;if(!this._stats)return i.dy`Loading…`;const r=this._config.prefs,n=(0,d.Jj)(r),l=void 0!==n.solar,c=n.grid[0].flow_to.length>0,f=null!==(t=(0,u.q6)(this._stats,n.grid[0].flow_from.map((t=>t.stat_energy_from))))&&void 0!==t?t:0;let p=null;l&&(p=(0,u.q6)(this._stats,n.solar.map((t=>t.stat_energy_from)))||0);let h=null;c&&(h=(0,u.q6)(this._stats,n.grid[0].flow_to.map((t=>t.stat_energy_to)))||0);const y=f+(p||0)-(h||0);let m,g,v,_,b;if(l){m=L*(((p||0)-(h||0))/y)}if(this._co2SignalEntity&&this._co2SignalEntity in this._stats){const t=(0,u.m2)(this._stats[this._co2SignalEntity],n.grid[0].flow_from.map((t=>this._stats[t.stat_energy_from])).filter(Boolean)),e=this.hass.states[this._co2SignalEntity];if(e&&(b=`https://www.electricitymap.org/zone/${e.attributes.country_code}`),null!==t){const e=t/y;g=f-f*e;_=L*(e*f/y),v=L-(m||0)-_}}return i.dy`
      <ha-card .header=${this._config.title}>
        <div class="card-content">
          ${void 0!==g||l?i.dy`<div class="row">
                ${void 0===g?i.dy`<div class="spacer"></div>`:i.dy`
                      <div class="circle-container low-carbon">
                        <span class="label">Non-fossil</span>
                        <a
                          class="circle"
                          href=${(0,o.o)(b)}
                          target="_blank"
                          rel="noopener no referrer"
                        >
                          <ha-svg-icon .path="${"M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z"}"></ha-svg-icon>
                          ${(0,a.N)(g,1)} kWh
                        </a>
                        <svg width="80" height="30">
                          <line x1="40" y1="0" x2="40" y2="30"></line>
                        </svg>
                      </div>
                    `}
                ${l?i.dy`<div class="circle-container solar">
                      <span class="label">Solar</span>
                      <div class="circle">
                        <ha-svg-icon .path="${"M11.45,2V5.55L15,3.77L11.45,2M10.45,8L8,10.46L11.75,11.71L10.45,8M2,11.45L3.77,15L5.55,11.45H2M10,2H2V10C2.57,10.17 3.17,10.25 3.77,10.25C7.35,10.26 10.26,7.35 10.27,3.75C10.26,3.16 10.17,2.57 10,2M17,22V16H14L19,7V13H22L17,22Z"}"></ha-svg-icon>
                        ${(0,a.N)(p||0,1)} kWh
                      </div>
                    </div>`:""}
                <div class="spacer"></div>
              </div>`:""}
          <div class="row">
            <div class="circle-container grid">
              <div class="circle">
                <ha-svg-icon .path="${"M8.28,5.45L6.5,4.55L7.76,2H16.23L17.5,4.55L15.72,5.44L15,4H9L8.28,5.45M18.62,8H14.09L13.3,5H10.7L9.91,8H5.38L4.1,10.55L5.89,11.44L6.62,10H17.38L18.1,11.45L19.89,10.56L18.62,8M17.77,22H15.7L15.46,21.1L12,15.9L8.53,21.1L8.3,22H6.23L9.12,11H11.19L10.83,12.35L12,14.1L13.16,12.35L12.81,11H14.88L17.77,22M11.4,15L10.5,13.65L9.32,18.13L11.4,15M14.68,18.12L13.5,13.64L12.6,15L14.68,18.12Z"}"></ha-svg-icon>
                <span class="consumption">
                  ${c?i.dy`<ha-svg-icon
                        class="small"
                        .path=${"M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"}
                      ></ha-svg-icon>`:""}${(0,a.N)(f,1)}
                  kWh
                </span>
                ${null!==h?i.dy`<span class="return">
                      <ha-svg-icon
                        class="small"
                        .path=${"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}
                      ></ha-svg-icon
                      >${(0,a.N)(h,1)} kWh
                    </span>`:""}
              </div>
              <span class="label">Grid</span>
            </div>
            <div class="circle-container home">
              <div
                class="circle ${(0,s.$)({border:void 0===m&&void 0===v})}"
              >
                <ha-svg-icon .path="${"M10,20V14H14V20H19V12H22L12,3L2,12H5V20H10Z"}"></ha-svg-icon>
                ${(0,a.N)(y,1)} kWh
                ${void 0!==m||void 0!==v?i.dy`<svg>
                      ${void 0!==m?i.YP`
              <circle
                  class="solar"
                  cx="40"
                  cy="40"
                  r="38"
                  stroke-dasharray="${m} ${L-m}"
                  shape-rendering="geometricPrecision"
                  stroke-dashoffset="0"
                />`:""}
                      ${_?i.YP`
                <circle
                  class="low-carbon"
                  cx="40"
                  cy="40"
                  r="38"
                  stroke-dasharray="${v} ${L-v}"
                  stroke-dashoffset="${-1*((m||0)+_)}"
                  shape-rendering="geometricPrecision"
                />`:""}
                      <circle
                        class="grid"
                        cx="40"
                        cy="40"
                        r="38"
                        stroke-dasharray="${null!==(e=_)&&void 0!==e?e:L-m} ${_?L-_:m}"
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
              preserveAspectRatio="xMidYMid slice"
            >
              ${c&&l?i.YP`<path
                    id="return"
                    class="return"
                    d="M47,0 v15 c0,40 -10,35 -30,35 h-20"
                    vector-effect="non-scaling-stroke"
                  ></path> `:""}
              ${l?i.YP`<path
                    id="solar"
                    class="solar"
                    d="M${c?53:50},0 v15 c0,40 10,35 30,35 h20"
                    vector-effect="non-scaling-stroke"
                  ></path>`:""}
              <path
                class="grid"
                id="grid"
                d="M0,${l?56:53} H100"
                vector-effect="non-scaling-stroke"
              ></path>
              ${h&&l?i.YP`<circle r="1" class="return" vector-effect="non-scaling-stroke">
                    <animateMotion
                      dur="${6-h/(f+(p||0))*5}s"
                      repeatCount="indefinite"
                      rotate="auto"
                    >
                      <mpath xlink:href="#return" />
                    </animateMotion>
                  </circle>`:""}
              ${p?i.YP`
                <circle r="1" class="solar" vector-effect="non-scaling-stroke">
                    <animateMotion
                      dur="${6-(p-(h||0))/(f+(p||0))*5}s"
                      repeatCount="indefinite"
                      rotate="auto"
                    >
                      <mpath xlink:href="#solar" />
                    </animateMotion>
                  </circle>`:""}
              ${f?i.YP`<circle r="1" class="grid" vector-effect="non-scaling-stroke">
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
    `}},{kind:"method",key:"_getStatistics",value:async function(){const[t,e]=await Promise.all([(0,c.pB)(this.hass),(0,l.l)(this.hass.connection,f.LM)]),r=t.find((t=>"co2signal"===t.domain));if(this._co2SignalEntity=void 0,r)for(const t of e){if(t.config_entry_id!==r.entry_id)continue;const e=this.hass.states[t.entity_id];if(e&&"%"===e.attributes.unit_of_measurement){this._co2SignalEntity=e.entity_id;break}}const i=new Date;i.setHours(0,0,0,0),i.setTime(i.getTime()-36e5);const n=[];void 0!==this._co2SignalEntity&&n.push(this._co2SignalEntity);const s=this._config.prefs;for(const t of s.energy_sources)if("solar"!==t.type){for(const e of t.flow_from)n.push(e.stat_energy_from);for(const e of t.flow_to)n.push(e.stat_energy_to)}else n.push(t.stat_energy_from);this._stats=await(0,u.dL)(this.hass,i,void 0,n)}},{kind:"field",static:!0,key:"styles",value:()=>i.iv`
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
    circle.solar,
    path.solar {
      stroke: #ff9800;
    }
    circle.solar {
      stroke-width: 4;
      fill: #ff9800;
    }
    circle.low-carbon {
      stroke: #0f9d58;
      fill: #0f9d58;
    }
    path.return,
    circle.return {
      stroke: #673ab7;
    }
    circle.return {
      stroke-width: 4;
      fill: #673ab7;
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
    circle.grid {
      stroke-width: 4;
      fill: #126a9a;
    }
    .home .circle {
      border: none;
    }
    .home .circle.border {
      border-color: var(--primary-color);
    }
    .circle svg circle {
      animation: rotate-in 0.2s ease-in;
      fill: none;
    }
    @keyframes rotate-in {
      from {
        stroke-dashoffset: 0;
      }
    }
  `}]}}),i.oi)}}]);
//# sourceMappingURL=ab3ed1b6.js.map