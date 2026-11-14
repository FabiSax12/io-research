# Problema de transporte con lpSolve::lp.transport.
# Si oferta != demanda agrega un nodo ficticio de costo 0.
# --- preámbulo (no va en las láminas) ---
raiz <- normalizePath(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE))), "..", ".."))
source(file.path(raiz, "comun", "utilidades.R"), encoding = "UTF-8")
library(lpSolve)

d <- leer_yaml("transporte")
origenes <- d$origenes; destinos <- d$destinos
oferta <- unlist(d$oferta); demanda <- unlist(d$demanda)
costo <- do.call(rbind, d$costos)                     # filas = orígenes, columnas = destinos
stopifnot(nrow(costo) == length(origenes), ncol(costo) == length(destinos),
          length(oferta) == length(origenes), length(demanda) == length(destinos))

# --- Balanceo: el exceso se absorbe con un nodo ficticio de costo 0 ---
ajustes <- character(0)
dif <- sum(oferta) - sum(demanda)
if (dif > 1e-9) {
  ajustes <- sprintf("Oferta (%s) > demanda (%s): se agregó el destino ficticio con demanda %s y costo 0",
                     fmt(sum(oferta)), fmt(sum(demanda)), fmt(dif))
  destinos <- c(destinos, "Ficticio"); demanda <- c(demanda, dif)
  costo <- cbind(costo, 0)
} else if (dif < -1e-9) {
  ajustes <- sprintf("Demanda (%s) > oferta (%s): se agregó el origen ficticio con oferta %s y costo 0",
                     fmt(sum(demanda)), fmt(sum(oferta)), fmt(-dif))
  origenes <- c(origenes, "Ficticio"); oferta <- c(oferta, -dif)
  costo <- rbind(costo, 0)
}

# --- Modelo: cada origen despacha toda su oferta y cada destino recibe su demanda ---
sol <- lp.transport(costo, direction = "min",
                    row.signs = rep("=", length(origenes)), row.rhs = oferta,
                    col.signs = rep("=", length(destinos)), col.rhs = demanda,
                    integers = NULL)                  # variables continuas, igual que en Python

estado <- estado_lp(sol$status)
optimo <- estado == "Optimal"
envios <- if (optimo) sol$solution else matrix(NA_real_, length(origenes), length(destinos))
dimnames(envios) <- list(origenes, destinos)
nombres <- as.vector(outer(origenes, destinos, paste, sep = "->"))   # recorre por columnas, como la matriz
res <- armar_resultado("transporte", estado, if (optimo) sol$objval else NA,
                       setNames(as.vector(envios), nombres), ajustes)

# Para la tabla de la lámina se reordena a un valor por origen (fila) y destino (columna)
tabla <- data.frame(`Envíos` = c(origenes, "Demanda"), check.names = FALSE)
for (j in seq_along(destinos)) tabla[[destinos[j]]] <- c(unname(envios[, j]), demanda[j])
tabla$Oferta <- c(oferta, sum(demanda))
emitir(res, d$nombre, tabla)
