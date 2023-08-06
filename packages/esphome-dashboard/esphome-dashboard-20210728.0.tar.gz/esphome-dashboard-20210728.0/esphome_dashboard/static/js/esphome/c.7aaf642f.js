import{i as o,_ as e,w as t,r as n,n as i,h as s,T as a}from"./c.1ff2516f.js";import"./c.20fae408.js";import{a as r}from"./c.8dbdd57a.js";import"./index-9fb59a6d.js";import"./c.c22a35d2.js";import"./c.8e7a8211.js";import"./c.8d16680b.js";let c=class extends s{render(){return a`
      <esphome-process-dialog
        .heading=${`Download ${this.configuration}`}
        .type=${"compile"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        ${void 0===this._result?"":0===this._result?a`
              <a
                slot="secondaryAction"
                href="${`./download.bin?configuration=${encodeURIComponent(this.configuration)}`}"
              >
                <mwc-button label="Download"></mwc-button>
              </a>
            `:a`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_handleProcessDone(o){if(this._result=o.detail,0!==o.detail)return;const e=document.createElement("a");e.download=this.configuration+".bin",e.href=`./download.bin?configuration=${encodeURIComponent(this.configuration)}`,document.body.appendChild(e),e.click(),e.remove()}_handleRetry(){r(this.configuration)}_handleClose(){this.parentNode.removeChild(this)}};c.styles=o`
    a {
      text-decoration: none;
    }
  `,e([t()],c.prototype,"configuration",void 0),e([n()],c.prototype,"_result",void 0),c=e([i("esphome-compile-dialog")],c);
