/*! For license information please see ecaf895c.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[86579,49995,93098,76628,33912,17463,38084,3035,89640,77516,38109,2891,90244,11139,5713,22946,92887],{18601:(t,e,i)=>{"use strict";i.d(e,{qN:()=>n.q,Wg:()=>o});var n=i(78220);class o extends n.H{click(){this.formElement&&(this.formElement.focus(),this.formElement.click())}setAriaLabel(t){this.formElement&&this.formElement.setAttribute("aria-label",t)}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(t=>{this.dispatchEvent(new Event("change",t))}))}}o.shadowRootOptions={mode:"open",delegatesFocus:!0}},14114:(t,e,i)=>{"use strict";i.d(e,{P:()=>n});const n=t=>(e,i)=>{if(e.constructor._observers){if(!e.constructor.hasOwnProperty("_observers")){const t=e.constructor._observers;e.constructor._observers=new Map,t.forEach(((t,i)=>e.constructor._observers.set(i,t)))}}else{e.constructor._observers=new Map;const t=e.updated;e.updated=function(e){t.call(this,e),e.forEach(((t,e)=>{const i=this.constructor._observers.get(e);void 0!==i&&i.call(this,this[e],t)}))}}e.constructor._observers.set(i,t)}},35487:(t,e,i)=>{"use strict";i.d(e,{Y:()=>f});var n=i(87480),o=i(55704),a=i(72774),r={ROOT:"mdc-form-field"},s={LABEL_SELECTOR:".mdc-form-field > label"};const l=function(t){function e(i){var o=t.call(this,(0,n.__assign)((0,n.__assign)({},e.defaultAdapter),i))||this;return o.click=function(){o.handleClick()},o}return(0,n.__extends)(e,t),Object.defineProperty(e,"cssClasses",{get:function(){return r},enumerable:!1,configurable:!0}),Object.defineProperty(e,"strings",{get:function(){return s},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{activateInputRipple:function(){},deactivateInputRipple:function(){},deregisterInteractionHandler:function(){},registerInteractionHandler:function(){}}},enumerable:!1,configurable:!0}),e.prototype.init=function(){this.adapter.registerInteractionHandler("click",this.click)},e.prototype.destroy=function(){this.adapter.deregisterInteractionHandler("click",this.click)},e.prototype.handleClick=function(){var t=this;this.adapter.activateInputRipple(),requestAnimationFrame((function(){t.adapter.deactivateInputRipple()}))},e}(a.K);var d=i(78220),c=i(18601),p=i(14114),h=i(81471);class u extends d.H{constructor(){super(...arguments),this.alignEnd=!1,this.spaceBetween=!1,this.nowrap=!1,this.label="",this.mdcFoundationClass=l}createAdapter(){return{registerInteractionHandler:(t,e)=>{this.labelEl.addEventListener(t,e)},deregisterInteractionHandler:(t,e)=>{this.labelEl.removeEventListener(t,e)},activateInputRipple:async()=>{const t=this.input;if(t instanceof c.Wg){const e=await t.ripple;e&&e.startPress()}},deactivateInputRipple:async()=>{const t=this.input;if(t instanceof c.Wg){const e=await t.ripple;e&&e.endPress()}}}}get input(){var t,e;return null!==(e=null===(t=this.slottedInputs)||void 0===t?void 0:t[0])&&void 0!==e?e:null}render(){const t={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return o.dy`
      <div class="mdc-form-field ${(0,h.$)(t)}">
        <slot></slot>
        <label class="mdc-label"
               @click="${this._labelClick}">${this.label}</label>
      </div>`}_labelClick(){const t=this.input;t&&(t.focus(),t.click())}}(0,n.__decorate)([(0,o.Cb)({type:Boolean})],u.prototype,"alignEnd",void 0),(0,n.__decorate)([(0,o.Cb)({type:Boolean})],u.prototype,"spaceBetween",void 0),(0,n.__decorate)([(0,o.Cb)({type:Boolean})],u.prototype,"nowrap",void 0),(0,n.__decorate)([(0,o.Cb)({type:String}),(0,p.P)((async function(t){const e=this.input;e&&("input"===e.localName?e.setAttribute("aria-label",t):e instanceof c.Wg&&(await e.updateComplete,e.setAriaLabel(t)))}))],u.prototype,"label",void 0),(0,n.__decorate)([(0,o.IO)(".mdc-form-field")],u.prototype,"mdcRoot",void 0),(0,n.__decorate)([(0,o.vZ)("",!0,"*")],u.prototype,"slottedInputs",void 0),(0,n.__decorate)([(0,o.IO)("label")],u.prototype,"labelEl",void 0);const m=o.iv`.mdc-form-field{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87));display:inline-flex;align-items:center;vertical-align:middle}.mdc-form-field>label{margin-left:0;margin-right:auto;padding-left:4px;padding-right:0;order:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{margin-left:auto;margin-right:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{padding-left:0;padding-right:4px}.mdc-form-field--nowrap>label{text-overflow:ellipsis;overflow:hidden;white-space:nowrap}.mdc-form-field--align-end>label{margin-left:auto;margin-right:0;padding-left:0;padding-right:4px;order:-1}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{margin-left:0;margin-right:auto}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{padding-left:4px;padding-right:0}.mdc-form-field--space-between{justify-content:space-between}.mdc-form-field--space-between>label{margin:0}[dir=rtl] .mdc-form-field--space-between>label,.mdc-form-field--space-between>label[dir=rtl]{margin:0}:host{display:inline-flex}.mdc-form-field{width:100%}::slotted(*){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}::slotted(mwc-switch){margin-right:10px}[dir=rtl] ::slotted(mwc-switch),::slotted(mwc-switch[dir=rtl]){margin-left:10px}`;let f=class extends u{};f.styles=[m],f=(0,n.__decorate)([(0,o.Mo)("mwc-formfield")],f)},24983:(t,e,i)=>{"use strict";i.d(e,{r:()=>y});var n=i(87480),o=i(55704),a=(i(66702),i(38103)),r=i(18601),s=i(14114),l=i(98734),d=i(72774),c={CHECKED:"mdc-switch--checked",DISABLED:"mdc-switch--disabled"},p={ARIA_CHECKED_ATTR:"aria-checked",NATIVE_CONTROL_SELECTOR:".mdc-switch__native-control",RIPPLE_SURFACE_SELECTOR:".mdc-switch__thumb-underlay"};const h=function(t){function e(i){return t.call(this,(0,n.__assign)((0,n.__assign)({},e.defaultAdapter),i))||this}return(0,n.__extends)(e,t),Object.defineProperty(e,"strings",{get:function(){return p},enumerable:!1,configurable:!0}),Object.defineProperty(e,"cssClasses",{get:function(){return c},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},setNativeControlChecked:function(){},setNativeControlDisabled:function(){},setNativeControlAttr:function(){}}},enumerable:!1,configurable:!0}),e.prototype.setChecked=function(t){this.adapter.setNativeControlChecked(t),this.updateAriaChecked(t),this.updateCheckedStyling(t)},e.prototype.setDisabled=function(t){this.adapter.setNativeControlDisabled(t),t?this.adapter.addClass(c.DISABLED):this.adapter.removeClass(c.DISABLED)},e.prototype.handleChange=function(t){var e=t.target;this.updateAriaChecked(e.checked),this.updateCheckedStyling(e.checked)},e.prototype.updateCheckedStyling=function(t){t?this.adapter.addClass(c.CHECKED):this.adapter.removeClass(c.CHECKED)},e.prototype.updateAriaChecked=function(t){this.adapter.setNativeControlAttr(p.ARIA_CHECKED_ATTR,""+!!t)},e}(d.K);var u=i(49629);class m extends r.Wg{constructor(){super(...arguments),this.checked=!1,this.disabled=!1,this.shouldRenderRipple=!1,this.mdcFoundationClass=h,this.rippleHandlers=new l.A((()=>(this.shouldRenderRipple=!0,this.ripple)))}changeHandler(t){this.mdcFoundation.handleChange(t),this.checked=this.formElement.checked}createAdapter(){return Object.assign(Object.assign({},(0,r.qN)(this.mdcRoot)),{setNativeControlChecked:t=>{this.formElement.checked=t},setNativeControlDisabled:t=>{this.formElement.disabled=t},setNativeControlAttr:(t,e)=>{this.formElement.setAttribute(t,e)}})}renderRipple(){return this.shouldRenderRipple?o.dy`
        <mwc-ripple
          .accent="${this.checked}"
          .disabled="${this.disabled}"
          unbounded>
        </mwc-ripple>`:""}focus(){const t=this.formElement;t&&(this.rippleHandlers.startFocus(),t.focus())}blur(){const t=this.formElement;t&&(this.rippleHandlers.endFocus(),t.blur())}render(){return o.dy`
      <div class="mdc-switch">
        <div class="mdc-switch__track"></div>
        <div class="mdc-switch__thumb-underlay">
          ${this.renderRipple()}
          <div class="mdc-switch__thumb">
            <input
              type="checkbox"
              id="basic-switch"
              class="mdc-switch__native-control"
              role="switch"
              aria-label="${(0,u.o)(this.ariaLabel)}"
              aria-labelledby="${(0,u.o)(this.ariaLabelledBy)}"
              @change="${this.changeHandler}"
              @focus="${this.handleRippleFocus}"
              @blur="${this.handleRippleBlur}"
              @mousedown="${this.handleRippleMouseDown}"
              @mouseenter="${this.handleRippleMouseEnter}"
              @mouseleave="${this.handleRippleMouseLeave}"
              @touchstart="${this.handleRippleTouchStart}"
              @touchend="${this.handleRippleDeactivate}"
              @touchcancel="${this.handleRippleDeactivate}">
          </div>
        </div>
      </div>`}handleRippleMouseDown(t){const e=()=>{window.removeEventListener("mouseup",e),this.handleRippleDeactivate()};window.addEventListener("mouseup",e),this.rippleHandlers.startPress(t)}handleRippleTouchStart(t){this.rippleHandlers.startPress(t)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}}(0,n.__decorate)([(0,o.Cb)({type:Boolean}),(0,s.P)((function(t){this.mdcFoundation.setChecked(t)}))],m.prototype,"checked",void 0),(0,n.__decorate)([(0,o.Cb)({type:Boolean}),(0,s.P)((function(t){this.mdcFoundation.setDisabled(t)}))],m.prototype,"disabled",void 0),(0,n.__decorate)([a.L,(0,o.Cb)({attribute:"aria-label"})],m.prototype,"ariaLabel",void 0),(0,n.__decorate)([a.L,(0,o.Cb)({attribute:"aria-labelledby"})],m.prototype,"ariaLabelledBy",void 0),(0,n.__decorate)([(0,o.IO)(".mdc-switch")],m.prototype,"mdcRoot",void 0),(0,n.__decorate)([(0,o.IO)("input")],m.prototype,"formElement",void 0),(0,n.__decorate)([(0,o.GC)("mwc-ripple")],m.prototype,"ripple",void 0),(0,n.__decorate)([(0,o.SB)()],m.prototype,"shouldRenderRipple",void 0),(0,n.__decorate)([(0,o.hO)({passive:!0})],m.prototype,"handleRippleMouseDown",null),(0,n.__decorate)([(0,o.hO)({passive:!0})],m.prototype,"handleRippleTouchStart",null);const f=o.iv`.mdc-switch__thumb-underlay{left:-14px;right:initial;top:-17px;width:48px;height:48px}[dir=rtl] .mdc-switch__thumb-underlay,.mdc-switch__thumb-underlay[dir=rtl]{left:initial;right:-14px}.mdc-switch__native-control{width:64px;height:48px}.mdc-switch{display:inline-block;position:relative;outline:none;user-select:none}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786);border-color:#018786;border-color:var(--mdc-theme-secondary, #018786)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:#000;background-color:var(--mdc-theme-on-surface, #000)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:#fff;background-color:var(--mdc-theme-surface, #fff);border-color:#fff;border-color:var(--mdc-theme-surface, #fff)}.mdc-switch__native-control{left:0;right:initial;position:absolute;top:0;margin:0;opacity:0;cursor:pointer;pointer-events:auto;transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1)}[dir=rtl] .mdc-switch__native-control,.mdc-switch__native-control[dir=rtl]{left:initial;right:0}.mdc-switch__track{box-sizing:border-box;width:36px;height:14px;border:1px solid transparent;border-radius:7px;opacity:.38;transition:opacity 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb-underlay{display:flex;position:absolute;align-items:center;justify-content:center;transform:translateX(0);transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb{box-shadow:0px 3px 1px -2px rgba(0, 0, 0, 0.2),0px 2px 2px 0px rgba(0, 0, 0, 0.14),0px 1px 5px 0px rgba(0,0,0,.12);box-sizing:border-box;width:20px;height:20px;border:10px solid;border-radius:50%;pointer-events:none;z-index:1}.mdc-switch--checked .mdc-switch__track{opacity:.54}.mdc-switch--checked .mdc-switch__thumb-underlay{transform:translateX(16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__thumb-underlay,.mdc-switch--checked .mdc-switch__thumb-underlay[dir=rtl]{transform:translateX(-16px)}.mdc-switch--checked .mdc-switch__native-control{transform:translateX(-16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__native-control,.mdc-switch--checked .mdc-switch__native-control[dir=rtl]{transform:translateX(16px)}.mdc-switch--disabled{opacity:.38;pointer-events:none}.mdc-switch--disabled .mdc-switch__thumb{border-width:1px}.mdc-switch--disabled .mdc-switch__native-control{cursor:default;pointer-events:none}:host{display:inline-flex;outline:none;-webkit-tap-highlight-color:transparent}`;let y=class extends m{};y.styles=[f],y=(0,n.__decorate)([(0,o.Mo)("mwc-switch")],y)},8878:(t,e,i)=>{"use strict";i(65233),i(8621),i(63207),i(30879),i(78814),i(60748),i(57548),i(73962);var n=i(51644),o=i(26110),a=i(21006),r=i(98235),s=i(18890),l=i(9672),d=i(87156),c=i(81668),p=i(50856),h=i(62276);const u=(0,s.x)(HTMLElement);(0,l.k)({_template:p.d`
    <style include="paper-dropdown-menu-shared-styles"></style>

    <paper-menu-button id="menuButton" vertical-align="[[verticalAlign]]" horizontal-align="[[horizontalAlign]]" dynamic-align="[[dynamicAlign]]" vertical-offset="[[_computeMenuVerticalOffset(noLabelFloat, verticalOffset)]]" disabled="[[disabled]]" no-animations="[[noAnimations]]" on-iron-select="_onIronSelect" on-iron-deselect="_onIronDeselect" opened="{{opened}}" close-on-activate allow-outside-scroll="[[allowOutsideScroll]]" restore-focus-on-close="[[restoreFocusOnClose]]" expand-sizing-target-for-scrollbars="[[expandSizingTargetForScrollbars]]">
      <!-- support hybrid mode: user might be using paper-menu-button 1.x which distributes via <content> -->
      <div class="dropdown-trigger" slot="dropdown-trigger">
        <paper-ripple></paper-ripple>
        <!-- paper-input has type="text" for a11y, do not remove -->
        <paper-input id="input" type="text" invalid="[[invalid]]" readonly disabled="[[disabled]]" value="[[value]]" placeholder="[[placeholder]]" error-message="[[errorMessage]]" always-float-label="[[alwaysFloatLabel]]" no-label-float="[[noLabelFloat]]" label="[[label]]" input-role="button" input-aria-haspopup="listbox" autocomplete="off">
          <!-- support hybrid mode: user might be using paper-input 1.x which distributes via <content> -->
          <iron-icon icon="paper-dropdown-menu:arrow-drop-down" suffix slot="suffix"></iron-icon>
        </paper-input>
      </div>
      <slot id="content" name="dropdown-content" slot="dropdown-content"></slot>
    </paper-menu-button>
`,is:"paper-dropdown-menu",behaviors:[n.P,o.a,a.V,r.x],properties:{selectedItemLabel:{type:String,notify:!0,readOnly:!0},selectedItem:{type:Object,notify:!0,readOnly:!0},value:{type:String,notify:!0},label:{type:String},placeholder:{type:String},errorMessage:{type:String},opened:{type:Boolean,notify:!0,value:!1,observer:"_openedChanged"},allowOutsideScroll:{type:Boolean,value:!1},noLabelFloat:{type:Boolean,value:!1,reflectToAttribute:!0},alwaysFloatLabel:{type:Boolean,value:!1},noAnimations:{type:Boolean,value:!1},horizontalAlign:{type:String,value:"right"},verticalAlign:{type:String,value:"top"},verticalOffset:Number,dynamicAlign:{type:Boolean},restoreFocusOnClose:{type:Boolean,value:!0},expandSizingTargetForScrollbars:{type:Boolean,value:!1}},listeners:{tap:"_onTap"},keyBindings:{"up down":"open",esc:"close"},observers:["_selectedItemChanged(selectedItem)"],_attachDom(t){const e=(0,h.r)(this);return e.attachShadow({mode:"open",delegatesFocus:!0,shadyUpgradeFragment:t}),e.shadowRoot.appendChild(t),u.prototype._attachDom.call(this,t)},focus(){this.$.input._focusableElement.focus()},attached:function(){var t=this.contentElement;t&&t.selectedItem&&this._setSelectedItem(t.selectedItem)},get contentElement(){for(var t=(0,d.vz)(this.$.content).getDistributedNodes(),e=0,i=t.length;e<i;e++)if(t[e].nodeType===Node.ELEMENT_NODE)return t[e]},open:function(){this.$.menuButton.open()},close:function(){this.$.menuButton.close()},_onIronSelect:function(t){this._setSelectedItem(t.detail.item)},_onIronDeselect:function(t){this._setSelectedItem(null)},_onTap:function(t){c.nJ(t)===this&&this.open()},_selectedItemChanged:function(t){var e="";e=t?t.label||t.getAttribute("label")||t.textContent.trim():"",this.value=e,this._setSelectedItemLabel(e)},_computeMenuVerticalOffset:function(t,e){return e||(t?-4:8)},_getValidity:function(t){return this.disabled||!this.required||this.required&&!!this.value},_openedChanged:function(){var t=this.opened?"true":"false",e=this.contentElement;e&&e.setAttribute("aria-expanded",t)}})},33760:(t,e,i)=>{"use strict";i.d(e,{U:()=>a});i(65233);var n=i(51644),o=i(26110);const a=[n.P,o.a,{hostAttributes:{role:"option",tabindex:"0"}}]},89194:(t,e,i)=>{"use strict";i(65233),i(65660),i(70019);var n=i(9672),o=i(50856);(0,n.k)({_template:o.d`
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
`,is:"paper-item-body"})},97968:(t,e,i)=>{"use strict";i(65660),i(70019);const n=document.createElement("template");n.setAttribute("style","display: none;"),n.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(n.content)},53973:(t,e,i)=>{"use strict";i(65233),i(65660),i(97968);var n=i(9672),o=i(50856),a=i(33760);(0,n.k)({_template:o.d`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[a.U]})},51095:(t,e,i)=>{"use strict";i(65233);var n=i(78161),o=i(9672),a=i(50856);(0,o.k)({_template:a.d`
    <style>
      :host {
        display: block;
        padding: 8px 0;

        background: var(--paper-listbox-background-color, var(--primary-background-color));
        color: var(--paper-listbox-color, var(--primary-text-color));

        @apply --paper-listbox;
      }
    </style>

    <slot></slot>
`,is:"paper-listbox",behaviors:[n.i],hostAttributes:{role:"listbox"}})},54444:(t,e,i)=>{"use strict";i(65233);var n=i(9672),o=i(87156),a=i(50856);(0,n.k)({_template:a.d`
    <style>
      :host {
        display: block;
        position: absolute;
        outline: none;
        z-index: 1002;
        -moz-user-select: none;
        -ms-user-select: none;
        -webkit-user-select: none;
        user-select: none;
        cursor: default;
      }

      #tooltip {
        display: block;
        outline: none;
        @apply --paper-font-common-base;
        font-size: 10px;
        line-height: 1;
        background-color: var(--paper-tooltip-background, #616161);
        color: var(--paper-tooltip-text-color, white);
        padding: 8px;
        border-radius: 2px;
        @apply --paper-tooltip;
      }

      @keyframes keyFrameScaleUp {
        0% {
          transform: scale(0.0);
        }
        100% {
          transform: scale(1.0);
        }
      }

      @keyframes keyFrameScaleDown {
        0% {
          transform: scale(1.0);
        }
        100% {
          transform: scale(0.0);
        }
      }

      @keyframes keyFrameFadeInOpacity {
        0% {
          opacity: 0;
        }
        100% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameFadeOutOpacity {
        0% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        100% {
          opacity: 0;
        }
      }

      @keyframes keyFrameSlideDownIn {
        0% {
          transform: translateY(-2000px);
          opacity: 0;
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameSlideDownOut {
        0% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(-2000px);
          opacity: 0;
        }
      }

      .fade-in-animation {
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameFadeInOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .fade-out-animation {
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 0ms);
        animation-name: keyFrameFadeOutOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-up-animation {
        transform: scale(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameScaleUp;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-down-animation {
        transform: scale(1);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameScaleDown;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation {
        transform: translateY(-2000px);
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownIn;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation-out {
        transform: translateY(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownOut;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.4, 0.0, 1, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .cancel-animation {
        animation-delay: -30s !important;
      }

      /* Thanks IE 10. */

      .hidden {
        display: none !important;
      }
    </style>

    <div id="tooltip" class="hidden">
      <slot></slot>
    </div>
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var t=(0,o.vz)(this).parentNode,e=(0,o.vz)(this).getOwnerRoot();return this.for?(0,o.vz)(e).querySelector("#"+this.for):t.nodeType==Node.DOCUMENT_FRAGMENT_NODE?e.host:t},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(t){"entry"===t?this.show():"exit"===t&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===(0,o.vz)(this).textContent.trim()){for(var t=!0,e=(0,o.vz)(this).getEffectiveChildNodes(),i=0;i<e.length;i++)if(""!==e[i].textContent.trim()){t=!1;break}if(t)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var t=this.offset;14!=this.marginTop&&14==this.offset&&(t=this.marginTop);var e,i,n=this.offsetParent.getBoundingClientRect(),o=this._target.getBoundingClientRect(),a=this.getBoundingClientRect(),r=(o.width-a.width)/2,s=(o.height-a.height)/2,l=o.left-n.left,d=o.top-n.top;switch(this.position){case"top":e=l+r,i=d-a.height-t;break;case"bottom":e=l+r,i=d+o.height+t;break;case"left":e=l-a.width-t,i=d+s;break;case"right":e=l+o.width+t,i=d+s}this.fitToVisibleBounds?(n.left+e+a.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,e)+"px",this.style.right="auto"),n.top+i+a.height>window.innerHeight?(this.style.bottom=n.height-d+t+"px",this.style.top="auto"):(this.style.top=Math.max(-n.top,i)+"px",this.style.bottom="auto")):(this.style.left=e+"px",this.style.top=i+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(t){500!==t&&this.updateStyles({"--paper-tooltip-delay-in":t+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(t){if("entry"===t&&""!==this.animationEntry)return this.animationEntry;if("exit"===t&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[t]&&"string"==typeof this.animationConfig[t][0].name){if(this.animationConfig[t][0].timing&&this.animationConfig[t][0].timing.delay&&0!==this.animationConfig[t][0].timing.delay){var e=this.animationConfig[t][0].timing.delay;"entry"===t?this.updateStyles({"--paper-tooltip-delay-in":e+"ms"}):"exit"===t&&this.updateStyles({"--paper-tooltip-delay-out":e+"ms"})}return this.animationConfig[t][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}})},68928:(t,e,i)=>{"use strict";i.d(e,{WU:()=>C});var n=/d{1,4}|M{1,4}|YY(?:YY)?|S{1,3}|Do|ZZ|Z|([HhMsDm])\1?|[aA]|"[^"]*"|'[^']*'/g,o="[1-9]\\d?",a="\\d\\d",r="[^\\s]+",s=/\[([^]*?)\]/gm;function l(t,e){for(var i=[],n=0,o=t.length;n<o;n++)i.push(t[n].substr(0,e));return i}var d=function(t){return function(e,i){var n=i[t].map((function(t){return t.toLowerCase()})).indexOf(e.toLowerCase());return n>-1?n:null}};function c(t){for(var e=[],i=1;i<arguments.length;i++)e[i-1]=arguments[i];for(var n=0,o=e;n<o.length;n++){var a=o[n];for(var r in a)t[r]=a[r]}return t}var p=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],h=["January","February","March","April","May","June","July","August","September","October","November","December"],u=l(h,3),m={dayNamesShort:l(p,3),dayNames:p,monthNamesShort:u,monthNames:h,amPm:["am","pm"],DoFn:function(t){return t+["th","st","nd","rd"][t%10>3?0:(t-t%10!=10?1:0)*t%10]}},f=c({},m),y=function(t,e){for(void 0===e&&(e=2),t=String(t);t.length<e;)t="0"+t;return t},g={D:function(t){return String(t.getDate())},DD:function(t){return y(t.getDate())},Do:function(t,e){return e.DoFn(t.getDate())},d:function(t){return String(t.getDay())},dd:function(t){return y(t.getDay())},ddd:function(t,e){return e.dayNamesShort[t.getDay()]},dddd:function(t,e){return e.dayNames[t.getDay()]},M:function(t){return String(t.getMonth()+1)},MM:function(t){return y(t.getMonth()+1)},MMM:function(t,e){return e.monthNamesShort[t.getMonth()]},MMMM:function(t,e){return e.monthNames[t.getMonth()]},YY:function(t){return y(String(t.getFullYear()),4).substr(2)},YYYY:function(t){return y(t.getFullYear(),4)},h:function(t){return String(t.getHours()%12||12)},hh:function(t){return y(t.getHours()%12||12)},H:function(t){return String(t.getHours())},HH:function(t){return y(t.getHours())},m:function(t){return String(t.getMinutes())},mm:function(t){return y(t.getMinutes())},s:function(t){return String(t.getSeconds())},ss:function(t){return y(t.getSeconds())},S:function(t){return String(Math.round(t.getMilliseconds()/100))},SS:function(t){return y(Math.round(t.getMilliseconds()/10),2)},SSS:function(t){return y(t.getMilliseconds(),3)},a:function(t,e){return t.getHours()<12?e.amPm[0]:e.amPm[1]},A:function(t,e){return t.getHours()<12?e.amPm[0].toUpperCase():e.amPm[1].toUpperCase()},ZZ:function(t){var e=t.getTimezoneOffset();return(e>0?"-":"+")+y(100*Math.floor(Math.abs(e)/60)+Math.abs(e)%60,4)},Z:function(t){var e=t.getTimezoneOffset();return(e>0?"-":"+")+y(Math.floor(Math.abs(e)/60),2)+":"+y(Math.abs(e)%60,2)}},b=function(t){return+t-1},v=[null,o],_=[null,r],w=["isPm",r,function(t,e){var i=t.toLowerCase();return i===e.amPm[0]?0:i===e.amPm[1]?1:null}],x=["timezoneOffset","[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z?",function(t){var e=(t+"").match(/([+-]|\d\d)/gi);if(e){var i=60*+e[1]+parseInt(e[2],10);return"+"===e[0]?i:-i}return 0}],k=(d("monthNamesShort"),d("monthNames"),{default:"ddd MMM DD YYYY HH:mm:ss",shortDate:"M/D/YY",mediumDate:"MMM D, YYYY",longDate:"MMMM D, YYYY",fullDate:"dddd, MMMM D, YYYY",isoDate:"YYYY-MM-DD",isoDateTime:"YYYY-MM-DDTHH:mm:ssZ",shortTime:"HH:mm",mediumTime:"HH:mm:ss",longTime:"HH:mm:ss.SSS"}),C=function(t,e,i){if(void 0===e&&(e=k.default),void 0===i&&(i={}),"number"==typeof t&&(t=new Date(t)),"[object Date]"!==Object.prototype.toString.call(t)||isNaN(t.getTime()))throw new Error("Invalid Date pass to format");var o=[];e=(e=k[e]||e).replace(s,(function(t,e){return o.push(e),"@@@"}));var a=c(c({},f),i);return(e=e.replace(n,(function(e){return g[e](t,a)}))).replace(/@@@/g,(function(){return o.shift()}))}},78389:(t,e,i)=>{"use strict";i.d(e,{s:()=>h});var n=i(99602),o=i(55122),a=i(57724);const r=(t,e)=>{var i,n;const o=t.N;if(void 0===o)return!1;for(const t of o)null===(n=(i=t).O)||void 0===n||n.call(i,e,!1),r(t,e);return!0},s=t=>{let e,i;do{if(void 0===(e=t.M))break;i=e.N,i.delete(t),t=e}while(0===(null==i?void 0:i.size))},l=t=>{for(let e;e=t.M;t=e){let i=e.N;if(void 0===i)e.N=i=new Set;else if(i.has(t))break;i.add(t),p(e)}};function d(t){void 0!==this.N?(s(this),this.M=t,l(this)):this.M=t}function c(t,e=!1,i=0){const n=this.H,o=this.N;if(void 0!==o&&0!==o.size)if(e)if(Array.isArray(n))for(let t=i;t<n.length;t++)r(n[t],!1),s(n[t]);else null!=n&&(r(n,!1),s(n));else r(this,t)}const p=t=>{var e,i,n,a;t.type==o.pX.CHILD&&(null!==(e=(n=t).P)&&void 0!==e||(n.P=c),null!==(i=(a=t).Q)&&void 0!==i||(a.Q=d))};class h extends o.Xe{constructor(){super(...arguments),this.isConnected=!0,this.ut=n.Jb,this.N=void 0}T(t,e,i){super.T(t,e,i),l(this)}O(t,e=!0){this.at(t),e&&(r(this,t),s(this))}at(t){var e,i;t!==this.isConnected&&(t?(this.isConnected=!0,this.ut!==n.Jb&&(this.setValue(this.ut),this.ut=n.Jb),null===(e=this.reconnected)||void 0===e||e.call(this)):(this.isConnected=!1,null===(i=this.disconnected)||void 0===i||i.call(this)))}S(t,e){if(!this.isConnected)throw Error(`AsyncDirective ${this.constructor.name} was rendered while its tree was disconnected.`);return super.S(t,e)}setValue(t){if(this.isConnected)if((0,a.OR)(this.Σdt))this.Σdt.I(t,this);else{const e=[...this.Σdt.H];e[this.Σct]=t,this.Σdt.I(e,this,0)}else this.ut=t}disconnected(){}reconnected(){}}},57724:(t,e,i)=>{"use strict";i.d(e,{E_:()=>f,i9:()=>u,_Y:()=>d,pt:()=>a,OR:()=>s,hN:()=>r,ws:()=>m,fk:()=>c,hl:()=>h});var n=i(99602);const{et:o}=n.Vm,a=t=>null===t||"object"!=typeof t&&"function"!=typeof t,r=(t,e)=>{var i,n;return void 0===e?void 0!==(null===(i=t)||void 0===i?void 0:i._$litType$):(null===(n=t)||void 0===n?void 0:n._$litType$)===e},s=t=>void 0===t.strings,l=()=>document.createComment(""),d=(t,e,i)=>{var n;const a=t.A.parentNode,r=void 0===e?t.B:e.A;if(void 0===i){const e=a.insertBefore(l(),r),n=a.insertBefore(l(),r);i=new o(e,n,t,t.options)}else{const e=i.B.nextSibling,o=i.M!==t;if(o&&(null===(n=i.Q)||void 0===n||n.call(i,t),i.M=t),e!==r||o){let t=i.A;for(;t!==e;){const e=t.nextSibling;a.insertBefore(t,r),t=e}}}return i},c=(t,e,i=t)=>(t.I(e,i),t),p={},h=(t,e=p)=>t.H=e,u=t=>t.H,m=t=>{var e;null===(e=t.P)||void 0===e||e.call(t,!1,!0);let i=t.A;const n=t.B.nextSibling;for(;i!==n;){const t=i.nextSibling;i.remove(),i=t}},f=t=>{t.R()}},19967:(t,e,i)=>{"use strict";i.d(e,{Xe:()=>n.Xe,pX:()=>n.pX,XM:()=>n.XM});var n=i(55122)},76666:(t,e,i)=>{"use strict";i.d(e,{$:()=>n.$});var n=i(81471)},82816:(t,e,i)=>{"use strict";i.d(e,{o:()=>n.o});var n=i(49629)},92483:(t,e,i)=>{"use strict";i.d(e,{V:()=>n.V});var n=i(79865)},11716:(t,e,i)=>{"use strict";i.d(e,{C:()=>l});var n=i(99602),o=i(55122),a=i(57724),r=i(78389);const s=t=>!(0,a.pt)(t)&&"function"==typeof t.then,l=(0,o.XM)(class extends r.s{constructor(){super(...arguments),this.Ct=2147483647,this.Rt=[]}render(...t){var e;return null!==(e=t.find((t=>!s(t))))&&void 0!==e?e:n.Jb}update(t,e){const i=this.Rt;let o=i.length;this.Rt=e;for(let t=0;t<e.length&&!(t>this.Ct);t++){const n=e[t];if(!s(n))return this.Ct=t,n;t<o&&n===i[t]||(this.Ct=2147483647,o=0,Promise.resolve(n).then((t=>{const e=this.Rt.indexOf(n);e>-1&&e<this.Ct&&(this.Ct=e,this.setValue(t))})))}return n.Jb}})}}]);
//# sourceMappingURL=ecaf895c.js.map