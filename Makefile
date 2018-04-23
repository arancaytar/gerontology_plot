all:
	python3 draw_plots.py
	python3 draw_plots.py labeled
	convert plot-unlabeled.svg plot-unlabeled.png
