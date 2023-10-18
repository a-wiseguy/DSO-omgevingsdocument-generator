

install-linux-deps:
	apt install libxml2-utils xmlstarlet


download-saxon:
	mkdir saxon-download saxon
	wget -P saxon-download https://github.com/Saxonica/Saxon-HE/releases/download/SaxonHE11-6/SaxonHE11-6J.zip
	unzip saxon-download/SaxonHE11-6J.zip -d saxon


./saxon/saxon-he-11.6.jar: 
	$(MAKE) download-saxon


compile-lvbb-aanlevering: ./saxon/saxon-he-11.6.jar
	java -jar ./saxon/saxon-he-11.6.jar -s:./sch/lvbb-aanlevering.sch -xsl:./xslt/iso_dsdl_include.xsl -o:./sch/parsed/lvbb-aanlevering-step1-output.xsl
	java -jar ./saxon/saxon-he-11.6.jar -s:./sch/parsed/lvbb-aanlevering-step1-output.xsl -xsl:./xslt/iso_abstract_expand.xsl -o:./sch/parsed/lvbb-aanlevering-step2-output.xsl
	java -jar ./saxon/saxon-he-11.6.jar -s:./sch/parsed/lvbb-aanlevering-step2-output.xsl -xsl:./xslt/iso_svrl_for_xslt2.xsl -o:./sch/parsed/lvbb-aanlevering-compiled.xsl


test: ./saxon/saxon-he-11.6.jar test-xsd test-schematron


test-xsd:
	@python scripts/cmds.py xsd-all ../../output


test-schematron:
	@python scripts/cmds.py schematron-all ../../output


test-sch: ./saxon/saxon-he-11.6.jar
	java -jar ./saxon/saxon-he-11.6.jar -s:../output/akn_nl_bill_pv28-2-2093.xml -xsl:./sch/parsed/lvbb-aanlevering-compiled.xsl -o:./report/akn_nl_bill_pv28-2-2093.xml-lvbb-aanlevering.svrl
	@echo "Errors in akn_nl_bill_pv28-2-2093.xml:" 
	@xmlstarlet sel -t -v "//svrl:failed-assert/svrl:text" ./report/akn_nl_bill_pv28-2-2093.xml-lvbb-aanlevering.svrl | while IFS= read -r line; do echo -e "\e[31mError:\e[0m $$line"; done
	@echo

	#java -jar ./saxon/saxon-he-11.6.jar -s:../output/akn_nl_bill_pv28-2-2093.xml -xsl:./sch/parsed/lvbb-aanlevering-compiled.xsl -o:./report/akn_nl_bill_pv28-2-2093.xml-lvbb-aanlevering.svrl
	java -jar ./saxon/saxon-he-11.6.jar -s:../output/manifest.xml -xsl:./sch/parsed/lvbb-aanlevering-compiled.xsl -o:./report/manifest.xml-lvbb-aanlevering.svrl
	java -jar ./saxon/saxon-he-11.6.jar -s:../output/opdracht.xml -xsl:./sch/parsed/lvbb-aanlevering-compiled.xsl -o:./report/opdracht.xml-lvbb-aanlevering.svrl
