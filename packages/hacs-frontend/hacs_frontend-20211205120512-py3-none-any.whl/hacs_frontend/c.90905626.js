import{L as o}from"./main-6af9b8d9.js";const a=()=>import("./c.23f3e6d0.js"),i=(i,l,n)=>new Promise(m=>{const r=l.cancel,s=l.confirm;o(i,"show-dialog",{dialogTag:"dialog-box",dialogImport:a,dialogParams:{...l,...n,cancel:()=>{m(!(null==n||!n.prompt)&&null),r&&r()},confirm:o=>{m(null==n||!n.prompt||o),s&&s(o)}}})}),l=(o,a)=>i(o,a),n=(o,a)=>i(o,a,{confirmation:!0});export{l as a,n as s};
