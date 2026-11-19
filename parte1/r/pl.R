# Programación lineal con lpSolve::lp
# --- preámbulo (no va en las láminas) ---
raiz <- normalizePath(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE))), "..", ".."))
source(file.path(raiz, "comun", "utilidades.R"), encoding = "UTF-8")
library(lpSolve)

d <- leer_yaml("pl")
stopifnot(length(d$objetivo) == length(d$variables))

# Matriz de coeficientes (una fila por restricción), signos y lados derechos
A      <- do.call(rbind, lapply(d$restricciones, function(r) r$coef))
signos <- sapply(d$restricciones, function(r) r$signo)
rhs    <- sapply(d$restricciones, function(r) r$rhs)

# lp() asume variables >= 0; compute.sens = TRUE calcula los precios sombra (sol$duals)
sol <- lp(direction = d$sentido, objective.in = d$objetivo,
          const.mat = A, const.dir = signos, const.rhs = rhs, compute.sens = TRUE)
sombra <- sol$duals[seq_len(nrow(A))]   # los primeros duales son los de las restricciones

estado <- estado_lp(sol$status)
optimo <- estado == "Optimal"
res <- armar_resultado("pl", estado, if (optimo) sol$objval else NA,
                       setNames(if (optimo) sol$solution else rep(NA_real_, length(d$variables)), d$variables),
                       precios_sombra = if (optimo) as.list(sapply(sombra, limpiar)) else list())
nombres_r <- sapply(d$restricciones, function(r) r$nombre)
tabla <- data.frame(Variable = c(d$variables, paste0("Z óptimo (", d$sentido, ")"),
                                 if (optimo) paste("Sombra:", nombres_r)),
                    Valor = c(unname(unlist(res$variables)), res$valor_objetivo, if (optimo) sombra))
emitir(res, d$nombre, tabla)
