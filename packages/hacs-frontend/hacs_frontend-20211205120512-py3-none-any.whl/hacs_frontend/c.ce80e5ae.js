import{_ as t,H as i,e,m as o,p as s,n as r}from"./main-6af9b8d9.js";import{m as a}from"./c.03d6465a.js";import"./c.c6a9dc5a.js";import"./c.9cdfab00.js";import"./c.3d0d18cf.js";import"./c.9f27b448.js";import"./c.0a038163.js";let d=t([r("hacs-generic-dialog")],(function(t,i){return{F:class extends i{constructor(...i){super(...i),t(this)}},d:[{kind:"field",decorators:[e({type:Boolean})],key:"markdown",value:()=>!1},{kind:"field",decorators:[e()],key:"repository",value:void 0},{kind:"field",decorators:[e()],key:"header",value:void 0},{kind:"field",decorators:[e()],key:"content",value:void 0},{kind:"field",key:"_getRepository",value:()=>o((t,i)=>null==t?void 0:t.find(t=>t.id===i))},{kind:"method",key:"render",value:function(){if(!this.active||!this.repository)return s``;const t=this._getRepository(this.hacs.repositories,this.repository);return s`
      <hacs-dialog .active=${this.active} .narrow=${this.narrow} .hass=${this.hass}>
        <div slot="header">${this.header||""}</div>
        ${this.markdown?this.repository?a.html(this.content||"",t):a.html(this.content||""):this.content||""}
      </hacs-dialog>
    `}}]}}),i);export{d as HacsGenericDialog};
