(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[56668],{47181:(e,t,r)=>{"use strict";r.d(t,{B:()=>i});const i=(e,t,r,i)=>{i=i||{},r=null==r?{}:r;const o=new Event(t,{bubbles:void 0===i.bubbles||i.bubbles,cancelable:Boolean(i.cancelable),composed:void 0===i.composed||i.composed});return o.detail=r,e.dispatchEvent(o),o}},87744:(e,t,r)=>{"use strict";function i(e){const t=e.language||"en";return e.translationMetadata.translations[t]&&e.translationMetadata.translations[t].isRTL||!1}function o(e){return n(i(e))}function n(e){return e?"rtl":"ltr"}r.d(t,{HE:()=>i,Zu:()=>o,$3:()=>n})},96151:(e,t,r)=>{"use strict";r.d(t,{T:()=>i,y:()=>o});const i=e=>{requestAnimationFrame((()=>setTimeout(e,0)))},o=()=>new Promise((e=>{i(e)}))},53822:(e,t,r)=>{"use strict";var i=r(50424),o=r(55358),n=r(47181);let a;function s(){s=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!c(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);r.push.apply(r,d)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return f(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?f(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=u(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function l(e){var t,r=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function p(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function f(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function m(e,t,r){return(m="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=v(e)););return e}(e,t);if(i){var o=Object.getOwnPropertyDescriptor(i,t);return o.get?o.get.call(r):o.value}})(e,t,r||e)}function v(e){return(v=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const y={key:"Mod-s",run:e=>((0,n.B)(e.dom,"editor-save"),!0)};!function(e,t,r,i){var o=s();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var a=t((function(e){o.initializeInstanceElements(e,h.elements)}),r),h=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(p(n.descriptor)||p(o.descriptor)){if(c(n)||c(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(c(n)){if(c(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}d(n,o)}else t.push(n)}return t}(a.d.map(l)),e);o.initializeClassElements(a.F,h.elements),o.runClassFinishers(a.F,h.finishers)}([(0,o.Mo)("ha-code-editor")],(function(e,t){class s extends t{constructor(...t){super(...t),e(this)}}return{F:s,d:[{kind:"field",key:"codemirror",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"mode",value:()=>"yaml"},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"autofocus",value:()=>!1},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"readOnly",value:()=>!1},{kind:"field",decorators:[(0,o.Cb)()],key:"error",value:()=>!1},{kind:"field",decorators:[(0,o.SB)()],key:"_value",value:()=>""},{kind:"field",key:"_loadedCodeMirror",value:void 0},{kind:"set",key:"value",value:function(e){this._value=e}},{kind:"get",key:"value",value:function(){return this.codemirror?this.codemirror.state.doc.toString():this._value}},{kind:"get",key:"hasComments",value:function(){if(!this.codemirror||!this._loadedCodeMirror)return!1;const e=this._loadedCodeMirror.HighlightStyle.get(this.codemirror.state,this._loadedCodeMirror.tags.comment);return!!this.shadowRoot.querySelector(`span.${e}`)}},{kind:"method",key:"connectedCallback",value:function(){m(v(s.prototype),"connectedCallback",this).call(this),this.codemirror&&!1!==this.autofocus&&this.codemirror.focus()}},{kind:"method",key:"update",value:function(e){m(v(s.prototype),"update",this).call(this,e),this.codemirror&&(e.has("mode")&&this.codemirror.dispatch({effects:this._loadedCodeMirror.langCompartment.reconfigure(this._mode)}),e.has("readOnly")&&this.codemirror.dispatch({effects:this._loadedCodeMirror.readonlyCompartment.reconfigure(this._loadedCodeMirror.EditorView.editable.of(!this.readOnly))}),e.has("_value")&&this._value!==this.value&&this.codemirror.dispatch({changes:{from:0,to:this.codemirror.state.doc.length,insert:this._value}}),e.has("error")&&this.classList.toggle("error-state",this.error))}},{kind:"method",key:"firstUpdated",value:function(e){m(v(s.prototype),"firstUpdated",this).call(this,e),this._blockKeyboardShortcuts(),this._load()}},{kind:"get",key:"_mode",value:function(){return this._loadedCodeMirror.langs[this.mode]}},{kind:"method",key:"_load",value:async function(){this._loadedCodeMirror=await(async()=>(a||(a=Promise.all([r.e(62118),r.e(39649),r.e(92914)]).then(r.bind(r,92914))),a))(),this.codemirror=new this._loadedCodeMirror.EditorView({state:this._loadedCodeMirror.EditorState.create({doc:this._value,extensions:[this._loadedCodeMirror.lineNumbers(),this._loadedCodeMirror.EditorState.allowMultipleSelections.of(!0),this._loadedCodeMirror.history(),this._loadedCodeMirror.highlightSelectionMatches(),this._loadedCodeMirror.highlightActiveLine(),this._loadedCodeMirror.drawSelection(),this._loadedCodeMirror.rectangularSelection(),this._loadedCodeMirror.keymap.of([...this._loadedCodeMirror.defaultKeymap,...this._loadedCodeMirror.searchKeymap,...this._loadedCodeMirror.historyKeymap,...this._loadedCodeMirror.tabKeyBindings,y]),this._loadedCodeMirror.langCompartment.of(this._mode),this._loadedCodeMirror.theme,this._loadedCodeMirror.Prec.fallback(this._loadedCodeMirror.highlightStyle),this._loadedCodeMirror.readonlyCompartment.of(this._loadedCodeMirror.EditorView.editable.of(!this.readOnly)),this._loadedCodeMirror.EditorView.updateListener.of((e=>this._onUpdate(e)))]}),root:this.shadowRoot,parent:this.shadowRoot})}},{kind:"method",key:"_blockKeyboardShortcuts",value:function(){this.addEventListener("keydown",(e=>e.stopPropagation()))}},{kind:"method",key:"_onUpdate",value:function(e){if(!e.docChanged)return;const t=this.value;t!==this._value&&(this._value=t,(0,n.B)(this,"value-changed",{value:this._value}))}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      :host(.error-state) div.cm-wrap .cm-gutters {
        border-color: var(--error-state-color, red);
      }
    `}}]}}),i.fl)},34821:(e,t,r)=>{"use strict";r.d(t,{i:()=>y});var i=r(29907),o=r(50424),n=r(55358),a=r(87744);r(10983);function s(){s=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!c(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);r.push.apply(r,d)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return f(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?f(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=u(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function l(e){var t,r=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function c(e){return e.decorators&&e.decorators.length}function p(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function f(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function m(e,t,r){return(m="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=v(e)););return e}(e,t);if(i){var o=Object.getOwnPropertyDescriptor(i,t);return o.get?o.get.call(r):o.value}})(e,t,r||e)}function v(e){return(v=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const y=(e,t)=>o.dy`
  <span class="header_title">${t}</span>
  <mwc-icon-button
    aria-label=${e.localize("ui.dialogs.generic.close")}
    dialogAction="close"
    class="header_button"
    dir=${(0,a.Zu)(e)}
  >
    <ha-svg-icon .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}></ha-svg-icon>
  </mwc-icon-button>
`;!function(e,t,r,i){var o=s();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var a=t((function(e){o.initializeInstanceElements(e,h.elements)}),r),h=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(p(n.descriptor)||p(o.descriptor)){if(c(n)||c(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(c(n)){if(c(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}d(n,o)}else t.push(n)}return t}(a.d.map(l)),e);o.initializeClassElements(a.F,h.elements),o.runClassFinishers(a.F,h.finishers)}([(0,n.Mo)("ha-dialog")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"method",key:"scrollToPos",value:function(e,t){this.contentElement.scrollTo(e,t)}},{kind:"method",key:"renderHeading",value:function(){return o.dy`<slot name="heading"> ${m(v(r.prototype),"renderHeading",this).call(this)} </slot>`}},{kind:"get",static:!0,key:"styles",value:function(){return[i.V.styles,o.iv`
        .mdc-dialog {
          --mdc-dialog-scroll-divider-color: var(--divider-color);
          z-index: var(--dialog-z-index, 7);
          backdrop-filter: var(--dialog-backdrop-filter, none);
        }
        .mdc-dialog__actions {
          justify-content: var(--justify-action-buttons, flex-end);
          padding-bottom: max(env(safe-area-inset-bottom), 8px);
        }
        .mdc-dialog__container {
          align-items: var(--vertial-align-dialog, center);
        }
        .mdc-dialog__title::before {
          display: block;
          height: 20px;
        }
        .mdc-dialog .mdc-dialog__content {
          position: var(--dialog-content-position, relative);
          padding: var(--dialog-content-padding, 20px 24px);
        }
        :host([hideactions]) .mdc-dialog .mdc-dialog__content {
          padding-bottom: max(
            var(--dialog-content-padding, 20px),
            env(safe-area-inset-bottom)
          );
        }
        .mdc-dialog .mdc-dialog__surface {
          position: var(--dialog-surface-position, relative);
          top: var(--dialog-surface-top);
          min-height: var(--mdc-dialog-min-height, auto);
        }
        :host([flexContent]) .mdc-dialog .mdc-dialog__content {
          display: flex;
          flex-direction: column;
        }
        .header_button {
          position: absolute;
          right: 16px;
          top: 10px;
          text-decoration: none;
          color: inherit;
        }
        .header_title {
          margin-right: 40px;
        }
        [dir="rtl"].header_button {
          right: auto;
          left: 16px;
        }
        [dir="rtl"].header_title {
          margin-left: 40px;
          margin-right: 0px;
        }
      `]}}]}}),i.V)},10983:(e,t,r)=>{"use strict";r(25230);var i=r(50424),o=r(55358);r(16509);function n(){n=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!l(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);r.push.apply(r,d)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=p(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:c(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=c(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function a(e){var t,r=p(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function s(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function l(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function c(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function p(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var o=n();if(i)for(var c=0;c<i.length;c++)o=i[c](o);var p=t((function(e){o.initializeInstanceElements(e,h.elements)}),r),h=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(d(n.descriptor)||d(o.descriptor)){if(l(n)||l(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(l(n)){if(l(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}s(n,o)}else t.push(n)}return t}(p.d.map(a)),e);o.initializeClassElements(p.F,h.elements),o.runClassFinishers(p.F,h.finishers)}([(0,o.Mo)("ha-icon-button")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,o.Cb)({type:String})],key:"icon",value:()=>""},{kind:"field",decorators:[(0,o.Cb)({type:String})],key:"label",value:()=>""},{kind:"field",static:!0,key:"shadowRootOptions",value:()=>({mode:"open",delegatesFocus:!0})},{kind:"method",key:"render",value:function(){return i.dy`
      <mwc-icon-button .label=${this.label} .disabled=${this.disabled}>
        <ha-icon .icon=${this.icon}></ha-icon>
      </mwc-icon-button>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      :host {
        display: inline-block;
        outline: none;
      }
      :host([disabled]) {
        pointer-events: none;
      }
      mwc-icon-button {
        --mdc-theme-on-primary: currentColor;
        --mdc-theme-text-disabled-on-light: var(--disabled-text-color);
      }
      ha-icon {
        --ha-icon-display: inline;
      }
    `}}]}}),i.oi)},81303:(e,t,r)=>{"use strict";r(8878);const i=customElements.get("paper-dropdown-menu");customElements.define("ha-paper-dropdown-menu",class extends i{ready(){super.ready(),setTimeout((()=>{"rtl"===window.getComputedStyle(this).direction&&(this.style.textAlign="right")}),100)}})},15327:(e,t,r)=>{"use strict";r.d(t,{eL:()=>i,SN:()=>o,id:()=>n,fg:()=>a,j2:()=>s,JR:()=>l,Y:()=>d,iM:()=>c,Q2:()=>p,Oh:()=>h,vj:()=>u,Gc:()=>f});const i=e=>e.sendMessagePromise({type:"lovelace/resources"}),o=(e,t)=>e.callWS({type:"lovelace/resources/create",...t}),n=(e,t,r)=>e.callWS({type:"lovelace/resources/update",resource_id:t,...r}),a=(e,t)=>e.callWS({type:"lovelace/resources/delete",resource_id:t}),s=e=>e.callWS({type:"lovelace/dashboards/list"}),l=(e,t)=>e.callWS({type:"lovelace/dashboards/create",...t}),d=(e,t,r)=>e.callWS({type:"lovelace/dashboards/update",dashboard_id:t,...r}),c=(e,t)=>e.callWS({type:"lovelace/dashboards/delete",dashboard_id:t}),p=(e,t,r)=>e.sendMessagePromise({type:"lovelace/config",url_path:t,force:r}),h=(e,t,r)=>e.callWS({type:"lovelace/config/save",url_path:t,config:r}),u=(e,t)=>e.callWS({type:"lovelace/config/delete",url_path:t}),f=(e,t,r)=>e.subscribeEvents((e=>{e.data.url_path===t&&r()}),"lovelace_updated")},96491:(e,t,r)=>{"use strict";r.d(t,{$:()=>s});var i=r(15327),o=r(26765),n=r(47512),a=r(4398);const s=async(e,t,r,s)=>{var l,d,c;const p=await(0,i.j2)(t),h=p.filter((e=>"storage"===e.mode)),u=null===(l=t.panels.lovelace)||void 0===l||null===(d=l.config)||void 0===d?void 0:d.mode;if("storage"!==u&&!h.length)return void(0,n.f)(e,{entities:r,yaml:!0});let f,m=null;if("storage"===u)try{f=await(0,i.Q2)(t.connection,null,!1)}catch(e){}if(!f&&h.length)for(const e of h)try{f=await(0,i.Q2)(t.connection,e.url_path,!1),m=e.url_path;break}catch(e){}f?h.length||null!==(c=f.views)&&void 0!==c&&c.length?h.length||1!==f.views.length?(0,a.i)(e,{lovelaceConfig:f,urlPath:m,allowDashboardChange:!0,dashboards:p,viewSelectedCallback:(o,a,l)=>{(0,n.f)(e,{lovelaceConfig:a,saveConfig:async e=>{try{await(0,i.Oh)(t,o,e)}catch{alert(t.localize("ui.panel.config.devices.add_entities.saving_failed"))}},path:[l],entities:r,cardConfig:s})}}):(0,n.f)(e,{lovelaceConfig:f,saveConfig:async e=>{try{await(0,i.Oh)(t,null,e)}catch(e){alert(t.localize("ui.panel.config.devices.add_entities.saving_failed"))}},path:[0],entities:r,cardConfig:s}):(0,o.Ys)(e,{text:"You don't have any Lovelace views, first create a view in Lovelace."}):p.length>h.length?(0,n.f)(e,{entities:r,yaml:!0}):(0,o.Ys)(e,{text:"You don't seem to be in control of any dashboard, please take control first."})}},47512:(e,t,r)=>{"use strict";r.d(t,{f:()=>n});var i=r(47181);const o=()=>Promise.all([r.e(75009),r.e(98595),r.e(30486),r.e(76628),r.e(77377),r.e(61030),r.e(16729),r.e(72168),r.e(11518),r.e(97209),r.e(18900),r.e(47150),r.e(51995),r.e(23340),r.e(57529),r.e(13542),r.e(78147)]).then(r.bind(r,9444)),n=(e,t)=>{(0,i.B)(e,"show-dialog",{dialogTag:"hui-dialog-suggest-card",dialogImport:o,dialogParams:t})}},4398:(e,t,r)=>{"use strict";r.d(t,{i:()=>o});var i=r(47181);const o=(e,t)=>{(0,i.B)(e,"show-dialog",{dialogTag:"hui-dialog-select-view",dialogImport:()=>Promise.all([r.e(75009),r.e(78161),r.e(42955),r.e(29907),r.e(16729),r.e(72168),r.e(15163),r.e(9700)]).then(r.bind(r,9700)),dialogParams:t})}},85494:(e,t,r)=>{"use strict";r.r(t),r.d(t,{HuiDialogWebBrowserAisEditImage:()=>y});var i=r(50424),o=r(55358),n=(r(51095),r(47181)),a=r(34821),s=(r(319),r(11654)),l=r(96491);r(53822),r(74535),r(81303);function d(){d=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!h(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);r.push.apply(r,d)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return v(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?v(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=m(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:f(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=f(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function c(e){var t,r=m(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function p(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function h(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function f(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function m(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function v(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}let y=function(e,t,r,i){var o=d();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var a=t((function(e){o.initializeInstanceElements(e,s.elements)}),r),s=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(u(n.descriptor)||u(o.descriptor)){if(h(n)||h(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(h(n)){if(h(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}p(n,o)}else t.push(n)}return t}(a.d.map(c)),e);return o.initializeClassElements(a.F,s.elements),o.runClassFinishers(a.F,s.finishers)}([(0,o.Mo)("hui-dialog-web-browser-ais-edit-image")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"codeValue",value:()=>""},{kind:"field",decorators:[(0,o.Cb)()],key:"selectedElementType",value:()=>""},{kind:"field",decorators:[(0,o.Cb)()],key:"selectedEntityId",value:()=>""},{kind:"field",decorators:[(0,o.Cb)()],key:"pictureElements",value:()=>[]},{kind:"field",decorators:[(0,o.Cb)()],key:"dragCurrentItemIndex",value:()=>-1},{kind:"field",decorators:[(0,o.Cb)()],key:"dragItems",value:()=>[]},{kind:"field",decorators:[(0,o.Cb)()],key:"dragItemStyle",value:()=>""},{kind:"field",decorators:[(0,o.Cb)()],key:"dragActive",value:()=>!1},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"_params",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this.codeValue="type: picture-elements\nimage: '/local/img/${this._params.title}'\ntitle: ''\nelements: []",this.selectedElementType="",this.selectedEntityId="",this.pictureElements=[]}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,(0,n.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"_dragStart",value:function(e){isNaN(e.target.id)||void 0!==this.dragItems[e.target.id]&&(this.dragCurrentItemIndex=e.target.id,"touchstart"===e.type?(this.dragItems[this.dragCurrentItemIndex].initialX=e.touches[0].clientX-this.dragItems[this.dragCurrentItemIndex].offsetX,this.dragItems[this.dragCurrentItemIndex].initialY=e.touches[0].clientY-this.dragItems[this.dragCurrentItemIndex].offsetY):(this.dragItems[this.dragCurrentItemIndex].initialX=e.clientX-this.dragItems[this.dragCurrentItemIndex].offsetX,this.dragItems[this.dragCurrentItemIndex].initialY=e.clientY-this.dragItems[this.dragCurrentItemIndex].offsetY),this.dragActive=!0)}},{kind:"method",key:"_dragEnd",value:function(e){this.dragActive&&(this.dragItems[this.dragCurrentItemIndex].initialX=this.dragItems[this.dragCurrentItemIndex].currentX,this.dragItems[this.dragCurrentItemIndex].initialY=this.dragItems[this.dragCurrentItemIndex].currentY,this.dragActive=!1,this.pictureElements[this.dragCurrentItemIndex].style.transform=this.dragItemStyle,this._handleCodeChanged())}},{kind:"method",key:"_getDragStyle",value:function(e){return e===this.dragCurrentItemIndex?"transform: "+this.dragItemStyle:"transform: "+this.dragItems[e].style}},{kind:"method",key:"_drag",value:function(e){if(this.dragActive){let t,r;e.preventDefault(),"touchmove"===e.type?(t=e.touches[0].clientX-this.dragItems[this.dragCurrentItemIndex].initialX,r=e.touches[0].clientY-this.dragItems[this.dragCurrentItemIndex].initialY):(t=e.clientX-this.dragItems[this.dragCurrentItemIndex].initialX,r=e.clientY-this.dragItems[this.dragCurrentItemIndex].initialY),this.dragItemStyle="translate3d("+t+"px, "+r+"px, 0)",this.dragItems[this.dragCurrentItemIndex].currentX=t,this.dragItems[this.dragCurrentItemIndex].currentY=r,this.dragItems[this.dragCurrentItemIndex].offsetX=t,this.dragItems[this.dragCurrentItemIndex].offsetY=r,this.dragItems[this.dragCurrentItemIndex].style="translate3d("+t+"px, "+r+"px, 0)"}}},{kind:"method",key:"_handleAddElement",value:function(){const e={type:this.selectedElementType,entity:this.selectedEntityId,style:{position:"absolute",top:"50%",left:"50%",transform:""}};this.pictureElements.push(e);this.dragItems.push({currentX:0,currentY:0,initialX:0,initialY:0,offsetX:0,offsetY:0,style:""}),this.selectedEntityId="",this.selectedElementType="",this._handleCodeChanged()}},{kind:"method",key:"_handleSelectedElementTypeChanged",value:function(e){const t=e.detail.item.getAttribute("itemid");this.selectedElementType=t}},{kind:"method",key:"_handleSelectedEntityIdChanged",value:function(e){this.selectedEntityId=e.detail.value}},{kind:"method",key:"entityFilter",value:function(e){return!e.entity_id.includes(".ais")}},{kind:"method",key:"_handleCodeChanged",value:function(){this.codeValue="type: picture-elements\nimage: '/local/img/${this._params.title}'\ntitle: ''\nelements: [\n",this.pictureElements.forEach((e=>{this.codeValue+=JSON.stringify(e)+",\n"})),this.codeValue+="]"}},{kind:"method",key:"_addToLovelaceView",value:function(){var e;const t=null===(e=this._params)||void 0===e?void 0:e.sourceUrl.split("?authSig=")[0].replace("/media/galeria/"," /local/img/");(0,l.$)(this,this.hass,[],[{type:"picture-elements",title:"",image:t,elements:this.pictureElements}]),this.closeDialog()}},{kind:"method",key:"render",value:function(){return this._params&&this._params.sourceType&&this._params.sourceUrl?i.dy`
      <ha-dialog
        open
        hideActions
        .heading=${(0,a.i)(this.hass,"Konfiguracja karty elementy obrazu")}
        @closed=${this.closeDialog}
      >
        <div id="outerContainer">
          <div
            id="container"
            style="background-image: url(${this._params.sourceUrl});"
            @touchstart=${this._dragStart}
            @touchend=${this._dragEnd}
            @touchmove=${this._drag}
            @mousedown=${this._dragStart}
            @mouseup=${this._dragEnd}
            @mousemove=${this._drag}
          >
            ${this.pictureElements.map(((e,t)=>i.dy` <div
                .id=${t.toString()}
                class="pictureElementItem"
                .style=${this._getDragStyle(t)}
              >
                ${e.entity}
              </div>`))}
          </div>
        </div>
        <h3>Wybierz element do dodania</h3>
        <ha-paper-dropdown-menu dynamic-align label-float label="Typ">
          <paper-listbox
            slot="dropdown-content"
            attr-for-selected="itemId"
            .selected=${this.selectedElementType}
            @iron-select=${this._handleSelectedElementTypeChanged}
          >
            <paper-item itemid="state-badge">State Badge</paper-item>
            <paper-item itemid="state-icon">State Icon</paper-item>
            <paper-item itemid="state-label">State Label</paper-item>
          </paper-listbox>
        </ha-paper-dropdown-menu>
        <ha-entity-picker
          .hass=${this.hass}
          .value=${this.selectedEntityId}
          @value-changed=${this._handleSelectedEntityIdChanged}
          .configValue=${"entity"}
          .entityFilter=${this.entityFilter}
          allow-custom-entity
        ></ha-entity-picker>
        ${""!==this.selectedEntityId&&""!==this.selectedElementType?i.dy` <mwc-button @click=${this._handleAddElement}>
              <ha-svg-icon .path=${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}></ha-svg-icon>
              Dodaj element do obrazu
            </mwc-button>`:""}
        <br /><br />
        <ha-code-editor mode="yaml" .value=${this.codeValue}></ha-code-editor>
        <div class="card-actions">
          <mwc-button @click=${this._addToLovelaceView}>
            ${this.hass.localize("ui.panel.config.devices.entities.add_entities_lovelace")||"Dodaj do interfejsu użytkownika"}
          </mwc-button>
        </div>
      </ha-dialog>
    `:i.dy``}},{kind:"get",static:!0,key:"styles",value:function(){return[s.yu,i.iv`
        /* @media (min-width: 800px) {
          ha-dialog {
            --mdc-dialog-max-width: 800px;
            --mdc-dialog-min-width: 400px;
            width: 100%;
          }
        } */
        /* make dialog fullscreen */
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
        #outerContainer {
          height: 50vh;
        }
        #container {
          height: 50vh;
          width: 50vw;
          display: flex;
          align-items: center;
          justify-content: center;
          overflow: hidden;
          border-radius: 7px;
          touch-action: none;
          background-size: 50vw 50vh;
          background-repeat: no-repeat;
          background-position: center;
          margin: auto;
        }
        div.pictureElementItem {
          width: 80px;
          height: 80px;
          background-color: rgb(245, 230, 99);
          border: 10px solid rgba(136, 136, 136, 0.5);
          border-radius: 50%;
          touch-action: none;
          user-select: none;
          top: 50%;
          left: 50%;
        }
        div.pictureElementItem:active {
          background-color: rgba(168, 218, 220, 1);
        }
        div.pictureElementItem:hover {
          cursor: pointer;
          /* border-width: 20px; */
        }
      `]}}]}}),i.oi)},11654:(e,t,r)=>{"use strict";r.d(t,{_l:()=>o,q0:()=>n,k1:()=>a,Qx:()=>s,yu:()=>l,$c:()=>d});var i=r(50424);const o={"primary-background-color":"#111111","card-background-color":"#1c1c1c","secondary-background-color":"#202020","primary-text-color":"#e1e1e1","secondary-text-color":"#9b9b9b","disabled-text-color":"#6f6f6f","app-header-text-color":"#e1e1e1","app-header-background-color":"#101e24","switch-unchecked-button-color":"#999999","switch-unchecked-track-color":"#9b9b9b","divider-color":"rgba(225, 225, 225, .12)","mdc-ripple-color":"#AAAAAA","codemirror-keyword":"#C792EA","codemirror-operator":"#89DDFF","codemirror-variable":"#f07178","codemirror-variable-2":"#EEFFFF","codemirror-variable-3":"#DECB6B","codemirror-builtin":"#FFCB6B","codemirror-atom":"#F78C6C","codemirror-number":"#FF5370","codemirror-def":"#82AAFF","codemirror-string":"#C3E88D","codemirror-string-2":"#f07178","codemirror-comment":"#545454","codemirror-tag":"#FF5370","codemirror-meta":"#FFCB6B","codemirror-attribute":"#C792EA","codemirror-property":"#C792EA","codemirror-qualifier":"#DECB6B","codemirror-type":"#DECB6B","energy-grid-return-color":"#b39bdb"},n={"state-icon-error-color":"var(--error-state-color, var(--error-color))","state-unavailable-color":"var(--state-icon-unavailable-color, var(--disabled-text-color))","sidebar-text-color":"var(--primary-text-color)","sidebar-background-color":"var(--card-background-color)","sidebar-selected-text-color":"var(--primary-color)","sidebar-selected-icon-color":"var(--primary-color)","sidebar-icon-color":"rgba(var(--rgb-primary-text-color), 0.6)","switch-checked-color":"var(--primary-color)","switch-checked-button-color":"var(--switch-checked-color, var(--primary-background-color))","switch-checked-track-color":"var(--switch-checked-color, #000000)","switch-unchecked-button-color":"var(--switch-unchecked-color, var(--primary-background-color))","switch-unchecked-track-color":"var(--switch-unchecked-color, #000000)","slider-color":"var(--primary-color)","slider-secondary-color":"var(--light-primary-color)","slider-bar-color":"var(--disabled-text-color)","label-badge-grey":"var(--paper-grey-500)","label-badge-background-color":"var(--card-background-color)","label-badge-text-color":"rgba(var(--rgb-primary-text-color), 0.8)","paper-listbox-background-color":"var(--card-background-color)","paper-item-icon-color":"var(--state-icon-color)","paper-item-icon-active-color":"var(--state-icon-active-color)","table-row-background-color":"var(--primary-background-color)","table-row-alternative-background-color":"var(--secondary-background-color)","paper-slider-knob-color":"var(--slider-color)","paper-slider-knob-start-color":"var(--slider-color)","paper-slider-pin-color":"var(--slider-color)","paper-slider-pin-start-color":"var(--slider-color)","paper-slider-active-color":"var(--slider-color)","paper-slider-secondary-color":"var(--slider-secondary-color)","paper-slider-container-color":"var(--slider-bar-color)","data-table-background-color":"var(--card-background-color)","markdown-code-background-color":"var(--primary-background-color)","mdc-theme-primary":"var(--primary-color)","mdc-theme-secondary":"var(--accent-color)","mdc-theme-background":"var(--primary-background-color)","mdc-theme-surface":"var(--card-background-color)","mdc-theme-on-primary":"var(--text-primary-color)","mdc-theme-on-secondary":"var(--text-primary-color)","mdc-theme-on-surface":"var(--primary-text-color)","mdc-theme-text-disabled-on-light":"var(--disabled-text-color)","mdc-theme-text-primary-on-background":"var(--primary-text-color)","mdc-theme-text-secondary-on-background":"var(--secondary-text-color)","mdc-theme-text-icon-on-background":"var(--secondary-text-color)","app-header-text-color":"var(--text-primary-color)","app-header-background-color":"var(--primary-color)","mdc-checkbox-unchecked-color":"rgba(var(--rgb-primary-text-color), 0.54)","mdc-checkbox-disabled-color":"var(--disabled-text-color)","mdc-radio-unchecked-color":"rgba(var(--rgb-primary-text-color), 0.54)","mdc-radio-disabled-color":"var(--disabled-text-color)","mdc-tab-text-label-color-default":"var(--primary-text-color)","mdc-button-disabled-ink-color":"var(--disabled-text-color)","mdc-button-outline-color":"var(--divider-color)","mdc-dialog-scroll-divider-color":"var(--divider-color)","chip-background-color":"rgba(var(--rgb-primary-text-color), 0.15)","material-body-text-color":"var(--primary-text-color)","material-background-color":"var(--card-background-color)","material-secondary-background-color":"var(--secondary-background-color)","material-secondary-text-color":"var(--secondary-text-color)"},a=i.iv`
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
`,s=i.iv`
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
`,l=i.iv`
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
`,d=i.iv`
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
`;i.iv`
  body {
    background-color: var(--primary-background-color);
    color: var(--primary-text-color);
    height: calc(100vh - 32px);
    width: 100vw;
  }
`}}]);
//# sourceMappingURL=4353ceff.js.map