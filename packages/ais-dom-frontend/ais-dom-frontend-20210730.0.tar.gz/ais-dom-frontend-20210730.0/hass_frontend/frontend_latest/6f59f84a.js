(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[16938],{55424:(e,t,r)=>{"use strict";r.d(t,{Bm:()=>a,o1:()=>s,iK:()=>o,rl:()=>i,xZ:()=>n,ZC:()=>l,_Z:()=>c,Jj:()=>d});const a=()=>({stat_energy_from:"",stat_cost:null,entity_energy_from:null,entity_energy_price:null,number_energy_price:null}),s=()=>({stat_energy_to:"",stat_compensation:null,entity_energy_to:null,entity_energy_price:null,number_energy_price:null}),o=()=>({type:"grid",flow_from:[],flow_to:[],cost_adjustment_day:0}),i=()=>({type:"solar",stat_energy_from:"",config_entry_solar_forecast:null}),n=e=>e.callWS({type:"energy/info"}),l=e=>e.callWS({type:"energy/get_prefs"}),c=(e,t)=>e.callWS({type:"energy/save_prefs",...t}),d=e=>{const t={};for(const r of e.energy_sources)r.type in t?t[r.type].push(r):t[r.type]=[r];return t}},16938:(e,t,r)=>{"use strict";r.r(t),r.d(t,{HuiEnergySourcesTableCard:()=>w});var a=r(23512),s=r(50424),o=r(55358),i=r(92483),n=r(15838),l=r(89525),c=r(91741),d=r(45524),u=(r(17595),r(22098),r(55424)),h=r(58763);function f(){f=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(a){t.forEach((function(t){var s=t.placement;if(t.kind===a&&("static"===s||"prototype"===s)){var o="static"===s?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var a=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===a?void 0:a.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],a=[],s={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,s)}),this),e.forEach((function(e){if(!_(e))return r.push(e);var t=this.decorateElement(e,s);r.push(t.element),r.push.apply(r,t.extras),a.push.apply(a,t.finishers)}),this),!t)return{elements:r,finishers:a};var o=this.decorateConstructor(r,t);return a.push.apply(a,o.finishers),o.finishers=a,o},addElementPlacement:function(e,t,r){var a=t[e.placement];if(!r&&-1!==a.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");a.push(e.key)},decorateElement:function(e,t){for(var r=[],a=[],s=e.decorators,o=s.length-1;o>=0;o--){var i=t[e.placement];i.splice(i.indexOf(e.key),1);var n=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,s[o])(n)||n);e=l.element,this.addElementPlacement(e,t),l.finisher&&a.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:a,extras:r}},decorateConstructor:function(e,t){for(var r=[],a=t.length-1;a>=0;a--){var s=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[a])(s)||s);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var i=0;i<e.length-1;i++)for(var n=i+1;n<e.length;n++)if(e[i].key===e[n].key&&e[i].placement===e[n].placement)throw new TypeError("Duplicated element ("+e[i].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return v(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?v(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=g(e.key),a=String(e.placement);if("static"!==a&&"prototype"!==a&&"own"!==a)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+a+'"');var s=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:a,descriptor:Object.assign({},s)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(s,"get","The property descriptor of a field descriptor"),this.disallowProperty(s,"set","The property descriptor of a field descriptor"),this.disallowProperty(s,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:b(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=b(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var a=(0,t[r])(e);if(void 0!==a){if("function"!=typeof a)throw new TypeError("Finishers must return a constructor.");e=a}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function p(e){var t,r=g(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var a={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(a.decorators=e.decorators),"field"===e.kind&&(a.initializer=e.value),a}function m(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function _(e){return e.decorators&&e.decorators.length}function y(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function b(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function g(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var a=r.call(e,t||"default");if("object"!=typeof a)return a;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function v(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,a=new Array(t);r<t;r++)a[r]=e[r];return a}let w=function(e,t,r,a){var s=f();if(a)for(var o=0;o<a.length;o++)s=a[o](s);var i=t((function(e){s.initializeInstanceElements(e,n.elements)}),r),n=s.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},a=0;a<e.length;a++){var s,o=e[a];if("method"===o.kind&&(s=t.find(r)))if(y(o.descriptor)||y(s.descriptor)){if(_(o)||_(s))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");s.descriptor=o.descriptor}else{if(_(o)){if(_(s))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");s.decorators=o.decorators}m(o,s)}else t.push(o)}return t}(i.d.map(p)),e);return s.initializeClassElements(i.F,n.elements),s.runClassFinishers(i.F,n.finishers)}([(0,o.Mo)("hui-energy-sources-table-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_stats",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_energyInfo",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"willUpdate",value:function(){this.hasUpdated||this._getEnergyInfo().then((()=>this._getStatistics()))}},{kind:"method",key:"render",value:function(){var e,t,r,a;if(!this.hass||!this._config)return s.dy``;if(!this._stats)return s.dy`Loading...`;let o=0,f=0,p=0;const m=(0,u.Jj)(this._config.prefs),_=getComputedStyle(this),y=_.getPropertyValue("--energy-solar-color").trim(),b=_.getPropertyValue("--energy-grid-return-color").trim(),g=_.getPropertyValue("--energy-grid-consumption-color").trim(),v=(null===(e=m.grid)||void 0===e?void 0:e[0].flow_from.some((e=>e.stat_cost||e.entity_energy_price||e.number_energy_price)))||(null===(t=m.grid)||void 0===t?void 0:t[0].flow_to.some((e=>e.stat_compensation||e.entity_energy_price||e.number_energy_price)));return s.dy` <ha-card>
      ${this._config.title?s.dy`<h1 class="card-header">${this._config.title}</h1>`:""}
      <div class="mdc-data-table">
        <div class="mdc-data-table__table-container">
          <table class="mdc-data-table__table" aria-label="Dessert calories">
            <thead>
              <tr class="mdc-data-table__header-row">
                <th class="mdc-data-table__header-cell"></th>
                <th
                  class="mdc-data-table__header-cell"
                  role="columnheader"
                  scope="col"
                >
                  Source
                </th>
                <th
                  class="mdc-data-table__header-cell mdc-data-table__header-cell--numeric"
                  role="columnheader"
                  scope="col"
                >
                  Energy
                </th>
                ${v?s.dy` <th
                      class="mdc-data-table__header-cell mdc-data-table__header-cell--numeric"
                      role="columnheader"
                      scope="col"
                    >
                      Cost
                    </th>`:""}
              </tr>
            </thead>
            <tbody class="mdc-data-table__content">
              ${null===(r=m.solar)||void 0===r?void 0:r.map(((e,t)=>{const r=this.hass.states[e.stat_energy_from],a=(0,h.Kj)(this._stats[e.stat_energy_from])||0;f+=a;const o=t>0?(0,n.CO)((0,n.p3)((0,l.W)((0,n.Rw)((0,n.wK)(y)),t))):y;return s.dy`<tr class="mdc-data-table__row">
                  <td class="mdc-data-table__cell cell-bullet">
                    <div
                      class="bullet"
                      style=${(0,i.V)({borderColor:o,backgroundColor:o+"7F"})}
                    ></div>
                  </td>
                  <th class="mdc-data-table__cell" scope="row">
                    ${r?(0,c.C)(r):e.stat_energy_from}
                  </th>
                  <td
                    class="mdc-data-table__cell mdc-data-table__cell--numeric"
                  >
                    ${(0,d.u)(a,this.hass.locale)} kWh
                  </td>
                  ${v?s.dy`<td class="mdc-data-table__cell"></td>`:""}
                </tr>`}))}
              ${m.solar?s.dy`<tr class="mdc-data-table__row total">
                    <td class="mdc-data-table__cell"></td>
                    <th class="mdc-data-table__cell" scope="row">
                      Solar total
                    </th>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${(0,d.u)(f,this.hass.locale)} kWh
                    </td>
                    ${v?s.dy`<td class="mdc-data-table__cell"></td>`:""}
                  </tr>`:""}
              ${null===(a=m.grid)||void 0===a?void 0:a.map((e=>s.dy`${e.flow_from.map(((e,t)=>{const r=this.hass.states[e.stat_energy_from],a=(0,h.Kj)(this._stats[e.stat_energy_from])||0;o+=a;const u=e.stat_cost||this._energyInfo.cost_sensors[e.stat_energy_from],f=u?(0,h.Kj)(this._stats[u])||0:null;null!==f&&(p+=f);const m=t>0?(0,n.CO)((0,n.p3)((0,l.W)((0,n.Rw)((0,n.wK)(g)),t))):g;return s.dy`<tr class="mdc-data-table__row">
                    <td class="mdc-data-table__cell cell-bullet">
                      <div
                        class="bullet"
                        style=${(0,i.V)({borderColor:m,backgroundColor:m+"7F"})}
                      ></div>
                    </td>
                    <th class="mdc-data-table__cell" scope="row">
                      ${r?(0,c.C)(r):e.stat_energy_from}
                    </th>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${(0,d.u)(a,this.hass.locale)} kWh
                    </td>
                    ${v?s.dy` <td
                          class="mdc-data-table__cell mdc-data-table__cell--numeric"
                        >
                          ${null!==f?(0,d.u)(f,this.hass.locale,{style:"currency",currency:this.hass.config.currency}):""}
                        </td>`:""}
                  </tr>`}))}
                ${e.flow_to.map(((e,t)=>{const r=this.hass.states[e.stat_energy_to],a=-1*((0,h.Kj)(this._stats[e.stat_energy_to])||0);o+=a;const u=e.stat_compensation||this._energyInfo.cost_sensors[e.stat_energy_to],f=u?-1*((0,h.Kj)(this._stats[u])||0):null;null!==f&&(p+=f);const m=t>0?(0,n.CO)((0,n.p3)((0,l.W)((0,n.Rw)((0,n.wK)(b)),t))):b;return s.dy`<tr class="mdc-data-table__row">
                    <td class="mdc-data-table__cell cell-bullet">
                      <div
                        class="bullet"
                        style=${(0,i.V)({borderColor:m,backgroundColor:m+"7F"})}
                      ></div>
                    </td>
                    <th class="mdc-data-table__cell" scope="row">
                      ${r?(0,c.C)(r):e.stat_energy_to}
                    </th>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${(0,d.u)(a,this.hass.locale)} kWh
                    </td>
                    ${v?s.dy` <td
                          class="mdc-data-table__cell mdc-data-table__cell--numeric"
                        >
                          ${null!==f?(0,d.u)(f,this.hass.locale,{style:"currency",currency:this.hass.config.currency}):""}
                        </td>`:""}
                  </tr>`}))}`))}
              ${m.grid?s.dy` <tr class="mdc-data-table__row total">
                    <td class="mdc-data-table__cell"></td>
                    <th class="mdc-data-table__cell" scope="row">Grid total</th>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${(0,d.u)(o,this.hass.locale)} kWh
                    </td>
                    ${v?s.dy`<td
                          class="mdc-data-table__cell mdc-data-table__cell--numeric"
                        >
                          ${(0,d.u)(p,this.hass.locale,{style:"currency",currency:this.hass.config.currency})}
                        </td>`:""}
                  </tr>`:""}
            </tbody>
          </table>
        </div>
      </div>
    </ha-card>`}},{kind:"method",key:"_getEnergyInfo",value:async function(){this._energyInfo=await(0,u.xZ)(this.hass)}},{kind:"method",key:"_getStatistics",value:async function(){const e=new Date;e.setHours(0,0,0,0),e.setTime(e.getTime()-36e5);const t=Object.values(this._energyInfo.cost_sensors),r=this._config.prefs;for(const e of r.energy_sources)if("solar"===e.type)t.push(e.stat_energy_from);else{for(const r of e.flow_from)t.push(r.stat_energy_from),r.stat_cost&&t.push(r.stat_cost);for(const r of e.flow_to)t.push(r.stat_energy_to),r.stat_compensation&&t.push(r.stat_compensation)}this._stats=await(0,h.dL)(this.hass,e,void 0,t)}},{kind:"get",static:!0,key:"styles",value:function(){return s.iv`
      ${(0,s.$m)(a)}
      .mdc-data-table {
        width: 100%;
        border: 0;
      }
      .mdc-data-table__header-cell,
      .mdc-data-table__cell {
        color: var(--primary-text-color);
        border-bottom-color: var(--divider-color);
      }
      .mdc-data-table__row:not(.mdc-data-table__row--selected):hover {
        background-color: rgba(var(--rgb-primary-text-color), 0.04);
      }
      .total {
        --mdc-typography-body2-font-weight: 500;
      }
      .total .mdc-data-table__cell {
        border-top: 1px solid var(--divider-color);
      }
      ha-card {
        height: 100%;
      }
      .card-header {
        padding-bottom: 0;
      }
      .content {
        padding: 16px;
      }
      .has-header {
        padding-top: 0;
      }
      .cell-bullet {
        width: 32px;
        padding-right: 0;
      }
      .bullet {
        border-width: 1px;
        border-style: solid;
        border-radius: 4px;
        height: 16px;
        width: 32px;
      }
    `}}]}}),s.oi)}}]);
//# sourceMappingURL=6f59f84a.js.map