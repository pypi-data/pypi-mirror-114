(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[971],{27593:(e,t,r)=>{"use strict";r.d(t,{N:()=>n});const n=(e,t=2)=>Math.round(e*10**t)/10**t},55424:(e,t,r)=>{"use strict";r.d(t,{Bm:()=>n,o1:()=>i,iK:()=>o,rl:()=>s,xZ:()=>a,ZC:()=>l,_Z:()=>c,Jj:()=>d});const n=()=>({stat_energy_from:"",stat_cost:null,entity_energy_from:null,entity_energy_price:null,number_energy_price:null}),i=()=>({stat_energy_to:"",stat_compensation:null,entity_energy_to:null,entity_energy_price:null,number_energy_price:null}),o=()=>({type:"grid",flow_from:[],flow_to:[],cost_adjustment_day:0}),s=()=>({type:"solar",stat_energy_from:"",config_entry_solar_forecast:null}),a=e=>e.callWS({type:"energy/info"}),l=e=>e.callWS({type:"energy/get_prefs"}),c=(e,t)=>e.callWS({type:"energy/save_prefs",...t}),d=e=>{const t={};for(const r of e.energy_sources)r.type in t?t[r.type].push(r):t[r.type]=[r];return t}},30971:(e,t,r)=>{"use strict";r.r(t),r.d(t,{HuiEnergyCostsTableCard:()=>g});var n=r(23512),i=r(50424),o=r(55358),s=r(91741),a=r(27593),l=(r(17595),r(22098),r(55424)),c=r(58763);function d(){d=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!p(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,o=i.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,i[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&n.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return _(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?_(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=y(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:m(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=m(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function f(e){var t,r=y(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function u(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function h(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function m(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function y(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!=typeof n)return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function _(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}let g=function(e,t,r,n){var i=d();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var s=t((function(e){i.initializeInstanceElements(e,a.elements)}),r),a=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var i,o=e[n];if("method"===o.kind&&(i=t.find(r)))if(h(o.descriptor)||h(i.descriptor)){if(p(o)||p(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(p(o)){if(p(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}u(o,i)}else t.push(o)}return t}(s.d.map(f)),e);return i.initializeClassElements(s.F,a.elements),i.runClassFinishers(s.F,a.finishers)}([(0,o.Mo)("hui-energy-costs-table-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_stats",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_energyInfo",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"willUpdate",value:function(){this.hasUpdated||this._getEnergyInfo().then((()=>this._getStatistics()))}},{kind:"method",key:"render",value:function(){var e;if(!this.hass||!this._config)return i.dy``;if(!this._stats)return i.dy`Loading...`;const t=null===(e=this._config.prefs.energy_sources)||void 0===e?void 0:e.find((e=>"grid"===e.type));if(!t)return i.dy`No grid source found.`;let r=0,n=0;return i.dy` <ha-card .header="${this._config.title}">
      <div class="mdc-data-table">
        <div class="mdc-data-table__table-container">
          <table class="mdc-data-table__table" aria-label="Dessert calories">
            <thead>
              <tr class="mdc-data-table__header-row">
                <th
                  class="mdc-data-table__header-cell"
                  role="columnheader"
                  scope="col"
                >
                  Grid source
                </th>
                <th
                  class="mdc-data-table__header-cell mdc-data-table__header-cell--numeric"
                  role="columnheader"
                  scope="col"
                >
                  Energy
                </th>
                <th
                  class="mdc-data-table__header-cell mdc-data-table__header-cell--numeric"
                  role="columnheader"
                  scope="col"
                >
                  Cost
                </th>
              </tr>
            </thead>
            <tbody class="mdc-data-table__content">
              ${t.flow_from.map((e=>{const t=this.hass.states[e.stat_energy_from],o=(0,c.Kj)(this._stats[e.stat_energy_from])||0;r+=o;const l=e.stat_cost||this._energyInfo.cost_sensors[e.stat_energy_from],d=l&&(0,c.Kj)(this._stats[l])||0;return n+=d,i.dy`<tr class="mdc-data-table__row">
                  <th class="mdc-data-table__cell" scope="row">
                    ${t?(0,s.C)(t):e.stat_energy_from}
                  </th>
                  <td
                    class="mdc-data-table__cell mdc-data-table__cell--numeric"
                  >
                    ${(0,a.N)(o)} kWh
                  </td>
                  <td
                    class="mdc-data-table__cell mdc-data-table__cell--numeric"
                  >
                    ${this._config.prefs.currency} ${d.toFixed(2)}
                  </td>
                </tr>`}))}
              ${t.flow_to.map((e=>{const t=this.hass.states[e.stat_energy_to],o=-1*((0,c.Kj)(this._stats[e.stat_energy_to])||0);r+=o;const l=e.stat_compensation||this._energyInfo.cost_sensors[e.stat_energy_to],d=-1*(l&&(0,c.Kj)(this._stats[l])||0);return n+=d,i.dy`<tr class="mdc-data-table__row">
                  <th class="mdc-data-table__cell" scope="row">
                    ${t?(0,s.C)(t):e.stat_energy_to}
                  </th>
                  <td
                    class="mdc-data-table__cell mdc-data-table__cell--numeric"
                  >
                    ${(0,a.N)(o)} kWh
                  </td>
                  <td
                    class="mdc-data-table__cell mdc-data-table__cell--numeric"
                  >
                    ${this._config.prefs.currency} ${d.toFixed(2)}
                  </td>
                </tr>`}))}
              <tr class="mdc-data-table__row total">
                <th class="mdc-data-table__cell" scope="row">Total</th>
                <td class="mdc-data-table__cell mdc-data-table__cell--numeric">
                  ${(0,a.N)(r)} kWh
                </td>
                <td class="mdc-data-table__cell mdc-data-table__cell--numeric">
                  ${this._config.prefs.currency} ${n.toFixed(2)}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </ha-card>`}},{kind:"method",key:"_getEnergyInfo",value:async function(){this._energyInfo=await(0,l.xZ)(this.hass)}},{kind:"method",key:"_getStatistics",value:async function(){const e=new Date;e.setHours(0,0,0,0),e.setTime(e.getTime()-36e5);const t=Object.values(this._energyInfo.cost_sensors),r=this._config.prefs;for(const e of r.energy_sources)if("solar"!==e.type){for(const r of e.flow_from)t.push(r.stat_energy_from),r.stat_cost&&t.push(r.stat_cost);for(const r of e.flow_to)t.push(r.stat_energy_to),r.stat_compensation&&t.push(r.stat_compensation)}this._stats=await(0,c.dL)(this.hass,e,void 0,t)}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      ${(0,i.$m)(n)}
      .mdc-data-table {
        width: 100%;
        border: 0;
      }
      .total {
        background-color: var(--primary-background-color);
        --mdc-typography-body2-font-weight: 500;
      }
      ha-card {
        height: 100%;
      }
      .content {
        padding: 16px;
      }
      .has-header {
        padding-top: 0;
      }
    `}}]}}),i.oi)}}]);
//# sourceMappingURL=130f1ee4.js.map