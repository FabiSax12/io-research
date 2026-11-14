# Instala los paquetes de R que usa el proyecto. Ejecutar una vez:  Rscript instalar_paquetes.R
# Si la librería del sistema no es escribible (Linux/macOS sin sudo), usa una librería de usuario.
paquetes <- c("lpSolve", "yaml", "jsonlite")
faltan <- paquetes[!paquetes %in% rownames(installed.packages())]
if (length(faltan) > 0) {
  destino <- .libPaths()[file.access(.libPaths(), 2) == 0][1]      # primera librería escribible
  if (is.na(destino)) {
    destino <- Sys.getenv("R_LIBS_USER")
    dir.create(destino, recursive = TRUE, showWarnings = FALSE)
    .libPaths(c(destino, .libPaths()))
    cat("Librería del sistema no escribible; se instala en", destino, "\n")
  }
  install.packages(faltan, lib = destino, repos = "https://cloud.r-project.org")
}
for (p in paquetes) {
  cat(sprintf("%-10s %s\n", p, if (requireNamespace(p, quietly = TRUE)) "OK" else "NO SE PUDO INSTALAR"))
}
