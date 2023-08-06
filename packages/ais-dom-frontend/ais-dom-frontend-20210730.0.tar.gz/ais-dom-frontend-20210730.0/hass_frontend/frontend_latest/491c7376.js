/*! For license information please see 491c7376.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[37797],{47181:(e,r,t)=>{"use strict";t.d(r,{B:()=>o});const o=(e,r,t,o)=>{o=o||{},t=null==t?{}:t;const i=new Event(r,{bubbles:void 0===o.bubbles||o.bubbles,cancelable:Boolean(o.cancelable),composed:void 0===o.composed||o.composed});return i.detail=t,e.dispatchEvent(i),i}},87744:(e,r,t)=>{"use strict";function o(e){const r=e.language||"en";return e.translationMetadata.translations[r]&&e.translationMetadata.translations[r].isRTL||!1}function i(e){return n(o(e))}function n(e){return e?"rtl":"ltr"}t.d(r,{HE:()=>o,Zu:()=>i,$3:()=>n})},28417:(e,r,t)=>{"use strict";t(50808);var o=t(33367),i=t(93592),n=t(87156);const a={getTabbableNodes:function(e){const r=[];return this._collectTabbableNodes(e,r)?i.H._sortByTabIndex(r):r},_collectTabbableNodes:function(e,r){if(e.nodeType!==Node.ELEMENT_NODE||!i.H._isVisible(e))return!1;const t=e,o=i.H._normalizedTabIndex(t);let a,l=o>0;o>=0&&r.push(t),a="content"===t.localName||"slot"===t.localName?(0,n.vz)(t).getDistributedNodes():(0,n.vz)(t.shadowRoot||t.root||t).children;for(let e=0;e<a.length;e++)l=this._collectTabbableNodes(a[e],r)||l;return l}},l=customElements.get("paper-dialog"),s={get _focusableNodes(){return a.getTabbableNodes(this)}};class c extends((0,o.P)([s],l)){}customElements.define("ha-paper-dialog",c)},31206:(e,r,t)=>{"use strict";var o=t(54930),i=t(50424),n=t(55358);function a(){a=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,r){["method","field"].forEach((function(t){r.forEach((function(r){r.kind===t&&"own"===r.placement&&this.defineClassElement(e,r)}),this)}),this)},initializeClassElements:function(e,r){var t=e.prototype;["method","field"].forEach((function(o){r.forEach((function(r){var i=r.placement;if(r.kind===o&&("static"===i||"prototype"===i)){var n="static"===i?e:t;this.defineClassElement(n,r)}}),this)}),this)},defineClassElement:function(e,r){var t=r.descriptor;if("field"===r.kind){var o=r.initializer;t={enumerable:t.enumerable,writable:t.writable,configurable:t.configurable,value:void 0===o?void 0:o.call(e)}}Object.defineProperty(e,r.key,t)},decorateClass:function(e,r){var t=[],o=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!c(e))return t.push(e);var r=this.decorateElement(e,i);t.push(r.element),t.push.apply(t,r.extras),o.push.apply(o,r.finishers)}),this),!r)return{elements:t,finishers:o};var n=this.decorateConstructor(t,r);return o.push.apply(o,n.finishers),n.finishers=o,n},addElementPlacement:function(e,r,t){var o=r[e.placement];if(!t&&-1!==o.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");o.push(e.key)},decorateElement:function(e,r){for(var t=[],o=[],i=e.decorators,n=i.length-1;n>=0;n--){var a=r[e.placement];a.splice(a.indexOf(e.key),1);var l=this.fromElementDescriptor(e),s=this.toElementFinisherExtras((0,i[n])(l)||l);e=s.element,this.addElementPlacement(e,r),s.finisher&&o.push(s.finisher);var c=s.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],r);t.push.apply(t,c)}}return{element:e,finishers:o,extras:t}},decorateConstructor:function(e,r){for(var t=[],o=r.length-1;o>=0;o--){var i=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,r[o])(i)||i);if(void 0!==n.finisher&&t.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var l=a+1;l<e.length;l++)if(e[a].key===e[l].key&&e[a].placement===e[l].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:t}},fromElementDescriptor:function(e){var r={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(r,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(r.initializer=e.initializer),r},toElementDescriptors:function(e){var r;if(void 0!==e)return(r=e,function(e){if(Array.isArray(e))return e}(r)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(r)||function(e,r){if(e){if("string"==typeof e)return f(e,r);var t=Object.prototype.toString.call(e).slice(8,-1);return"Object"===t&&e.constructor&&(t=e.constructor.name),"Map"===t||"Set"===t?Array.from(e):"Arguments"===t||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t)?f(e,r):void 0}}(r)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var r=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),r}),this)},toElementDescriptor:function(e){var r=String(e.kind);if("method"!==r&&"field"!==r)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+r+'"');var t=u(e.key),o=String(e.placement);if("static"!==o&&"prototype"!==o&&"own"!==o)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+o+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:r,key:t,placement:o,descriptor:Object.assign({},i)};return"field"!==r?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var r={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(r,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),r},toClassDescriptor:function(e){var r=String(e.kind);if("class"!==r)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+r+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var t=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:t}},runClassFinishers:function(e,r){for(var t=0;t<r.length;t++){var o=(0,r[t])(e);if(void 0!==o){if("function"!=typeof o)throw new TypeError("Finishers must return a constructor.");e=o}}return e},disallowProperty:function(e,r,t){if(void 0!==e[r])throw new TypeError(t+" can't have a ."+r+" property.")}};return e}function l(e){var r,t=u(e.key);"method"===e.kind?r={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?r={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?r={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(r={configurable:!0,writable:!0,enumerable:!0});var o={kind:"field"===e.kind?"field":"method",key:t,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:r};return e.decorators&&(o.decorators=e.decorators),"field"===e.kind&&(o.initializer=e.value),o}function s(e,r){void 0!==e.descriptor.get?r.descriptor.get=e.descriptor.get:r.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,r){var t=e[r];if(void 0!==t&&"function"!=typeof t)throw new TypeError("Expected '"+r+"' to be a function");return t}function u(e){var r=function(e,r){if("object"!=typeof e||null===e)return e;var t=e[Symbol.toPrimitive];if(void 0!==t){var o=t.call(e,r||"default");if("object"!=typeof o)return o;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===r?String:Number)(e)}(e,"string");return"symbol"==typeof r?r:String(r)}function f(e,r){(null==r||r>e.length)&&(r=e.length);for(var t=0,o=new Array(r);t<r;t++)o[t]=e[t];return o}function h(e,r,t){return(h="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,r,t){var o=function(e,r){for(;!Object.prototype.hasOwnProperty.call(e,r)&&null!==(e=m(e)););return e}(e,r);if(o){var i=Object.getOwnPropertyDescriptor(o,r);return i.get?i.get.call(t):i.value}})(e,r,t||e)}function m(e){return(m=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,r,t,o){var i=a();if(o)for(var n=0;n<o.length;n++)i=o[n](i);var p=r((function(e){i.initializeInstanceElements(e,u.elements)}),t),u=i.decorateClass(function(e){for(var r=[],t=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},o=0;o<e.length;o++){var i,n=e[o];if("method"===n.kind&&(i=r.find(t)))if(d(n.descriptor)||d(i.descriptor)){if(c(n)||c(i))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");i.descriptor=n.descriptor}else{if(c(n)){if(c(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");i.decorators=n.decorators}s(n,i)}else r.push(n)}return r}(p.d.map(l)),e);i.initializeClassElements(p.F,u.elements),i.runClassFinishers(p.F,u.finishers)}([(0,n.Mo)("ha-circular-progress")],(function(e,r){class t extends r{constructor(...r){super(...r),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"active",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)()],key:"alt",value:()=>"Loading"},{kind:"field",decorators:[(0,n.Cb)()],key:"size",value:()=>"medium"},{kind:"set",key:"density",value:function(e){}},{kind:"get",key:"density",value:function(){switch(this.size){case"tiny":return-8;case"small":return-5;case"medium":return 0;case"large":return 5;default:return 0}}},{kind:"set",key:"indeterminate",value:function(e){}},{kind:"get",key:"indeterminate",value:function(){return this.active}},{kind:"get",static:!0,key:"styles",value:function(){return[h(m(t),"styles",this),i.iv`
        :host {
          overflow: hidden;
        }
      `]}}]}}),o.D)},52039:(e,r,t)=>{"use strict";t.d(r,{C:()=>f});var o=t(50424),i=t(55358);function n(){n=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,r){["method","field"].forEach((function(t){r.forEach((function(r){r.kind===t&&"own"===r.placement&&this.defineClassElement(e,r)}),this)}),this)},initializeClassElements:function(e,r){var t=e.prototype;["method","field"].forEach((function(o){r.forEach((function(r){var i=r.placement;if(r.kind===o&&("static"===i||"prototype"===i)){var n="static"===i?e:t;this.defineClassElement(n,r)}}),this)}),this)},defineClassElement:function(e,r){var t=r.descriptor;if("field"===r.kind){var o=r.initializer;t={enumerable:t.enumerable,writable:t.writable,configurable:t.configurable,value:void 0===o?void 0:o.call(e)}}Object.defineProperty(e,r.key,t)},decorateClass:function(e,r){var t=[],o=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!s(e))return t.push(e);var r=this.decorateElement(e,i);t.push(r.element),t.push.apply(t,r.extras),o.push.apply(o,r.finishers)}),this),!r)return{elements:t,finishers:o};var n=this.decorateConstructor(t,r);return o.push.apply(o,n.finishers),n.finishers=o,n},addElementPlacement:function(e,r,t){var o=r[e.placement];if(!t&&-1!==o.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");o.push(e.key)},decorateElement:function(e,r){for(var t=[],o=[],i=e.decorators,n=i.length-1;n>=0;n--){var a=r[e.placement];a.splice(a.indexOf(e.key),1);var l=this.fromElementDescriptor(e),s=this.toElementFinisherExtras((0,i[n])(l)||l);e=s.element,this.addElementPlacement(e,r),s.finisher&&o.push(s.finisher);var c=s.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],r);t.push.apply(t,c)}}return{element:e,finishers:o,extras:t}},decorateConstructor:function(e,r){for(var t=[],o=r.length-1;o>=0;o--){var i=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,r[o])(i)||i);if(void 0!==n.finisher&&t.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var l=a+1;l<e.length;l++)if(e[a].key===e[l].key&&e[a].placement===e[l].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:t}},fromElementDescriptor:function(e){var r={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(r,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(r.initializer=e.initializer),r},toElementDescriptors:function(e){var r;if(void 0!==e)return(r=e,function(e){if(Array.isArray(e))return e}(r)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(r)||function(e,r){if(e){if("string"==typeof e)return u(e,r);var t=Object.prototype.toString.call(e).slice(8,-1);return"Object"===t&&e.constructor&&(t=e.constructor.name),"Map"===t||"Set"===t?Array.from(e):"Arguments"===t||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t)?u(e,r):void 0}}(r)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var r=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),r}),this)},toElementDescriptor:function(e){var r=String(e.kind);if("method"!==r&&"field"!==r)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+r+'"');var t=p(e.key),o=String(e.placement);if("static"!==o&&"prototype"!==o&&"own"!==o)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+o+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:r,key:t,placement:o,descriptor:Object.assign({},i)};return"field"!==r?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:d(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var r={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(r,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),r},toClassDescriptor:function(e){var r=String(e.kind);if("class"!==r)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+r+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var t=d(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:t}},runClassFinishers:function(e,r){for(var t=0;t<r.length;t++){var o=(0,r[t])(e);if(void 0!==o){if("function"!=typeof o)throw new TypeError("Finishers must return a constructor.");e=o}}return e},disallowProperty:function(e,r,t){if(void 0!==e[r])throw new TypeError(t+" can't have a ."+r+" property.")}};return e}function a(e){var r,t=p(e.key);"method"===e.kind?r={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?r={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?r={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(r={configurable:!0,writable:!0,enumerable:!0});var o={kind:"field"===e.kind?"field":"method",key:t,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:r};return e.decorators&&(o.decorators=e.decorators),"field"===e.kind&&(o.initializer=e.value),o}function l(e,r){void 0!==e.descriptor.get?r.descriptor.get=e.descriptor.get:r.descriptor.set=e.descriptor.set}function s(e){return e.decorators&&e.decorators.length}function c(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function d(e,r){var t=e[r];if(void 0!==t&&"function"!=typeof t)throw new TypeError("Expected '"+r+"' to be a function");return t}function p(e){var r=function(e,r){if("object"!=typeof e||null===e)return e;var t=e[Symbol.toPrimitive];if(void 0!==t){var o=t.call(e,r||"default");if("object"!=typeof o)return o;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===r?String:Number)(e)}(e,"string");return"symbol"==typeof r?r:String(r)}function u(e,r){(null==r||r>e.length)&&(r=e.length);for(var t=0,o=new Array(r);t<r;t++)o[t]=e[t];return o}let f=function(e,r,t,o){var i=n();if(o)for(var d=0;d<o.length;d++)i=o[d](i);var p=r((function(e){i.initializeInstanceElements(e,u.elements)}),t),u=i.decorateClass(function(e){for(var r=[],t=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},o=0;o<e.length;o++){var i,n=e[o];if("method"===n.kind&&(i=r.find(t)))if(c(n.descriptor)||c(i.descriptor)){if(s(n)||s(i))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");i.descriptor=n.descriptor}else{if(s(n)){if(s(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");i.decorators=n.decorators}l(n,i)}else r.push(n)}return r}(p.d.map(a)),e);return i.initializeClassElements(p.F,u.elements),i.runClassFinishers(p.F,u.finishers)}([(0,i.Mo)("ha-svg-icon")],(function(e,r){return{F:class extends r{constructor(...r){super(...r),e(this)}},d:[{kind:"field",decorators:[(0,i.Cb)()],key:"path",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"viewBox",value:void 0},{kind:"method",key:"render",value:function(){return o.YP`
    <svg
      viewBox=${this.viewBox||"0 0 24 24"}
      preserveAspectRatio="xMidYMid meet"
      focusable="false">
      <g>
      ${this.path?o.YP`<path d=${this.path}></path>`:""}
      </g>
    </svg>`}},{kind:"get",static:!0,key:"styles",value:function(){return o.iv`
      :host {
        display: var(--ha-icon-display, inline-flex);
        align-items: center;
        justify-content: center;
        position: relative;
        vertical-align: middle;
        fill: currentcolor;
        width: var(--mdc-icon-size, 24px);
        height: var(--mdc-icon-size, 24px);
      }
      svg {
        width: 100%;
        height: 100%;
        pointer-events: none;
        display: block;
      }
    `}}]}}),o.oi)},24841:(e,r,t)=>{"use strict";t.r(r),t.d(r,{HaDialogAisgalery:()=>v});t(30879),t(10983),t(53918),t(12730),t(28417);var o=t(34821),i=t(50424),n=t(55358),a=t(11654);t(59005);function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,r){["method","field"].forEach((function(t){r.forEach((function(r){r.kind===t&&"own"===r.placement&&this.defineClassElement(e,r)}),this)}),this)},initializeClassElements:function(e,r){var t=e.prototype;["method","field"].forEach((function(o){r.forEach((function(r){var i=r.placement;if(r.kind===o&&("static"===i||"prototype"===i)){var n="static"===i?e:t;this.defineClassElement(n,r)}}),this)}),this)},defineClassElement:function(e,r){var t=r.descriptor;if("field"===r.kind){var o=r.initializer;t={enumerable:t.enumerable,writable:t.writable,configurable:t.configurable,value:void 0===o?void 0:o.call(e)}}Object.defineProperty(e,r.key,t)},decorateClass:function(e,r){var t=[],o=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!d(e))return t.push(e);var r=this.decorateElement(e,i);t.push(r.element),t.push.apply(t,r.extras),o.push.apply(o,r.finishers)}),this),!r)return{elements:t,finishers:o};var n=this.decorateConstructor(t,r);return o.push.apply(o,n.finishers),n.finishers=o,n},addElementPlacement:function(e,r,t){var o=r[e.placement];if(!t&&-1!==o.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");o.push(e.key)},decorateElement:function(e,r){for(var t=[],o=[],i=e.decorators,n=i.length-1;n>=0;n--){var a=r[e.placement];a.splice(a.indexOf(e.key),1);var l=this.fromElementDescriptor(e),s=this.toElementFinisherExtras((0,i[n])(l)||l);e=s.element,this.addElementPlacement(e,r),s.finisher&&o.push(s.finisher);var c=s.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],r);t.push.apply(t,c)}}return{element:e,finishers:o,extras:t}},decorateConstructor:function(e,r){for(var t=[],o=r.length-1;o>=0;o--){var i=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,r[o])(i)||i);if(void 0!==n.finisher&&t.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var l=a+1;l<e.length;l++)if(e[a].key===e[l].key&&e[a].placement===e[l].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:t}},fromElementDescriptor:function(e){var r={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(r,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(r.initializer=e.initializer),r},toElementDescriptors:function(e){var r;if(void 0!==e)return(r=e,function(e){if(Array.isArray(e))return e}(r)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(r)||function(e,r){if(e){if("string"==typeof e)return h(e,r);var t=Object.prototype.toString.call(e).slice(8,-1);return"Object"===t&&e.constructor&&(t=e.constructor.name),"Map"===t||"Set"===t?Array.from(e):"Arguments"===t||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t)?h(e,r):void 0}}(r)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var r=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),r}),this)},toElementDescriptor:function(e){var r=String(e.kind);if("method"!==r&&"field"!==r)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+r+'"');var t=f(e.key),o=String(e.placement);if("static"!==o&&"prototype"!==o&&"own"!==o)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+o+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:r,key:t,placement:o,descriptor:Object.assign({},i)};return"field"!==r?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:u(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var r={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(r,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),r},toClassDescriptor:function(e){var r=String(e.kind);if("class"!==r)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+r+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var t=u(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:t}},runClassFinishers:function(e,r){for(var t=0;t<r.length;t++){var o=(0,r[t])(e);if(void 0!==o){if("function"!=typeof o)throw new TypeError("Finishers must return a constructor.");e=o}}return e},disallowProperty:function(e,r,t){if(void 0!==e[r])throw new TypeError(t+" can't have a ."+r+" property.")}};return e}function s(e){var r,t=f(e.key);"method"===e.kind?r={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?r={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?r={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(r={configurable:!0,writable:!0,enumerable:!0});var o={kind:"field"===e.kind?"field":"method",key:t,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:r};return e.decorators&&(o.decorators=e.decorators),"field"===e.kind&&(o.initializer=e.value),o}function c(e,r){void 0!==e.descriptor.get?r.descriptor.get=e.descriptor.get:r.descriptor.set=e.descriptor.set}function d(e){return e.decorators&&e.decorators.length}function p(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function u(e,r){var t=e[r];if(void 0!==t&&"function"!=typeof t)throw new TypeError("Expected '"+r+"' to be a function");return t}function f(e){var r=function(e,r){if("object"!=typeof e||null===e)return e;var t=e[Symbol.toPrimitive];if(void 0!==t){var o=t.call(e,r||"default");if("object"!=typeof o)return o;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===r?String:Number)(e)}(e,"string");return"symbol"==typeof r?r:String(r)}function h(e,r){(null==r||r>e.length)&&(r=e.length);for(var t=0,o=new Array(r);t<r;t++)o[t]=e[t];return o}const m={round:!1,type:"image/jpeg",quality:.75,aspectRatio:NaN};let v=function(e,r,t,o){var i=l();if(o)for(var n=0;n<o.length;n++)i=o[n](i);var a=r((function(e){i.initializeInstanceElements(e,u.elements)}),t),u=i.decorateClass(function(e){for(var r=[],t=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},o=0;o<e.length;o++){var i,n=e[o];if("method"===n.kind&&(i=r.find(t)))if(p(n.descriptor)||p(i.descriptor)){if(d(n)||d(i))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");i.descriptor=n.descriptor}else{if(d(n)){if(d(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");i.decorators=n.decorators}c(n,i)}else r.push(n)}return r}(a.d.map(s)),e);return i.initializeClassElements(a.F,u.elements),i.runClassFinishers(a.F,u.finishers)}(null,(function(e,r){return{F:class extends r{constructor(...r){super(...r),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"_params",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"_picture",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"_picture_last_value",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"_submitting",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)()],key:"_closeDialog",value:()=>!1},{kind:"method",key:"showDialog",value:async function(e){this._params=e,this._error=void 0,this._picture=null,this._name="",this._closeDialog=!1}},{kind:"method",key:"render",value:function(){if(this._closeDialog)return i.dy``;const e=""===this._name.trim(),r=null==this._picture;return i.dy`
      <ha-dialog
        open
        @closed=${this._close}
        scrimClickAction
        escapeKeyAction
        .heading=${(0,o.i)(this.hass,"Nowe zdjęcie")}     
      >
      <div>
          ${this._error?i.dy` <div class="error">${this._error}</div> `:""}
          <div class="form">
            <paper-input
                dialogInitialFocus
                .value=${this._name}
                @value-changed=${this._nameChanged}
                label="Nazwa"
                error-message="Nazwa jest wymagana"
                required
                auto-validate
              ></paper-input>
            <ha-picture-upload
                  .hass=${this.hass}
                  .value=${this._picture}
                  crop
                  .cropOptions=${m}
                  required
                  auto-validate
                  error-message="Zdjęcie jest wymagane"
                  @change=${this._pictureChanged}
                ></ha-picture-upload>
          </div>
      </div>
        <mwc-button
            slot="primaryAction"
            @click="${this._addPicture}"
            .disabled=${e||r||this._submitting}
          > Dodaj
          </mwc-button>
        </ha-dialog>
      </ha-dialog>
    `}},{kind:"method",key:"_pictureChanged",value:function(e){this._error=void 0,this._picture=e.target.value,""===this._name.trim()&&(this._name=e.target.fileName||"",this._name=this._name.split(".")[0]),null==this._picture?this._deletePicture():this._picture_last_value=this._picture}},{kind:"method",key:"_deletePicture",value:async function(){this._picture_last_value&&await this.hass.callService("ais_files","remove_file",{path:this._picture_last_value})}},{kind:"method",key:"_savePicture",value:async function(){var e;await this.hass.callService("ais_files","transfer_file",{path:this._picture_last_value,name:this._name}),this._picture_last_value=null,null===(e=this._params)||void 0===e||e.jsCallback()}},{kind:"method",key:"_nameChanged",value:function(e){this._error=void 0,this._name=e.detail.value}},{kind:"method",key:"_addPicture",value:async function(){this._submitting=!0;try{this._savePicture(),this._closeDialog=!0}catch(e){this._error=e?e.message:"Unknown error"}finally{this._submitting=!1}}},{kind:"method",key:"_close",value:function(){this._closeDialog=!0,this._deletePicture()}},{kind:"get",static:!0,key:"styles",value:function(){return[a.yu,i.iv`
        .form {
          padding-bottom: 24px;
        }
        ha-picture-upload {
          display: block;
        }
        ha-user-picker {
          margin-top: 16px;
        }
        a {
          color: var(--primary-color);
        }
        p {
          color: var(--primary-text-color);
        }
      `]}}]}}),i.oi);customElements.define("ha-dialog-aisgalery",v)},11654:(e,r,t)=>{"use strict";t.d(r,{_l:()=>i,q0:()=>n,k1:()=>a,Qx:()=>l,yu:()=>s,$c:()=>c});var o=t(50424);const i={"primary-background-color":"#111111","card-background-color":"#1c1c1c","secondary-background-color":"#202020","primary-text-color":"#e1e1e1","secondary-text-color":"#9b9b9b","disabled-text-color":"#6f6f6f","app-header-text-color":"#e1e1e1","app-header-background-color":"#101e24","switch-unchecked-button-color":"#999999","switch-unchecked-track-color":"#9b9b9b","divider-color":"rgba(225, 225, 225, .12)","mdc-ripple-color":"#AAAAAA","codemirror-keyword":"#C792EA","codemirror-operator":"#89DDFF","codemirror-variable":"#f07178","codemirror-variable-2":"#EEFFFF","codemirror-variable-3":"#DECB6B","codemirror-builtin":"#FFCB6B","codemirror-atom":"#F78C6C","codemirror-number":"#FF5370","codemirror-def":"#82AAFF","codemirror-string":"#C3E88D","codemirror-string-2":"#f07178","codemirror-comment":"#545454","codemirror-tag":"#FF5370","codemirror-meta":"#FFCB6B","codemirror-attribute":"#C792EA","codemirror-property":"#C792EA","codemirror-qualifier":"#DECB6B","codemirror-type":"#DECB6B","energy-grid-return-color":"#b39bdb"},n={"state-icon-error-color":"var(--error-state-color, var(--error-color))","state-unavailable-color":"var(--state-icon-unavailable-color, var(--disabled-text-color))","sidebar-text-color":"var(--primary-text-color)","sidebar-background-color":"var(--card-background-color)","sidebar-selected-text-color":"var(--primary-color)","sidebar-selected-icon-color":"var(--primary-color)","sidebar-icon-color":"rgba(var(--rgb-primary-text-color), 0.6)","switch-checked-color":"var(--primary-color)","switch-checked-button-color":"var(--switch-checked-color, var(--primary-background-color))","switch-checked-track-color":"var(--switch-checked-color, #000000)","switch-unchecked-button-color":"var(--switch-unchecked-color, var(--primary-background-color))","switch-unchecked-track-color":"var(--switch-unchecked-color, #000000)","slider-color":"var(--primary-color)","slider-secondary-color":"var(--light-primary-color)","slider-bar-color":"var(--disabled-text-color)","label-badge-grey":"var(--paper-grey-500)","label-badge-background-color":"var(--card-background-color)","label-badge-text-color":"rgba(var(--rgb-primary-text-color), 0.8)","paper-listbox-background-color":"var(--card-background-color)","paper-item-icon-color":"var(--state-icon-color)","paper-item-icon-active-color":"var(--state-icon-active-color)","table-row-background-color":"var(--primary-background-color)","table-row-alternative-background-color":"var(--secondary-background-color)","paper-slider-knob-color":"var(--slider-color)","paper-slider-knob-start-color":"var(--slider-color)","paper-slider-pin-color":"var(--slider-color)","paper-slider-pin-start-color":"var(--slider-color)","paper-slider-active-color":"var(--slider-color)","paper-slider-secondary-color":"var(--slider-secondary-color)","paper-slider-container-color":"var(--slider-bar-color)","data-table-background-color":"var(--card-background-color)","markdown-code-background-color":"var(--primary-background-color)","mdc-theme-primary":"var(--primary-color)","mdc-theme-secondary":"var(--accent-color)","mdc-theme-background":"var(--primary-background-color)","mdc-theme-surface":"var(--card-background-color)","mdc-theme-on-primary":"var(--text-primary-color)","mdc-theme-on-secondary":"var(--text-primary-color)","mdc-theme-on-surface":"var(--primary-text-color)","mdc-theme-text-disabled-on-light":"var(--disabled-text-color)","mdc-theme-text-primary-on-background":"var(--primary-text-color)","mdc-theme-text-secondary-on-background":"var(--secondary-text-color)","mdc-theme-text-icon-on-background":"var(--secondary-text-color)","app-header-text-color":"var(--text-primary-color)","app-header-background-color":"var(--primary-color)","mdc-checkbox-unchecked-color":"rgba(var(--rgb-primary-text-color), 0.54)","mdc-checkbox-disabled-color":"var(--disabled-text-color)","mdc-radio-unchecked-color":"rgba(var(--rgb-primary-text-color), 0.54)","mdc-radio-disabled-color":"var(--disabled-text-color)","mdc-tab-text-label-color-default":"var(--primary-text-color)","mdc-button-disabled-ink-color":"var(--disabled-text-color)","mdc-button-outline-color":"var(--divider-color)","mdc-dialog-scroll-divider-color":"var(--divider-color)","chip-background-color":"rgba(var(--rgb-primary-text-color), 0.15)","material-body-text-color":"var(--primary-text-color)","material-background-color":"var(--card-background-color)","material-secondary-background-color":"var(--secondary-background-color)","material-secondary-text-color":"var(--secondary-text-color)"},a=o.iv`
  button.link {
    background: none;
    color: inherit;
    border: none;
    padding: 0;
    font: inherit;
    text-align: left;
    text-decoration: underline;
    cursor: pointer;
  }
`,l=o.iv`
  :host {
    font-family: var(--paper-font-body1_-_font-family);
    -webkit-font-smoothing: var(--paper-font-body1_-_-webkit-font-smoothing);
    font-size: var(--paper-font-body1_-_font-size);
    font-weight: var(--paper-font-body1_-_font-weight);
    line-height: var(--paper-font-body1_-_line-height);
  }

  app-header-layout,
  ha-app-layout {
    background-color: var(--primary-background-color);
  }

  app-header,
  app-toolbar {
    background-color: var(--app-header-background-color);
    font-weight: 400;
    color: var(--app-header-text-color, white);
  }

  app-toolbar {
    height: var(--header-height);
  }

  app-header div[sticky] {
    height: 48px;
  }

  app-toolbar [main-title] {
    margin-left: 20px;
  }

  h1 {
    font-family: var(--paper-font-headline_-_font-family);
    -webkit-font-smoothing: var(--paper-font-headline_-_-webkit-font-smoothing);
    white-space: var(--paper-font-headline_-_white-space);
    overflow: var(--paper-font-headline_-_overflow);
    text-overflow: var(--paper-font-headline_-_text-overflow);
    font-size: var(--paper-font-headline_-_font-size);
    font-weight: var(--paper-font-headline_-_font-weight);
    line-height: var(--paper-font-headline_-_line-height);
  }

  h2 {
    font-family: var(--paper-font-title_-_font-family);
    -webkit-font-smoothing: var(--paper-font-title_-_-webkit-font-smoothing);
    white-space: var(--paper-font-title_-_white-space);
    overflow: var(--paper-font-title_-_overflow);
    text-overflow: var(--paper-font-title_-_text-overflow);
    font-size: var(--paper-font-title_-_font-size);
    font-weight: var(--paper-font-title_-_font-weight);
    line-height: var(--paper-font-title_-_line-height);
  }

  h3 {
    font-family: var(--paper-font-subhead_-_font-family);
    -webkit-font-smoothing: var(--paper-font-subhead_-_-webkit-font-smoothing);
    white-space: var(--paper-font-subhead_-_white-space);
    overflow: var(--paper-font-subhead_-_overflow);
    text-overflow: var(--paper-font-subhead_-_text-overflow);
    font-size: var(--paper-font-subhead_-_font-size);
    font-weight: var(--paper-font-subhead_-_font-weight);
    line-height: var(--paper-font-subhead_-_line-height);
  }

  a {
    color: var(--primary-color);
  }

  .secondary {
    color: var(--secondary-text-color);
  }

  .error {
    color: var(--error-color);
  }

  .warning {
    color: var(--error-color);
  }

  mwc-button.warning {
    --mdc-theme-primary: var(--error-color);
  }

  ${a}

  .card-actions a {
    text-decoration: none;
  }

  .card-actions .warning {
    --mdc-theme-primary: var(--error-color);
  }

  .layout.horizontal,
  .layout.vertical {
    display: flex;
  }
  .layout.inline {
    display: inline-flex;
  }
  .layout.horizontal {
    flex-direction: row;
  }
  .layout.vertical {
    flex-direction: column;
  }
  .layout.wrap {
    flex-wrap: wrap;
  }
  .layout.no-wrap {
    flex-wrap: nowrap;
  }
  .layout.center,
  .layout.center-center {
    align-items: center;
  }
  .layout.bottom {
    align-items: flex-end;
  }
  .layout.center-justified,
  .layout.center-center {
    justify-content: center;
  }
  .flex {
    flex: 1;
    flex-basis: 0.000000001px;
  }
  .flex-auto {
    flex: 1 1 auto;
  }
  .flex-none {
    flex: none;
  }
  .layout.justified {
    justify-content: space-between;
  }
`,s=o.iv`
  /* prevent clipping of positioned elements */
  paper-dialog-scrollable {
    --paper-dialog-scrollable: {
      -webkit-overflow-scrolling: auto;
    }
  }

  /* force smooth scrolling for iOS 10 */
  paper-dialog-scrollable.can-scroll {
    --paper-dialog-scrollable: {
      -webkit-overflow-scrolling: touch;
    }
  }

  .paper-dialog-buttons {
    align-items: flex-end;
    padding: 8px;
    padding-bottom: max(env(safe-area-inset-bottom), 8px);
  }

  @media all and (min-width: 450px) and (min-height: 500px) {
    ha-paper-dialog {
      min-width: 400px;
    }
  }

  @media all and (max-width: 450px), all and (max-height: 500px) {
    paper-dialog,
    ha-paper-dialog {
      margin: 0;
      width: calc(
        100% - env(safe-area-inset-right) - env(safe-area-inset-left)
      ) !important;
      min-width: calc(
        100% - env(safe-area-inset-right) - env(safe-area-inset-left)
      ) !important;
      max-width: calc(
        100% - env(safe-area-inset-right) - env(safe-area-inset-left)
      ) !important;
      max-height: calc(100% - var(--header-height));

      position: fixed !important;
      bottom: 0px;
      left: env(safe-area-inset-left);
      right: env(safe-area-inset-right);
      overflow: scroll;
      border-bottom-left-radius: 0px;
      border-bottom-right-radius: 0px;
    }
  }

  /* mwc-dialog (ha-dialog) styles */
  ha-dialog {
    --mdc-dialog-min-width: 400px;
    --mdc-dialog-max-width: 600px;
    --mdc-dialog-heading-ink-color: var(--primary-text-color);
    --mdc-dialog-content-ink-color: var(--primary-text-color);
    --justify-action-buttons: space-between;
  }

  ha-dialog .form {
    padding-bottom: 24px;
    color: var(--primary-text-color);
  }

  a {
    color: var(--primary-color);
  }

  /* make dialog fullscreen on small screens */
  @media all and (max-width: 450px), all and (max-height: 500px) {
    ha-dialog {
      --mdc-dialog-min-width: calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );
      --mdc-dialog-max-width: calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );
      --mdc-dialog-min-height: 100%;
      --mdc-dialog-max-height: 100%;
      --mdc-shape-medium: 0px;
      --vertial-align-dialog: flex-end;
    }
  }
  mwc-button.warning {
    --mdc-theme-primary: var(--error-color);
  }
  .error {
    color: var(--error-color);
  }
`,c=o.iv`
  .ha-scrollbar::-webkit-scrollbar {
    width: 0.4rem;
    height: 0.4rem;
  }

  .ha-scrollbar::-webkit-scrollbar-thumb {
    -webkit-border-radius: 4px;
    border-radius: 4px;
    background: var(--scrollbar-thumb-color);
  }

  .ha-scrollbar {
    overflow-y: auto;
    scrollbar-color: var(--scrollbar-thumb-color) transparent;
    scrollbar-width: thin;
  }
`;o.iv`
  body {
    background-color: var(--primary-background-color);
    color: var(--primary-text-color);
    height: calc(100vh - 32px);
    width: 100vw;
  }
`}}]);
//# sourceMappingURL=491c7376.js.map