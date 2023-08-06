/*! For license information please see d30b844c.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[38156],{65660:(e,t,o)=>{"use strict";o(65233);const n=o(50856).d`
<custom-style>
  <style is="custom-style">
    [hidden] {
      display: none !important;
    }
  </style>
</custom-style>
<custom-style>
  <style is="custom-style">
    html {

      --layout: {
        display: -ms-flexbox;
        display: -webkit-flex;
        display: flex;
      };

      --layout-inline: {
        display: -ms-inline-flexbox;
        display: -webkit-inline-flex;
        display: inline-flex;
      };

      --layout-horizontal: {
        @apply --layout;

        -ms-flex-direction: row;
        -webkit-flex-direction: row;
        flex-direction: row;
      };

      --layout-horizontal-reverse: {
        @apply --layout;

        -ms-flex-direction: row-reverse;
        -webkit-flex-direction: row-reverse;
        flex-direction: row-reverse;
      };

      --layout-vertical: {
        @apply --layout;

        -ms-flex-direction: column;
        -webkit-flex-direction: column;
        flex-direction: column;
      };

      --layout-vertical-reverse: {
        @apply --layout;

        -ms-flex-direction: column-reverse;
        -webkit-flex-direction: column-reverse;
        flex-direction: column-reverse;
      };

      --layout-wrap: {
        -ms-flex-wrap: wrap;
        -webkit-flex-wrap: wrap;
        flex-wrap: wrap;
      };

      --layout-wrap-reverse: {
        -ms-flex-wrap: wrap-reverse;
        -webkit-flex-wrap: wrap-reverse;
        flex-wrap: wrap-reverse;
      };

      --layout-flex-auto: {
        -ms-flex: 1 1 auto;
        -webkit-flex: 1 1 auto;
        flex: 1 1 auto;
      };

      --layout-flex-none: {
        -ms-flex: none;
        -webkit-flex: none;
        flex: none;
      };

      --layout-flex: {
        -ms-flex: 1 1 0.000000001px;
        -webkit-flex: 1;
        flex: 1;
        -webkit-flex-basis: 0.000000001px;
        flex-basis: 0.000000001px;
      };

      --layout-flex-2: {
        -ms-flex: 2;
        -webkit-flex: 2;
        flex: 2;
      };

      --layout-flex-3: {
        -ms-flex: 3;
        -webkit-flex: 3;
        flex: 3;
      };

      --layout-flex-4: {
        -ms-flex: 4;
        -webkit-flex: 4;
        flex: 4;
      };

      --layout-flex-5: {
        -ms-flex: 5;
        -webkit-flex: 5;
        flex: 5;
      };

      --layout-flex-6: {
        -ms-flex: 6;
        -webkit-flex: 6;
        flex: 6;
      };

      --layout-flex-7: {
        -ms-flex: 7;
        -webkit-flex: 7;
        flex: 7;
      };

      --layout-flex-8: {
        -ms-flex: 8;
        -webkit-flex: 8;
        flex: 8;
      };

      --layout-flex-9: {
        -ms-flex: 9;
        -webkit-flex: 9;
        flex: 9;
      };

      --layout-flex-10: {
        -ms-flex: 10;
        -webkit-flex: 10;
        flex: 10;
      };

      --layout-flex-11: {
        -ms-flex: 11;
        -webkit-flex: 11;
        flex: 11;
      };

      --layout-flex-12: {
        -ms-flex: 12;
        -webkit-flex: 12;
        flex: 12;
      };

      /* alignment in cross axis */

      --layout-start: {
        -ms-flex-align: start;
        -webkit-align-items: flex-start;
        align-items: flex-start;
      };

      --layout-center: {
        -ms-flex-align: center;
        -webkit-align-items: center;
        align-items: center;
      };

      --layout-end: {
        -ms-flex-align: end;
        -webkit-align-items: flex-end;
        align-items: flex-end;
      };

      --layout-baseline: {
        -ms-flex-align: baseline;
        -webkit-align-items: baseline;
        align-items: baseline;
      };

      /* alignment in main axis */

      --layout-start-justified: {
        -ms-flex-pack: start;
        -webkit-justify-content: flex-start;
        justify-content: flex-start;
      };

      --layout-center-justified: {
        -ms-flex-pack: center;
        -webkit-justify-content: center;
        justify-content: center;
      };

      --layout-end-justified: {
        -ms-flex-pack: end;
        -webkit-justify-content: flex-end;
        justify-content: flex-end;
      };

      --layout-around-justified: {
        -ms-flex-pack: distribute;
        -webkit-justify-content: space-around;
        justify-content: space-around;
      };

      --layout-justified: {
        -ms-flex-pack: justify;
        -webkit-justify-content: space-between;
        justify-content: space-between;
      };

      --layout-center-center: {
        @apply --layout-center;
        @apply --layout-center-justified;
      };

      /* self alignment */

      --layout-self-start: {
        -ms-align-self: flex-start;
        -webkit-align-self: flex-start;
        align-self: flex-start;
      };

      --layout-self-center: {
        -ms-align-self: center;
        -webkit-align-self: center;
        align-self: center;
      };

      --layout-self-end: {
        -ms-align-self: flex-end;
        -webkit-align-self: flex-end;
        align-self: flex-end;
      };

      --layout-self-stretch: {
        -ms-align-self: stretch;
        -webkit-align-self: stretch;
        align-self: stretch;
      };

      --layout-self-baseline: {
        -ms-align-self: baseline;
        -webkit-align-self: baseline;
        align-self: baseline;
      };

      /* multi-line alignment in main axis */

      --layout-start-aligned: {
        -ms-flex-line-pack: start;  /* IE10 */
        -ms-align-content: flex-start;
        -webkit-align-content: flex-start;
        align-content: flex-start;
      };

      --layout-end-aligned: {
        -ms-flex-line-pack: end;  /* IE10 */
        -ms-align-content: flex-end;
        -webkit-align-content: flex-end;
        align-content: flex-end;
      };

      --layout-center-aligned: {
        -ms-flex-line-pack: center;  /* IE10 */
        -ms-align-content: center;
        -webkit-align-content: center;
        align-content: center;
      };

      --layout-between-aligned: {
        -ms-flex-line-pack: justify;  /* IE10 */
        -ms-align-content: space-between;
        -webkit-align-content: space-between;
        align-content: space-between;
      };

      --layout-around-aligned: {
        -ms-flex-line-pack: distribute;  /* IE10 */
        -ms-align-content: space-around;
        -webkit-align-content: space-around;
        align-content: space-around;
      };

      /*******************************
                Other Layout
      *******************************/

      --layout-block: {
        display: block;
      };

      --layout-invisible: {
        visibility: hidden !important;
      };

      --layout-relative: {
        position: relative;
      };

      --layout-fit: {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
      };

      --layout-scroll: {
        -webkit-overflow-scrolling: touch;
        overflow: auto;
      };

      --layout-fullbleed: {
        margin: 0;
        height: 100vh;
      };

      /* fixed position */

      --layout-fixed-top: {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
      };

      --layout-fixed-right: {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
      };

      --layout-fixed-bottom: {
        position: fixed;
        right: 0;
        bottom: 0;
        left: 0;
      };

      --layout-fixed-left: {
        position: fixed;
        top: 0;
        bottom: 0;
        left: 0;
      };

    }
  </style>
</custom-style>`;n.setAttribute("style","display: none;"),document.head.appendChild(n.content);var i=document.createElement("style");i.textContent="[hidden] { display: none !important; }",document.head.appendChild(i)},43835:(e,t,o)=>{"use strict";o(65660),o(54242),o(70019)},70019:(e,t,o)=>{"use strict";o(65233);const n=o(50856).d`<custom-style>
  <style is="custom-style">
    html {

      /* Shared Styles */
      --paper-font-common-base: {
        font-family: 'Roboto', 'Noto', sans-serif;
        -webkit-font-smoothing: antialiased;
      };

      --paper-font-common-code: {
        font-family: 'Roboto Mono', 'Consolas', 'Menlo', monospace;
        -webkit-font-smoothing: antialiased;
      };

      --paper-font-common-expensive-kerning: {
        text-rendering: optimizeLegibility;
      };

      --paper-font-common-nowrap: {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      };

      /* Material Font Styles */

      --paper-font-display4: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 112px;
        font-weight: 300;
        letter-spacing: -.044em;
        line-height: 120px;
      };

      --paper-font-display3: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 56px;
        font-weight: 400;
        letter-spacing: -.026em;
        line-height: 60px;
      };

      --paper-font-display2: {
        @apply --paper-font-common-base;

        font-size: 45px;
        font-weight: 400;
        letter-spacing: -.018em;
        line-height: 48px;
      };

      --paper-font-display1: {
        @apply --paper-font-common-base;

        font-size: 34px;
        font-weight: 400;
        letter-spacing: -.01em;
        line-height: 40px;
      };

      --paper-font-headline: {
        @apply --paper-font-common-base;

        font-size: 24px;
        font-weight: 400;
        letter-spacing: -.012em;
        line-height: 32px;
      };

      --paper-font-title: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 20px;
        font-weight: 500;
        line-height: 28px;
      };

      --paper-font-subhead: {
        @apply --paper-font-common-base;

        font-size: 16px;
        font-weight: 400;
        line-height: 24px;
      };

      --paper-font-body2: {
        @apply --paper-font-common-base;

        font-size: 14px;
        font-weight: 500;
        line-height: 24px;
      };

      --paper-font-body1: {
        @apply --paper-font-common-base;

        font-size: 14px;
        font-weight: 400;
        line-height: 20px;
      };

      --paper-font-caption: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 12px;
        font-weight: 400;
        letter-spacing: 0.011em;
        line-height: 20px;
      };

      --paper-font-menu: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 13px;
        font-weight: 500;
        line-height: 24px;
      };

      --paper-font-button: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 14px;
        font-weight: 500;
        letter-spacing: 0.018em;
        line-height: 24px;
        text-transform: uppercase;
      };

      --paper-font-code2: {
        @apply --paper-font-common-code;

        font-size: 14px;
        font-weight: 700;
        line-height: 20px;
      };

      --paper-font-code1: {
        @apply --paper-font-common-code;

        font-size: 14px;
        font-weight: 500;
        line-height: 20px;
      };

    }

  </style>
</custom-style>`;n.setAttribute("style","display: none;"),document.head.appendChild(n.content)},21384:(e,t,o)=>{"use strict";o.d(t,{t:()=>c});o(56646);var n=o(42687),i=o(74460);let r={},s={};function l(e,t){r[e]=s[e.toLowerCase()]=t}function a(e){return r[e]||s[e.toLowerCase()]}class c extends HTMLElement{static get observedAttributes(){return["id"]}static import(e,t){if(e){let o=a(e);return o&&t?o.querySelector(t):o}return null}attributeChangedCallback(e,t,o,n){t!==o&&this.register()}get assetpath(){if(!this.__assetpath){const e=window.HTMLImports&&HTMLImports.importForElement?HTMLImports.importForElement(this)||document:this.ownerDocument,t=(0,n.Kk)(this.getAttribute("assetpath")||"",e.baseURI);this.__assetpath=(0,n.iY)(t)}return this.__assetpath}register(e){if(e=e||this.id){if(i.XN&&void 0!==a(e))throw l(e,null),new Error(`strictTemplatePolicy: dom-module ${e} re-registered`);this.id=e,l(e,this),(t=this).querySelector("style")&&console.warn("dom-module %s has style outside template",t.id)}var t}}c.prototype.modules=r,customElements.define("dom-module",c)},33367:(e,t,o)=>{"use strict";o.d(t,{w:()=>f});var n=o(18890),i=o(74460);const r={attached:!0,detached:!0,ready:!0,created:!0,beforeRegister:!0,registered:!0,attributeChanged:!0,listeners:!0,hostAttributes:!0},s={attached:!0,detached:!0,ready:!0,created:!0,beforeRegister:!0,registered:!0,attributeChanged:!0,behaviors:!0,_noAccessors:!0},l=Object.assign({listeners:!0,hostAttributes:!0,properties:!0,observers:!0},s);function a(e,t,o,n){!function(e,t,o){const n=e._noAccessors,i=Object.getOwnPropertyNames(e);for(let r=0;r<i.length;r++){let s=i[r];if(!(s in o))if(n)t[s]=e[s];else{let o=Object.getOwnPropertyDescriptor(e,s);o&&(o.configurable=!0,Object.defineProperty(t,s,o))}}}(t,e,n);for(let e in r)t[e]&&(o[e]=o[e]||[],o[e].push(t[e]))}function c(e,t,o){t=t||[];for(let n=e.length-1;n>=0;n--){let i=e[n];i?Array.isArray(i)?c(i,t):t.indexOf(i)<0&&(!o||o.indexOf(i)<0)&&t.unshift(i):console.warn("behavior is null, check for missing or 404 import")}return t}function p(e,t){for(const o in t){const n=e[o],i=t[o];e[o]=!("value"in i)&&n&&"value"in n?Object.assign({value:n.value},i):i}}const d=(0,n.x)(HTMLElement);function u(e,t,o){let n;const r={};class d extends t{static _finalizeClass(){if(this.hasOwnProperty(JSCompiler_renameProperty("generatedFrom",this))){if(n)for(let e,t=0;t<n.length;t++)e=n[t],e.properties&&this.createProperties(e.properties),e.observers&&this.createObservers(e.observers,e.properties);e.properties&&this.createProperties(e.properties),e.observers&&this.createObservers(e.observers,e.properties),this._prepareTemplate()}else t._finalizeClass.call(this)}static get properties(){const t={};if(n)for(let e=0;e<n.length;e++)p(t,n[e].properties);return p(t,e.properties),t}static get observers(){let t=[];if(n)for(let e,o=0;o<n.length;o++)e=n[o],e.observers&&(t=t.concat(e.observers));return e.observers&&(t=t.concat(e.observers)),t}created(){super.created();const e=r.created;if(e)for(let t=0;t<e.length;t++)e[t].call(this)}_registered(){const e=d.prototype;if(!e.hasOwnProperty(JSCompiler_renameProperty("__hasRegisterFinished",e))){const t=Object.getPrototypeOf(this);t===e&&(e.__hasRegisterFinished=!0),super._registered(),i.nL&&!Object.hasOwnProperty(e,"__hasCopiedProperties")&&(e.__hasCopiedProperties=!0,u(e));let o=r.beforeRegister;if(o)for(let e=0;e<o.length;e++)o[e].call(t);if(o=r.registered,o)for(let e=0;e<o.length;e++)o[e].call(t)}}_applyListeners(){super._applyListeners();const e=r.listeners;if(e)for(let t=0;t<e.length;t++){const o=e[t];if(o)for(let e in o)this._addMethodEventListenerToNode(this,e,o[e])}}_ensureAttributes(){const e=r.hostAttributes;if(e)for(let t=e.length-1;t>=0;t--){const o=e[t];for(let e in o)this._ensureAttribute(e,o[e])}super._ensureAttributes()}ready(){super.ready();let e=r.ready;if(e)for(let t=0;t<e.length;t++)e[t].call(this)}attached(){super.attached();let e=r.attached;if(e)for(let t=0;t<e.length;t++)e[t].call(this)}detached(){super.detached();let e=r.detached;if(e)for(let t=0;t<e.length;t++)e[t].call(this)}attributeChanged(e,t,o){super.attributeChanged();let n=r.attributeChanged;if(n)for(let i=0;i<n.length;i++)n[i].call(this,e,t,o)}}if(o){Array.isArray(o)||(o=[o]);let e=t.prototype.behaviors;n=c(o,null,e),d.prototype.behaviors=e?e.concat(o):n}const u=t=>{n&&function(e,t,o){for(let n=0;n<t.length;n++)a(e,t[n],o,l)}(t,n,r),a(t,e,r,s)};return i.nL||u(d.prototype),d.generatedFrom=e,d}const f=function(e,t){e||console.warn("Polymer.Class requires `info` argument");let o=t?t(d):d;return o=u(e,o,e.behaviors),o.is=o.prototype.is=e.is,o}},72419:(e,t,o)=>{"use strict";var n=o(18691);let i;i=n.E._mutablePropertyChange;Boolean},9672:(e,t,o)=>{"use strict";var n=o(33367);o(56646);const i=function(e){let t;return t="function"==typeof e?e:i.Class(e),e._legacyForceObservedAttributes&&(t.prototype._legacyForceObservedAttributes=e._legacyForceObservedAttributes),customElements.define(t.is,t),t};i.Class=n.w},87156:(e,t,o)=>{"use strict";o.d(t,{Ku:()=>l,vz:()=>u});o(56646);var n=o(62276),i=(o(74460),o(20723));o(93252),o(78956);const r=Element.prototype,s=r.matches||r.matchesSelector||r.mozMatchesSelector||r.msMatchesSelector||r.oMatchesSelector||r.webkitMatchesSelector,l=function(e,t){return s.call(e,t)};class a{constructor(e){window.ShadyDOM&&window.ShadyDOM.inUse&&window.ShadyDOM.patch(e),this.node=e}observeNodes(e){return new i.o(this.node,e)}unobserveNodes(e){e.disconnect()}notifyObserver(){}deepContains(e){if((0,n.r)(this.node).contains(e))return!0;let t=e,o=e.ownerDocument;for(;t&&t!==o&&t!==this.node;)t=(0,n.r)(t).parentNode||(0,n.r)(t).host;return t===this.node}getOwnerRoot(){return(0,n.r)(this.node).getRootNode()}getDistributedNodes(){return"slot"===this.node.localName?(0,n.r)(this.node).assignedNodes({flatten:!0}):[]}getDestinationInsertionPoints(){let e=[],t=(0,n.r)(this.node).assignedSlot;for(;t;)e.push(t),t=(0,n.r)(t).assignedSlot;return e}importNode(e,t){let o=this.node instanceof Document?this.node:this.node.ownerDocument;return(0,n.r)(o).importNode(e,t)}getEffectiveChildNodes(){return i.o.getFlattenedNodes(this.node)}queryDistributedElements(e){let t=this.getEffectiveChildNodes(),o=[];for(let n,i=0,r=t.length;i<r&&(n=t[i]);i++)n.nodeType===Node.ELEMENT_NODE&&l(n,e)&&o.push(n);return o}get activeElement(){let e=this.node;return void 0!==e._activeElement?e._activeElement:e.activeElement}}function c(e,t){for(let o=0;o<t.length;o++){let n=t[o];Object.defineProperty(e,n,{get:function(){return this.node[n]},configurable:!0})}}class p{constructor(e){this.event=e}get rootTarget(){return this.path[0]}get localTarget(){return this.event.target}get path(){return this.event.composedPath()}}a.prototype.cloneNode,a.prototype.appendChild,a.prototype.insertBefore,a.prototype.removeChild,a.prototype.replaceChild,a.prototype.setAttribute,a.prototype.removeAttribute,a.prototype.querySelector,a.prototype.querySelectorAll,a.prototype.parentNode,a.prototype.firstChild,a.prototype.lastChild,a.prototype.nextSibling,a.prototype.previousSibling,a.prototype.firstElementChild,a.prototype.lastElementChild,a.prototype.nextElementSibling,a.prototype.previousElementSibling,a.prototype.childNodes,a.prototype.children,a.prototype.classList,a.prototype.textContent,a.prototype.innerHTML;let d=a;if(window.ShadyDOM&&window.ShadyDOM.inUse&&window.ShadyDOM.noPatch&&window.ShadyDOM.Wrapper){class e extends window.ShadyDOM.Wrapper{}Object.getOwnPropertyNames(a.prototype).forEach((t=>{"activeElement"!=t&&(e.prototype[t]=a.prototype[t])})),c(e.prototype,["classList"]),d=e,Object.defineProperties(p.prototype,{localTarget:{get(){const e=this.event.currentTarget,t=e&&u(e).getOwnerRoot(),o=this.path;for(let e=0;e<o.length;e++){const n=o[e];if(u(n).getOwnerRoot()===t)return n}},configurable:!0},path:{get(){return window.ShadyDOM.composedPath(this.event)},configurable:!0}})}else!function(e,t){for(let o=0;o<t.length;o++){let n=t[o];e[n]=function(){return this.node[n].apply(this.node,arguments)}}}(a.prototype,["cloneNode","appendChild","insertBefore","removeChild","replaceChild","setAttribute","removeAttribute","querySelector","querySelectorAll"]),c(a.prototype,["parentNode","firstChild","lastChild","nextSibling","previousSibling","firstElementChild","lastElementChild","nextElementSibling","previousElementSibling","childNodes","children","classList"]),function(e,t){for(let o=0;o<t.length;o++){let n=t[o];Object.defineProperty(e,n,{get:function(){return this.node[n]},set:function(e){this.node[n]=e},configurable:!0})}}(a.prototype,["textContent","innerHTML","className"]);const u=function(e){if((e=e||document)instanceof d)return e;if(e instanceof p)return e;let t=e.__domApi;return t||(t=e instanceof Event?new p(e):new d(e),e.__domApi=t),t}},37692:(e,t,o)=>{"use strict";o(52521)},16777:(e,t,o)=>{"use strict";o.d(t,{X:()=>l});var n=o(36608),i=o(76389),r=o(62276);const s="disable-upgrade",l=e=>{for(;e;){const t=Object.getOwnPropertyDescriptor(e,"observedAttributes");if(t)return t.get;e=Object.getPrototypeOf(e.prototype).constructor}return()=>[]};(0,i.o)((e=>{const t=(0,n.SH)(e);let o=l(t);return class extends t{constructor(){super(),this.__isUpgradeDisabled}static get observedAttributes(){return o.call(this).concat(s)}_initializeProperties(){this.hasAttribute(s)?this.__isUpgradeDisabled=!0:super._initializeProperties()}_enableProperties(){this.__isUpgradeDisabled||super._enableProperties()}_canApplyPropertyDefault(e){return super._canApplyPropertyDefault(e)&&!(this.__isUpgradeDisabled&&this._isPropertyPending(e))}attributeChangedCallback(e,t,o,n){e==s?this.__isUpgradeDisabled&&null==o&&(super._initializeProperties(),this.__isUpgradeDisabled=!1,(0,r.r)(this).isConnected&&super.connectedCallback()):super.attributeChangedCallback(e,t,o,n)}connectedCallback(){this.__isUpgradeDisabled||super.connectedCallback()}disconnectedCallback(){this.__isUpgradeDisabled||super.disconnectedCallback()}}}))},21683:(e,t,o)=>{"use strict";o.d(t,{Wc:()=>c,YA:()=>p});o(56646);let n=0,i=0,r=[],s=0,l=!1,a=document.createTextNode("");new window.MutationObserver((function(){l=!1;const e=r.length;for(let t=0;t<e;t++){let e=r[t];if(e)try{e()}catch(e){setTimeout((()=>{throw e}))}}r.splice(0,e),i+=e})).observe(a,{characterData:!0});const c={after:e=>({run:t=>window.setTimeout(t,e),cancel(e){window.clearTimeout(e)}}),run:(e,t)=>window.setTimeout(e,t),cancel(e){window.clearTimeout(e)}},p={run:e=>(l||(l=!0,a.textContent=s++),r.push(e),n++),cancel(e){const t=e-i;if(t>=0){if(!r[t])throw new Error("invalid async handle: "+e);r[t]=null}}}},81668:(e,t,o)=>{"use strict";o.d(t,{NH:()=>z,ys:()=>A,BP:()=>L});o(56646);var n=o(21683),i=o(78956),r=o(74460),s=o(62276);let l="string"==typeof document.head.style.touchAction,a="__polymerGestures",c="__polymerGesturesHandled",p="__polymerGesturesTouchAction",d=["mousedown","mousemove","mouseup","click"],u=[0,1,4,2],f=function(){try{return 1===new MouseEvent("test",{buttons:1}).buttons}catch(e){return!1}}();function h(e){return d.indexOf(e)>-1}let m=!1;function y(e){if(!h(e)&&"touchend"!==e)return l&&m&&r.f6?{passive:!0}:void 0}!function(){try{let e=Object.defineProperty({},"passive",{get(){m=!0}});window.addEventListener("test",null,e),window.removeEventListener("test",null,e)}catch(e){}}();let w=navigator.userAgent.match(/iP(?:[oa]d|hone)|Android/);const g=[],_={button:!0,input:!0,keygen:!0,meter:!0,output:!0,textarea:!0,progress:!0,select:!0},b={button:!0,command:!0,fieldset:!0,input:!0,keygen:!0,optgroup:!0,option:!0,select:!0,textarea:!0};function x(e){let t=Array.prototype.slice.call(e.labels||[]);if(!t.length){t=[];let o=e.getRootNode();if(e.id){let n=o.querySelectorAll(`label[for = ${e.id}]`);for(let e=0;e<n.length;e++)t.push(n[e])}}return t}let v=function(e){let t=e.sourceCapabilities;var o;if((!t||t.firesTouchEvents)&&(e[c]={skip:!0},"click"===e.type)){let t=!1,n=T(e);for(let e=0;e<n.length;e++){if(n[e].nodeType===Node.ELEMENT_NODE)if("label"===n[e].localName)g.push(n[e]);else if(o=n[e],_[o.localName]){let o=x(n[e]);for(let e=0;e<o.length;e++)t=t||g.indexOf(o[e])>-1}if(n[e]===k.mouse.target)return}if(t)return;e.preventDefault(),e.stopPropagation()}};function P(e){let t=w?["click"]:d;for(let o,n=0;n<t.length;n++)o=t[n],e?(g.length=0,document.addEventListener(o,v,!0)):document.removeEventListener(o,v,!0)}function E(e){let t=e.type;if(!h(t))return!1;if("mousemove"===t){let t=void 0===e.buttons?1:e.buttons;return e instanceof window.MouseEvent&&!f&&(t=u[e.which]||0),Boolean(1&t)}return 0===(void 0===e.button?0:e.button)}let k={mouse:{target:null,mouseIgnoreJob:null},touch:{x:0,y:0,id:-1,scrollDecided:!1}};function C(e,t,o){e.movefn=t,e.upfn=o,document.addEventListener("mousemove",t),document.addEventListener("mouseup",o)}function O(e){document.removeEventListener("mousemove",e.movefn),document.removeEventListener("mouseup",e.upfn),e.movefn=null,e.upfn=null}r.z2&&document.addEventListener("touchend",(function(e){if(!r.z2)return;k.mouse.mouseIgnoreJob||P(!0),k.mouse.target=T(e)[0],k.mouse.mouseIgnoreJob=i.dx.debounce(k.mouse.mouseIgnoreJob,n.Wc.after(2500),(function(){P(),k.mouse.target=null,k.mouse.mouseIgnoreJob=null}))}),!!m&&{passive:!0});const T=window.ShadyDOM&&window.ShadyDOM.noPatch?window.ShadyDOM.composedPath:e=>e.composedPath&&e.composedPath()||[],S={},N=[];function M(e){const t=T(e);return t.length>0?t[0]:e.target}function D(e){let t,o=e.type,n=e.currentTarget[a];if(!n)return;let i=n[o];if(i){if(!e[c]&&(e[c]={},"touch"===o.slice(0,5))){let t=(e=e).changedTouches[0];if("touchstart"===o&&1===e.touches.length&&(k.touch.id=t.identifier),k.touch.id!==t.identifier)return;l||"touchstart"!==o&&"touchmove"!==o||function(e){let t=e.changedTouches[0],o=e.type;if("touchstart"===o)k.touch.x=t.clientX,k.touch.y=t.clientY,k.touch.scrollDecided=!1;else if("touchmove"===o){if(k.touch.scrollDecided)return;k.touch.scrollDecided=!0;let o=function(e){let t="auto",o=T(e);for(let e,n=0;n<o.length;n++)if(e=o[n],e[p]){t=e[p];break}return t}(e),n=!1,i=Math.abs(k.touch.x-t.clientX),r=Math.abs(k.touch.y-t.clientY);e.cancelable&&("none"===o?n=!0:"pan-x"===o?n=r>i:"pan-y"===o&&(n=i>r)),n?e.preventDefault():R("track")}}(e)}if(t=e[c],!t.skip){for(let o,n=0;n<N.length;n++)o=N[n],i[o.name]&&!t[o.name]&&o.flow&&o.flow.start.indexOf(e.type)>-1&&o.reset&&o.reset();for(let n,r=0;r<N.length;r++)n=N[r],i[n.name]&&!t[n.name]&&(t[n.name]=!0,n[o](e))}}}function z(e,t,o){return!!S[t]&&(function(e,t,o){let n=S[t],i=n.deps,r=n.name,s=e[a];s||(e[a]=s={});for(let t,o,n=0;n<i.length;n++)t=i[n],w&&h(t)&&"click"!==t||(o=s[t],o||(s[t]=o={_count:0}),0===o._count&&e.addEventListener(t,D,y(t)),o[r]=(o[r]||0)+1,o._count=(o._count||0)+1);e.addEventListener(t,o),n.touchAction&&L(e,n.touchAction)}(e,t,o),!0)}function A(e,t,o){return!!S[t]&&(function(e,t,o){let n=S[t],i=n.deps,r=n.name,s=e[a];if(s)for(let t,o,n=0;n<i.length;n++)t=i[n],o=s[t],o&&o[r]&&(o[r]=(o[r]||1)-1,o._count=(o._count||1)-1,0===o._count&&e.removeEventListener(t,D,y(t)));e.removeEventListener(t,o)}(e,t,o),!0)}function H(e){N.push(e);for(let t=0;t<e.emits.length;t++)S[e.emits[t]]=e}function L(e,t){l&&e instanceof HTMLElement&&n.YA.run((()=>{e.style.touchAction=t})),e[p]=t}function j(e,t,o){let n=new Event(t,{bubbles:!0,cancelable:!0,composed:!0});if(n.detail=o,(0,s.r)(e).dispatchEvent(n),n.defaultPrevented){let e=o.preventer||o.sourceEvent;e&&e.preventDefault&&e.preventDefault()}}function R(e){let t=function(e){for(let t,o=0;o<N.length;o++){t=N[o];for(let o,n=0;n<t.emits.length;n++)if(o=t.emits[n],o===e)return t}return null}(e);t.info&&(t.info.prevent=!0)}function Y(e,t,o,n){t&&j(t,e,{x:o.clientX,y:o.clientY,sourceEvent:o,preventer:n,prevent:function(e){return R(e)}})}function I(e,t,o){if(e.prevent)return!1;if(e.started)return!0;let n=Math.abs(e.x-t),i=Math.abs(e.y-o);return n>=5||i>=5}function F(e,t,o){if(!t)return;let n,i=e.moves[e.moves.length-2],r=e.moves[e.moves.length-1],s=r.x-e.x,l=r.y-e.y,a=0;i&&(n=r.x-i.x,a=r.y-i.y),j(t,"track",{state:e.state,x:o.clientX,y:o.clientY,dx:s,dy:l,ddx:n,ddy:a,sourceEvent:o,hover:function(){return function(e,t){let o=document.elementFromPoint(e,t),n=o;for(;n&&n.shadowRoot&&!window.ShadyDOM;){let i=n;if(n=n.shadowRoot.elementFromPoint(e,t),i===n)break;n&&(o=n)}return o}(o.clientX,o.clientY)}})}function X(e,t,o){let n=Math.abs(t.clientX-e.x),i=Math.abs(t.clientY-e.y),r=M(o||t);!r||b[r.localName]&&r.hasAttribute("disabled")||(isNaN(n)||isNaN(i)||n<=25&&i<=25||function(e){if("click"===e.type){if(0===e.detail)return!0;let t=M(e);if(!t.nodeType||t.nodeType!==Node.ELEMENT_NODE)return!0;let o=t.getBoundingClientRect(),n=e.pageX,i=e.pageY;return!(n>=o.left&&n<=o.right&&i>=o.top&&i<=o.bottom)}return!1}(t))&&(e.prevent||j(r,"tap",{x:t.clientX,y:t.clientY,sourceEvent:t,preventer:o}))}H({name:"downup",deps:["mousedown","touchstart","touchend"],flow:{start:["mousedown","touchstart"],end:["mouseup","touchend"]},emits:["down","up"],info:{movefn:null,upfn:null},reset:function(){O(this.info)},mousedown:function(e){if(!E(e))return;let t=M(e),o=this;C(this.info,(function(e){E(e)||(Y("up",t,e),O(o.info))}),(function(e){E(e)&&Y("up",t,e),O(o.info)})),Y("down",t,e)},touchstart:function(e){Y("down",M(e),e.changedTouches[0],e)},touchend:function(e){Y("up",M(e),e.changedTouches[0],e)}}),H({name:"track",touchAction:"none",deps:["mousedown","touchstart","touchmove","touchend"],flow:{start:["mousedown","touchstart"],end:["mouseup","touchend"]},emits:["track"],info:{x:0,y:0,state:"start",started:!1,moves:[],addMove:function(e){this.moves.length>2&&this.moves.shift(),this.moves.push(e)},movefn:null,upfn:null,prevent:!1},reset:function(){this.info.state="start",this.info.started=!1,this.info.moves=[],this.info.x=0,this.info.y=0,this.info.prevent=!1,O(this.info)},mousedown:function(e){if(!E(e))return;let t=M(e),o=this,n=function(e){let n=e.clientX,i=e.clientY;I(o.info,n,i)&&(o.info.state=o.info.started?"mouseup"===e.type?"end":"track":"start","start"===o.info.state&&R("tap"),o.info.addMove({x:n,y:i}),E(e)||(o.info.state="end",O(o.info)),t&&F(o.info,t,e),o.info.started=!0)};C(this.info,n,(function(e){o.info.started&&n(e),O(o.info)})),this.info.x=e.clientX,this.info.y=e.clientY},touchstart:function(e){let t=e.changedTouches[0];this.info.x=t.clientX,this.info.y=t.clientY},touchmove:function(e){let t=M(e),o=e.changedTouches[0],n=o.clientX,i=o.clientY;I(this.info,n,i)&&("start"===this.info.state&&R("tap"),this.info.addMove({x:n,y:i}),F(this.info,t,o),this.info.state="track",this.info.started=!0)},touchend:function(e){let t=M(e),o=e.changedTouches[0];this.info.started&&(this.info.state="end",this.info.addMove({x:o.clientX,y:o.clientY}),F(this.info,t,o))}}),H({name:"tap",deps:["mousedown","click","touchstart","touchend"],flow:{start:["mousedown","touchstart"],end:["click","touchend"]},emits:["tap"],info:{x:NaN,y:NaN,prevent:!1},reset:function(){this.info.x=NaN,this.info.y=NaN,this.info.prevent=!1},mousedown:function(e){E(e)&&(this.info.x=e.clientX,this.info.y=e.clientY)},click:function(e){E(e)&&X(this.info,e)},touchstart:function(e){const t=e.changedTouches[0];this.info.x=t.clientX,this.info.y=t.clientY},touchend:function(e){X(this.info,e.changedTouches[0],e)}})},87529:(e,t,o)=>{"use strict";o(56646)},74460:(e,t,o)=>{"use strict";o.d(t,{my:()=>i,FV:()=>r,sM:()=>s,v1:()=>l,f6:()=>a,XN:()=>c,ZN:()=>p,nL:()=>d,a2:()=>u,Hr:()=>f,HY:()=>h,ls:()=>m,z2:()=>y,gx:()=>w,ew:()=>g,dJ:()=>_,j8:()=>b,md:()=>x});o(56646);var n=o(42687);const i=!window.ShadyDOM||!window.ShadyDOM.inUse,r=(Boolean(!window.ShadyCSS||window.ShadyCSS.nativeCss),window.customElements.polyfillWrapFlushCallback,i&&"adoptedStyleSheets"in Document.prototype&&"replaceSync"in CSSStyleSheet.prototype&&(()=>{try{const e=new CSSStyleSheet;e.replaceSync("");const t=document.createElement("div");return t.attachShadow({mode:"open"}),t.shadowRoot.adoptedStyleSheets=[e],t.shadowRoot.adoptedStyleSheets[0]===e}catch(e){return!1}})());let s=window.Polymer&&window.Polymer.rootPath||(0,n.iY)(document.baseURI||window.location.href);let l=window.Polymer&&window.Polymer.sanitizeDOMValue||void 0;let a=window.Polymer&&window.Polymer.setPassiveTouchGestures||!1;let c=window.Polymer&&window.Polymer.strictTemplatePolicy||!1;let p=window.Polymer&&window.Polymer.allowTemplateFromDomModule||!1;let d=window.Polymer&&window.Polymer.legacyOptimizations||!1;let u=window.Polymer&&window.Polymer.legacyWarnings||!1;let f=window.Polymer&&window.Polymer.syncInitialRender||!1;let h=window.Polymer&&window.Polymer.legacyUndefined||!1;let m=window.Polymer&&window.Polymer.orderedComputed||!1;let y=!0;let w=window.Polymer&&window.Polymer.removeNestedTemplates||!1;let g=window.Polymer&&window.Polymer.fastDomIf||!1;let _=window.Polymer&&window.Polymer.suppressTemplateNotifications||!1;let b=window.Polymer&&window.Polymer.legacyNoObservedAttributes||!1;let x=window.Polymer&&window.Polymer.useAdoptedStyleSheetsWithBuiltCSS||!1},52521:(e,t,o)=>{"use strict";o.d(t,{aZ:()=>u,Uv:()=>b,GJ:()=>x});o(56646);var n=o(40729),i=o(18691),r=o(74460),s=o(62276);let l=null;function a(){return l}a.prototype=Object.create(HTMLTemplateElement.prototype,{constructor:{value:a,writable:!0}});const c=(0,n.q)(a),p=(0,i.E)(c);const d=(0,n.q)(class{});function u(e,t){for(let o=0;o<t.length;o++){let n=t[o];if(Boolean(e)!=Boolean(n.__hideTemplateChildren__))if(n.nodeType===Node.TEXT_NODE)e?(n.__polymerTextContent__=n.textContent,n.textContent=""):n.textContent=n.__polymerTextContent__;else if("slot"===n.localName)if(e)n.__polymerReplaced__=document.createComment("hidden-slot"),(0,s.r)((0,s.r)(n).parentNode).replaceChild(n.__polymerReplaced__,n);else{const e=n.__polymerReplaced__;e&&(0,s.r)((0,s.r)(e).parentNode).replaceChild(n,e)}else n.style&&(e?(n.__polymerDisplay__=n.style.display,n.style.display="none"):n.style.display=n.__polymerDisplay__);n.__hideTemplateChildren__=e,n._showHideChildren&&n._showHideChildren(e)}}class f extends d{constructor(e){super(),this._configureProperties(e),this.root=this._stampTemplate(this.__dataHost);let t=[];this.children=t;for(let e=this.root.firstChild;e;e=e.nextSibling)t.push(e),e.__templatizeInstance=this;this.__templatizeOwner&&this.__templatizeOwner.__hideTemplateChildren__&&this._showHideChildren(!0);let o=this.__templatizeOptions;(e&&o.instanceProps||!o.instanceProps)&&this._enableProperties()}_configureProperties(e){if(this.__templatizeOptions.forwardHostProp)for(let e in this.__hostProps)this._setPendingProperty(e,this.__dataHost["_host_"+e]);for(let t in e)this._setPendingProperty(t,e[t])}forwardHostProp(e,t){this._setPendingPropertyOrPath(e,t,!1,!0)&&this.__dataHost._enqueueClient(this)}_addEventListenerToNode(e,t,o){if(this._methodHost&&this.__templatizeOptions.parentModel)this._methodHost._addEventListenerToNode(e,t,(e=>{e.model=this,o(e)}));else{let n=this.__dataHost.__dataHost;n&&n._addEventListenerToNode(e,t,o)}}_showHideChildren(e){u(e,this.children)}_setUnmanagedPropertyToNode(e,t,o){e.__hideTemplateChildren__&&e.nodeType==Node.TEXT_NODE&&"textContent"==t?e.__polymerTextContent__=o:super._setUnmanagedPropertyToNode(e,t,o)}get parentModel(){let e=this.__parentModel;if(!e){let t;e=this;do{e=e.__dataHost.__dataHost}while((t=e.__templatizeOptions)&&!t.parentModel);this.__parentModel=e}return e}dispatchEvent(e){return!0}}f.prototype.__dataHost,f.prototype.__templatizeOptions,f.prototype._methodHost,f.prototype.__templatizeOwner,f.prototype.__hostProps;const h=(0,i.E)(f);function m(e){let t=e.__dataHost;return t&&t._methodHost||t}function y(e,t,o){let n=o.mutableData?h:f;b.mixin&&(n=b.mixin(n));let i=class extends n{};return i.prototype.__templatizeOptions=o,i.prototype._bindTemplate(e),function(e,t,o,n){let i=o.hostProps||{};for(let t in n.instanceProps){delete i[t];let o=n.notifyInstanceProp;o&&e.prototype._addPropertyEffect(t,e.prototype.PROPERTY_EFFECT_TYPES.NOTIFY,{fn:_(t,o)})}if(n.forwardHostProp&&t.__dataHost)for(let t in i)o.hasHostProps||(o.hasHostProps=!0),e.prototype._addPropertyEffect(t,e.prototype.PROPERTY_EFFECT_TYPES.NOTIFY,{fn:function(e,t,o){e.__dataHost._setPendingPropertyOrPath("_host_"+t,o[t],!0,!0)}})}(i,e,t,o),i}function w(e,t,o,n){let i=o.forwardHostProp;if(i&&t.hasHostProps){const d="template"==e.localName;let u=t.templatizeTemplateClass;if(!u){if(d){let e=o.mutableData?p:c;class n extends e{}u=t.templatizeTemplateClass=n}else{const o=e.constructor;class n extends o{}u=t.templatizeTemplateClass=n}let s=t.hostProps;for(let e in s)u.prototype._addPropertyEffect("_host_"+e,u.prototype.PROPERTY_EFFECT_TYPES.PROPAGATE,{fn:g(e,i)}),u.prototype._createNotifyingProperty("_host_"+e);r.a2&&n&&function(e,t,o){const n=o.constructor._properties,{propertyEffects:i}=e,{instanceProps:r}=t;for(let e in i)if(!(n[e]||r&&r[e])){const t=i[e];for(let o=0;o<t.length;o++){const{part:n}=t[o].info;if(!n.signature||!n.signature.static){console.warn(`Property '${e}' used in template but not declared in 'properties'; attribute will not be observed.`);break}}}}(t,o,n)}if(e.__dataProto&&Object.assign(e.__data,e.__dataProto),d)a=u,l=s=e,Object.setPrototypeOf(s,a.prototype),new a,l=null,e.__dataTemp={},e.__dataPending=null,e.__dataOld=null,e._enableProperties();else{Object.setPrototypeOf(e,u.prototype);const o=t.hostProps;for(let t in o)if(t="_host_"+t,t in e){const o=e[t];delete e[t],e.__data[t]=o}}}var s,a}function g(e,t){return function(e,o,n){t.call(e.__templatizeOwner,o.substring("_host_".length),n[o])}}function _(e,t){return function(e,o,n){t.call(e.__templatizeOwner,e,o,n[o])}}function b(e,t,o){if(r.XN&&!m(e))throw new Error("strictTemplatePolicy: template owner not trusted");if(o=o||{},e.__templatizeOwner)throw new Error("A <template> can only be templatized once");e.__templatizeOwner=t;let n=(t?t.constructor:f)._parseTemplate(e),i=n.templatizeInstanceClass;i||(i=y(e,n,o),n.templatizeInstanceClass=i);const s=m(e);w(e,n,o,s);let l=class extends i{};return l.prototype._methodHost=s,l.prototype.__dataHost=e,l.prototype.__templatizeOwner=t,l.prototype.__hostProps=n.hostProps,l=l,l}function x(e,t){let o;for(;t;)if(o=t.__dataHost?t:t.__templatizeInstance){if(o.__dataHost==e)return o;t=o.__dataHost}else t=(0,s.r)(t).parentNode;return null}},28426:(e,t,o)=>{"use strict";o.d(t,{H3:()=>i});var n=o(36608);o(50856);const i=(0,n.SH)(HTMLElement)},65233:(e,t,o)=>{"use strict";var n=o(18890);o(9672),o(37692),o(9024),o(42173),o(26047),o(37961),o(5618),o(72419),o(50856);(0,n.x)(HTMLElement).prototype}}]);
//# sourceMappingURL=d30b844c.js.map