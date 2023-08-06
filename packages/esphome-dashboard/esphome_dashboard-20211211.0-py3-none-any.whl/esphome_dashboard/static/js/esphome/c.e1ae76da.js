import{r as t,_ as e,e as i,t as o,i as s,n as d,a,y as r,x as n,O as l,L as c}from"./index-6b4dee4b.js";import"./c.644ce6a3.js";import{c as h,s as p}from"./c.aab6931a.js";let u=class extends a{constructor(){super(...arguments),this._adopted=!1,this._busy=!1,this._cleanSSIDBlur=t=>{const e=t.target;e.value=e.value.trim()}}render(){return r`
      <mwc-dialog
        .heading=${this._adopted?"Configuration created":"Adopt device"}
        @closed=${this._handleClose}
        open
      >
        ${this._adopted?r`
              <div>
                To finish adoption, the new configuration needs to be installed
                on the device. This can be done wirelessly.
              </div>
              <mwc-button
                slot="primaryAction"
                dialogAction="install"
                label="Install"
                @click=${()=>n(`${this.device.name}.yaml`)}
              ></mwc-button>
              <mwc-button
                slot="secondaryAction"
                dialogAction="skip"
                label="skip"
              ></mwc-button>
            `:r`
              <div>
                Adopting ${this.device.name} will create an ESPHome
                configuration for this device allowing you to install updates
                and customize the original firmware.
              </div>

              ${this._error?r`<div class="error">${this._error}</div>`:""}
              ${!1!==this._hasWifiSecrets?r`
                    <div>
                      This device will be configured to connect to the Wi-Fi
                      network stored in your secrets.
                    </div>
                  `:r`
                    <div>
                      Enter the credentials of the Wi-Fi network that you want
                      your device to connect to.
                    </div>
                    <div>
                      This information will be stored in your secrets and used
                      for this and future devices. You can edit the information
                      later by editing your secrets at the top of the page.
                    </div>

                    <mwc-textfield
                      label="Network name"
                      name="ssid"
                      required
                      @blur=${this._cleanSSIDBlur}
                      .disabled=${this._busy}
                    ></mwc-textfield>

                    <mwc-textfield
                      label="Password"
                      name="password"
                      type="password"
                      helper="Leave blank if no password"
                      .disabled=${this._busy}
                    ></mwc-textfield>
                  `}

              <mwc-button
                slot="primaryAction"
                .label=${this._busy?"Adopting…":"Adopt"}
                @click=${this._handleAdopt}
                .disabled=${void 0===this._hasWifiSecrets}
              ></mwc-button>
              ${this._busy?"":r`
                    <mwc-button
                      slot="secondaryAction"
                      label="Cancel"
                      dialogAction="cancel"
                    ></mwc-button>
                  `}
            `}
      </mwc-dialog>
    `}firstUpdated(t){super.firstUpdated(t),h().then((t=>{this._hasWifiSecrets=t}))}_handleClose(){this.parentNode.removeChild(this)}async _handleAdopt(){if(this._error=void 0,!1===this._hasWifiSecrets){if(!this._inputSSID.reportValidity())return void this._inputSSID.focus();this._busy=!0;try{await p(this._inputSSID.value,this._inputPassword.value)}catch(t){return this._busy=!1,void(this._error="Failed to store Wi-Fi credentials")}}this._busy=!0;try{await l(this.device),c(this,"adopted"),this._adopted=!0}catch(t){this._busy=!1,this._error="Failed to import device"}}};u.styles=t`
    :host {
      --mdc-dialog-max-width: 390px;
    }
    mwc-textfield {
      display: block;
      margin-top: 16px;
    }
    div + div {
      margin-top: 16px;
    }
    .error {
      color: #db4437;
      margin-bottom: 16px;
    }
  `,e([i()],u.prototype,"device",void 0),e([o()],u.prototype,"_hasWifiSecrets",void 0),e([o()],u.prototype,"_adopted",void 0),e([o()],u.prototype,"_busy",void 0),e([o()],u.prototype,"_error",void 0),e([s("mwc-textfield[name=ssid]")],u.prototype,"_inputSSID",void 0),e([s("mwc-textfield[name=password]")],u.prototype,"_inputPassword",void 0),u=e([d("esphome-adopt-dialog")],u);
