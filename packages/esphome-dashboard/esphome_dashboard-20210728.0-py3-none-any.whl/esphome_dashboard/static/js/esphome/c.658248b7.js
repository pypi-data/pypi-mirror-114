import{_ as o,w as t,r as e,n as s,h as i,T as r}from"./c.1ff2516f.js";import"./c.c22a35d2.js";import"./c.20fae408.js";import{o as n}from"./index-9fb59a6d.js";import{o as a}from"./c.34047af3.js";import"./c.8d16680b.js";let c=class extends i{render(){return r`
      <esphome-process-dialog
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
    `}_openEdit(){n(this.configuration)}_handleProcessDone(o){this._result=o.detail}_handleRetry(){a(this.configuration,this.target)}_handleClose(){this.parentNode.removeChild(this)}};o([t()],c.prototype,"configuration",void 0),o([t()],c.prototype,"target",void 0),o([e()],c.prototype,"_result",void 0),c=o([s("esphome-logs-dialog")],c);
