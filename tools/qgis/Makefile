
download-saxon:
	mkdir saxon-download saxon
	wget -P saxon-download https://github.com/Saxonica/Saxon-HE/releases/download/SaxonHE11-6/SaxonHE11-6J.zip
	unzip saxon-download/SaxonHE11-6J.zip -d saxon


./saxon/saxon-he-11.6.jar: 
	$(MAKE) download-saxon


parse: ./saxon/saxon-he-11.6.jar
ifndef I
	$(error I (input) is not set)
endif
ifndef O
	$(error O (output) is not set)
endif
	java -jar ./saxon/saxon-he-11.6.jar -s:$(I) -xsl:./data/GIO2Qgis.xsl -o:$(O)
