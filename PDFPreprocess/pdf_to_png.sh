# pdftoppm Bulldog.pdf a -jpeg
for p in *.pdf
do 
   pdftoppm "$p" "$p" -png
done