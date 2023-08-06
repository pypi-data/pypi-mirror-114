(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[2039],{32833:(t,e,i)=>{"use strict";var r=i(50424),n=i(55358),o=i(76666),s=i(92483);function a(){a=function(){return t};var t={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(t,e){["method","field"].forEach((function(i){e.forEach((function(e){e.kind===i&&"own"===e.placement&&this.defineClassElement(t,e)}),this)}),this)},initializeClassElements:function(t,e){var i=t.prototype;["method","field"].forEach((function(r){e.forEach((function(e){var n=e.placement;if(e.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?t:i;this.defineClassElement(o,e)}}),this)}),this)},defineClassElement:function(t,e){var i=e.descriptor;if("field"===e.kind){var r=e.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(t)}}Object.defineProperty(t,e.key,i)},decorateClass:function(t,e){var i=[],r=[],n={static:[],prototype:[],own:[]};if(t.forEach((function(t){this.addElementPlacement(t,n)}),this),t.forEach((function(t){if(!c(t))return i.push(t);var e=this.decorateElement(t,n);i.push(e.element),i.push.apply(i,e.extras),r.push.apply(r,e.finishers)}),this),!e)return{elements:i,finishers:r};var o=this.decorateConstructor(i,e);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(t,e,i){var r=e[t.placement];if(!i&&-1!==r.indexOf(t.key))throw new TypeError("Duplicated element ("+t.key+")");r.push(t.key)},decorateElement:function(t,e){for(var i=[],r=[],n=t.decorators,o=n.length-1;o>=0;o--){var s=e[t.placement];s.splice(s.indexOf(t.key),1);var a=this.fromElementDescriptor(t),l=this.toElementFinisherExtras((0,n[o])(a)||a);t=l.element,this.addElementPlacement(t,e),l.finisher&&r.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],e);i.push.apply(i,d)}}return{element:t,finishers:r,extras:i}},decorateConstructor:function(t,e){for(var i=[],r=e.length-1;r>=0;r--){var n=this.fromClassDescriptor(t),o=this.toClassDescriptor((0,e[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){t=o.elements;for(var s=0;s<t.length-1;s++)for(var a=s+1;a<t.length;a++)if(t[s].key===t[a].key&&t[s].placement===t[a].placement)throw new TypeError("Duplicated element ("+t[s].key+")")}}return{elements:t,finishers:i}},fromElementDescriptor:function(t){var e={kind:t.kind,key:t.key,placement:t.placement,descriptor:t.descriptor};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===t.kind&&(e.initializer=t.initializer),e},toElementDescriptors:function(t){var e;if(void 0!==t)return(e=t,function(t){if(Array.isArray(t))return t}(e)||function(t){if("undefined"!=typeof Symbol&&null!=t[Symbol.iterator]||null!=t["@@iterator"])return Array.from(t)}(e)||function(t,e){if(t){if("string"==typeof t)return f(t,e);var i=Object.prototype.toString.call(t).slice(8,-1);return"Object"===i&&t.constructor&&(i=t.constructor.name),"Map"===i||"Set"===i?Array.from(t):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?f(t,e):void 0}}(e)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(t){var e=this.toElementDescriptor(t);return this.disallowProperty(t,"finisher","An element descriptor"),this.disallowProperty(t,"extras","An element descriptor"),e}),this)},toElementDescriptor:function(t){var e=String(t.kind);if("method"!==e&&"field"!==e)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+e+'"');var i=u(t.key),r=String(t.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=t.descriptor;this.disallowProperty(t,"elements","An element descriptor");var o={kind:e,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==e?this.disallowProperty(t,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=t.initializer),o},toElementFinisherExtras:function(t){return{element:this.toElementDescriptor(t),finisher:p(t,"finisher"),extras:this.toElementDescriptors(t.extras)}},fromClassDescriptor:function(t){var e={kind:"class",elements:t.map(this.fromElementDescriptor,this)};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),e},toClassDescriptor:function(t){var e=String(t.kind);if("class"!==e)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+e+'"');this.disallowProperty(t,"key","A class descriptor"),this.disallowProperty(t,"placement","A class descriptor"),this.disallowProperty(t,"descriptor","A class descriptor"),this.disallowProperty(t,"initializer","A class descriptor"),this.disallowProperty(t,"extras","A class descriptor");var i=p(t,"finisher");return{elements:this.toElementDescriptors(t.elements),finisher:i}},runClassFinishers:function(t,e){for(var i=0;i<e.length;i++){var r=(0,e[i])(t);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");t=r}}return t},disallowProperty:function(t,e,i){if(void 0!==t[e])throw new TypeError(i+" can't have a ."+e+" property.")}};return t}function l(t){var e,i=u(t.key);"method"===t.kind?e={value:t.value,writable:!0,configurable:!0,enumerable:!1}:"get"===t.kind?e={get:t.value,configurable:!0,enumerable:!1}:"set"===t.kind?e={set:t.value,configurable:!0,enumerable:!1}:"field"===t.kind&&(e={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===t.kind?"field":"method",key:i,placement:t.static?"static":"field"===t.kind?"own":"prototype",descriptor:e};return t.decorators&&(r.decorators=t.decorators),"field"===t.kind&&(r.initializer=t.value),r}function d(t,e){void 0!==t.descriptor.get?e.descriptor.get=t.descriptor.get:e.descriptor.set=t.descriptor.set}function c(t){return t.decorators&&t.decorators.length}function h(t){return void 0!==t&&!(void 0===t.value&&void 0===t.writable)}function p(t,e){var i=t[e];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+e+"' to be a function");return i}function u(t){var e=function(t,e){if("object"!=typeof t||null===t)return t;var i=t[Symbol.toPrimitive];if(void 0!==i){var r=i.call(t,e||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===e?String:Number)(t)}(t,"string");return"symbol"==typeof e?e:String(e)}function f(t,e){(null==e||e>t.length)&&(e=t.length);for(var i=0,r=new Array(e);i<e;i++)r[i]=t[i];return r}function m(t,e,i){return(m="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(t,e,i){var r=function(t,e){for(;!Object.prototype.hasOwnProperty.call(t,e)&&null!==(t=y(t)););return t}(t,e);if(r){var n=Object.getOwnPropertyDescriptor(r,e);return n.get?n.get.call(i):n.value}})(t,e,i||t)}function y(t){return(y=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)})(t)}!function(t,e,i,r){var n=a();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=e((function(t){n.initializeInstanceElements(t,p.elements)}),i),p=n.decorateClass(function(t){for(var e=[],i=function(t){return"method"===t.kind&&t.key===o.key&&t.placement===o.placement},r=0;r<t.length;r++){var n,o=t[r];if("method"===o.kind&&(n=e.find(i)))if(h(o.descriptor)||h(n.descriptor)){if(c(o)||c(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(c(o)){if(c(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}d(o,n)}else e.push(o)}return e}(s.d.map(l)),t);n.initializeClassElements(s.F,p.elements),n.runClassFinishers(s.F,p.finishers)}([(0,n.Mo)("ha-chart-base")],(function(t,e){class a extends e{constructor(...e){super(...e),t(this)}}return{F:a,d:[{kind:"field",key:"chart",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:"chart-type",reflect:!0})],key:"chartType",value:()=>"line"},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"data",value:()=>({datasets:[]})},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"options",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"plugins",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_tooltip",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_height",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_hiddenDatasets",value:()=>new Set},{kind:"method",key:"firstUpdated",value:function(){this._setupChart(),this.data.datasets.forEach(((t,e)=>{t.hidden&&this._hiddenDatasets.add(e)}))}},{kind:"method",key:"willUpdate",value:function(t){if(m(y(a.prototype),"willUpdate",this).call(this,t),this.hasUpdated&&this.chart){if(t.has("plugins"))return this.chart.destroy(),void this._setupChart();t.has("type")&&(this.chart.config.type=this.chartType),t.has("data")&&(this.chart.data=this.data),t.has("options")&&(this.chart.options=this._createOptions()),this.chart.update("none")}}},{kind:"method",key:"render",value:function(){var t,e,i;return r.dy`
      ${!0===(null===(t=this.options)||void 0===t||null===(e=t.plugins)||void 0===e||null===(i=e.legend)||void 0===i?void 0:i.display)?r.dy`<div class="chartLegend">
            <ul>
              ${this.data.datasets.map(((t,e)=>r.dy`<li
                  .datasetIndex=${e}
                  @click=${this._legendClick}
                  class=${(0,o.$)({hidden:this._hiddenDatasets.has(e)})}
                >
                  <div
                    class="bullet"
                    style=${(0,s.V)({backgroundColor:t.backgroundColor,borderColor:t.borderColor})}
                  ></div>
                  ${t.label}
                </li>`))}
            </ul>
          </div>`:""}
      <div
        class="chartContainer"
        style=${(0,s.V)({height:"timeline"===this.chartType?30*this.data.datasets.length+30+"px":this._height,overflow:this._height?"initial":"hidden"})}
      >
        <canvas></canvas>
        ${this._tooltip?r.dy`<div
              class="chartTooltip ${(0,o.$)({[this._tooltip.yAlign]:!0})}"
              style=${(0,s.V)({top:this._tooltip.top,left:this._tooltip.left})}
            >
              <div class="title">${this._tooltip.title}</div>
              ${this._tooltip.beforeBody?r.dy`<div class="beforeBody">
                    ${this._tooltip.beforeBody}
                  </div>`:""}
              <div>
                <ul>
                  ${this._tooltip.body.map(((t,e)=>r.dy`<li>
                      <div
                        class="bullet"
                        style=${(0,s.V)({backgroundColor:this._tooltip.labelColors[e].backgroundColor,borderColor:this._tooltip.labelColors[e].borderColor})}
                      ></div>
                      ${t.lines.join("\n")}
                    </li>`))}
                </ul>
              </div>
              ${this._tooltip.footer.length?r.dy`<div class="footer">
                    ${this._tooltip.footer.map((t=>r.dy`${t}<br />`))}
                  </div>`:""}
            </div>`:""}
      </div>
    `}},{kind:"method",key:"_setupChart",value:async function(){const t=this.renderRoot.querySelector("canvas").getContext("2d");this.chart=new((await Promise.all([i.e(1164),i.e(4521)]).then(i.bind(i,84521))).Chart)(t,{type:this.chartType,data:this.data,options:this._createOptions(),plugins:this._createPlugins()})}},{kind:"method",key:"_createOptions",value:function(){var t,e,i,r,n;return{...this.options,plugins:{...null===(t=this.options)||void 0===t?void 0:t.plugins,tooltip:{...null===(e=this.options)||void 0===e||null===(i=e.plugins)||void 0===i?void 0:i.tooltip,enabled:!1,external:t=>this._handleTooltip(t)},legend:{...null===(r=this.options)||void 0===r||null===(n=r.plugins)||void 0===n?void 0:n.legend,display:!1}}}}},{kind:"method",key:"_createPlugins",value:function(){var t,e;return[...this.plugins||[],{id:"afterRenderHook",afterRender:t=>{this._height=`${t.height}px`},legend:{...null===(t=this.options)||void 0===t||null===(e=t.plugins)||void 0===e?void 0:e.legend,display:!1}}]}},{kind:"method",key:"_legendClick",value:function(t){if(!this.chart)return;const e=t.currentTarget.datasetIndex;this.chart.isDatasetVisible(e)?(this.chart.setDatasetVisibility(e,!1),this._hiddenDatasets.add(e)):(this.chart.setDatasetVisibility(e,!0),this._hiddenDatasets.delete(e)),this.chart.update("none"),this.requestUpdate("_hiddenDatasets")}},{kind:"method",key:"_handleTooltip",value:function(t){var e,i,r;0!==t.tooltip.opacity?this._tooltip={...t.tooltip,top:this.chart.canvas.offsetTop+t.tooltip.caretY+12+"px",left:this.chart.canvas.offsetLeft+(e=t.tooltip.caretX,i=100,r=this.clientWidth-100,Math.min(Math.max(e,i),r))-100+"px"}:this._tooltip=void 0}},{kind:"field",key:"updateChart",value(){return()=>{this.chart&&this.chart.update()}}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`
      :host {
        display: block;
      }
      .chartContainer {
        overflow: hidden;
        height: 0;
        transition: height 300ms cubic-bezier(0.4, 0, 0.2, 1);
      }
      :host(:not([chart-type="timeline"])) canvas {
        max-height: 400px;
      }
      .chartLegend {
        text-align: center;
      }
      .chartLegend li {
        cursor: pointer;
        display: inline-flex;
        padding: 0 8px;
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
        box-sizing: border-box;
        align-items: center;
        color: var(--secondary-text-color);
      }
      .chartLegend .hidden {
        text-decoration: line-through;
      }
      .chartLegend .bullet,
      .chartTooltip .bullet {
        border-width: 1px;
        border-style: solid;
        border-radius: 50%;
        display: inline-block;
        height: 16px;
        margin-right: 6px;
        width: 16px;
        flex-shrink: 0;
        box-sizing: border-box;
      }
      .chartTooltip .bullet {
        align-self: baseline;
      }
      :host([rtl]) .chartLegend .bullet,
      :host([rtl]) .chartTooltip .bullet {
        margin-right: inherit;
        margin-left: 6px;
      }
      .chartTooltip {
        padding: 8px;
        font-size: 90%;
        position: absolute;
        background: rgba(80, 80, 80, 0.9);
        color: white;
        border-radius: 4px;
        pointer-events: none;
        z-index: 1000;
        width: 200px;
        box-sizing: border-box;
      }
      :host([rtl]) .chartTooltip {
        direction: rtl;
      }
      .chartLegend ul,
      .chartTooltip ul {
        display: inline-block;
        padding: 0 0px;
        margin: 8px 0 0 0;
        width: 100%;
      }
      .chartTooltip ul {
        margin: 0 4px;
      }
      .chartTooltip li {
        display: flex;
        white-space: pre-line;
        align-items: center;
        line-height: 16px;
        padding: 4px 0;
      }
      .chartTooltip .title {
        text-align: center;
        font-weight: 500;
      }
      .chartTooltip .footer {
        font-weight: 500;
      }
      .chartTooltip .beforeBody {
        text-align: center;
        font-weight: 300;
        word-break: break-all;
      }
    `}}]}}),r.oi)},58763:(t,e,i)=>{"use strict";i.d(e,{vq:()=>l,_J:()=>d,Nu:()=>h,uR:()=>p,dL:()=>u,Kj:()=>f,q6:()=>m,Nw:()=>y});var r=i(29171),n=i(22311),o=i(91741);const s=["climate","humidifier","water_heater"],a=["temperature","current_temperature","target_temp_low","target_temp_high","hvac_action","humidity","mode"],l=(t,e,i,r,n=!1,o,s=!0)=>{let a="history/period";return i&&(a+="/"+i.toISOString()),a+="?filter_entity_id="+e,r&&(a+="&end_time="+r.toISOString()),n&&(a+="&skip_initial_state"),void 0!==o&&(a+=`&significant_changes_only=${Number(o)}`),s&&(a+="&minimal_response"),t.callApi("GET",a)},d=(t,e,i,r)=>t.callApi("GET",`history/period/${e.toISOString()}?end_time=${i.toISOString()}&minimal_response${r?`&filter_entity_id=${r}`:""}`),c=(t,e)=>t.state===e.state&&(!t.attributes||!e.attributes||a.every((i=>t.attributes[i]===e.attributes[i]))),h=(t,e,i)=>{const l={},d=[];if(!e)return{line:[],timeline:[]};e.forEach((e=>{if(0===e.length)return;const s=e.find((t=>t.attributes&&"unit_of_measurement"in t.attributes));let a;a=s?s.attributes.unit_of_measurement:{climate:t.config.unit_system.temperature,counter:"#",humidifier:"%",input_number:"#",number:"#",water_heater:t.config.unit_system.temperature}[(0,n.N)(e[0])],a?a in l?l[a].push(e):l[a]=[e]:d.push(((t,e,i)=>{const n=[],s=i.length-1;for(const o of i)n.length>0&&o.state===n[n.length-1].state||(o.entity_id||(o.attributes=i[s].attributes,o.entity_id=i[s].entity_id),n.push({state_localize:(0,r.D)(t,o,e),state:o.state,last_changed:o.last_changed}));return{name:(0,o.C)(i[0]),entity_id:i[0].entity_id,data:n}})(i,t.locale,e))}));return{line:Object.keys(l).map((t=>((t,e)=>{const i=[];for(const t of e){const e=t[t.length-1],r=(0,n.N)(e),l=[];for(const e of t){let t;if(s.includes(r)){t={state:e.state,last_changed:e.last_updated,attributes:{}};for(const i of a)i in e.attributes&&(t.attributes[i]=e.attributes[i])}else t=e;l.length>1&&c(t,l[l.length-1])&&c(t,l[l.length-2])||l.push(t)}i.push({domain:r,name:(0,o.C)(e),entity_id:e.entity_id,states:l})}return{unit:t,identifier:e.map((t=>t[0].entity_id)).join(""),data:i}})(t,l[t]))),timeline:d}},p=(t,e)=>t.callWS({type:"history/list_statistic_ids",statistic_type:e}),u=(t,e,i,r)=>t.callWS({type:"history/statistics_during_period",start_time:e.toISOString(),end_time:null==i?void 0:i.toISOString(),statistic_ids:r}),f=t=>{if(!t||t.length<2)return null;const e=t[t.length-1].sum;if(null===e)return null;const i=t[0].sum;return null===i?e:e-i},m=(t,e)=>{let i=null;for(const r of e){if(!(r in t))continue;const e=f(t[r]);null!==e&&(null===i?i=e:i+=e)}return i},y=(t,e)=>t.some((t=>null!==t[e]))}}]);
//# sourceMappingURL=0a4834fe.js.map