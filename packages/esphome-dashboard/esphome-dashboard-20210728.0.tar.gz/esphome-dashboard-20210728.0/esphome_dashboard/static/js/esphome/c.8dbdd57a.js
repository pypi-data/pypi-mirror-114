import{i as t,_ as e,r as i,n as o,h as s,T as r,x as a}from"./c.1ff2516f.js";import{g as n}from"./c.c22a35d2.js";import{g as c,c as l,a as d,f as p}from"./c.8e7a8211.js";import{m as h,s as m,a as g}from"./c.8d16680b.js";const _=(t,e)=>{import("./c.2727a499.js");const i=document.createElement("esphome-install-server-dialog");i.configuration=t,i.target=e,document.body.append(i)},u=t=>{import("./c.7aaf642f.js");const e=document.createElement("esphome-compile-dialog");e.configuration=t,document.body.append(e)},w=a`
  <svg width="24" height="24" viewBox="0 0 24 24" slot="meta">
    <path d="M11,18H13V16H11V18M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,6A4,4 0 0,0 8,10H10A2,2 0 0,1 12,8A2,2 0 0,1 14,10C14,12 11,11.75 11,15H13C13,12.75 16,12.5 16,10A4,4 0 0,0 12,6Z" />
  </svg>
`;let v=class extends s{constructor(){super(...arguments),this._writeProgress=0,this._state="pick_option"}render(){let t,e,i=!1;return"pick_option"===this._state?(t="How do you want to install this on your ESP device?",e=r`
        <mwc-list-item
          twoline
          hasMeta
          .port=${"OTA"}
          @click=${this._handleLegacyOption}
        >
          <span>Wirelessly</span>
          <span slot="secondary">Requires the device to be online</span>
          ${h}
        </mwc-list-item>

        ${this._error?r`<div class="error">${this._error}</div>`:""}

        <mwc-list-item twoline hasMeta @click=${this._handleBrowserInstall}>
          <span>Plug into this computer</span>
          <span slot="secondary">
            ${m?"For devices connected via USB to this computer":g?"Your browser is not supported":"Dashboard needs to opened via HTTPS"}
          </span>
          ${m?h:w}
        </mwc-list-item>

        <mwc-list-item twoline hasMeta @click=${this._showServerPorts}>
          <span>Plug into the computer running ESPHome Dashboard</span>
          <span slot="secondary">
            For devices connected via USB to the server
          </span>
          ${h}
        </mwc-list-item>

        <mwc-list-item twoline hasMeta @click=${this._showCompileDialog}>
          <span>Manual download</span>
          <span slot="secondary">
            Install it yourself using ESPHome Flasher or other tools
          </span>
          ${h}
        </mwc-list-item>

        <mwc-button
          no-attention
          slot="secondaryAction"
          dialogAction="close"
          label="Cancel"
        ></mwc-button>
      `):"pick_server_port"===this._state?(t="Pick Server Port",e=r`
        ${this._ports.map((t=>r`
            <mwc-list-item
              twoline
              hasMeta
              .port=${t.port}
              @click=${this._handleLegacyOption}
            >
              <span>${t.desc}</span>
              <span slot="secondary">${t.port}</span>
              ${h}
            </mwc-list-item>
          `))}

        <mwc-button
          no-attention
          slot="secondaryAction"
          dialogAction="close"
          label="Cancel"
        ></mwc-button>
      `):"connecting_webserial"===this._state?(e=this._renderProgress("Connecting"),i=!0):"prepare_installation"===this._state?(e=this._renderProgress("Preparing installation"),i=!0):"installing"===this._state?(e=this._renderProgress(r`
          Installing<br /><br />
          This will take
          ${"ESP8266"===this._configuration.esp_platform?"a minute":"2 minutes"}.<br />
          Keep this page visible to prevent slow down
        `,this._writeProgress>3?this._writeProgress:void 0),i=!0):"done"===this._state&&(e=this._error?this._renderMessage("👀",this._error,!0):this._renderMessage("🎉","Configuration installed!",!0)),r`
      <mwc-dialog
        open
        heading=${t}
        scrimClickAction
        @closed=${this._handleClose}
        .hideActions=${i}
      >
        ${e}
      </mwc-dialog>
    `}_renderProgress(t,e){return r`
      <div class="center">
        <div>
          <mwc-circular-progress
            active
            ?indeterminate=${void 0===e}
            .progress=${void 0!==e?e/100:void 0}
            density="8"
          ></mwc-circular-progress>
          ${void 0!==e?r`<div class="progress-pct">${e}%</div>`:""}
        </div>
        ${t}
      </div>
    `}_renderMessage(t,e,i){return r`
      <div class="center">
        <div class="icon">${t}</div>
        ${e}
      </div>
      ${i&&r`
        <mwc-button
          slot="primaryAction"
          dialogAction="ok"
          label="Close"
        ></mwc-button>
      `}
    `}firstUpdated(t){super.firstUpdated(t),this._updateSerialPorts()}async _updateSerialPorts(){this._ports=await n()}updated(t){if(super.updated(t),t.has("_state")&&"pick_server_port"===this._state){(async()=>{await this._updateSerialPorts(),this._updateSerialInterval=window.setTimeout((async()=>{await this._updateSerialPorts()}),5e3)})()}}_showServerPorts(){this.style.setProperty("--mdc-dialog-min-width",`${this.shadowRoot.querySelector("mwc-list-item").clientWidth+4}px`),this._state="pick_server_port"}_showCompileDialog(){u(this.configuration),this._close()}_handleLegacyOption(t){this._close(),_(this.configuration,t.currentTarget.port)}async _handleBrowserInstall(){if(!m||!g)return void window.open("https://esphome.io/guides/getting_started_hassio.html#webserial","_blank");this._error=void 0;const t=c(this.configuration);let e;try{e=await l(console)}catch(t){return}try{try{this._configuration=await t}catch(t){return this._state="done",void(this._error="Error fetching configuration information")}const i=d(this.configuration);this._state="connecting_webserial";try{await e.initialize()}catch(t){return console.error(t),this._state="pick_option",this._error="Failed to initialize.",void(e.connected&&(this._error+=" Try resetting your device or holding the BOOT button while selecting your serial port until it starts preparing the installation."))}this._state="prepare_installation";try{await i}catch(t){return this._error=r`
          Failed to prepare configuration<br /><br />
          <button class="link" @click=${this._showCompileDialog}>
            See what went wrong.
          </button>
        `,void(this._state="done")}this._state="installing";try{await p(e,this.configuration,!1,(t=>{this._writeProgress=t}))}catch(t){return this._error="Installation failed",void(this._state="done")}await e.hardReset(),this._state="done"}finally{(null==e?void 0:e.connected)&&(console.log("Disconnecting esp"),await e.disconnect())}}_close(){this.shadowRoot.querySelector("mwc-dialog").close()}async _handleClose(){this._updateSerialInterval&&clearTimeout(this._updateSerialInterval),this.parentNode.removeChild(this)}};v.styles=t`
    :host {
      --mdc-theme-primary: #03a9f4;
    }
    a {
      color: var(--mdc-theme-primary);
    }
    mwc-button[no-attention] {
      --mdc-theme-primary: #444;
      --mdc-theme-on-primary: white;
    }
    mwc-list-item {
      margin: 0 -20px;
    }
    svg {
      fill: currentColor;
    }
    .center {
      text-align: center;
    }
    mwc-circular-progress {
      margin-bottom: 16px;
    }
    .progress-pct {
      position: absolute;
      top: 50px;
      left: 0;
      right: 0;
    }
    .icon {
      font-size: 50px;
      line-height: 80px;
      color: black;
    }
    button.link {
      background: none;
      color: var(--mdc-theme-primary);
      border: none;
      padding: 0;
      font: inherit;
      text-align: left;
      text-decoration: underline;
      cursor: pointer;
    }
    .show-ports {
      margin-top: 16px;
    }
    .error {
      padding: 8px 24px;
      background-color: #fff59d;
      margin: 0 -24px;
    }
  `,e([i()],v.prototype,"configuration",void 0),e([i()],v.prototype,"_ports",void 0),e([i()],v.prototype,"_writeProgress",void 0),e([i()],v.prototype,"_configuration",void 0),e([i()],v.prototype,"_state",void 0),e([i()],v.prototype,"_error",void 0),v=e([o("esphome-install-dialog")],v);var y=Object.freeze({__proto__:null});export{u as a,y as i,_ as o};
