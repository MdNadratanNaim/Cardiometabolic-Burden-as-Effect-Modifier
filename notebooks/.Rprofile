# Activates the parent project's renv environment for notebooks/ specifically.
#
# Why this file exists (in addition to the repo-root .Rprofile): R only auto-sources
# .Rprofile from the *current working directory* on startup -- it does not walk up
# parent directories. Jupyter launches the R (IRkernel) process with the working
# directory set to wherever the .ipynb file lives, i.e. notebooks/, not the repo root.
# Without this file, the R kernel silently falls back to the system-wide R library
# instead of this project's pinned renv library, defeating the whole point of renv.
#
# renv::load() is used instead of source("../renv/activate.R") because activate.R's
# own bootstrap logic hardcodes `project <- getwd()`, which is wrong when sourced from
# a subdirectory -- it would try to treat notebooks/ itself as the project root and
# fail. renv::load(path) takes the project path explicitly and has no such issue.
local({
  has_renv <- tryCatch({ loadNamespace("renv"); TRUE }, error = function(e) FALSE)
  if (has_renv) {
    renv::load(normalizePath(".."))
  } else {
    # renv itself isn't installed anywhere yet -- fall back to the standard
    # getwd()-based autoloader, temporarily switching to the project root so its
    # getwd()-based project detection resolves correctly.
    owd <- getwd()
    setwd("..")
    source("renv/activate.R")
    setwd(owd)
  }
})
