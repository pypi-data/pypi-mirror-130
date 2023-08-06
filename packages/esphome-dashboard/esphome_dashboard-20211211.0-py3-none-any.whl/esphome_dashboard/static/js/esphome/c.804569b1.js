import{_ as o,e as t,t as e,n as s,a as i,y as a,N as r}from"./index-6b4dee4b.js";import"./c.ac1fcdb2.js";import{o as c}from"./c.55c9d097.js";import"./c.644ce6a3.js";import"./c.fd15de7a.js";import"./c.56258c5a.js";let n=class extends i{render(){return a`
      <esphome-process-dialog
        always-show-close
        .heading=${`Logs ${this.configuration}`}
        .type=${"logs"}
        .spawnParams=${{configuration:this.configuration,port:this.target}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        ${void 0===this._result||0===this._result?"":a`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_openEdit(){r(this.configuration)}_handleProcessDone(o){this._result=o.detail}_handleRetry(){c(this.configuration,this.target)}_handleClose(){this.parentNode.removeChild(this)}};o([t()],n.prototype,"configuration",void 0),o([t()],n.prototype,"target",void 0),o([e()],n.prototype,"_result",void 0),n=o([s("esphome-logs-dialog")],n);
