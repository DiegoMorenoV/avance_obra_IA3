import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputDir = `${process.cwd()}/outputs/avance_obra`;
await fs.mkdir(outputDir, { recursive: true });
const meses = ["Ene-26", "Feb-26", "Mar-26", "Abr-26", "May-26", "Jun-26", "Jul-26", "Ago-26", "Sep-26", "Oct-26", "Nov-26", "Dic-26"];
const avanceProgramado = [2, 3, 5, 8, 12, 14, 15, 14, 11, 8, 5, 3];
const avanceReal = [2, 2, 4, 7, 10, 12, 14, 15, 14, 8, 4, 1.2];
const costoProgramado = [59000000, 88500000, 147500000, 236000000, 354000000, 413000000, 442500000, 413000000, 324500000, 236000000, 147500000, 88500000];
const costoReal = [59000000, 59000000, 118000000, 206500000, 295000000, 354000000, 413000000, 442500000, 413000000, 236000000, 118000000, 35400000];
const partidas = [[1, "Obras preliminares", 165000000, 6, 6, 100, 100, "Finalizada"], [2, "Movimiento de tierras", 225000000, 8, 8, 100, 100, "Finalizada"], [3, "Cimentaciones y estructura", 885000000, 30, 30, 100, 96, "En cierre"], [4, "Albañilería y fachada", 590000000, 20, 20, 100, 92, "En cierre"], [5, "Instalaciones técnicas", 531000000, 18, 18, 100, 89, "Con retraso"], [6, "Acabados y entrega", 554000000, 18, 18, 100, 82, "Con retraso"]];

const workbook = Workbook.create();
const curva = workbook.worksheets.add("Curva S");
const avance = workbook.worksheets.add("Avance por partidas");
const resumen = workbook.worksheets.add("Resumen");
for (const sheet of [curva, avance, resumen]) { sheet.showGridLines = false; sheet.tabColor = "#6D28D9"; }
curva.mergeCells("A1:G1");
curva.getRange("A1").values = [["Datos sintéticos - Curva S de obra"]];
curva.getRange("A3:G3").values = [["Mes", "Avance fisico mensual programado (%)", "Avance fisico mensual real (%)", "Avance fisico acumulado programado (%)", "Avance fisico acumulado real (%)", "Costo mensual programado (COP)", "Costo mensual real (COP)"]];
curva.getRange("A4:G15").values = meses.map((mes, i) => [mes, avanceProgramado[i], avanceReal[i], avanceProgramado.slice(0, i + 1).reduce((a, b) => a + b, 0), avanceReal.slice(0, i + 1).reduce((a, b) => a + b, 0), costoProgramado[i], costoReal[i]]);
avance.mergeCells("A1:H1");
avance.getRange("A1").values = [["Datos sintéticos - Avance por partidas al corte de diciembre de 2026"]];
avance.getRange("A3:H3").values = [["Orden", "Partida", "Presupuesto (COP)", "Peso presupuestal (%)", "Peso fisico (%)", "Avance fisico programado (%)", "Avance fisico real (%)", "Estado"]];
avance.getRange("A4:H9").values = partidas;
resumen.mergeCells("A1:B1");
resumen.getRange("A1").values = [["Resumen del proyecto"]];
resumen.getRange("A3:B7").values = [["Periodo", "Enero a diciembre de 2026"], ["Presupuesto contractual", 2950000000], ["Avance programado al corte", 100], ["Avance real al corte", 93.2], ["Desviación de avance (p.p.)", -6.8]];

const titulo = { fill: "#2E1065", font: { bold: true, color: "#FFFFFF", size: 14 }, horizontalAlignment: "left", verticalAlignment: "center" };
const encabezado = { fill: "#6D28D9", font: { bold: true, color: "#FFFFFF" }, horizontalAlignment: "center", verticalAlignment: "center", wrapText: true, borders: { preset: "all", style: "thin", color: "#E9D5FF" } };
const cuerpo = { font: { color: "#1F1726" }, verticalAlignment: "center", borders: { preset: "inside", style: "thin", color: "#E9D5FF" } };
for (const [sheet, titleRange, headerRange, bodyRange] of [[curva, "A1:G1", "A3:G3", "A4:G15"], [avance, "A1:H1", "A3:H3", "A4:H9"], [resumen, "A1:B1", "A3:B3", "A4:B7"]]) { sheet.getRange(titleRange).format = titulo; sheet.getRange(titleRange).format.rowHeight = 28; sheet.getRange(headerRange).format = encabezado; sheet.getRange(headerRange).format.rowHeight = 34; sheet.getRange(bodyRange).format = cuerpo; sheet.getRange(bodyRange).format.rowHeight = 21; }
curva.getRange("B4:E15").format.numberFormat = "0.0";
curva.getRange("F4:G15").format.numberFormat = '"$"#,##0';
avance.getRange("C4:C9").format.numberFormat = '"$"#,##0';
avance.getRange("D4:G9").format.numberFormat = "0.0";
resumen.getRange("B5").format.numberFormat = '"$"#,##0';
resumen.getRange("B6:B8").format.numberFormat = "0.0";
curva.getRange("A:G").format.autofitColumns();
avance.getRange("A:H").format.autofitColumns();
resumen.getRange("A:B").format.autofitColumns();
curva.getRange("A1:G15").format.font = { name: "Arial", size: 10 };
avance.getRange("A1:H9").format.font = { name: "Arial", size: 10 };
resumen.getRange("A1:B7").format.font = { name: "Arial", size: 10 };
curva.freezePanes.freezeRows(3);
avance.freezePanes.freezeRows(3);
workbook.recalculate();
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(`${outputDir}/datos_sinteticos_obra.xlsx`);
const check = await workbook.inspect({ kind: "table", range: "Curva S!A1:G15", include: "values,formulas", tableMaxRows: 15, tableMaxCols: 7 });
console.log(check.ndjson);
