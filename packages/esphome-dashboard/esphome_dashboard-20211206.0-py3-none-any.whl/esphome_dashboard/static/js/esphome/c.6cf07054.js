import{_ as e,e as t,n as o,a as i,y as n,f as a}from"./index-81d48766.js";import"./c.167fcd66.js";import{d}from"./c.013e99c4.js";let l=class extends i{render(){return n`
      <mwc-dialog
        .heading=${`Delete ${this.name}`}
        @closed=${this._handleClose}
        open
      >
        <div>Are you sure you want to delete ${this.name}?</div>
        <mwc-button
          slot="primaryAction"
          dialogAction="close"
          @click=${this._handleDelete}
        >
          Delete
        </mwc-button>
        <mwc-button slot="secondaryAction" dialogAction="cancel">
          Cancel
        </mwc-button>
      </mwc-dialog>
    `}_handleClose(){this.parentNode.removeChild(this)}async _handleDelete(){await d(this.configuration),a(this,"deleted")}};e([t()],l.prototype,"name",void 0),e([t()],l.prototype,"configuration",void 0),l=e([o("esphome-delete-device-dialog")],l);
