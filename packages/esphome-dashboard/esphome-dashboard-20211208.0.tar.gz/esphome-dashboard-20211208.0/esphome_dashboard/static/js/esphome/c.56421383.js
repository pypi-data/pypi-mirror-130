import{_ as o,e as t,t as e,n as s,a as i,y as r,N as a}from"./index-bc9049cd.js";import"./c.dbd2e702.js";import{o as c}from"./c.afe3d856.js";import"./c.75df1f63.js";import"./c.ee0ef29c.js";import"./c.c4cda974.js";let n=class extends i{render(){return r`
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
        ${void 0===this._result||0===this._result?"":r`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_openEdit(){a(this.configuration)}_handleProcessDone(o){this._result=o.detail}_handleRetry(){c(this.configuration,this.target)}_handleClose(){this.parentNode.removeChild(this)}};o([t()],n.prototype,"configuration",void 0),o([t()],n.prototype,"target",void 0),o([e()],n.prototype,"_result",void 0),n=o([s("esphome-logs-dialog")],n);
