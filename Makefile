# ----------------------------------------
# Makefile for cleaning LaTeX build files
# and stripping Jupyter notebooks
# ----------------------------------------

# Files and extensions to remove for LaTeX cleanup
LATEX_EXTS = aux bbl blg bcf fls fdb_latexmk log lof lot out toc \
             synctex.gz run.xml acn glo loa brf ist idx ilg ind \
             nlo tdo nav snm vrb tex~

LATEX_DIRS = Aux Bibliography out

# ----------------------------------------
# Clean LaTeX build artifacts
# ----------------------------------------
clean:
	@echo "🧹 Cleaning LaTeX build artifacts..."
	@for ext in $(LATEX_EXTS); do \
		find . -type f -name "*.$$ext" -delete; \
	done
	@for d in $(LATEX_DIRS); do \
		if [ -d "$$d" ]; then \
			echo "Removing directory $$d"; \
			rm -rf "$$d"; \
		fi; \
	done
	@echo "✔ Done."

# ----------------------------------------
# Strip all Jupyter notebook outputs
# ----------------------------------------
strip:
	@echo "🧽 Stripping all Jupyter notebooks with nbstripout..."
	@find . -type f -name "*.ipynb" -print -exec uvx nbstripout {} \;
	@echo "✔ Done."

fmt:
	@echo "✨ Running tex-fmt on all .tex files..."
	@find . -name "*.tex" -type f -exec tex-fmt {} \;
	@echo "✔ Done."


.PHONY: clean strip fmt

