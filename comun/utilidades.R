# Utilidades mínimas de I/O compartidas por los scripts de R.
# Leer YAML, guardar JSON, imprimir la solución y guardar la tabla como PNG.
# Requiere la variable `raiz` (la define el preámbulo de cada script).
# Si existe la variable de entorno IO_DIR, se lee de IO_DIR/datos y se escribe
# en IO_DIR/resultados y IO_DIR/capturas (lo usan los tests).

suppressPackageStartupMessages({ library(yaml); library(jsonlite) })

BASE <- Sys.getenv("IO_DIR", unset = raiz)
LENGUAJE <- "r"

# Los nombres como y/n (variables, nodos) deben quedar como texto, no como TRUE/FALSE
leer_yaml <- function(nombre) {
  yaml.load_file(file.path(BASE, "datos", paste0(nombre, ".yaml")),
                 handlers = list("bool#yes" = function(x) x, "bool#no" = function(x) x))
}

ruta_salida <- function(carpeta, archivo) {
  dir.create(file.path(BASE, carpeta), showWarnings = FALSE, recursive = TRUE)
  file.path(BASE, carpeta, archivo)
}

# Número sin decimales sobrantes (2 -> "2", 2.5 -> "2.5")
fmt <- function(x) {
  sapply(x, function(v) {
    if (is.na(v)) "n/d" else format(round(v, 4), scientific = FALSE, trim = TRUE, drop0trailing = TRUE)
  })
}

limpiar <- function(x) if (is.null(x) || is.na(x)) NA_real_ else round(x, 6) + 0

# Códigos de estado de lpSolve -> mismos textos que usa PuLP en Python
estado_lp <- function(codigo) {
  switch(as.character(codigo), "0" = "Optimal", "2" = "Infeasible", "3" = "Unbounded", paste("Estado", codigo))
}

# Lista con el esquema común a Python y R (se guarda como JSON).
# `variables` es un vector numérico con nombres; `verificacion` es NA o una lista(metodo, valor, coincide).
armar_resultado <- function(problema, estado, valor, variables, ajustes = character(0),
                            verificacion = NA, ...) {
  list(problema = problema, lenguaje = LENGUAJE, estado = estado,
       valor_objetivo = limpiar(valor),
       variables = as.list(sapply(variables, limpiar)),
       ajustes = as.list(ajustes), verificacion = verificacion, ...)
}

# Guarda una tabla (data.frame) como imagen PNG lista para las láminas
tabla_png <- function(ruta, titulo, tabla) {
  tabla[] <- lapply(tabla, function(col) if (is.numeric(col)) fmt(col) else as.character(col))
  nf <- nrow(tabla) + 1
  nc <- ncol(tabla)
  png(ruta, width = max(800, 190 * nc), height = 120 + 46 * nf, res = 130,
      type = if (isTRUE(capabilities("cairo"))) "cairo" else getOption("bitmapType"))
  par(mar = c(0.5, 0.5, 2.5, 0.5))
  plot.new()
  plot.window(xlim = c(0, nc), ylim = c(nf, 0))
  title(titulo, font.main = 2, cex.main = 1)
  rect(0, 0, nc, 1, col = "#dbe7f5", border = NA)
  for (j in seq_len(nc)) {
    text(j - 0.5, 0.5, names(tabla)[j], font = 2)
    for (i in seq_len(nrow(tabla))) text(j - 0.5, i + 0.5, tabla[i, j])
  }
  segments(0, 0:nf, nc, 0:nf, col = "grey40")
  segments(0:nc, 0, 0:nc, nf, col = "grey40")
  invisible(dev.off())
}

# Imprime la solución, guarda resultados/<problema>_r.json y la tabla PNG
emitir <- function(res, titulo, tabla) {
  cat(sprintf("=== %s ===\n", titulo))
  cat(sprintf("Estado: %s\n", res$estado))
  cat(sprintf("Valor óptimo: %s\n", fmt(res$valor_objetivo)))
  cat("Solución (variables distintas de cero):\n")
  for (nombre in names(res$variables)) {
    v <- res$variables[[nombre]]
    if (!is.na(v) && abs(v) > 1e-9) cat(sprintf("  %s = %s\n", nombre, fmt(v)))
  }
  for (aviso in res$ajustes) cat(sprintf("Ajuste: %s\n", aviso))
  v <- res$verificacion
  if (is.list(v)) cat(sprintf("Verificación (%s): %s -> %s\n", v$metodo, fmt(v$valor),
                              if (v$coincide) "coincide" else "NO COINCIDE"))

  nombre <- paste0(res$problema, "_", LENGUAJE)
  write_json(res, ruta_salida("resultados", paste0(nombre, ".json")),
             auto_unbox = TRUE, pretty = TRUE, digits = NA, na = "null")
  optimo <- if (is.na(res$valor_objetivo)) "" else paste0(" | óptimo = ", fmt(res$valor_objetivo))
  tabla_png(ruta_salida("capturas", paste0(nombre, "_tabla.png")),
            paste0(titulo, " (", LENGUAJE, ")", optimo), tabla)
}
