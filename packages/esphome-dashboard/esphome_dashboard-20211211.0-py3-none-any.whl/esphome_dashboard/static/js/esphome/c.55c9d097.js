import{r as t,_ as o,e,t as s,n as i,a,y as r}from"./index-6b4dee4b.js";import"./c.644ce6a3.js";import"./c.ac1fcdb2.js";import{g as n}from"./c.fd15de7a.js";import{m as c,s as p,a as l,b as d}from"./c.56258c5a.js";const m=(t,o)=>{import("./c.804569b1.js");const e=document.createElement("esphome-logs-dialog");e.configuration=t,e.target=o,document.body.append(e)},h=(t,o)=>{import("./c.905ed45e.js");const e=document.createElement("esphome-logs-webserial-dialog");e.configuration=t,e.port=o,document.body.append(e)};let w=class extends a{constructor(){super(...arguments),this._show="options"}render(){return r`
      <mwc-dialog
        open
        heading=${"options"===this._show?"How to get the logs for your ESP device?":"Pick server port"}
        scrimClickAction
        @closed=${this._handleClose}
      >
        ${"options"===this._show?r`
              <mwc-list-item
                twoline
                hasMeta
                dialogAction="close"
                .port=${"OTA"}
                @click=${this._pickPort}
              >
                <span>Wirelessly</span>
                <span slot="secondary">Requires the device to be online</span>
                ${c}
              </mwc-list-item>

              <mwc-list-item
                twoline
                hasMeta
                .port=${"WEBSERIAL"}
                @click=${this._pickWebSerial}
              >
                <span>Plug into this computer</span>
                <span slot="secondary">
                  ${p?"For devices connected via USB to this computer":l?"Your browser is not supported":"Dashboard needs to opened via HTTPS"}
                </span>
                ${p?c:d}
              </mwc-list-item>

              <mwc-list-item twoline hasMeta @click=${this._showServerPorts}>
                <span>Plug into the computer running ESPHome Dashboard</span>
                <span slot="secondary">
                  For devices connected via USB to the server
                </span>
                ${c}
              </mwc-list-item>
            `:void 0===this._ports?r`
              <mwc-list-item>
                <span>Loading ports…</span>
              </mwc-list-item>
            `:0===this._ports.length?r`
              <mwc-list-item>
                <span>No serial ports found.</span>
              </mwc-list-item>
            `:this._ports.map((t=>r`
                <mwc-list-item
                  twoline
                  hasMeta
                  dialogAction="close"
                  .port=${t.port}
                  @click=${this._pickPort}
                >
                  <span>${t.desc}</span>
                  <span slot="secondary">${t.port}</span>
                  ${c}
                </mwc-list-item>
              `))}

        <mwc-button
          no-attention
          slot="secondaryAction"
          dialogAction="close"
          label="Cancel"
        ></mwc-button>
      </mwc-dialog>
    `}firstUpdated(t){super.firstUpdated(t),n().then((t=>{0!==t.length||p?this._ports=t:(this._handleClose(),m(this.configuration,"OTA"))}))}_showServerPorts(){this._show="server_ports"}_pickPort(t){m(this.configuration,t.currentTarget.port)}async _pickWebSerial(t){if(p&&l)try{const t=await navigator.serial.requestPort();await t.open({baudRate:115200}),this.shadowRoot.querySelector("mwc-dialog").close(),h(this.configuration,t)}catch(t){console.error(t)}else window.open("https://esphome.io/guides/getting_started_hassio.html#webserial","_blank")}_handleClose(){this.parentNode.removeChild(this)}};w.styles=t`
    mwc-list-item {
      margin: 0 -20px;
    }
  `,o([e()],w.prototype,"configuration",void 0),o([s()],w.prototype,"_ports",void 0),o([s()],w.prototype,"_show",void 0),w=o([i("esphome-logs-target-dialog")],w);var g=Object.freeze({__proto__:null});export{g as l,m as o};
