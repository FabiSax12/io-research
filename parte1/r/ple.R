# Programación lineal entera con lpSolve::lp (argumento int.vec)
# --- preámbulo (no va en las láminas) ---
raiz <- normalizePath(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE))), "..", ".."))
source(file.path(raiz, "comun", "utilidades.R"), encoding = "UTF-8")
library(lpSolve)

d <- leer_yaml("ple")
stopifnot(length(d$objetivo) == length(d$variables))

A      <- do.call(rbind, lapply(d$restricciones, function(r) r$coef))
signos <- sapply(d$restricciones, function(r) r$signo)
rhs    <- sapply(d$restricciones, function(r) r$rhs)

# int.vec: posiciones de las variables enteras
enteras <- which(d$variables %in% unlist(d$enteras))
sol <- lp(direction = d$sentido, objective.in = d$objetivo,
          const.mat = A, const.dir = signos, const.rhs = rhs, int.vec = enteras)

estado <- estado_lp(sol$status)
optimo <- estado == "Optimal"
res <- armar_resultado("ple", estado, if (optimo) sol$objval else NA,
                       setNames(if (optimo) sol$solution else rep(NA_real_, length(d$variables)), d$variables))
tabla <- data.frame(Variable = c(d$variables, paste0("Z óptimo (", d$sentido, ")")),
                    Valor = c(unname(unlist(res$variables)), res$valor_objetivo))
emitir(res, d$nombre, tabla)
