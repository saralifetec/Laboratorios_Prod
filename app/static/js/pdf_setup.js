// Adiciona jsPDF via CDN para geração de PDF no frontend
// Incluir este script no bloco scripts do ensaios.html

var jsPDFScript = document.createElement('script');
jsPDFScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js';
document.head.appendChild(jsPDFScript);

var jsPDFImageScript = document.createElement('script');
jsPDFImageScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.plugin.addimage.min.js';
document.head.appendChild(jsPDFImageScript);
