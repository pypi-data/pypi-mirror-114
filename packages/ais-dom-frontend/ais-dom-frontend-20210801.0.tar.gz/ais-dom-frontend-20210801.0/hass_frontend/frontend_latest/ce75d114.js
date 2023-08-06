/*! For license information please see ce75d114.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[37077],{49706:(e,t,r)=>{"use strict";r.d(t,{Rb:()=>i,Zy:()=>a,h2:()=>n,PS:()=>s,l:()=>o,ht:()=>l,f0:()=>c,tj:()=>u,uo:()=>d,lC:()=>h,Kk:()=>m,iY:()=>p,ot:()=>f,gD:()=>g,AZ:()=>y});const i="hass:bookmark",a={alert:"hass:alert",alexa:"hass:amazon-alexa",air_quality:"hass:air-filter",automation:"hass:robot",calendar:"hass:calendar",camera:"hass:video",climate:"hass:thermostat",configurator:"hass:cog",conversation:"hass:text-to-speech",counter:"hass:counter",device_tracker:"hass:account",fan:"hass:fan",google_assistant:"hass:google-assistant",group:"hass:google-circles-communities",homeassistant:"hass:home-assistant",homekit:"hass:home-automation",image_processing:"hass:image-filter-frames",input_boolean:"hass:toggle-switch-outline",input_datetime:"hass:calendar-clock",input_number:"hass:ray-vertex",input_select:"hass:format-list-bulleted",input_text:"hass:form-textbox",light:"hass:lightbulb",mailbox:"hass:mailbox",notify:"hass:comment-alert",number:"hass:ray-vertex",persistent_notification:"hass:bell",person:"hass:account",plant:"hass:flower",proximity:"hass:apple-safari",remote:"hass:remote",scene:"hass:palette",script:"hass:script-text",select:"hass:format-list-bulleted",sensor:"hass:eye",simple_alarm:"hass:bell",sun:"hass:white-balance-sunny",switch:"hass:flash",timer:"hass:timer-outline",updater:"hass:cloud-upload",vacuum:"hass:robot-vacuum",water_heater:"hass:thermometer",weather:"hass:weather-cloudy",zone:"hass:map-marker-radius"},n={current:"hass:current-ac",carbon_dioxide:"mdi:molecule-co2",carbon_monoxide:"mdi:molecule-co",energy:"hass:lightning-bolt",humidity:"hass:water-percent",illuminance:"hass:brightness-5",temperature:"hass:thermometer",monetary:"mdi:cash",pressure:"hass:gauge",power:"hass:flash",power_factor:"hass:angle-acute",signal_strength:"hass:wifi",timestamp:"hass:clock",voltage:"hass:sine-wave"},s=["climate","cover","configurator","input_select","input_number","input_text","lock","media_player","number","scene","script","select","timer","vacuum","water_heater"],o=["alarm_control_panel","automation","camera","climate","configurator","counter","cover","fan","group","humidifier","input_datetime","light","lock","media_player","person","remote","script","sun","timer","vacuum","water_heater","weather"],l=["input_number","input_select","input_text","number","scene","select"],c=["camera","configurator","scene"],u=["closed","locked","off"],d="on",h="off",m=new Set(["fan","input_boolean","light","switch","group","automation","humidifier"]),p=new Set(["camera","media_player"]),f="°C",g="°F",y=["ff0029","66a61e","377eb8","984ea3","00d2d5","ff7f00","af8d00","7f80cd","b3e900","c42e60","a65628","f781bf","8dd3c7","bebada","fb8072","80b1d3","fdb462","fccde5","bc80bd","ffed6f","c4eaff","cf8c00","1b9e77","d95f02","e7298a","e6ab02","a6761d","0097ff","00d067","f43600","4ba93b","5779bb","927acc","97ee3f","bf3947","9f5b00","f48758","8caed6","f2b94f","eff26e","e43872","d9b100","9d7a00","698cff","d9d9d9","00d27e","d06800","009f82","c49200","cbe8ff","fecddf","c27eb6","8cd2ce","c4b8d9","f883b0","a49100","f48800","27d0df","a04a9b"]},43274:(e,t,r)=>{"use strict";r.d(t,{Sb:()=>i,BF:()=>a,Op:()=>n});const i=function(){try{(new Date).toLocaleDateString("i")}catch(e){return"RangeError"===e.name}return!1}(),a=function(){try{(new Date).toLocaleTimeString("i")}catch(e){return"RangeError"===e.name}return!1}(),n=function(){try{(new Date).toLocaleString("i")}catch(e){return"RangeError"===e.name}return!1}()},12198:(e,t,r)=>{"use strict";r.d(t,{p6:()=>o,mn:()=>c,D_:()=>d});var i=r(68928),a=r(14516),n=r(43274);const s=(0,a.Z)((e=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"long",day:"numeric"}))),o=n.Sb?(e,t)=>s(t).format(e):e=>(0,i.WU)(e,"longDate"),l=(0,a.Z)((e=>new Intl.DateTimeFormat(e.language,{day:"numeric",month:"short"}))),c=n.Sb?(e,t)=>l(t).format(e):e=>(0,i.WU)(e,"shortDate"),u=(0,a.Z)((e=>new Intl.DateTimeFormat(e.language,{weekday:"long",month:"long",day:"numeric"}))),d=n.Sb?(e,t)=>u(t).format(e):e=>(0,i.WU)(e,"dddd, MMM D")},44583:(e,t,r)=>{"use strict";r.d(t,{o:()=>l,E:()=>u});var i=r(68928),a=r(14516),n=r(43274),s=r(65810);const o=(0,a.Z)((e=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit",hour12:(0,s.y)(e)}))),l=n.Op?(e,t)=>o(t).format(e):(e,t)=>(0,i.WU)(e,((0,s.y)(t)," A")),c=(0,a.Z)((e=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit",second:"2-digit",hour12:(0,s.y)(e)}))),u=n.Op?(e,t)=>c(t).format(e):(e,t)=>(0,i.WU)(e,((0,s.y)(t)," A"))},49684:(e,t,r)=>{"use strict";r.d(t,{mr:()=>l,Vu:()=>u,xO:()=>h});var i=r(68928),a=r(14516),n=r(43274),s=r(65810);const o=(0,a.Z)((e=>new Intl.DateTimeFormat(e.language,{hour:"numeric",minute:"2-digit",hour12:(0,s.y)(e)}))),l=n.BF?(e,t)=>o(t).format(e):(e,t)=>(0,i.WU)(e,((0,s.y)(t)," A")),c=(0,a.Z)((e=>new Intl.DateTimeFormat(e.language,{hour:"numeric",minute:"2-digit",second:"2-digit",hour12:(0,s.y)(e)}))),u=n.BF?(e,t)=>c(t).format(e):(e,t)=>(0,i.WU)(e,((0,s.y)(t)," A")),d=(0,a.Z)((e=>new Intl.DateTimeFormat(e.language,{weekday:"long",hour:"numeric",minute:"2-digit",hour12:(0,s.y)(e)}))),h=n.BF?(e,t)=>d(t).format(e):(e,t)=>(0,i.WU)(e,((0,s.y)(t)," A"))},65810:(e,t,r)=>{"use strict";r.d(t,{y:()=>a});var i=r(66477);const a=e=>{if(e.time_format===i.zt.language||e.time_format===i.zt.system){const t=e.time_format===i.zt.language?e.language:void 0,r=(new Date).toLocaleString(t);return r.includes("AM")||r.includes("PM")}return e.time_format===i.zt.am_pm}},29171:(e,t,r)=>{"use strict";r.d(t,{D:()=>c});var i=r(56007),a=r(12198),n=r(44583),s=r(49684),o=r(45524),l=r(22311);const c=(e,t,r,c)=>{const u=void 0!==c?c:t.state;if(u===i.lz||u===i.nZ)return e(`state.default.${u}`);if(t.attributes.unit_of_measurement){if("monetary"===t.attributes.device_class)try{return(0,o.u)(u,r,{style:"currency",currency:t.attributes.unit_of_measurement})}catch(e){}return`${(0,o.u)(u,r)} ${t.attributes.unit_of_measurement}`}const d=(0,l.N)(t);if("input_datetime"===d){if(!c){let e;return t.attributes.has_time?t.attributes.has_date?(e=new Date(t.attributes.year,t.attributes.month-1,t.attributes.day,t.attributes.hour,t.attributes.minute),(0,n.o)(e,r)):(e=new Date,e.setHours(t.attributes.hour,t.attributes.minute),(0,s.mr)(e,r)):(e=new Date(t.attributes.year,t.attributes.month-1,t.attributes.day),(0,a.p6)(e,r))}try{const e=c.split(" ");if(2===e.length)return(0,n.o)(new Date(e.join("T")),r);if(1===e.length){if(c.includes("-"))return(0,a.p6)(new Date(`${c}T00:00`),r);if(c.includes(":")){const e=new Date;return(0,s.mr)(new Date(`${e.toISOString().split("T")[0]}T${c}`),r)}}return c}catch{return c}}return"humidifier"===d&&"on"===u&&t.attributes.humidity?`${t.attributes.humidity} %`:"counter"===d||"number"===d||"input_number"===d?(0,o.u)(u,r):t.attributes.device_class&&e(`component.${d}.state.${t.attributes.device_class}.${u}`)||e(`component.${d}.state._.${u}`)||u}},22311:(e,t,r)=>{"use strict";r.d(t,{N:()=>a});var i=r(58831);const a=e=>(0,i.M)(e.entity_id)},27593:(e,t,r)=>{"use strict";r.d(t,{N:()=>i});const i=(e,t=2)=>Math.round(e*10**t)/10**t},45524:(e,t,r)=>{"use strict";r.d(t,{H:()=>n,u:()=>s});var i=r(66477),a=r(27593);const n=e=>{switch(e.number_format){case i.y4.comma_decimal:return["en-US","en"];case i.y4.decimal_comma:return["de","es","it"];case i.y4.space_comma:return["fr","sv","cs"];case i.y4.system:return;default:return e.language}},s=(e,t,r)=>{const s=t?n(t):void 0;if(Number.isNaN=Number.isNaN||function e(t){return"number"==typeof t&&e(t)},(null==t?void 0:t.number_format)!==i.y4.none&&!Number.isNaN(Number(e))&&Intl)try{return new Intl.NumberFormat(s,o(e,r)).format(Number(e))}catch(t){return console.error(t),new Intl.NumberFormat(void 0,o(e,r)).format(Number(e))}return"string"==typeof e?e:`${(0,a.N)(e,null==r?void 0:r.maximumFractionDigits).toString()}${"currency"===(null==r?void 0:r.style)?` ${r.currency}`:""}`},o=(e,t)=>{const r={maximumFractionDigits:2,...t};if("string"!=typeof e)return r;if(!t||!t.minimumFractionDigits&&!t.maximumFractionDigits){const t=e.indexOf(".")>-1?e.split(".")[1].length:0;r.minimumFractionDigits=t,r.maximumFractionDigits=t}return r}},56007:(e,t,r)=>{"use strict";r.d(t,{nZ:()=>i,lz:()=>a,V_:()=>n});const i="unavailable",a="unknown",n=[i,a]},27849:(e,t,r)=>{"use strict";r(39841);var i=r(50856);r(28426);class a extends(customElements.get("app-header-layout")){static get template(){return i.d`
      <style>
        :host {
          display: block;
          /**
         * Force app-header-layout to have its own stacking context so that its parent can
         * control the stacking of it relative to other elements (e.g. app-drawer-layout).
         * This could be done using \`isolation: isolate\`, but that's not well supported
         * across browsers.
         */
          position: relative;
          z-index: 0;
        }

        #wrapper ::slotted([slot="header"]) {
          @apply --layout-fixed-top;
          z-index: 1;
        }

        #wrapper.initializing ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) {
          height: 100%;
        }

        :host([has-scrolling-region]) #wrapper ::slotted([slot="header"]) {
          position: absolute;
        }

        :host([has-scrolling-region])
          #wrapper.initializing
          ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) #wrapper #contentContainer {
          @apply --layout-fit;
          overflow-y: auto;
          -webkit-overflow-scrolling: touch;
        }

        :host([has-scrolling-region]) #wrapper.initializing #contentContainer {
          position: relative;
        }

        #contentContainer {
          /* Create a stacking context here so that all children appear below the header. */
          position: relative;
          z-index: 0;
          /* Using 'transform' will cause 'position: fixed' elements to behave like
           'position: absolute' relative to this element. */
          transform: translate(0);
          margin-left: env(safe-area-inset-left);
          margin-right: env(safe-area-inset-right);
        }

        @media print {
          :host([has-scrolling-region]) #wrapper #contentContainer {
            overflow-y: visible;
          }
        }
      </style>

      <div id="wrapper" class="initializing">
        <slot id="headerSlot" name="header"></slot>

        <div id="contentContainer"><slot></slot></div>
        <slot id="fab" name="fab"></slot>
      </div>
    `}}customElements.define("ha-app-layout",a)},3542:(e,t,r)=>{"use strict";r.r(t);r(53268),r(12730);var i=r(50424),a=r(55358),n=r(59401),s=r(59281),o=r(27088),l=r(70390),c=r(83008),u=r(61334),d=r(79021),h=r(87744),m=(r(74535),r(31206),r(44491),r(48932),r(17633),r(58763)),p=(r(27849),r(11654));function f(){f=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var a=t.placement;if(t.kind===i&&("static"===a||"prototype"===a)){var n="static"===a?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],a={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,a)}),this),e.forEach((function(e){if(!b(e))return r.push(e);var t=this.decorateElement(e,a);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],a=e.decorators,n=a.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var o=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,a[n])(o)||o);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var u=0;u<c.length;u++)this.addElementPlacement(c[u],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var a=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(a)||a);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var o=s+1;o<e.length;o++)if(e[s].key===e[o].key&&e[s].placement===e[o].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return _(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?_(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=k(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var a=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},a)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(a,"get","The property descriptor of a field descriptor"),this.disallowProperty(a,"set","The property descriptor of a field descriptor"),this.disallowProperty(a,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:w(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=w(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function g(e){var t,r=k(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function y(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function b(e){return e.decorators&&e.decorators.length}function v(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function w(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function k(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function _(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function D(e,t,r){return(D="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=x(e)););return e}(e,t);if(i){var a=Object.getOwnPropertyDescriptor(i,t);return a.get?a.get.call(r):a.value}})(e,t,r||e)}function x(e){return(x=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}let E=function(e,t,r,i){var a=f();if(i)for(var n=0;n<i.length;n++)a=i[n](a);var s=t((function(e){a.initializeInstanceElements(e,o.elements)}),r),o=a.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var a,n=e[i];if("method"===n.kind&&(a=t.find(r)))if(v(n.descriptor)||v(a.descriptor)){if(b(n)||b(a))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");a.descriptor=n.descriptor}else{if(b(n)){if(b(a))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");a.decorators=n.decorators}y(n,a)}else t.push(n)}return t}(s.d.map(g)),e);return a.initializeClassElements(s.F,o.elements),a.runClassFinishers(s.F,o.finishers)}(null,(function(e,t){class r extends t{constructor(){super(),e(this);const t=new Date;t.setHours(t.getHours()-2,0,0,0),this._startDate=t;const r=new Date;r.setHours(r.getHours()+1,0,0,0),this._endDate=r}}return{F:r,d:[{kind:"field",decorators:[(0,a.Cb)()],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({reflect:!0,type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"_startDate",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"_endDate",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"_entityId",value:()=>""},{kind:"field",decorators:[(0,a.Cb)()],key:"_isLoading",value:()=>!1},{kind:"field",decorators:[(0,a.Cb)()],key:"_stateHistory",value:void 0},{kind:"field",decorators:[(0,a.Cb)({reflect:!0,type:Boolean})],key:"rtl",value:()=>!1},{kind:"field",decorators:[(0,a.SB)()],key:"_ranges",value:void 0},{kind:"method",key:"render",value:function(){return i.dy`
      <ha-app-layout>
        <app-header slot="header" fixed>
          <app-toolbar>
            <ha-menu-button
              .hass=${this.hass}
              .narrow=${this.narrow}
            ></ha-menu-button>
            <div main-title>${this.hass.localize("panel.history")}</div>
          </app-toolbar>
        </app-header>

        <div class="flex content">
          <div class="flex layout horizontal wrap">
            <ha-date-range-picker
              .hass=${this.hass}
              ?disabled=${this._isLoading}
              .startDate=${this._startDate}
              .endDate=${this._endDate}
              .ranges=${this._ranges}
              @change=${this._dateRangeChanged}
            ></ha-date-range-picker>

            <ha-entity-picker
              .hass=${this.hass}
              .value=${this._entityId}
              .label=${this.hass.localize("ui.components.entity.entity-picker.entity")}
              .disabled=${this._isLoading}
              @change=${this._entityPicked}
            ></ha-entity-picker>
          </div>
          ${this._isLoading?i.dy`<div class="progress-wrapper">
                <ha-circular-progress
                  active
                  alt=${this.hass.localize("ui.common.loading")}
                ></ha-circular-progress>
              </div>`:i.dy`
                <state-history-charts
                  .hass=${this.hass}
                  .historyData=${this._stateHistory}
                  .endTime=${this._endDate}
                  no-single
                >
                </state-history-charts>
              `}
        </div>
      </ha-app-layout>
    `}},{kind:"method",key:"firstUpdated",value:function(e){D(x(r.prototype),"firstUpdated",this).call(this,e);const t=new Date,i=(0,n.Z)(t),a=(0,s.Z)(t);this._ranges={[this.hass.localize("ui.components.date-range-picker.ranges.today")]:[(0,o.Z)(),(0,l.Z)()],[this.hass.localize("ui.components.date-range-picker.ranges.yesterday")]:[(0,c.Z)(),(0,u.Z)()],[this.hass.localize("ui.components.date-range-picker.ranges.this_week")]:[i,a],[this.hass.localize("ui.components.date-range-picker.ranges.last_week")]:[(0,d.Z)(i,-7),(0,d.Z)(a,-7)]}}},{kind:"method",key:"updated",value:function(e){if((e.has("_startDate")||e.has("_endDate")||e.has("_entityId"))&&this._getHistory(),e.has("hass")){const t=e.get("hass");t&&t.language===this.hass.language||(this.rtl=(0,h.HE)(this.hass))}}},{kind:"method",key:"_getHistory",value:async function(){this._isLoading=!0;const e=await(0,m._J)(this.hass,this._startDate,this._endDate,this._entityId);this._stateHistory=(0,m.Nu)(this.hass,e,this.hass.localize),this._isLoading=!1}},{kind:"method",key:"_dateRangeChanged",value:function(e){this._startDate=e.detail.startDate;const t=e.detail.endDate;0===t.getHours()&&0===t.getMinutes()&&(t.setDate(t.getDate()+1),t.setMilliseconds(t.getMilliseconds()-1)),this._endDate=t}},{kind:"method",key:"_entityPicked",value:function(e){this._entityId=e.target.value}},{kind:"get",static:!0,key:"styles",value:function(){return[p.Qx,i.iv`
        .content {
          padding: 0 16px 16px;
        }

        .progress-wrapper {
          height: calc(100vh - 136px);
        }

        :host([narrow]) .progress-wrapper {
          height: calc(100vh - 198px);
        }

        .progress-wrapper {
          position: relative;
        }

        ha-date-range-picker {
          margin-right: 16px;
          max-width: 100%;
        }

        :host([narrow]) ha-date-range-picker {
          margin-right: 0;
        }

        ha-circular-progress {
          position: absolute;
          left: 50%;
          top: 50%;
          transform: translate(-50%, -50%);
        }

        ha-entity-picker {
          display: inline-block;
          flex-grow: 1;
          max-width: 400px;
        }

        :host([narrow]) ha-entity-picker {
          max-width: none;
          width: 100%;
        }
      `]}}]}}),i.oi);customElements.define("ha-panel-history",E)}}]);
//# sourceMappingURL=ce75d114.js.map