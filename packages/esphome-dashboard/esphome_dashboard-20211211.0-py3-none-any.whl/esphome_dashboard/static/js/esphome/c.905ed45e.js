import{r as e,_ as o,e as n,n as t,a as i,y as s,N as a}from"./index-6b4dee4b.js";import{c,C as r}from"./c.ac1fcdb2.js";import"./c.644ce6a3.js";class l{constructor(){this.chunks=""}transform(e,o){this.chunks+=e;const n=this.chunks.split("\r\n");this.chunks=n.pop(),n.forEach((e=>o.enqueue(e+"\r\n")))}flush(e){e.enqueue(this.chunks)}}class d extends HTMLElement{constructor(){super(...arguments),this.allowInput=!0}connectedCallback(){if(this._console)return;if(this.attachShadow({mode:"open"}).innerHTML=`\n      <style>\n        :host, input {\n          background-color: #1c1c1c;\n          color: #ddd;\n          font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier,\n            monospace;\n          line-height: 1.45;\n        }\n        form {\n          display: flex;\n          align-items: center;\n          padding: 0 8px 0 16px;\n        }\n        input {\n          flex: 1;\n          padding: 4px;\n          margin: 0 8px;\n          border: 0;\n          outline: none;\n        }\n        ${c}\n      </style>\n      <div class="log"></div>\n      ${this.allowInput?"<form>\n                >\n                <input autofocus>\n              </form>\n            ":""}\n    `,this._console=new r(this.shadowRoot.querySelector("div")),this.allowInput){const e=this.shadowRoot.querySelector("input");this.addEventListener("click",(()=>{var o;""===(null===(o=getSelection())||void 0===o?void 0:o.toString())&&e.focus()})),e.addEventListener("keydown",(e=>{"Enter"===e.key&&(e.preventDefault(),e.stopPropagation(),this._sendCommand())}))}const e=new AbortController,o=this._connect(e.signal);this._cancelConnection=()=>(e.abort(),o)}async _connect(e){this.logger.debug("Starting console read loop");try{await this.port.readable.pipeThrough(new TextDecoderStream,{signal:e}).pipeThrough(new TransformStream(new l)).pipeTo(new WritableStream({write:e=>{this._console.addLine(e.replace("\r",""))}})),e.aborted||(this._console.addLine(""),this._console.addLine(""),this._console.addLine("Terminal disconnected"))}catch(e){this._console.addLine(""),this._console.addLine(""),this._console.addLine(`Terminal disconnected: ${e}`)}finally{await(o=100,new Promise((e=>setTimeout(e,o)))),this.logger.debug("Finished console read loop")}var o}async _sendCommand(){const e=this.shadowRoot.querySelector("input"),o=e.value,n=new TextEncoder,t=this.port.writable.getWriter();await t.write(n.encode(o+"\r\n")),this._console.addLine(`> ${o}\r\n`),e.value="",e.focus();try{t.releaseLock()}catch(e){console.error("Ignoring release lock error",e)}}async disconnect(){this._cancelConnection&&(await this._cancelConnection(),this._cancelConnection=void 0)}async reset(){this.logger.debug("Triggering reset."),await this.port.setSignals({dataTerminalReady:!1,requestToSend:!0}),await this.port.setSignals({dataTerminalReady:!1,requestToSend:!1}),await new Promise((e=>setTimeout(e,1e3)))}}customElements.define("ewt-console",d);let h=class extends i{render(){return s`
      <mwc-dialog
        open
        .heading=${`Logs ${this.configuration}`}
        scrimClickAction
        @closed=${this._handleClose}
      >
        <ewt-console
          .port=${this.port}
          .logger=${console}
          .allowInput=${!1}
        ></ewt-console>
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          label="Reset Device"
          @click=${this._resetDevice}
        ></mwc-button>
        <mwc-button
          slot="primaryAction"
          dialogAction="close"
          label="Close"
        ></mwc-button>
      </mwc-dialog>
    `}_openEdit(){a(this.configuration)}async _handleClose(){await this.shadowRoot.querySelector("ewt-console").disconnect(),await this.port.close(),this.parentNode.removeChild(this)}async _resetDevice(){await this.shadowRoot.querySelector("ewt-console").reset()}};h.styles=e`
    mwc-dialog {
      --mdc-dialog-max-width: 90vw;
    }
    ewt-console {
      display: block;
      width: calc(80vw - 48px);
      height: 80vh;
    }
  `,o([n()],h.prototype,"configuration",void 0),o([n()],h.prototype,"port",void 0),h=o([t("esphome-logs-webserial-dialog")],h);
