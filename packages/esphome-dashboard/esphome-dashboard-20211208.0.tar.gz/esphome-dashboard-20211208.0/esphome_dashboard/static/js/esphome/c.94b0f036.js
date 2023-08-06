import{_ as e,e as o,n as s,a as i,y as t}from"./index-bc9049cd.js";import"./c.dbd2e702.js";import"./c.75df1f63.js";let a=class extends i{render(){return t`
      <esphome-process-dialog
        .heading=${`Clean MQTT discovery topics for ${this.configuration}`}
        .type=${"clean-mqtt"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
      >
      </esphome-process-dialog>
    `}_handleClose(){this.parentNode.removeChild(this)}};e([o()],a.prototype,"configuration",void 0),a=e([s("esphome-clean-mqtt-dialog")],a);
