import{_ as e,e as t,n as o,a as i,y as a,L as l}from"./index-bc9049cd.js";import"./c.75df1f63.js";import{d as n}from"./c.98b2050f.js";let d=class extends i{render(){return a`
      <mwc-dialog
        .heading=${`Delete ${this.name}`}
        @closed=${this._handleClose}
        open
      >
        <div>Are you sure you want to delete ${this.name}?</div>
        <mwc-button
          slot="primaryAction"
          label="Delete"
          dialogAction="close"
          @click=${this._handleDelete}
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          label="Cancel"
          dialogAction="cancel"
        ></mwc-button>
      </mwc-dialog>
    `}_handleClose(){this.parentNode.removeChild(this)}async _handleDelete(){await n(this.configuration),l(this,"deleted")}};e([t()],d.prototype,"name",void 0),e([t()],d.prototype,"configuration",void 0),d=e([o("esphome-delete-device-dialog")],d);
