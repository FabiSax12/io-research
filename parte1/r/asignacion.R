# Asignación (PL) con lpSolve::lp.assign.
# Si la matriz no es cuadrada la completa con filas/columnas ficticias de valor 0.
# --- preámbulo (no va en las láminas) ---
raiz <- normalizePath(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE))), "..", ".."))
source(file.path(raiz, "comun", "utilidades.R"), encoding = "UTF-8")
library(lpSolve)

d <- leer_yaml("asignacion")
agentes <- d$agentes; tareas <- d$tareas
matriz <- do.call(rbind, d$matriz)                    # filas = agentes, columnas = tareas
stopifnot(nrow(matriz) == length(agentes), ncol(matriz) == length(tareas))

# --- Si no es cuadrada: filas o columnas ficticias con valor 0 ---
ajustes <- character(0)
sobran <- length(tareas) - length(agentes)
if (sobran > 0) {                                     # más tareas que agentes
  agentes <- c(agentes, paste("Ficticio", seq_len(sobran)))
  matriz <- rbind(matriz, matrix(0, sobran, ncol(matriz)))
} else if (sobran < 0) {                              # más agentes que tareas
  tareas <- c(tareas, paste("Ficticio", seq_len(-sobran)))
  matriz <- cbind(matriz, matrix(0, nrow(matriz), -sobran))
}
if (sobran != 0) {
  ajustes <- sprintf("Matriz %dx%d no cuadrada: se agregaron %d %s ficticio(s) con valor 0; quien se asigna a uno queda sin asignar",
                     length(d$agentes), length(d$tareas), abs(sobran), if (sobran > 0) "agente(s)" else "tarea(s)")
}

# --- Modelo de asignación (PL con variables 0/1) ---
sol <- lp.assign(matriz, direction = d$sentido)

estado <- estado_lp(sol$status)
optimo <- estado == "Optimal"
asig <- if (optimo) sol$solution else matrix(NA_real_, length(agentes), length(tareas))
nombres <- as.vector(outer(agentes, tareas, paste, sep = "->"))
res <- armar_resultado("asignacion", estado, if (optimo) sol$objval else NA,
                       setNames(as.vector(asig), nombres), ajustes)

pares <- which(asig > 0.5, arr.ind = TRUE)
pares <- pares[order(pares[, "row"]), , drop = FALSE]
pares <- pares[!grepl("Ficticio", agentes[pares[, "row"]]), , drop = FALSE]
tabla <- data.frame(Agente = c(agentes[pares[, "row"]], "Total"),
                    Tarea = c(ifelse(grepl("Ficticio", tareas[pares[, "col"]]), "(sin tarea)", tareas[pares[, "col"]]), ""),
                    Valor = c(matriz[pares], res$valor_objetivo))
emitir(res, d$nombre, tabla)
