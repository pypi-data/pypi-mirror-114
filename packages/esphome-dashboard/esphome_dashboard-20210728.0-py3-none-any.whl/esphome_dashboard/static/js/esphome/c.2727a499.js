import{i as t,_ as o,w as e,r as s,n as i,h as a,T as r}from"./c.1ff2516f.js";import"./c.20fae408.js";import{o as n}from"./index-9fb59a6d.js";import{o as l}from"./c.8dbdd57a.js";import"./c.c22a35d2.js";import"./c.8e7a8211.js";import"./c.8d16680b.js";let c=class extends a{render(){return r`
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
    `}_openEdit(){n(this.configuration)}_handleProcessDone(t){this._result=t.detail}_handleRetry(){l(this.configuration,this.target)}_handleClose(){this.parentNode.removeChild(this)}};c.styles=t`
    a[slot="secondaryAction"] {
      text-decoration: none;
      line-height: 32px;
    }
  `,o([e()],c.prototype,"configuration",void 0),o([e()],c.prototype,"target",void 0),o([s()],c.prototype,"_result",void 0),c=o([i("esphome-install-server-dialog")],c);
