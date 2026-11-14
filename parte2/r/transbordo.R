# Transbordo: (1) modelo de red con conservación de flujo y (2) modelo matricial con buffer.
# Uso:  Rscript parte2/r/transbordo.R [nombre_del_yaml]     (por defecto: transbordo)
# Si oferta != demanda agrega un nodo ficticio. Guarda además la matriz ampliada (CSV + PNG).
# --- preámbulo (no va en las láminas) ---
raiz <- normalizePath(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE))), "..", ".."))
source(file.path(raiz, "comun", "utilidades.R"), encoding = "UTF-8")
library(lpSolve)

args <- commandArgs(trailingOnly = TRUE)
nombre <- if (length(args) > 0) args[1] else "transbordo"
d <- leer_yaml(nombre)

# ---------------------------------------------------------------- 1. Datos
campo <- function(n, x) if (is.null(n[[x]])) 0 else n[[x]]       # oferta/demanda ausentes valen 0
nodos <- data.frame(nombre  = sapply(d$nodos, function(n) as.character(n$nombre)),
                    tipo    = sapply(d$nodos, function(n) n$tipo),
                    oferta  = sapply(d$nodos, campo, "oferta"),
                    demanda = sapply(d$nodos, campo, "demanda"), stringsAsFactors = FALSE)
arcos <- data.frame(desde = sapply(d$arcos, function(a) as.character(a$desde)),
                    hasta = sapply(d$arcos, function(a) as.character(a$hasta)),
                    costo = sapply(d$arcos, function(a) a$costo), stringsAsFactors = FALSE)
stopifnot(all(c(arcos$desde, arcos$hasta) %in% nodos$nombre))

# ---------------------------------------------------------------- 2. Balanceo (oferta vs demanda)
ajustes <- character(0)
dif <- sum(nodos$oferta) - sum(nodos$demanda)
origenes <- nodos$nombre[nodos$tipo == "origen"]
destinos <- nodos$nombre[nodos$tipo == "destino"]
if (dif > 1e-9) {                   # sobra oferta: destino ficticio que recibe el excedente
  ajustes <- sprintf("Oferta (%s) > demanda (%s): se agregó el nodo destino Ficticio con demanda %s y arcos de costo 0 desde cada origen",
                     fmt(sum(nodos$oferta)), fmt(sum(nodos$demanda)), fmt(dif))
  nodos <- rbind(nodos, data.frame(nombre = "Ficticio", tipo = "destino", oferta = 0, demanda = dif))
  arcos <- rbind(arcos, data.frame(desde = origenes, hasta = "Ficticio", costo = 0))
} else if (dif < -1e-9) {           # falta oferta: origen ficticio que cubre el faltante
  ajustes <- sprintf("Demanda (%s) > oferta (%s): se agregó el nodo origen Ficticio con oferta %s y arcos de costo 0 hacia cada destino",
                     fmt(sum(nodos$demanda)), fmt(sum(nodos$oferta)), fmt(-dif))
  nodos <- rbind(nodos, data.frame(nombre = "Ficticio", tipo = "origen", oferta = -dif, demanda = 0))
  arcos <- rbind(arcos, data.frame(desde = "Ficticio", hasta = destinos, costo = 0))
}
nodos <- nodos[order(match(nodos$tipo, c("origen", "transbordo", "destino"))), ]   # orígenes, transbordos, destinos
nombres <- nodos$nombre
n <- length(nombres)

# ---------------------------------------------------------------- 3. Modelo de red (conservación de flujo)
# Fila = nodo, columna = arco: +1 si el arco sale del nodo, -1 si entra. sale - entra = oferta - demanda
A <- outer(nombres, arcos$desde, "==") * 1 - outer(nombres, arcos$hasta, "==") * 1
red <- lp("min", arcos$costo, A, rep("=", n), nodos$oferta - nodos$demanda)
estado <- estado_lp(red$status)
valor_red <- if (estado == "Optimal") red$objval else NA
flujo <- if (estado == "Optimal") red$solution else rep(NA_real_, nrow(arcos))

# ---------------------------------------------------------------- 4. Modelo matricial con buffer
B <- max(sum(nodos$oferta), sum(nodos$demanda))                  # buffer = flujo total
cota <- B * (n - 1) * max(arcos$costo)                           # ningún plan sin M cuesta más que esto
M <- 10^nchar(sprintf("%.0f", floor(cota)))                      # potencia de 10 mayor que cota
C <- matrix(M, n, n, dimnames = list(nombres, nombres))          # arcos inexistentes = M
diag(C) <- 0                                                     # buffer sin usar
C[cbind(match(arcos$desde, nombres), match(arcos$hasta, nombres))] <- arcos$costo
oferta_amp  <- nodos$oferta + B                                  # fila: oferta + B
demanda_amp <- nodos$demanda + B                                 # columna: demanda + B

buf <- lp.transport(C, "min", rep("=", n), oferta_amp, rep("=", n), demanda_amp, integers = NULL)
valor_buf <- if (buf$status == 0) buf$objval else NA
if (!is.na(valor_buf) && valor_buf >= M) {                       # usó un arco inexistente: no hay plan factible
  estado <- "Infeasible"; valor_buf <- NA
}
coincide <- !is.na(valor_red) && !is.na(valor_buf) && abs(valor_red - valor_buf) < 1e-6

# ---------------------------------------------------------------- 5. Resultado (JSON, consola, tabla PNG)
res <- armar_resultado(nombre, estado, valor_red, setNames(flujo, paste0(arcos$desde, "->", arcos$hasta)), ajustes,
                       verificacion = list(metodo = "transporte con buffer", valor = limpiar(valor_buf), coincide = coincide),
                       buffer = list(B = B, M = M))
cat(sprintf("Buffer B = %s, M = %s\n", fmt(B), fmt(M)))
cat(sprintf("Modelo de red: %s | Modelo con buffer: %s\n", fmt(valor_red), fmt(valor_buf)))
usados <- which(flujo > 1e-9)
tabla <- data.frame(Arco = c(paste(arcos$desde[usados], "->", arcos$hasta[usados]), "Costo total"),
                    `Costo unitario` = c(fmt(arcos$costo[usados]), ""),
                    Flujo = c(flujo[usados], res$valor_objetivo), check.names = FALSE)
emitir(res, d$nombre, tabla)

# ---------------------------------------------------------------- 6. Matriz ampliada (CSV + PNG)
cuerpo <- cbind(nombres, matrix(ifelse(C == M, "M", fmt(C)), n, n), fmt(oferta_amp))
cuerpo <- rbind(cuerpo, c("Demanda", fmt(demanda_amp), ""))
matriz <- as.data.frame(cuerpo, stringsAsFactors = FALSE)
names(matriz) <- c("De / A", nombres, "Oferta")
write.csv(matriz, ruta_salida("capturas", paste0(nombre, "_matriz_r.csv")), row.names = FALSE, fileEncoding = "UTF-8")
tabla_png(ruta_salida("capturas", paste0(nombre, "_matriz_r.png")),
          sprintf("Matriz de costos ampliada (B = %s, M = %s)", fmt(B), fmt(M)), matriz)
cat(sprintf("Archivos: capturas/%s_matriz_r.csv/.png\n", nombre))
