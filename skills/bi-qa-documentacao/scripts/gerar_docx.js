// Gera a documentação .docx a partir do JSON de extrair_modelo.py.
// Uso: node gerar_docx.js modelo.json documentacao-modelo.docx ["Nome do Modelo"] [corHex]
// Requer: npm install docx
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, ShadingType, TableOfContents, PageBreak, Footer, AlignmentType, BorderStyle,
} = require("docx");

const [, , entrada, saida = "documentacao-modelo.docx", titulo = "Documentação do Modelo", cor = "2B579A"] = process.argv;
if (!entrada) { console.error("Uso: node gerar_docx.js modelo.json saida.docx [titulo] [corHex]"); process.exit(2); }
const m = JSON.parse(fs.readFileSync(entrada, "utf8"));

const LARGURA = 9360; // A4/Carta com margens de 1" em DXA
const borda = { style: BorderStyle.SINGLE, size: 4, color: "D0D5DD" };
const bordas = { top: borda, bottom: borda, left: borda, right: borda };

function tabela(cabecalho, linhas, pesos) {
  const total = pesos.reduce((a, b) => a + b, 0);
  const larguras = pesos.map(p => Math.round((LARGURA * p) / total));
  const celula = (texto, i, head) => new TableCell({
    borders: bordas,
    width: { size: larguras[i], type: WidthType.DXA },
    shading: head ? { fill: cor, type: ShadingType.CLEAR, color: "auto" } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ children: [new TextRun({ text: String(texto ?? "—"), bold: head, color: head ? "FFFFFF" : undefined, size: 18 })] })],
  });
  return new Table({
    width: { size: LARGURA, type: WidthType.DXA },
    columnWidths: larguras,
    rows: [
      new TableRow({ tableHeader: true, children: cabecalho.map((t, i) => celula(t, i, true)) }),
      ...linhas.map(l => new TableRow({ children: l.map((t, i) => celula(t, i, false)) })),
    ],
  });
}

const codigo = texto => texto.split("\n").map(l => new Paragraph({
  shading: { fill: "F3F4F6", type: ShadingType.CLEAR, color: "auto" },
  spacing: { after: 0 },
  children: [new TextRun({ text: l || " ", font: "Consolas", size: 18 })],
}));

const papel = nome => nome.startsWith("TabFat") ? "Fato" : nome.startsWith("TabDim") ? "Dimensão"
  : nome.startsWith("TabFlt") ? "Monolítica" : nome.startsWith("TabPon") ? "Ponte" : "A classificar";

const filhos = [
  new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun(titulo)] }),
  new Paragraph({ children: [new TextRun({ text: `Gerado a partir do commit ${m.origem?.commit ?? "(fora do Git)"}${m.origem?.data ? " de " + m.origem.data : ""}.`, color: "6B7280" })] }),
  new TableOfContents("Sumário", { hyperlink: true, headingStyleRange: "1-2" }),
  new Paragraph({ children: [new PageBreak()] }),

  new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Tabelas")] }),
  tabela(["Tabela", "Papel", "Armazenamento", "Colunas", "Medidas"],
    m.tabelas.map(t => [t.nome, papel(t.nome), t.modo, t.colunas.length, t.medidas.length]), [3, 2, 2, 1.3, 1.3]),
];

for (const t of m.tabelas) {
  if (!t.colunas.length) continue;
  filhos.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t.nome)] }));
  if (t.descricao) filhos.push(new Paragraph(t.descricao));
  filhos.push(tabela(["Coluna", "Tipo", "Origem", "Oculta"],
    t.colunas.map(c => [c.nome, c.props.dataType, c.props.sourceColumn, c.props.isHidden === "true" ? "Sim" : "Não"]), [3, 2, 3, 1]));
}

filhos.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: true, children: [new TextRun("Relacionamentos")] }));
filhos.push(m.relacionamentos.length
  ? tabela(["De", "Para", "Filtro", "Ativo"], m.relacionamentos.map(r => [r.fromColumn, r.toColumn,
      r.crossFilteringBehavior === "bothDirections" ? "Ambas" : "Única", r.isActive === "false" ? "Não" : "Sim"]), [3, 3, 1, 1])
  : new Paragraph("Nenhum relacionamento encontrado."));

filhos.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: true, children: [new TextRun("Medidas")] }));
for (const t of m.tabelas) for (const med of t.medidas) {
  filhos.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(`${med.nome}`)] }));
  filhos.push(new Paragraph({ children: [new TextRun({ text: `Tabela: ${t.nome} · Pasta: ${med.props.displayFolder ?? "—"} · Formato: ${med.props.formatString ?? "❗ sem formato"}`, color: "6B7280", size: 18 })] }));
  filhos.push(new Paragraph(med.descricao ?? "❗ Sem descrição (///)."));
  filhos.push(...codigo(med.expressao ?? ""));
}

if (m.paginas?.length) {
  filhos.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: true, children: [new TextRun("Páginas do relatório")] }));
  for (const p of m.paginas) {
    filhos.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(p.nome)] }));
    filhos.push(tabela(["Visual", "Tipo", "Campos e medidas"], p.visuais.map(v => [v.nome, v.tipo, v.campos.join(", ")]), [2, 2, 5]));
  }
}

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Segoe UI", size: 20 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", run: { size: 48, bold: true, color: cor }, paragraph: { spacing: { after: 200 } } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 32, bold: true, color: cor }, paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 24, bold: true }, paragraph: { spacing: { before: 200, after: 80 }, outlineLevel: 1 } },
    ],
  },
  features: { updateFields: true },
  sections: [{
    properties: { page: { margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: `commit ${m.origem?.commit ?? "—"}`, size: 16, color: "6B7280" })] })] }) },
    children: filhos,
  }],
});

Packer.toBuffer(doc).then(buf => { fs.writeFileSync(saida, buf); console.log(`✔️ ${saida}`); });
