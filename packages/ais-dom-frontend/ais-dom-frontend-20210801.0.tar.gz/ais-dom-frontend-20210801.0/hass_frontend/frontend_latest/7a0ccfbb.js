/*! For license information please see 7a0ccfbb.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[57310,49577,89857,42169,23624,1127,54207],{14114:(t,e,n)=>{"use strict";n.d(e,{P:()=>i});const i=t=>(e,n)=>{if(e.constructor._observers){if(!e.constructor.hasOwnProperty("_observers")){const t=e.constructor._observers;e.constructor._observers=new Map,t.forEach(((t,n)=>e.constructor._observers.set(n,t)))}}else{e.constructor._observers=new Map;const t=e.updated;e.updated=function(e){t.call(this,e),e.forEach(((t,e)=>{const n=this.constructor._observers.get(e);void 0!==n&&n.call(this,this[e],t)}))}}e.constructor._observers.set(n,t)}},39841:(t,e,n)=>{"use strict";n(65233),n(65660);var i=n(9672),o=n(87156),r=n(50856),s=n(44181);(0,i.k)({_template:r.d`
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

      #wrapper ::slotted([slot=header]) {
        @apply --layout-fixed-top;
        z-index: 1;
      }

      #wrapper.initializing ::slotted([slot=header]) {
        position: relative;
      }

      :host([has-scrolling-region]) {
        height: 100%;
      }

      :host([has-scrolling-region]) #wrapper ::slotted([slot=header]) {
        position: absolute;
      }

      :host([has-scrolling-region]) #wrapper.initializing ::slotted([slot=header]) {
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

      :host([fullbleed]) {
        @apply --layout-vertical;
        @apply --layout-fit;
      }

      :host([fullbleed]) #wrapper,
      :host([fullbleed]) #wrapper #contentContainer {
        @apply --layout-vertical;
        @apply --layout-flex;
      }

      #contentContainer {
        /* Create a stacking context here so that all children appear below the header. */
        position: relative;
        z-index: 0;
      }

      @media print {
        :host([has-scrolling-region]) #wrapper #contentContainer {
          overflow-y: visible;
        }
      }

    </style>

    <div id="wrapper" class="initializing">
      <slot id="headerSlot" name="header"></slot>

      <div id="contentContainer">
        <slot></slot>
      </div>
    </div>
`,is:"app-header-layout",behaviors:[s.Y],properties:{hasScrollingRegion:{type:Boolean,value:!1,reflectToAttribute:!0}},observers:["resetLayout(isAttached, hasScrollingRegion)"],get header(){return(0,o.vz)(this.$.headerSlot).getDistributedNodes()[0]},_updateLayoutStates:function(){var t=this.header;if(this.isAttached&&t){this.$.wrapper.classList.remove("initializing"),t.scrollTarget=this.hasScrollingRegion?this.$.contentContainer:this.ownerDocument.documentElement;var e=t.offsetHeight;this.hasScrollingRegion?(t.style.left="",t.style.right=""):requestAnimationFrame(function(){var e=this.getBoundingClientRect(),n=document.documentElement.clientWidth-e.right;t.style.left=e.left+"px",t.style.right=n+"px"}.bind(this));var n=this.$.contentContainer.style;t.fixed&&!t.condenses&&this.hasScrollingRegion?(n.marginTop=e+"px",n.paddingTop=""):(n.paddingTop=e+"px",n.marginTop="")}}})},63207:(t,e,n)=>{"use strict";n(65660),n(15112);var i=n(9672),o=n(87156),r=n(50856),s=n(65233);(0,i.k)({_template:r.d`
    <style>
      :host {
        @apply --layout-inline;
        @apply --layout-center-center;
        position: relative;

        vertical-align: middle;

        fill: var(--iron-icon-fill-color, currentcolor);
        stroke: var(--iron-icon-stroke-color, none);

        width: var(--iron-icon-width, 24px);
        height: var(--iron-icon-height, 24px);
        @apply --iron-icon;
      }

      :host([hidden]) {
        display: none;
      }
    </style>
`,is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:s.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(t){var e=(t||"").split(":");this._iconName=e.pop(),this._iconsetName=e.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(t){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,o.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,o.vz)(this.root).appendChild(this._img))}})},15112:(t,e,n)=>{"use strict";n.d(e,{P:()=>o});n(65233);var i=n(9672);class o{constructor(t){o[" "](t),this.type=t&&t.type||"default",this.key=t&&t.key,t&&"value"in t&&(this.value=t.value)}get value(){var t=this.type,e=this.key;if(t&&e)return o.types[t]&&o.types[t][e]}set value(t){var e=this.type,n=this.key;e&&n&&(e=o.types[e]=o.types[e]||{},null==t?delete e[n]:e[n]=t)}get list(){if(this.type){var t=o.types[this.type];return t?Object.keys(t).map((function(t){return r[this.type][t]}),this):[]}}byKey(t){return this.key=t,this.value}}o[" "]=function(){},o.types={};var r=o.types;(0,i.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(t,e,n){var i=new o({type:t,key:e});return void 0!==n&&n!==i.value?i.value=n:this.value!==i.value&&(this.value=i.value),i},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(t){t&&(this.value=this)},byKey:function(t){return new o({type:this.type,key:t}).value}})},25782:(t,e,n)=>{"use strict";n(65233),n(65660),n(70019),n(97968);var i=n(9672),o=n(50856),r=n(33760);(0,i.k)({_template:o.d`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[r.U]})},33760:(t,e,n)=>{"use strict";n.d(e,{U:()=>r});n(65233);var i=n(51644),o=n(26110);const r=[i.P,o.a,{hostAttributes:{role:"option",tabindex:"0"}}]},89194:(t,e,n)=>{"use strict";n(65233),n(65660),n(70019);var i=n(9672),o=n(50856);(0,i.k)({_template:o.d`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},97968:(t,e,n)=>{"use strict";n(65660),n(70019);const i=document.createElement("template");i.setAttribute("style","display: none;"),i.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(i.content)},68928:(t,e,n)=>{"use strict";n.d(e,{WU:()=>D});var i=/d{1,4}|M{1,4}|YY(?:YY)?|S{1,3}|Do|ZZ|Z|([HhMsDm])\1?|[aA]|"[^"]*"|'[^']*'/g,o="[1-9]\\d?",r="\\d\\d",s="[^\\s]+",a=/\[([^]*?)\]/gm;function l(t,e){for(var n=[],i=0,o=t.length;i<o;i++)n.push(t[i].substr(0,e));return n}var c=function(t){return function(e,n){var i=n[t].map((function(t){return t.toLowerCase()})).indexOf(e.toLowerCase());return i>-1?i:null}};function u(t){for(var e=[],n=1;n<arguments.length;n++)e[n-1]=arguments[n];for(var i=0,o=e;i<o.length;i++){var r=o[i];for(var s in r)t[s]=r[s]}return t}var d=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],p=["January","February","March","April","May","June","July","August","September","October","November","December"],h=l(p,3),m={dayNamesShort:l(d,3),dayNames:d,monthNamesShort:h,monthNames:p,amPm:["am","pm"],DoFn:function(t){return t+["th","st","nd","rd"][t%10>3?0:(t-t%10!=10?1:0)*t%10]}},f=u({},m),y=function(t,e){for(void 0===e&&(e=2),t=String(t);t.length<e;)t="0"+t;return t},v={D:function(t){return String(t.getDate())},DD:function(t){return y(t.getDate())},Do:function(t,e){return e.DoFn(t.getDate())},d:function(t){return String(t.getDay())},dd:function(t){return y(t.getDay())},ddd:function(t,e){return e.dayNamesShort[t.getDay()]},dddd:function(t,e){return e.dayNames[t.getDay()]},M:function(t){return String(t.getMonth()+1)},MM:function(t){return y(t.getMonth()+1)},MMM:function(t,e){return e.monthNamesShort[t.getMonth()]},MMMM:function(t,e){return e.monthNames[t.getMonth()]},YY:function(t){return y(String(t.getFullYear()),4).substr(2)},YYYY:function(t){return y(t.getFullYear(),4)},h:function(t){return String(t.getHours()%12||12)},hh:function(t){return y(t.getHours()%12||12)},H:function(t){return String(t.getHours())},HH:function(t){return y(t.getHours())},m:function(t){return String(t.getMinutes())},mm:function(t){return y(t.getMinutes())},s:function(t){return String(t.getSeconds())},ss:function(t){return y(t.getSeconds())},S:function(t){return String(Math.round(t.getMilliseconds()/100))},SS:function(t){return y(Math.round(t.getMilliseconds()/10),2)},SSS:function(t){return y(t.getMilliseconds(),3)},a:function(t,e){return t.getHours()<12?e.amPm[0]:e.amPm[1]},A:function(t,e){return t.getHours()<12?e.amPm[0].toUpperCase():e.amPm[1].toUpperCase()},ZZ:function(t){var e=t.getTimezoneOffset();return(e>0?"-":"+")+y(100*Math.floor(Math.abs(e)/60)+Math.abs(e)%60,4)},Z:function(t){var e=t.getTimezoneOffset();return(e>0?"-":"+")+y(Math.floor(Math.abs(e)/60),2)+":"+y(Math.abs(e)%60,2)}},g=function(t){return+t-1},b=[null,o],_=[null,s],w=["isPm",s,function(t,e){var n=t.toLowerCase();return n===e.amPm[0]?0:n===e.amPm[1]?1:null}],M=["timezoneOffset","[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z?",function(t){var e=(t+"").match(/([+-]|\d\d)/gi);if(e){var n=60*+e[1]+parseInt(e[2],10);return"+"===e[0]?n:-n}return 0}],S=(c("monthNamesShort"),c("monthNames"),{default:"ddd MMM DD YYYY HH:mm:ss",shortDate:"M/D/YY",mediumDate:"MMM D, YYYY",longDate:"MMMM D, YYYY",fullDate:"dddd, MMMM D, YYYY",isoDate:"YYYY-MM-DD",isoDateTime:"YYYY-MM-DDTHH:mm:ssZ",shortTime:"HH:mm",mediumTime:"HH:mm:ss",longTime:"HH:mm:ss.SSS"}),D=function(t,e,n){if(void 0===e&&(e=S.default),void 0===n&&(n={}),"number"==typeof t&&(t=new Date(t)),"[object Date]"!==Object.prototype.toString.call(t)||isNaN(t.getTime()))throw new Error("Invalid Date pass to format");var o=[];e=(e=S[e]||e).replace(a,(function(t,e){return o.push(e),"@@@"}));var r=u(u({},f),n);return(e=e.replace(i,(function(e){return v[e](t,r)}))).replace(/@@@/g,(function(){return o.shift()}))}},98626:(t,e,n)=>{"use strict";function i(t){return new Promise(((e,n)=>{t.oncomplete=t.onsuccess=()=>e(t.result),t.onabort=t.onerror=()=>n(t.error)}))}function o(t,e){const n=indexedDB.open(t);n.onupgradeneeded=()=>n.result.createObjectStore(e);const o=i(n);return(t,n)=>o.then((i=>n(i.transaction(e,t).objectStore(e))))}let r;function s(){return r||(r=o("keyval-store","keyval")),r}function a(t,e=s()){return e("readonly",(e=>i(e.get(t))))}function l(t,e,n=s()){return n("readwrite",(n=>(n.put(e,t),i(n.transaction))))}function c(t=s()){return t("readwrite",(t=>(t.clear(),i(t.transaction))))}n.d(e,{ZH:()=>c,MT:()=>o,U2:()=>a,RV:()=>i,t8:()=>l})},78389:(t,e,n)=>{"use strict";n.d(e,{s:()=>p});var i=n(99602),o=n(55122),r=n(57724);const s=(t,e)=>{var n,i;const o=t.N;if(void 0===o)return!1;for(const t of o)null===(i=(n=t).O)||void 0===i||i.call(n,e,!1),s(t,e);return!0},a=t=>{let e,n;do{if(void 0===(e=t.M))break;n=e.N,n.delete(t),t=e}while(0===(null==n?void 0:n.size))},l=t=>{for(let e;e=t.M;t=e){let n=e.N;if(void 0===n)e.N=n=new Set;else if(n.has(t))break;n.add(t),d(e)}};function c(t){void 0!==this.N?(a(this),this.M=t,l(this)):this.M=t}function u(t,e=!1,n=0){const i=this.H,o=this.N;if(void 0!==o&&0!==o.size)if(e)if(Array.isArray(i))for(let t=n;t<i.length;t++)s(i[t],!1),a(i[t]);else null!=i&&(s(i,!1),a(i));else s(this,t)}const d=t=>{var e,n,i,r;t.type==o.pX.CHILD&&(null!==(e=(i=t).P)&&void 0!==e||(i.P=u),null!==(n=(r=t).Q)&&void 0!==n||(r.Q=c))};class p extends o.Xe{constructor(){super(...arguments),this.isConnected=!0,this.ut=i.Jb,this.N=void 0}T(t,e,n){super.T(t,e,n),l(this)}O(t,e=!0){this.at(t),e&&(s(this,t),a(this))}at(t){var e,n;t!==this.isConnected&&(t?(this.isConnected=!0,this.ut!==i.Jb&&(this.setValue(this.ut),this.ut=i.Jb),null===(e=this.reconnected)||void 0===e||e.call(this)):(this.isConnected=!1,null===(n=this.disconnected)||void 0===n||n.call(this)))}S(t,e){if(!this.isConnected)throw Error(`AsyncDirective ${this.constructor.name} was rendered while its tree was disconnected.`);return super.S(t,e)}setValue(t){if(this.isConnected)if((0,r.OR)(this.Σdt))this.Σdt.I(t,this);else{const e=[...this.Σdt.H];e[this.Σct]=t,this.Σdt.I(e,this,0)}else this.ut=t}disconnected(){}reconnected(){}}},57724:(t,e,n)=>{"use strict";n.d(e,{E_:()=>f,i9:()=>h,_Y:()=>c,pt:()=>r,OR:()=>a,hN:()=>s,ws:()=>m,fk:()=>u,hl:()=>p});var i=n(99602);const{et:o}=i.Vm,r=t=>null===t||"object"!=typeof t&&"function"!=typeof t,s=(t,e)=>{var n,i;return void 0===e?void 0!==(null===(n=t)||void 0===n?void 0:n._$litType$):(null===(i=t)||void 0===i?void 0:i._$litType$)===e},a=t=>void 0===t.strings,l=()=>document.createComment(""),c=(t,e,n)=>{var i;const r=t.A.parentNode,s=void 0===e?t.B:e.A;if(void 0===n){const e=r.insertBefore(l(),s),i=r.insertBefore(l(),s);n=new o(e,i,t,t.options)}else{const e=n.B.nextSibling,o=n.M!==t;if(o&&(null===(i=n.Q)||void 0===i||i.call(n,t),n.M=t),e!==s||o){let t=n.A;for(;t!==e;){const e=t.nextSibling;r.insertBefore(t,s),t=e}}}return n},u=(t,e,n=t)=>(t.I(e,n),t),d={},p=(t,e=d)=>t.H=e,h=t=>t.H,m=t=>{var e;null===(e=t.P)||void 0===e||e.call(t,!1,!0);let n=t.A;const i=t.B.nextSibling;for(;n!==i;){const t=n.nextSibling;n.remove(),n=t}},f=t=>{t.R()}},19967:(t,e,n)=>{"use strict";n.d(e,{Xe:()=>i.Xe,pX:()=>i.pX,XM:()=>i.XM});var i=n(55122)},76666:(t,e,n)=>{"use strict";n.d(e,{$:()=>i.$});var i=n(81471)},82816:(t,e,n)=>{"use strict";n.d(e,{o:()=>i.o});var i=n(49629)},92483:(t,e,n)=>{"use strict";n.d(e,{V:()=>i.V});var i=n(79865)}}]);
//# sourceMappingURL=7a0ccfbb.js.map