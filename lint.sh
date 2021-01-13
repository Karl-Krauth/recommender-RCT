pylint --rcfile=.pylintrc backend -f parseable -r n --load-plugins pylint_quotes
pycodestyle backend --max-line-length=100
pydocstyle backend
