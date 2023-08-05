import{r as t,_ as o,e,t as s,n as i,a,y as r,J as n}from"./index-81d48766.js";import"./c.0032773b.js";import{o as c}from"./c.c6ad50b4.js";import"./c.167fcd66.js";import"./c.ecd92d0e.js";import"./c.070781ac.js";import"./c.cf289fa2.js";import"./c.013e99c4.js";let l=class extends a{render(){return r`
      <esphome-process-dialog
        .heading=${`Install ${this.configuration}`}
        .type=${"upload"}
        .spawnParams=${{configuration:this.configuration,port:this.target}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        ${"OTA"===this.target?"":r`
              <a
                href="https://esphome.io/guides/faq.html#i-can-t-get-flashing-over-usb-to-work"
                slot="secondaryAction"
                target="_blank"
                >❓</a
              >
            `}
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        ${void 0===this._result||0===this._result?"":r`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_openEdit(){n(this.configuration)}_handleProcessDone(t){this._result=t.detail}_handleRetry(){c(this.configuration,this.target)}_handleClose(){this.parentNode.removeChild(this)}};l.styles=t`
    a[slot="secondaryAction"] {
      text-decoration: none;
      line-height: 32px;
    }
  `,o([e()],l.prototype,"configuration",void 0),o([e()],l.prototype,"target",void 0),o([s()],l.prototype,"_result",void 0),l=o([i("esphome-install-server-dialog")],l);
