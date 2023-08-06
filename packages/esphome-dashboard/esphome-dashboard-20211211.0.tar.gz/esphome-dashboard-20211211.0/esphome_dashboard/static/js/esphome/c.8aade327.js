import{r as t,_ as e,t as i,n as o,a as s,y as r}from"./index-6b4dee4b.js";import{g as a}from"./c.fd15de7a.js";import"./c.644ce6a3.js";import{c as n,f as c}from"./c.2543b431.js";import{m as l,s as d,a as p,b as h}from"./c.56258c5a.js";import{g as m,c as _}from"./c.423f4a55.js";const g=(t,e)=>{import("./c.c6a5da15.js");const i=document.createElement("esphome-install-server-dialog");i.configuration=t,i.target=e,document.body.append(i)},u=t=>{import("./c.5e45a076.js");const e=document.createElement("esphome-compile-dialog");e.configuration=t,document.body.append(e)};let w=class extends s{constructor(){super(...arguments),this._writeProgress=0,this._state="pick_option"}render(){let t,e,i=!1;return"pick_option"===this._state?(t="How do you want to install this on your ESP device?",e=r`
        <mwc-list-item
          twoline
          hasMeta
          .port=${"OTA"}
          @click=${this._handleLegacyOption}
        >
          <span>Wirelessly</span>
          <span slot="secondary">Requires the device to be online</span>
          ${l}
        </mwc-list-item>

        ${this._error?r`<div class="error">${this._error}</div>`:""}

        <mwc-list-item twoline hasMeta @click=${this._handleBrowserInstall}>
          <span>Plug into this computer</span>
          <span slot="secondary">
            ${d?"For devices connected via USB to this computer":p?"Your browser is not supported":"Dashboard needs to opened via HTTPS"}
          </span>
          ${d?l:h}
        </mwc-list-item>

        <mwc-list-item twoline hasMeta @click=${this._showServerPorts}>
          <span>Plug into the computer running ESPHome Dashboard</span>
          <span slot="secondary">
            For devices connected via USB to the server
          </span>
          ${l}
        </mwc-list-item>

        <mwc-list-item twoline hasMeta @click=${this._showCompileDialog}>
          <span>Manual download</span>
          <span slot="secondary">
            Install it yourself using ESPHome Flasher or other tools
          </span>
          ${l}
        </mwc-list-item>

        <mwc-button
          no-attention
          slot="secondaryAction"
          dialogAction="close"
          label="Cancel"
        ></mwc-button>
      `):"pick_server_port"===this._state?(t="Pick Server Port",e=void 0===this._ports?this._renderProgress("Loading serial devices"):0===this._ports.length?this._renderMessage("👀","No serial devices found.",!0):r`
              ${this._ports.map((t=>r`
                  <mwc-list-item
                    twoline
                    hasMeta
                    .port=${t.port}
                    @click=${this._handleLegacyOption}
                  >
                    <span>${t.desc}</span>
                    <span slot="secondary">${t.port}</span>
                    ${l}
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
          ${"esp8266"===this._configuration.esp_platform?"a minute":"2 minutes"}.<br />
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
    `}firstUpdated(t){super.firstUpdated(t),this._updateSerialPorts()}async _updateSerialPorts(){this._ports=await a()}updated(t){if(super.updated(t),t.has("_state"))if("pick_server_port"===this._state){const t=async()=>{await this._updateSerialPorts(),this._updateSerialInterval=window.setTimeout((async()=>{await t()}),5e3)};t()}else"pick_server_port"===t.get("_state")&&(clearTimeout(this._updateSerialInterval),this._updateSerialInterval=void 0)}_showServerPorts(){this.style.setProperty("--mdc-dialog-min-width",`${this.shadowRoot.querySelector("mwc-list-item").clientWidth+4}px`),this._state="pick_server_port"}_showCompileDialog(){u(this.configuration),this._close()}_handleLegacyOption(t){this._close(),g(this.configuration,t.currentTarget.port)}async _handleBrowserInstall(){if(!d||!p)return void window.open("https://esphome.io/guides/getting_started_hassio.html#webserial","_blank");this._error=void 0;const t=m(this.configuration);let e;try{e=await n(console)}catch(t){return}try{try{this._configuration=await t}catch(t){return this._state="done",void(this._error="Error fetching configuration information")}const i=_(this.configuration);this._state="connecting_webserial";try{await e.initialize()}catch(t){return console.error(t),this._state="pick_option",this._error="Failed to initialize.",void(e.connected&&(this._error+=" Try resetting your device or holding the BOOT button while selecting your serial port until it starts preparing the installation."))}this._state="prepare_installation";try{await i}catch(t){return this._error=r`
          Failed to prepare configuration<br /><br />
          <button class="link" @click=${this._showCompileDialog}>
            See what went wrong.
          </button>
        `,void(this._state="done")}this._state="installing";try{await c(e,this.configuration,!1,(t=>{this._writeProgress=t}))}catch(t){return this._error=`Installation failed: ${t}`,void(this._state="done")}await e.hardReset(),this._state="done"}finally{e&&(e.connected&&(console.log("Disconnecting esp"),await e.disconnect()),console.log("Closing port"),await(null==e?void 0:e.port.close()))}}_close(){this.shadowRoot.querySelector("mwc-dialog").close()}async _handleClose(){this._updateSerialInterval&&(clearTimeout(this._updateSerialInterval),this._updateSerialInterval=void 0),this.parentNode.removeChild(this)}};w.styles=t`
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
  `,e([i()],w.prototype,"configuration",void 0),e([i()],w.prototype,"_ports",void 0),e([i()],w.prototype,"_writeProgress",void 0),e([i()],w.prototype,"_configuration",void 0),e([i()],w.prototype,"_state",void 0),e([i()],w.prototype,"_error",void 0),w=e([o("esphome-install-dialog")],w);var v=Object.freeze({__proto__:null});export{u as a,v as i,g as o};
