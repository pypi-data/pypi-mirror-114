(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[2609],{27593:(e,t,r)=>{"use strict";r.d(t,{N:()=>i});const i=(e,t=2)=>Math.round(e*10**t)/10**t},11950:(e,t,r)=>{"use strict";r.d(t,{l:()=>i});const i=async(e,t)=>new Promise((r=>{const i=t(e,(e=>{i(),r(e)}))}))},81582:(e,t,r)=>{"use strict";r.d(t,{LZ:()=>i,pB:()=>n,SO:()=>o,iJ:()=>s,Nn:()=>a,Ny:()=>l,T0:()=>c});const i=2143==r.j?["migration_error","setup_error","setup_retry"]:null,n=e=>e.callApi("GET","config/config_entries/entry"),o=(e,t,r)=>e.callWS({type:"config_entries/update",entry_id:t,...r}),s=(e,t)=>e.callApi("DELETE",`config/config_entries/entry/${t}`),a=(e,t)=>e.callApi("POST",`config/config_entries/entry/${t}/reload`),l=(e,t)=>e.callWS({type:"config_entries/disable",entry_id:t,disabled_by:"user"}),c=(e,t)=>e.callWS({type:"config_entries/disable",entry_id:t,disabled_by:null})},55424:(e,t,r)=>{"use strict";r.d(t,{Bm:()=>i,o1:()=>n,iK:()=>o,rl:()=>s,xZ:()=>a,ZC:()=>l,_Z:()=>c,Jj:()=>d});const i=()=>({stat_energy_from:"",stat_cost:null,entity_energy_from:null,entity_energy_price:null,number_energy_price:null}),n=()=>({stat_energy_to:"",stat_compensation:null,entity_energy_to:null,entity_energy_price:null,number_energy_price:null}),o=()=>({type:"grid",flow_from:[],flow_to:[],cost_adjustment_day:0}),s=()=>({type:"solar",stat_energy_from:"",config_entry_solar_forecast:null}),a=e=>e.callWS({type:"energy/info"}),l=e=>e.callWS({type:"energy/get_prefs"}),c=(e,t)=>e.callWS({type:"energy/save_prefs",...t}),d=e=>{const t={};for(const r of e.energy_sources)r.type in t?t[r.type].push(r):t[r.type]=[r];return t}},74186:(e,t,r)=>{"use strict";r.d(t,{eD:()=>s,Mw:()=>a,vA:()=>l,L3:()=>c,Nv:()=>d,z3:()=>u,LM:()=>h});var i=r(95282);if(2143==r.j)var n=r(91741);var o=r(38346);const s=(e,t)=>t.find((t=>e.states[t.entity_id]&&"battery"===e.states[t.entity_id].attributes.device_class)),a=(e,t)=>t.find((t=>e.states[t.entity_id]&&"battery_charging"===e.states[t.entity_id].attributes.device_class)),l=(e,t)=>{if(t.name)return t.name;const r=e.states[t.entity_id];return r?(0,n.C)(r):null},c=(e,t)=>e.callWS({type:"config/entity_registry/get",entity_id:t}),d=(e,t,r)=>e.callWS({type:"config/entity_registry/update",entity_id:t,...r}),u=(e,t)=>e.callWS({type:"config/entity_registry/remove",entity_id:t}),f=e=>e.sendMessagePromise({type:"config/entity_registry/list"}),p=(e,t)=>e.subscribeEvents((0,o.D)((()=>f(e).then((e=>t.setState(e,!0)))),500,!0),"entity_registry_updated"),h=(e,t)=>(0,i.B)("_entityRegistry",f,p,e,t)},58763:(e,t,r)=>{"use strict";r.d(t,{vq:()=>l,_J:()=>c,Nu:()=>u,uR:()=>f,dL:()=>p,Kj:()=>h,q6:()=>y,Nw:()=>m});var i=r(29171),n=r(22311),o=r(91741);const s=["climate","humidifier","water_heater"],a=["temperature","current_temperature","target_temp_low","target_temp_high","hvac_action","humidity","mode"],l=(e,t,r,i,n=!1,o,s=!0)=>{let a="history/period";return r&&(a+="/"+r.toISOString()),a+="?filter_entity_id="+t,i&&(a+="&end_time="+i.toISOString()),n&&(a+="&skip_initial_state"),void 0!==o&&(a+=`&significant_changes_only=${Number(o)}`),s&&(a+="&minimal_response"),e.callApi("GET",a)},c=(e,t,r,i)=>e.callApi("GET",`history/period/${t.toISOString()}?end_time=${r.toISOString()}&minimal_response${i?`&filter_entity_id=${i}`:""}`),d=(e,t)=>e.state===t.state&&(!e.attributes||!t.attributes||a.every((r=>e.attributes[r]===t.attributes[r]))),u=(e,t,r)=>{const l={},c=[];if(!t)return{line:[],timeline:[]};t.forEach((t=>{if(0===t.length)return;const s=t.find((e=>e.attributes&&"unit_of_measurement"in e.attributes));let a;a=s?s.attributes.unit_of_measurement:{climate:e.config.unit_system.temperature,counter:"#",humidifier:"%",input_number:"#",number:"#",water_heater:e.config.unit_system.temperature}[(0,n.N)(t[0])],a?a in l?l[a].push(t):l[a]=[t]:c.push(((e,t,r)=>{const n=[],s=r.length-1;for(const o of r)n.length>0&&o.state===n[n.length-1].state||(o.entity_id||(o.attributes=r[s].attributes,o.entity_id=r[s].entity_id),n.push({state_localize:(0,i.D)(e,o,t),state:o.state,last_changed:o.last_changed}));return{name:(0,o.C)(r[0]),entity_id:r[0].entity_id,data:n}})(r,e.locale,t))}));return{line:Object.keys(l).map((e=>((e,t)=>{const r=[];for(const e of t){const t=e[e.length-1],i=(0,n.N)(t),l=[];for(const t of e){let e;if(s.includes(i)){e={state:t.state,last_changed:t.last_updated,attributes:{}};for(const r of a)r in t.attributes&&(e.attributes[r]=t.attributes[r])}else e=t;l.length>1&&d(e,l[l.length-1])&&d(e,l[l.length-2])||l.push(e)}r.push({domain:i,name:(0,o.C)(t),entity_id:t.entity_id,states:l})}return{unit:e,identifier:t.map((e=>e[0].entity_id)).join(""),data:r}})(e,l[e]))),timeline:c}},f=(e,t)=>e.callWS({type:"history/list_statistic_ids",statistic_type:t}),p=(e,t,r,i)=>e.callWS({type:"history/statistics_during_period",start_time:t.toISOString(),end_time:null==r?void 0:r.toISOString(),statistic_ids:i}),h=e=>{if(0===e.length)return null;if(1===e.length)return e[0].sum;const t=e[e.length-1].sum;if(null===t)return null;const r=e[0].sum;return null===r?t:t-r},y=(e,t)=>{let r=0;for(const i of t){if(!(i in e))return null;const t=h(e[i]);if(null===t)return null;r+=t}return r},m=(e,t)=>e.some((e=>null!==e[t]))},12609:(e,t,r)=>{"use strict";r.r(t);var i=r(50424),n=r(55358),o=r(11950),s=(r(52039),r(81582)),a=r(55424),l=r(74186),c=r(58763),d=(r(22098),r(27593));function u(){u=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!h(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return _(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?_(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=g(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:m(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=m(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function f(e){var t,r=g(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function p(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function y(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function m(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function g(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function _(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function v(e,t,r){return(v="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=b(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}})(e,t,r||e)}function b(e){return(b=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,r,i){var n=u();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),r),a=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(y(o.descriptor)||y(n.descriptor)){if(h(o)||h(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(h(o)){if(h(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}p(o,n)}else t.push(o)}return t}(s.d.map(f)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,n.Mo)("hui-energy-usage-card")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_stats",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_co2SignalEntity",value:void 0},{kind:"field",key:"_fetching",value:()=>!1},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"willUpdate",value:function(e){v(b(r.prototype),"willUpdate",this).call(this,e),this._fetching||this._stats||(this._fetching=!0,Promise.all([this._getStatistics(),this._fetchCO2SignalEntity()]).then((()=>{this._fetching=!1})))}},{kind:"method",key:"render",value:function(){if(!this._config)return i.dy``;if(!this._stats)return i.dy`Loading…`;const e=this._config.prefs,t=(0,a.Jj)(e),r=void 0!==t.solar,n=t.grid[0].flow_to.length>0,o=(0,c.q6)(this._stats,t.grid[0].flow_from.map((e=>e.stat_energy_from)));if(null===o)return i.dy`Total consumption couldn't be calculated`;let s=null;if(r&&(s=(0,c.q6)(this._stats,t.solar.map((e=>e.stat_energy_from))),null===s))return i.dy`Total production couldn't be calculated`;let l,u=null;if(n&&(u=(0,c.q6)(this._stats,t.grid[0].flow_to.map((e=>e.stat_energy_to))),void 0===u))return i.dy`Production returned to grid couldn't be calculated`;if(this._co2SignalEntity){const e=this.hass.states[this._co2SignalEntity];e&&(l=Number(e.state),isNaN(l)&&(l=void 0))}const f=o-(u||0);let p;void 0!==l&&(p=f>0?(0,d.N)(f*(l/100)):0);const h=o+(s||0)-(u||0),y=void 0===l?0:l/100,m=1-y,g=((s||0)-(u||0))/h,_=y*(1-g),v=m*(1-g);return i.dy`
      <ha-card header="Usage">
        <div class="card-content">
          <div class="row">
            ${void 0===l?"":i.dy`
                  <div class="circle-container">
                    <span class="label">Low-carbon</span>
                    <div class="circle low-carbon">
                      <ha-svg-icon .path="${"M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z"}"></ha-svg-icon>
                      ${l}% / ${(0,d.N)(p)} kWh
                    </div>
                  </div>
                `}
            <div class="circle-container">
              <span class="label">Solar</span>
              <div class="circle solar">
                <ha-svg-icon .path="${"M11.45,2V5.55L15,3.77L11.45,2M10.45,8L8,10.46L11.75,11.71L10.45,8M2,11.45L3.77,15L5.55,11.45H2M10,2H2V10C2.57,10.17 3.17,10.25 3.77,10.25C7.35,10.26 10.26,7.35 10.27,3.75C10.26,3.16 10.17,2.57 10,2M17,22V16H14L19,7V13H22L17,22Z"}"></ha-svg-icon>
                ${(0,d.N)(s||0)} kWh
              </div>
            </div>
          </div>
          <div class="row">
            <div class="circle-container">
              <div class="circle grid">
                <ha-svg-icon .path="${"M8.28,5.45L6.5,4.55L7.76,2H16.23L17.5,4.55L15.72,5.44L15,4H9L8.28,5.45M18.62,8H14.09L13.3,5H10.7L9.91,8H5.38L4.1,10.55L5.89,11.44L6.62,10H17.38L18.1,11.45L19.89,10.56L18.62,8M17.77,22H15.7L15.46,21.1L12,15.9L8.53,21.1L8.3,22H6.23L9.12,11H11.19L10.83,12.35L12,14.1L13.16,12.35L12.81,11H14.88L17.77,22M11.4,15L10.5,13.65L9.32,18.13L11.4,15M14.68,18.12L13.5,13.64L12.6,15L14.68,18.12Z"}"></ha-svg-icon>
                ${(0,d.N)(o-(u||0))}
                kWh
                <ul>
                  <li>
                    Grid high carbon: ${(0,d.N)(100*m,1)}%
                  </li>
                  <li>Grid low carbon: ${(0,d.N)(100*y,1)}%</li>
                </ul>
              </div>
              <span class="label">Grid</span>
            </div>
            <div class="circle-container home">
              <div class="circle home">
                <ha-svg-icon .path="${"M10,20V14H14V20H19V12H22L12,3L2,12H5V20H10Z"}"></ha-svg-icon>
                ${(0,d.N)(h)} kWh
                <ul>
                  <li>
                    Grid high carbon: ${(0,d.N)(100*v)}%
                  </li>
                  <li>
                    Grid low carbon: ${(0,d.N)(100*_)}%
                  </li>
                  <li>Solar: ${(0,d.N)(100*g)}%</li>
                </ul>
              </div>
              <span class="label">Home</span>
            </div>
          </div>
        </div>
      </ha-card>
    `}},{kind:"method",key:"_fetchCO2SignalEntity",value:async function(){const[e,t]=await Promise.all([(0,s.pB)(this.hass),(0,o.l)(this.hass.connection,l.LM)]),r=e.find((e=>"co2signal"===e.domain));if(r)for(const e of t){if(e.config_entry_id!==r.entry_id)continue;const t=this.hass.states[e.entity_id];if(t&&"%"===t.attributes.unit_of_measurement){this._co2SignalEntity=t.entity_id;break}}}},{kind:"method",key:"_getStatistics",value:async function(){const e=new Date;e.setHours(0,0,0,0),e.setTime(e.getTime()-36e5);const t=[],r=this._config.prefs;for(const e of r.energy_sources)if("solar"!==e.type){for(const r of e.flow_from)t.push(r.stat_energy_from);for(const r of e.flow_to)t.push(r.stat_energy_to)}else t.push(e.stat_energy_from);this._stats=await(0,c.dL)(this.hass,e,void 0,t)}},{kind:"field",static:!0,key:"styles",value:()=>i.iv`
    :host {
      --mdc-icon-size: 26px;
    }
    .row {
      display: flex;
      margin-bottom: 30px;
    }
    .row:last-child {
      margin-bottom: 0;
    }
    .circle-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-right: 40px;
    }
    .circle {
      width: 80px;
      height: 80px;
      border-radius: 50%;
      border: 2px solid;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      font-size: 12px;
    }
    .label {
      color: var(--secondary-text-color);
      font-size: 12px;
    }
    .circle-container:last-child {
      margin-right: 0;
    }
    .circle ul {
      display: none;
    }
    .low-carbon {
      border-color: #0da035;
    }
    .low-carbon ha-svg-icon {
      color: #0da035;
    }
    .solar {
      border-color: #ff9800;
    }
    .grid {
      border-color: #134763;
    }
    .circle-container.home {
      margin-left: 120px;
    }
  `}]}}),i.oi)}}]);
//# sourceMappingURL=e06e9e01.js.map