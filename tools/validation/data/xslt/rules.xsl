<?xml version="1.0" standalone="yes"?>
<axsl:stylesheet xmlns:xs="http://www.w3.org/2001/XMLSchema"
   xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:saxon="http://saxon.sf.net/"
   xmlns:axsl="http://www.w3.org/1999/XSL/Transform"
   xmlns:schold="http://www.ascc.net/xml/schematron"
   xmlns:iso="http://purl.oclc.org/dsdl/schematron" xmlns:xhtml="http://www.w3.org/1999/xhtml"
   xmlns:tekst="https://standaarden.overheid.nl/stop/imop/tekst/"
   xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"><!--Implementers:
   please note that overriding process-prolog or process-root is 
    the preferred method for meta-stylesheets to use where possible. -->
   <axsl:param name="archiveDirParameter" />
   <axsl:param name="archiveNameParameter" />
   <axsl:param name="fileNameParameter" />
   <axsl:param name="fileDirParameter" />
   <axsl:variable name="document-uri"><axsl:value-of select="document-uri(/)" /></axsl:variable>

   <!--PHASES-->


   <!--PROLOG-->
   <axsl:output xmlns:svrl="http://purl.oclc.org/dsdl/svrl" method="xml" omit-xml-declaration="no"
      standalone="yes" indent="yes" />

   <!--XSD
   TYPES FOR XSLT2-->


   <!--KEYS
   AND FUNCTIONS-->
   <axsl:key
      match="tekst:*[@eId][not(ancestor-or-self::tekst:*[@componentnaam])][not(ancestor-or-self::tekst:WijzigInstructies)]"
      name="alleEIDs" use="@eId" />
   <axsl:key
      match="tekst:*[@wId][not(ancestor-or-self::tekst:*[@componentnaam])][not(ancestor-or-self::tekst:WijzigInstructies)]"
      name="alleWIDs" use="@wId" />
   <axsl:key
      match="tekst:Noot[not(ancestor-or-self::tekst:*[@componentnaam])][not(ancestor-or-self::tekst:WijzigInstructies)]"
      name="alleNootIDs" use="@id" />

   <!--DEFAULT
   RULES-->


   <!--MODE:
   SCHEMATRON-SELECT-FULL-PATH-->
   <!--This
   mode can be used to generate an ugly though full XPath for locators-->
   <axsl:template match="*" mode="schematron-select-full-path"><axsl:apply-templates select="."
         mode="schematron-get-full-path" /></axsl:template>

   <!--MODE:
   SCHEMATRON-FULL-PATH-->
   <!--This
   mode can be used to generate an ugly though full XPath for locators-->
   <axsl:template match="*" mode="schematron-get-full-path"><axsl:apply-templates select="parent::*"
         mode="schematron-get-full-path" /><axsl:text>/</axsl:text><axsl:choose>
         <axsl:when test="namespace-uri()=''"><axsl:value-of select="name()" /></axsl:when>
         <axsl:otherwise><axsl:text>*:</axsl:text><axsl:value-of select="local-name()" /><axsl:text>
      [namespace-uri()='</axsl:text><axsl:value-of select="namespace-uri()" /><axsl:text>']</axsl:text></axsl:otherwise>
      </axsl:choose><axsl:variable
         name="preceding"
         select="count(preceding-sibling::*[local-name()=local-name(current())                                   and namespace-uri() = namespace-uri(current())])" /><axsl:text>
      [</axsl:text><axsl:value-of select="1+ $preceding" /><axsl:text>]</axsl:text></axsl:template>
   <axsl:template match="@*" mode="schematron-get-full-path"><axsl:apply-templates
         select="parent::*" mode="schematron-get-full-path" /><axsl:text>/</axsl:text><axsl:choose>
         <axsl:when test="namespace-uri()=''">@<axsl:value-of select="name()" /></axsl:when>
         <axsl:otherwise><axsl:text>@*[local-name()='</axsl:text><axsl:value-of
               select="local-name()" /><axsl:text>' and namespace-uri()='</axsl:text><axsl:value-of
               select="namespace-uri()" /><axsl:text>']</axsl:text></axsl:otherwise>
      </axsl:choose></axsl:template>

   <!--MODE:
   SCHEMATRON-FULL-PATH-2-->
   <!--This
   mode can be used to generate prefixed XPath for humans-->
   <axsl:template match="node() | @*" mode="schematron-get-full-path-2"><axsl:for-each
         select="ancestor-or-self::*"><axsl:text>/</axsl:text><axsl:value-of select="name(.)" /><axsl:if
            test="preceding-sibling::*[name(.)=name(current())]"><axsl:text>[</axsl:text><axsl:value-of
               select="count(preceding-sibling::*[name(.)=name(current())])+1" /><axsl:text>]</axsl:text></axsl:if></axsl:for-each><axsl:if
         test="not(self::*)"><axsl:text />/@<axsl:value-of select="name(.)" /></axsl:if></axsl:template><!--MODE:
   SCHEMATRON-FULL-PATH-3-->
   <!--This
   mode can be used to generate prefixed XPath for humans 
	(Top-level element has index)-->
   <axsl:template match="node() | @*" mode="schematron-get-full-path-3"><axsl:for-each
         select="ancestor-or-self::*"><axsl:text>/</axsl:text><axsl:value-of select="name(.)" /><axsl:if
            test="parent::*"><axsl:text>[</axsl:text><axsl:value-of
               select="count(preceding-sibling::*[name(.)=name(current())])+1" /><axsl:text>]</axsl:text></axsl:if></axsl:for-each><axsl:if
         test="not(self::*)"><axsl:text />/@<axsl:value-of select="name(.)" /></axsl:if></axsl:template>

   <!--MODE:
   GENERATE-ID-FROM-PATH -->
   <axsl:template match="/" mode="generate-id-from-path" />
   <axsl:template match="text()" mode="generate-id-from-path"><axsl:apply-templates
         select="parent::*" mode="generate-id-from-path" /><axsl:value-of
         select="concat('.text-', 1+count(preceding-sibling::text()), '-')" /></axsl:template>
   <axsl:template match="comment()" mode="generate-id-from-path"><axsl:apply-templates
         select="parent::*" mode="generate-id-from-path" /><axsl:value-of
         select="concat('.comment-', 1+count(preceding-sibling::comment()), '-')" /></axsl:template>
   <axsl:template match="processing-instruction()" mode="generate-id-from-path"><axsl:apply-templates
         select="parent::*" mode="generate-id-from-path" /><axsl:value-of
         select="concat('.processing-instruction-', 1+count(preceding-sibling::processing-instruction()), '-')" /></axsl:template>
   <axsl:template match="@*" mode="generate-id-from-path"><axsl:apply-templates select="parent::*"
         mode="generate-id-from-path" /><axsl:value-of select="concat('.@', name())" /></axsl:template>
   <axsl:template match="*" mode="generate-id-from-path" priority="-0.5"><axsl:apply-templates
         select="parent::*" mode="generate-id-from-path" /><axsl:text>.</axsl:text><axsl:value-of
         select="concat('.',name(),'-',1+count(preceding-sibling::*[name()=name(current())]),'-')" /></axsl:template>

   <!--MODE:
   GENERATE-ID-2 -->
   <axsl:template match="/" mode="generate-id-2">U</axsl:template>
   <axsl:template match="*" mode="generate-id-2" priority="2"><axsl:text>U</axsl:text><axsl:number
         level="multiple" count="*" /></axsl:template>
   <axsl:template match="node()" mode="generate-id-2"><axsl:text>U.</axsl:text><axsl:number
         level="multiple" count="*" /><axsl:text>n</axsl:text><axsl:number count="node()" /></axsl:template>
   <axsl:template match="@*" mode="generate-id-2"><axsl:text>U.</axsl:text><axsl:number
         level="multiple" count="*" /><axsl:text>_</axsl:text><axsl:value-of
         select="string-length(local-name(.))" /><axsl:text>_</axsl:text><axsl:value-of
         select="translate(name(),':','.')" /></axsl:template><!--Strip
   characters-->
   <axsl:template match="text()" priority="-1" />

   <!--SCHEMA
   SETUP-->
   <axsl:template match="/"><svrl:schematron-output xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
         title="" schemaVersion="">
         <axsl:comment><axsl:value-of select="$archiveDirParameter" />   <axsl:value-of
               select="$archiveNameParameter" />   <axsl:value-of select="$fileNameParameter" />   <axsl:value-of
               select="$fileDirParameter" /></axsl:comment>
         <svrl:text>Versie 1.3.0</svrl:text>
         <svrl:text>Schematron voor aanvullende validatie voor imop-tekst.xsd</svrl:text>
         <svrl:ns-prefix-in-attribute-values uri="https://standaarden.overheid.nl/stop/imop/tekst/"
            prefix="tekst" />
         <svrl:ns-prefix-in-attribute-values uri="http://www.w3.org/1999/XSL/Transform" prefix="xsl" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_001</axsl:attribute>
            <axsl:attribute name="name">Lijst - Nummering lijstitems</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M4" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_022</axsl:attribute>
            <axsl:attribute name="name">Alinea - Bevat content</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M5" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_027</axsl:attribute>
            <axsl:attribute name="name">Kop - Bevat content</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M6" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_003</axsl:attribute>
            <axsl:attribute name="name">Tabel - Referenties naar een noot</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M7" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_004</axsl:attribute>
            <axsl:attribute name="name">Lijst - plaatsing tabel in een lijst</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M8" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_032</axsl:attribute>
            <axsl:attribute name="name">Illustratie - attributen kleur en schaal worden niet
      ondersteund</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M9" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_006</axsl:attribute>
            <axsl:attribute name="name">Referentie intern - correcte verwijzing</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M10" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_028</axsl:attribute>
            <axsl:attribute name="name">Referentie informatieobject - correcte verwijzing</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M11" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_007</axsl:attribute>
            <axsl:attribute name="name">Referentie extern informatieobject</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M12" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_008</axsl:attribute>
            <axsl:attribute name="name">Identificatie - correct gebruik wId, eId </axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M13" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_023</axsl:attribute>
            <axsl:attribute name="name">RegelingTijdelijkdeel - WijzigArtikel niet toegestaan</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M14" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_026</axsl:attribute>
            <axsl:attribute name="name">RegelingCompact - WijzigArtikel niet toegestaan</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M15" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_009</axsl:attribute>
            <axsl:attribute name="name">Mutaties - Wijzigingen tekstueel</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M16" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_010</axsl:attribute>
            <axsl:attribute name="name">Mutaties - Wijzigingen structuur</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M17" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_011</axsl:attribute>
            <axsl:attribute name="name">Identificatie - Alle wId en eId buiten een AKN-component
      zijn uniek</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M21" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_020</axsl:attribute>
            <axsl:attribute name="name">Identificatie - AKN-naamgeving voor eId en wId</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M22" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_014</axsl:attribute>
            <axsl:attribute name="name">Tabel - minimale opbouw</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M23" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_016</axsl:attribute>
            <axsl:attribute name="name">Tabel - positie en identificatie van een tabelcel</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M24" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M25" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M26" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_017</axsl:attribute>
            <axsl:attribute name="name">Tabel - het aantal cellen is correct</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M27" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_033</axsl:attribute>
            <axsl:attribute name="name">Externe referentie, notatie</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M28" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_037</axsl:attribute>
            <axsl:attribute name="name">Gereserveerd zonder opvolgende elementen</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M29" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_070</axsl:attribute>
            <axsl:attribute name="name">Vervallen zonder opvolgende elementen</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M30" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_039</axsl:attribute>
            <axsl:attribute name="name">Structuur compleet</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M31" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_041</axsl:attribute>
            <axsl:attribute name="name">Divisietekst compleet</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M32" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_043</axsl:attribute>
            <axsl:attribute name="name">Kennisgeving zonder divisie</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M33" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_044</axsl:attribute>
            <axsl:attribute name="name">Vervallen structuur</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M34" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_045</axsl:attribute>
            <axsl:attribute name="name">sch_tekst_045</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M35" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_046</axsl:attribute>
            <axsl:attribute name="name">sch_tekst_046</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M36" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_081</axsl:attribute>
            <axsl:attribute name="name">Toelichting specifiek</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M37" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_082</axsl:attribute>
            <axsl:attribute name="name">ArtikelgewijzeToelichting buiten Toelichting</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M38" />
         <svrl:active-pattern>
            <axsl:attribute name="document"><axsl:value-of select="document-uri(/)" /></axsl:attribute>
            <axsl:attribute name="id">sch_tekst_083</axsl:attribute>
            <axsl:attribute name="name">Inleidende tekst in Toelichtingen</axsl:attribute>
            <axsl:apply-templates />
         </svrl:active-pattern>
         <axsl:apply-templates select="/" mode="M39" />
      </svrl:schematron-output></axsl:template>

   <!--SCHEMATRON
   PATTERNS-->


   <!--PATTERN
   sch_tekst_001Lijst - Nummering lijstitems-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Lijst - Nummering lijstitems</svrl:text>

   <!--RULE -->
   <axsl:template match="tekst:Lijst[@type = 'ongemarkeerd']" priority="1001" mode="M4"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="tekst:Lijst[@type = 'ongemarkeerd']" />

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="count(tekst:Li/tekst:LiNummer) = 0" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="count(tekst:Li/tekst:LiNummer) = 0">
               <axsl:attribute name="id">STOP0001</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0001", "eId": "<axsl:text /><axsl:value-of select="@eId" /><axsl:text />",
      "melding": "De Lijst met eId <axsl:text /><axsl:value-of select="@eId" /><axsl:text /> van
      type 'ongemarkeerd' heeft LiNummer-elementen met een nummering of opsommingstekens, dit is
      niet toegestaan. Pas het type van de lijst aan of verwijder de LiNummer-elementen.", "ernst":
      "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M4" /></axsl:template>

   <!--RULE -->
   <axsl:template match="tekst:Lijst[@type = 'expliciet']" priority="1000" mode="M4"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="tekst:Lijst[@type = 'expliciet']" />

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="count(tekst:Li[tekst:LiNummer]) = count(tekst:Li)" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="count(tekst:Li[tekst:LiNummer]) = count(tekst:Li)">
               <axsl:attribute name="id">STOP0002</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0002", "eId": "<axsl:text /><axsl:value-of select="@eId" /><axsl:text />",
      "melding": "De Lijst met eId <axsl:text /><axsl:value-of select="@eId" /><axsl:text /> van
      type 'expliciet' heeft geen LiNummer elementen met nummering of opsommingstekens, het gebruik
      van LiNummer is verplicht. Pas het type van de lijst aan of voeg LiNummer's met nummering of
      opsommingstekens toe aan de lijst-items", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M4" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M4" />
   <axsl:template match="@*|node()" priority="-2" mode="M4"><axsl:apply-templates select="*"
         mode="M4" /></axsl:template>

   <!--PATTERN
   sch_tekst_022Alinea - Bevat content-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Alinea - Bevat content</svrl:text>

   <!--RULE -->
   <axsl:template match="tekst:Al" priority="1000" mode="M5"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="tekst:Al" />

      <!--REPORT
      fout-->
<axsl:if
         test="normalize-space(./string()) = '' and not(tekst:InlineTekstAfbeelding | tekst:Nootref)"><svrl:successful-report
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
            test="normalize-space(./string()) = '' and not(tekst:InlineTekstAfbeelding | tekst:Nootref)">
            <axsl:attribute name="id">STOP0005</axsl:attribute>
            <axsl:attribute name="role">fout</axsl:attribute>
            <axsl:attribute name="location"><axsl:apply-templates select="."
                  mode="schematron-select-full-path" /></axsl:attribute>
            <svrl:text> {"code": "STOP0005", "element": "<axsl:text /><axsl:value-of
                  select="ancestor::tekst:*[@eId][1]/local-name()" /><axsl:text />", "eId": "<axsl:text /><axsl:value-of
                  select="ancestor::tekst:*[@eId][1]/@eId" /><axsl:text />", "melding": "De alinea
      voor element <axsl:text /><axsl:value-of select="ancestor::tekst:*[@eId][1]/local-name()" /><axsl:text />
      met id <axsl:text /><axsl:value-of select="ancestor::tekst:*[@eId][1]/@eId" /><axsl:text />
      bevat geen tekst. Verwijder de lege alinea", "ernst": "fout"},</svrl:text>
         </svrl:successful-report></axsl:if><axsl:apply-templates
         select="*" mode="M5" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M5" />
   <axsl:template match="@*|node()" priority="-2" mode="M5"><axsl:apply-templates select="*"
         mode="M5" /></axsl:template>

   <!--PATTERN
   sch_tekst_027Kop - Bevat content-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Kop - Bevat content</svrl:text>

   <!--RULE -->
   <axsl:template match="tekst:Kop" priority="1000" mode="M6"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="tekst:Kop" />

      <!--REPORT
      fout-->
<axsl:if
         test="normalize-space(./string()) = ''"><svrl:successful-report
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl" test="normalize-space(./string()) = ''">
            <axsl:attribute name="id">STOP0006</axsl:attribute>
            <axsl:attribute name="role">fout</axsl:attribute>
            <axsl:attribute name="location"><axsl:apply-templates select="."
                  mode="schematron-select-full-path" /></axsl:attribute>
            <svrl:text> {"code": "STOP0006", "element": "<axsl:text /><axsl:value-of
                  select="ancestor::tekst:*[@eId][1]/local-name()" /><axsl:text />", "eId": "<axsl:text /><axsl:value-of
                  select="ancestor::tekst:*[@eId][1]/@eId" /><axsl:text />", "melding": "De kop voor
      element <axsl:text /><axsl:value-of select="ancestor::tekst:*[@eId][1]/local-name()" /><axsl:text />
      met id <axsl:text /><axsl:value-of select="ancestor::tekst:*[@eId][1]/@eId" /><axsl:text />
      bevat geen tekst. Corrigeer de kop of verplaats de inhoud naar een ander element", "ernst":
      "fout"},</svrl:text>
         </svrl:successful-report></axsl:if><axsl:apply-templates
         select="*" mode="M6" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M6" />
   <axsl:template match="@*|node()" priority="-2" mode="M6"><axsl:apply-templates select="*"
         mode="M6" /></axsl:template>

   <!--PATTERN
   sch_tekst_003Tabel - Referenties naar een noot-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Tabel - Referenties naar een noot</svrl:text>

   <!--RULE -->
   <axsl:template match="tekst:table//tekst:Nootref" priority="1001" mode="M7"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="tekst:table//tekst:Nootref" /><axsl:variable
         name="nootID" select="@refid" />

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="ancestor::tekst:table//tekst:Noot[@id = $nootID]" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="ancestor::tekst:table//tekst:Noot[@id = $nootID]">
               <axsl:attribute name="id">STOP0008</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0008", "ref": "<axsl:text /><axsl:value-of select="@refid" /><axsl:text />",
      "eId": "<axsl:text /><axsl:value-of select="ancestor::tekst:table/@eId" /><axsl:text />",
      "melding": "De referentie naar de noot met id <axsl:text /><axsl:value-of select="@refid" /><axsl:text />
      verwijst niet naar een noot in dezelfde tabel <axsl:text /><axsl:value-of
                     select="ancestor::tekst:table/@eId" /><axsl:text />. Verplaats de noot waarnaar
      verwezen wordt naar de tabel of vervang de referentie in de tabel voor de noot waarnaar
      verwezen wordt", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M7" /></axsl:template>

   <!--RULE -->
   <axsl:template match="tekst:Nootref" priority="1000" mode="M7"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="tekst:Nootref" /><axsl:variable
         name="nootID" select="@refid" />

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="ancestor::tekst:table" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="ancestor::tekst:table">
               <axsl:attribute name="id">STOP0007</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0007", "ref": "<axsl:text /><axsl:value-of select="@refid" /><axsl:text />",
      "melding": "De referentie naar de noot met id <axsl:text /><axsl:value-of select="@refid" /><axsl:text />
      staat niet in een tabel. Vervang de referentie naar de noot voor de noot waarnaar verwezen
      wordt", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M7" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M7" />
   <axsl:template match="@*|node()" priority="-2" mode="M7"><axsl:apply-templates select="*"
         mode="M7" /></axsl:template>

   <!--PATTERN
   sch_tekst_004Lijst - plaatsing tabel in een lijst-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Lijst - plaatsing tabel in een lijst</svrl:text>

   <!--RULE -->
   <axsl:template match="tekst:Li[tekst:table]" priority="1000" mode="M8"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="tekst:Li[tekst:table]" />

      <!--REPORT
      waarschuwing-->
<axsl:if
         test="self::tekst:Li/tekst:table and not(ancestor::tekst:Instructie)"><svrl:successful-report
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
            test="self::tekst:Li/tekst:table and not(ancestor::tekst:Instructie)">
            <axsl:attribute name="id">STOP0009</axsl:attribute>
            <axsl:attribute name="role">waarschuwing</axsl:attribute>
            <axsl:attribute name="location"><axsl:apply-templates select="."
                  mode="schematron-select-full-path" /></axsl:attribute>
            <svrl:text> {"code": "STOP0009", "eId": "<axsl:text /><axsl:value-of select="@eId" /><axsl:text />",
      "melding": "Het lijst-item <axsl:text /><axsl:value-of select="@eId" /><axsl:text /> bevat een
      tabel, onderzoek of de tabel buiten de lijst kan worden geplaatst, eventueel door de lijst in
      delen op te splitsen", "ernst": "waarschuwing"},</svrl:text>
         </svrl:successful-report></axsl:if><axsl:apply-templates
         select="*" mode="M8" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M8" />
   <axsl:template match="@*|node()" priority="-2" mode="M8"><axsl:apply-templates select="*"
         mode="M8" /></axsl:template>

   <!--PATTERN
   sch_tekst_032Illustratie - attributen kleur en schaal worden niet ondersteund-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Illustratie - attributen kleur en schaal
      worden niet ondersteund</svrl:text>

   <!--RULE -->
   <axsl:template match="tekst:Illustratie | tekst:InlineTekstAfbeelding" priority="1000" mode="M9"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
         context="tekst:Illustratie | tekst:InlineTekstAfbeelding" />

      <!--REPORT
      waarschuwing-->
<axsl:if test="@schaal"><svrl:successful-report
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl" test="@schaal">
            <axsl:attribute name="id">STOP0045</axsl:attribute>
            <axsl:attribute name="role">waarschuwing</axsl:attribute>
            <axsl:attribute name="location"><axsl:apply-templates select="."
                  mode="schematron-select-full-path" /></axsl:attribute>
            <svrl:text> {"code": "STOP0045", "ouder": "<axsl:text /><axsl:value-of
                  select="local-name(ancestor::*[@eId][1])" /><axsl:text />", "eId": "<axsl:text /><axsl:value-of
                  select="ancestor::*[@eId][1]/@eId" /><axsl:text />", "melding": "De Illustratie
      binnen <axsl:text /><axsl:value-of select="local-name(ancestor::*[@eId][1])" /><axsl:text />
      met eId <axsl:text /><axsl:value-of select="ancestor::*[@eId][1]/@eId" /><axsl:text /> heeft
      een waarde voor attribuut @schaal. Dit attribuut wordt genegeerd in de publicatie van
      documenten volgens STOP 1.3.0. In plaats daarvan wordt het attribuut @dpi gebruikt voor de
      berekening van de afbeeldingsgrootte. Verwijder het attribuut @schaal.", "ernst":
      "waarschuwing"},</svrl:text>
         </svrl:successful-report></axsl:if>

      <!--REPORT
      waarschuwing-->
<axsl:if test="@kleur"><svrl:successful-report
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl" test="@kleur">
            <axsl:attribute name="id">STOP0046</axsl:attribute>
            <axsl:attribute name="role">waarschuwing</axsl:attribute>
            <axsl:attribute name="location"><axsl:apply-templates select="."
                  mode="schematron-select-full-path" /></axsl:attribute>
            <svrl:text> {"code": "STOP0046", "ouder": "<axsl:text /><axsl:value-of
                  select="local-name(ancestor::*[@eId][1])" /><axsl:text />", "eId": "<axsl:text /><axsl:value-of
                  select="ancestor::*[@eId][1]/@eId" /><axsl:text />", "melding": "De Illustratie
      binnen <axsl:text /><axsl:value-of select="local-name(ancestor::*[@eId][1])" /><axsl:text />
      met eId <axsl:text /><axsl:value-of select="ancestor::*[@eId][1]/@eId" /><axsl:text /> heeft
      een waarde voor attribuut @kleur. Dit attribuut wordt genegeerd in de publicatie van STOP
      1.3.0. Verwijder het attribuut @kleur.", "ernst": "waarschuwing"},</svrl:text>
         </svrl:successful-report></axsl:if><axsl:apply-templates
         select="*" mode="M9" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M9" />
   <axsl:template match="@*|node()" priority="-2" mode="M9"><axsl:apply-templates select="*"
         mode="M9" /></axsl:template>

   <!--PATTERN
   sch_tekst_006Referentie intern - correcte verwijzing-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Referentie intern - correcte verwijzing</svrl:text>

   <!--RULE -->
   <axsl:template
      match="tekst:IntRef[not(ancestor::tekst:RegelingMutatie | ancestor::tekst:BesluitMutatie)]"
      priority="1000" mode="M10"><svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
         context="tekst:IntRef[not(ancestor::tekst:RegelingMutatie | ancestor::tekst:BesluitMutatie)]" /><axsl:variable
         name="doelwit">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
            xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="starts-with(@ref, '!')">
               <xsl:value-of select="substring-after(@ref, '#')" />
            </xsl:when>
            <xsl:otherwise>
               <xsl:value-of select="@ref" />
            </xsl:otherwise>
         </xsl:choose>
      </axsl:variable><axsl:variable
         name="component">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
            xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="starts-with(@ref, '!')">
               <xsl:value-of select="substring-before(translate(@ref, '!', ''), '#')" />
            </xsl:when>
            <xsl:when test="ancestor::tekst:*[@componentnaam]">
               <xsl:value-of select="ancestor::tekst:*[@componentnaam]/@componentnaam" />
            </xsl:when>
            <xsl:otherwise>[is_geen_component]</xsl:otherwise>
         </xsl:choose>
      </axsl:variable><axsl:variable
         name="scopeNaam">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
            xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="@scope">
               <xsl:value-of select="@scope" />
            </xsl:when>
            <xsl:otherwise>[geen-scope]</xsl:otherwise>
         </xsl:choose>
      </axsl:variable><axsl:variable
         name="localName">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
            xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when
               test="//tekst:*[@eId = $doelwit and ($component = '[is_geen_component]' or ancestor::tekst:*[@componentnaam][1]/@componentnaam = $component) and not(ancestor::tekst:RegelingMutatie | ancestor::tekst:BesluitMutatie)]">
               <xsl:choose>
                  <xsl:when test="$component = '[is_geen_component]'">
                     <xsl:value-of
                        select="//tekst:*[@eId = $doelwit][not(ancestor::tekst:*[@componentnaam])]/local-name()" />
                  </xsl:when>
                  <xsl:otherwise>
                     <xsl:value-of
                        select="//tekst:*[@eId = $doelwit][ancestor::tekst:*[@componentnaam][1]/@componentnaam = $component]/local-name()" />
                  </xsl:otherwise>
               </xsl:choose>
            </xsl:when>
            <xsl:otherwise />
         </xsl:choose>
      </axsl:variable>

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when
            test="//tekst:*[@eId = $doelwit and ($component = '[is_geen_component]' or ancestor::tekst:*[@componentnaam][1]/@componentnaam = $component) and not(ancestor::tekst:RegelingMutatie | ancestor::tekst:BesluitMutatie)]" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="//tekst:*[@eId = $doelwit and ($component = '[is_geen_component]' or ancestor::tekst:*[@componentnaam][1]/@componentnaam = $component) and not(ancestor::tekst:RegelingMutatie | ancestor::tekst:BesluitMutatie)]">
               <axsl:attribute name="id">STOP0010</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0010", "ref": "<axsl:text /><axsl:value-of
                     select="$doelwit" /><axsl:text />", "melding": "De waarde van @ref van element
      tekst:IntRef met waarde <axsl:text /><axsl:value-of select="$doelwit" /><axsl:text /> komt
      niet voor als eId van een tekst-element in (de mutatie van) de tekst van dezelfde expression
      als de IntRef. Controleer de referentie, corrigeer of de referentie of de identificatie van
      het element waarnaar wordt verwezen.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose>

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="$scopeNaam = '[geen-scope]' or $scopeNaam = $localName" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="$scopeNaam = '[geen-scope]' or $scopeNaam = $localName">
               <axsl:attribute name="id">STOP0053</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0053", "ref": "<axsl:text /><axsl:value-of
                     select="$doelwit" /><axsl:text />", "scope": "<axsl:text /><axsl:value-of
                     select="$scopeNaam" /><axsl:text />", "local": "<axsl:text /><axsl:value-of
                     select="$localName" /><axsl:text />", "melding": "De scope <axsl:text /><axsl:value-of
                     select="$scopeNaam" /><axsl:text /> van de IntRef met <axsl:text /><axsl:value-of
                     select="$doelwit" /><axsl:text /> is niet gelijk aan de naam van het
      doelelement <axsl:text /><axsl:value-of select="$localName" /><axsl:text />.", "ernst":
      "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M10" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M10" />
   <axsl:template match="@*|node()" priority="-2" mode="M10"><axsl:apply-templates select="*"
         mode="M10" /></axsl:template>

   <!--PATTERN
   sch_tekst_028Referentie informatieobject - correcte verwijzing-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Referentie informatieobject - correcte
      verwijzing</svrl:text>

   <!--RULE -->
   <axsl:template
      match="tekst:IntIoRef[not(ancestor::tekst:RegelingMutatie | ancestor::BesluitMutatie)]"
      priority="1000" mode="M11"><svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
         context="tekst:IntIoRef[not(ancestor::tekst:RegelingMutatie | ancestor::BesluitMutatie)]" /><axsl:variable
         name="doelwit" select="@ref" />

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="//tekst:ExtIoRef[@wId = $doelwit]" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="//tekst:ExtIoRef[@wId = $doelwit]">
               <axsl:attribute name="id">STOP0011</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0011", "element": "<axsl:text /><axsl:value-of
                     select="name(.)" /><axsl:text />", "ref": "<axsl:text /><axsl:value-of
                     select="$doelwit" /><axsl:text />", "melding": "De @ref van element <axsl:text /><axsl:value-of
                     select="name(.)" /><axsl:text /> met waarde <axsl:text /><axsl:value-of
                     select="$doelwit" /><axsl:text /> verwijst niet naar een wId van een ExtIoRef
      binnen hetzelfde bestand. Controleer de referentie, corrigeer of de referentie of de wId
      identificatie van het element waarnaar wordt verwezen", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M11" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M11" />
   <axsl:template match="@*|node()" priority="-2" mode="M11"><axsl:apply-templates select="*"
         mode="M11" /></axsl:template>

   <!--PATTERN
   sch_tekst_007Referentie extern informatieobject-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Referentie extern informatieobject</svrl:text>

   <!--RULE -->
   <axsl:template match="tekst:ExtIoRef" priority="1000" mode="M12"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="tekst:ExtIoRef" /><axsl:variable
         name="ref" select="normalize-space(@ref)" />

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="normalize-space(.) = $ref" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="normalize-space(.) = $ref">
               <axsl:attribute name="id">STOP0012</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0012", "eId": "<axsl:text /><axsl:value-of select="@eId" /><axsl:text />",
      "melding": "De JOIN-identifier van ExtIoRef <axsl:text /><axsl:value-of select="@eId" /><axsl:text />
      in de tekst is niet gelijk aan de als referentie opgenomen JOIN-identificatie. Controleer de
      gebruikte JOIN-identicatie en plaats de juiste verwijzing als zowel de @ref als de tekst van
      het element ExtIoRef", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M12" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M12" />
   <axsl:template match="@*|node()" priority="-2" mode="M12"><axsl:apply-templates select="*"
         mode="M12" /></axsl:template>

   <!--PATTERN
   sch_tekst_008Identificatie - correct gebruik wId, eId -->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Identificatie - correct gebruik wId, eId </svrl:text>

   <!--RULE -->
   <axsl:template match="//*[@eId]" priority="1000" mode="M13"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="//*[@eId]" /><axsl:variable
         name="doelwitE" select="@eId" /><axsl:variable name="doelwitW" select="@wId" />

      <!--REPORT
      fout-->
<axsl:if
         test="ends-with($doelwitE, '.')"><svrl:successful-report
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl" test="ends-with($doelwitE, '.')">
            <axsl:attribute name="id">STOP0013</axsl:attribute>
            <axsl:attribute name="role">fout</axsl:attribute>
            <axsl:attribute name="location"><axsl:apply-templates select="."
                  mode="schematron-select-full-path" /></axsl:attribute>
            <svrl:text> {"code": "STOP0013", "eId": "<axsl:text /><axsl:value-of select="@eId" /><axsl:text />",
      "element": "<axsl:text /><axsl:value-of select="name(.)" /><axsl:text />", "melding": "Het
      attribuut @eId of een deel van de eId <axsl:text /><axsl:value-of select="@eId" /><axsl:text />
      van element <axsl:text /><axsl:value-of select="name(.)" /><axsl:text /> eindigt op een '.',
      dit is niet toegestaan. Verwijder de laatste punt(en) '.' voor deze eId", "ernst": "fout"},</svrl:text>
         </svrl:successful-report></axsl:if>

      <!--REPORT
      fout-->
<axsl:if
         test="contains($doelwitE, '.__')"><svrl:successful-report
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl" test="contains($doelwitE, '.__')">
            <axsl:attribute name="id">STOP0043</axsl:attribute>
            <axsl:attribute name="role">fout</axsl:attribute>
            <axsl:attribute name="location"><axsl:apply-templates select="."
                  mode="schematron-select-full-path" /></axsl:attribute>
            <svrl:text> {"code": "STOP0043", "eId": "<axsl:text /><axsl:value-of select="@eId" /><axsl:text />",
      "element": "<axsl:text /><axsl:value-of select="name(.)" /><axsl:text />", "melding": "Het
      attribuut @eId of een deel van de eId <axsl:text /><axsl:value-of select="@eId" /><axsl:text />
      van element <axsl:text /><axsl:value-of select="name(.)" /><axsl:text /> eindigt op '.__', dit
      is niet toegestaan. Verwijder deze punt '.' binnen deze eId", "ernst": "fout"},</svrl:text>
         </svrl:successful-report></axsl:if>

      <!--REPORT
      fout-->
<axsl:if
         test="ends-with($doelwitW, '.')"><svrl:successful-report
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl" test="ends-with($doelwitW, '.')">
            <axsl:attribute name="id">STOP0014</axsl:attribute>
            <axsl:attribute name="role">fout</axsl:attribute>
            <axsl:attribute name="location"><axsl:apply-templates select="."
                  mode="schematron-select-full-path" /></axsl:attribute>
            <svrl:text> {"code": "STOP0014", "wId": "<axsl:text /><axsl:value-of select="@wId" /><axsl:text />",
      "element": "<axsl:text /><axsl:value-of select="name(.)" /><axsl:text />", "melding": "Het
      attribuut @wId <axsl:text /><axsl:value-of select="@wId" /><axsl:text /> van element <axsl:text /><axsl:value-of
                  select="name(.)" /><axsl:text /> eindigt op een '.', dit is niet toegestaan.
      Verwijder de laatste punt '.' van deze wId", "ernst": "fout"},</svrl:text>
         </svrl:successful-report></axsl:if>

      <!--REPORT
      fout-->
<axsl:if
         test="contains($doelwitW, '.__')"><svrl:successful-report
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl" test="contains($doelwitW, '.__')">
            <axsl:attribute name="id">STOP0044</axsl:attribute>
            <axsl:attribute name="role">fout</axsl:attribute>
            <axsl:attribute name="location"><axsl:apply-templates select="."
                  mode="schematron-select-full-path" /></axsl:attribute>
            <svrl:text> {"code": "STOP0044", "wId": "<axsl:text /><axsl:value-of select="@wId" /><axsl:text />",
      "element": "<axsl:text /><axsl:value-of select="name(.)" /><axsl:text />", "melding": "Het
      attribuut @wId <axsl:text /><axsl:value-of select="@wId" /><axsl:text /> van element <axsl:text /><axsl:value-of
                  select="name(.)" /><axsl:text /> eindigt op een '.__', dit is niet toegestaan.
      Verwijder deze punt '.' binnen deze wId", "ernst": "fout"},</svrl:text>
         </svrl:successful-report></axsl:if><axsl:apply-templates
         select="*" mode="M13" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M13" />
   <axsl:template match="@*|node()" priority="-2" mode="M13"><axsl:apply-templates select="*"
         mode="M13" /></axsl:template>

   <!--PATTERN
   sch_tekst_023RegelingTijdelijkdeel - WijzigArtikel niet toegestaan-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">RegelingTijdelijkdeel - WijzigArtikel niet
      toegestaan</svrl:text>

   <!--RULE -->
   <axsl:template match="tekst:RegelingTijdelijkdeel//tekst:WijzigArtikel" priority="1000"
      mode="M14"><svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
         context="tekst:RegelingTijdelijkdeel//tekst:WijzigArtikel" />

      <!--REPORT
      fout-->
<axsl:if
         test="self::tekst:WijzigArtikel"><svrl:successful-report
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl" test="self::tekst:WijzigArtikel">
            <axsl:attribute name="id">STOP0015</axsl:attribute>
            <axsl:attribute name="role">fout</axsl:attribute>
            <axsl:attribute name="location"><axsl:apply-templates select="."
                  mode="schematron-select-full-path" /></axsl:attribute>
            <svrl:text> {"code": "STOP0015", "eId": "<axsl:text /><axsl:value-of select="@eId" /><axsl:text />",
      "melding": "Het WijzigArtikel <axsl:text /><axsl:value-of select="@eId" /><axsl:text /> is in
      een RegelingTijdelijkdeel niet toegestaan. Verwijder het WijzigArtikel of pas dit aan naar een
      Artikel indien dit mogelijk is", "ernst": "fout"},</svrl:text>
         </svrl:successful-report></axsl:if><axsl:apply-templates
         select="*" mode="M14" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M14" />
   <axsl:template match="@*|node()" priority="-2" mode="M14"><axsl:apply-templates select="*"
         mode="M14" /></axsl:template>

   <!--PATTERN
   sch_tekst_026RegelingCompact - WijzigArtikel niet toegestaan-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">RegelingCompact - WijzigArtikel niet
      toegestaan</svrl:text>

   <!--RULE -->
   <axsl:template match="tekst:RegelingCompact//tekst:WijzigArtikel" priority="1000" mode="M15"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
         context="tekst:RegelingCompact//tekst:WijzigArtikel" />

      <!--REPORT
      fout-->
<axsl:if
         test="self::tekst:WijzigArtikel"><svrl:successful-report
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl" test="self::tekst:WijzigArtikel">
            <axsl:attribute name="id">STOP0016</axsl:attribute>
            <axsl:attribute name="role">fout</axsl:attribute>
            <axsl:attribute name="location"><axsl:apply-templates select="."
                  mode="schematron-select-full-path" /></axsl:attribute>
            <svrl:text> {"code": "STOP0016", "eId": "<axsl:text /><axsl:value-of select="@eId" /><axsl:text />",
      "melding": "Het WijzigArtikel <axsl:text /><axsl:value-of select="@eId" /><axsl:text /> is in
      een RegelingCompact niet toegestaan. Verwijder het WijzigArtikel of pas dit aan naar een
      Artikel indien dit mogelijk is", "ernst": "fout"},</svrl:text>
         </svrl:successful-report></axsl:if><axsl:apply-templates
         select="*" mode="M15" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M15" />
   <axsl:template match="@*|node()" priority="-2" mode="M15"><axsl:apply-templates select="*"
         mode="M15" /></axsl:template>

   <!--PATTERN
   sch_tekst_009Mutaties - Wijzigingen tekstueel-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Mutaties - Wijzigingen tekstueel</svrl:text>

   <!--RULE -->
   <axsl:template match="tekst:NieuweTekst | tekst:VerwijderdeTekst" priority="1000" mode="M16"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
         context="tekst:NieuweTekst | tekst:VerwijderdeTekst" />

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="ancestor::tekst:RegelingMutatie or ancestor::tekst:BesluitMutatie" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="ancestor::tekst:RegelingMutatie or ancestor::tekst:BesluitMutatie">
               <axsl:attribute name="id">STOP0017</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0017", "ouder": "<axsl:text /><axsl:value-of
                     select="local-name(parent::tekst:*)" /><axsl:text />", "eId": "<axsl:text /><axsl:value-of
                     select="ancestor::tekst:*[@eId][1]/@eId" /><axsl:text />", "element": "<axsl:text /><axsl:value-of
                     select="name(.)" /><axsl:text />", "melding": "Tekstuele wijziging is niet
      toegestaan buiten de context van een tekst:RegelingMutatie of tekst:BesluitMutatie. element <axsl:text /><axsl:value-of
                     select="local-name(parent::tekst:*)" /><axsl:text /> met id \"<axsl:text /><axsl:value-of
                     select="ancestor::tekst:*[@eId][1]/@eId" /><axsl:text />\" bevat een <axsl:text /><axsl:value-of
                     select="name(.)" /><axsl:text />. Verwijder het element <axsl:text /><axsl:value-of
                     select="name(.)" /><axsl:text />", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M16" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M16" />
   <axsl:template match="@*|node()" priority="-2" mode="M16"><axsl:apply-templates select="*"
         mode="M16" /></axsl:template>

   <!--PATTERN
   sch_tekst_010Mutaties - Wijzigingen structuur-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Mutaties - Wijzigingen structuur</svrl:text>

   <!--RULE -->
   <axsl:template match="tekst:*[@wijzigactie]" priority="1000" mode="M17"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="tekst:*[@wijzigactie]" />

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="ancestor::tekst:RegelingMutatie or ancestor::tekst:BesluitMutatie" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="ancestor::tekst:RegelingMutatie or ancestor::tekst:BesluitMutatie">
               <axsl:attribute name="id">STOP0018</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0018", "element": "<axsl:text /><axsl:value-of
                     select="local-name()" /><axsl:text />", "eId": "<axsl:text /><axsl:value-of
                     select="ancestor-or-self::tekst:*[@eId][1]/@eId" /><axsl:text />", "melding":
      "Een attribuut @wijzigactie is niet toegestaan op element <axsl:text /><axsl:value-of
                     select="local-name()" /><axsl:text /> met id \"<axsl:text /><axsl:value-of
                     select="ancestor-or-self::tekst:*[@eId][1]/@eId" /><axsl:text />\" buiten de
      context van een tekst:RegelingMutatie of tekst:BesluitMutatie. Verwijder het attribuut
      @wijzigactie", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M17" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M17" />
   <axsl:template match="@*|node()" priority="-2" mode="M17"><axsl:apply-templates select="*"
         mode="M17" /></axsl:template>

   <!--PATTERN
   sch_tekst_011Identificatie - Alle wId en eId buiten een AKN-component zijn uniek-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Identificatie - Alle wId en eId buiten een
      AKN-component zijn uniek</svrl:text>

   <!--RULE -->
   <axsl:template
      match="tekst:*[@eId][not(ancestor-or-self::tekst:*[@componentnaam])][not(ancestor-or-self::tekst:WijzigInstructies)]"
      priority="1001" mode="M21"><svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
         context="tekst:*[@eId][not(ancestor-or-self::tekst:*[@componentnaam])][not(ancestor-or-self::tekst:WijzigInstructies)]" />

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="count(key('alleEIDs', @eId)) = 1" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="count(key('alleEIDs', @eId)) = 1">
               <axsl:attribute name="id">STOP0020</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0020", "eId": "<axsl:text /><axsl:value-of select="@eId" /><axsl:text />",
      "melding": "De eId '<axsl:text /><axsl:value-of select="@eId" /><axsl:text />' binnen het
      bereik is niet uniek. Controleer de opbouw van de eId en corrigeer deze", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose>

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="count(key('alleWIDs', @wId)) = 1" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="count(key('alleWIDs', @wId)) = 1">
               <axsl:attribute name="id">STOP0021</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0021", "wId": "<axsl:text /><axsl:value-of select="@wId" /><axsl:text />",
      "melding": "De wId '<axsl:text /><axsl:value-of select="@wId" /><axsl:text />' binnen het
      bereik is niet uniek. Controleer de opbouw van de wId en corrigeer deze", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M21" /></axsl:template>

   <!--RULE -->
   <axsl:template
      match="tekst:Noot[not(ancestor-or-self::tekst:*[@componentnaam])][not(ancestor-or-self::tekst:WijzigInstructies)]"
      priority="1000" mode="M21"><svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
         context="tekst:Noot[not(ancestor-or-self::tekst:*[@componentnaam])][not(ancestor-or-self::tekst:WijzigInstructies)]" />

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="count(key('alleNootIDs', @id)) &lt;= 1" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="count(key('alleNootIDs', @id)) &lt;= 1">
               <axsl:attribute name="id">STOP0068</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0068", "id": "<axsl:text /><axsl:value-of select="@id" /><axsl:text />",
      "melding": "De id '<axsl:text /><axsl:value-of select="@id" /><axsl:text />' is niet uniek
      binnen zijn component. Controleer id en corrigeer deze", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M21" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M21" />
   <axsl:template match="@*|node()" priority="-2" mode="M21"><axsl:apply-templates select="*"
         mode="M21" /></axsl:template>

   <!--PATTERN
   sch_tekst_020Identificatie - AKN-naamgeving voor eId en wId-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Identificatie - AKN-naamgeving voor eId en
      wId</svrl:text>

   <!--RULE -->
   <axsl:template match="*[@eId]" priority="1000" mode="M22"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="*[@eId]" /><axsl:variable
         name="AKNnaam">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
            xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="matches(local-name(), 'Lichaam')">body</xsl:when>
            <xsl:when test="matches(local-name(), 'RegelingOpschrift')">longTitle</xsl:when>
            <xsl:when test="matches(local-name(), 'AlgemeneToelichting')">genrecital</xsl:when>
            <xsl:when test="matches(local-name(), '^ArtikelgewijzeToelichting$')">artrecital</xsl:when>
            <xsl:when test="matches(local-name(), 'Artikel|WijzigArtikel')">art</xsl:when>
            <xsl:when test="matches(local-name(), 'WijzigLid|Lid')">para</xsl:when>
            <xsl:when test="matches(local-name(), 'Divisietekst')">content</xsl:when>
            <xsl:when test="matches(local-name(), 'Divisie')">div</xsl:when>
            <xsl:when test="matches(local-name(), 'Boek')">book</xsl:when>
            <xsl:when test="matches(local-name(), 'Titel')">title</xsl:when>
            <xsl:when test="matches(local-name(), 'Deel')">part</xsl:when>
            <xsl:when test="matches(local-name(), 'Hoofdstuk')">chp</xsl:when>
            <xsl:when test="matches(local-name(), 'Afdeling')">subchp</xsl:when>
            <xsl:when test="matches(local-name(), 'Paragraaf|Subparagraaf|Subsubparagraaf')">subsec</xsl:when>
            <xsl:when test="matches(local-name(), 'WijzigBijlage|Bijlage')">cmp</xsl:when>
            <xsl:when test="matches(local-name(), 'Inhoudsopgave')">toc</xsl:when>
            <xsl:when test="matches(local-name(), 'Motivering')">acc</xsl:when>
            <xsl:when test="matches(local-name(), 'Toelichting')">recital</xsl:when>
            <xsl:when test="matches(local-name(), 'InleidendeTekst')">intro</xsl:when>
            <xsl:when test="matches(local-name(), 'Aanhef')">formula_1</xsl:when>
            <xsl:when test="matches(local-name(), 'Kadertekst')">recital</xsl:when>
            <xsl:when test="matches(local-name(), 'Sluiting')">formula_2</xsl:when>
            <xsl:when test="matches(local-name(), 'table')">table</xsl:when>
            <xsl:when test="matches(local-name(), 'Figuur')">img</xsl:when>
            <xsl:when test="matches(local-name(), 'Formule')">math</xsl:when>
            <xsl:when test="matches(local-name(), 'Citaat')">cit</xsl:when>
            <xsl:when test="matches(local-name(), 'Begrippenlijst|Lijst')">list</xsl:when>
            <xsl:when test="matches(local-name(), 'Li|Begrip')">item</xsl:when>
            <xsl:when test="matches(local-name(), 'IntIoRef|ExtIoRef')">ref</xsl:when>
            <xsl:when test="matches(local-name(), 'Rectificatietekst')">content</xsl:when>
            <xsl:otherwise>AKN-prefix-van-onbekend-element</xsl:otherwise>
         </xsl:choose>
      </axsl:variable><axsl:variable
         name="mijnEID">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
            xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="contains(@eId, '__')">
               <xsl:value-of select="tokenize(@eId, '__')[last()]" />
            </xsl:when>
            <xsl:otherwise>
               <xsl:value-of select="@eId" />
            </xsl:otherwise>
         </xsl:choose>
      </axsl:variable><axsl:variable
         name="mijnWID">
         <xsl:value-of xmlns:sch="http://purl.oclc.org/dsdl/schematron"
            xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
            select="tokenize(@wId, '__')[last()]" />
      </axsl:variable>

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="starts-with($mijnEID, $AKNnaam)" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="starts-with($mijnEID, $AKNnaam)">
               <axsl:attribute name="id">STOP0022</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0022", "AKNdeel": "<axsl:text /><axsl:value-of
                     select="$mijnEID" /><axsl:text />", "element": "<axsl:text /><axsl:value-of
                     select="name(.)" /><axsl:text />", "waarde": "<axsl:text /><axsl:value-of
                     select="$AKNnaam" /><axsl:text />", "wId": "<axsl:text /><axsl:value-of
                     select="@wId" /><axsl:text />", "melding": "De AKN-naamgeving voor eId '<axsl:text /><axsl:value-of
                     select="$mijnEID" /><axsl:text />' is niet correct voor element <axsl:text /><axsl:value-of
                     select="name(.)" /><axsl:text /> met id '<axsl:text /><axsl:value-of
                     select="@wId" /><axsl:text />', Dit moet zijn: '<axsl:text /><axsl:value-of
                     select="$AKNnaam" /><axsl:text />'. Pas de naamgeving voor dit element en alle
      onderliggende elementen aan. Controleer ook de naamgeving van de bijbehorende wId en
      onderliggende elementen.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose>

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="starts-with($mijnWID, $AKNnaam)" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="starts-with($mijnWID, $AKNnaam)">
               <axsl:attribute name="id">STOP0023</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0023", "AKNdeel": "<axsl:text /><axsl:value-of
                     select="$mijnWID" /><axsl:text />", "element": "<axsl:text /><axsl:value-of
                     select="name(.)" /><axsl:text />", "waarde": "<axsl:text /><axsl:value-of
                     select="$AKNnaam" /><axsl:text />", "wId": "<axsl:text /><axsl:value-of
                     select="@wId" /><axsl:text />", "melding": "De AKN-naamgeving voor wId '<axsl:text /><axsl:value-of
                     select="$mijnWID" /><axsl:text />' is niet correct voor element <axsl:text /><axsl:value-of
                     select="name(.)" /><axsl:text /> met id '<axsl:text /><axsl:value-of
                     select="@wId" /><axsl:text />', Dit moet zijn: '<axsl:text /><axsl:value-of
                     select="$AKNnaam" /><axsl:text />'. Pas de naamgeving voor dit element en alle
      onderliggende elementen aan. Controleer ook de naamgeving van de bijbehorende eId en
      onderliggende elementen.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M22" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M22" />
   <axsl:template match="@*|node()" priority="-2" mode="M22"><axsl:apply-templates select="*"
         mode="M22" /></axsl:template>

   <!--PATTERN
   sch_tekst_014Tabel - minimale opbouw-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Tabel - minimale opbouw</svrl:text>

   <!--RULE -->
   <axsl:template match="tekst:table/tekst:tgroup" priority="1000" mode="M23"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="tekst:table/tekst:tgroup" />

      <!--ASSERT
      waarschuwing-->
<axsl:choose>
         <axsl:when test="number(@cols) &gt;= 2" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="number(@cols) &gt;= 2">
               <axsl:attribute name="id">STOP0029</axsl:attribute>
               <axsl:attribute name="role">waarschuwing</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0029", "eId": "<axsl:text /><axsl:value-of
                     select="parent::tekst:table/@eId" /><axsl:text />", "melding": "De tabel met <axsl:text /><axsl:value-of
                     select="parent::tekst:table/@eId" /><axsl:text /> heeft slechts 1 kolom, dit is
      niet toegestaan. Pas de tabel aan, of plaats de inhoud van de tabel naar bijvoorbeeld een
      element Kadertekst", "ernst": "waarschuwing"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M23" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M23" />
   <axsl:template match="@*|node()" priority="-2" mode="M23"><axsl:apply-templates select="*"
         mode="M23" /></axsl:template>

   <!--PATTERN
   sch_tekst_016Tabel - positie en identificatie van een tabelcel-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Tabel - positie en identificatie van een
      tabelcel</svrl:text>

   <!--RULE -->
   <axsl:template match="tekst:entry[@namest and @colname]" priority="1000" mode="M24"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="tekst:entry[@namest and @colname]" /><axsl:variable
         name="start" select="@namest" /><axsl:variable name="col" select="@colname" />

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="$col = $start" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="$col = $start">
               <axsl:attribute name="id">STOP0033</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0033", "naam": "<axsl:text /><axsl:value-of
                     select="@namest" /><axsl:text />", "nummer": "<axsl:text /><axsl:value-of
                     select="count(parent::tekst:row/preceding-sibling::tekst:row) + 1" /><axsl:text />",
      "ouder": "<axsl:text /><axsl:value-of
                     select="local-name(ancestor::tekst:thead | ancestor::tekst:tbody)" /><axsl:text />",
      "eId": "<axsl:text /><axsl:value-of select="ancestor::tekst:table/@eId" /><axsl:text />",
      "melding": "De start van de overspanning (@namest) van de cel <axsl:text /><axsl:value-of
                     select="@namest" /><axsl:text />, in de <axsl:text /><axsl:value-of
                     select="count(parent::tekst:row/preceding-sibling::tekst:row) + 1" /><axsl:text />e
      rij, van de <axsl:text /><axsl:value-of
                     select="local-name(ancestor::tekst:thead | ancestor::tekst:tbody)" /><axsl:text />
      van tabel <axsl:text /><axsl:value-of select="ancestor::tekst:table/@eId" /><axsl:text /> is
      niet gelijk aan de @colname van de cel.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M24" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M24" />
   <axsl:template match="@*|node()" priority="-2" mode="M24"><axsl:apply-templates select="*"
         mode="M24" /></axsl:template>

   <!--PATTERN -->


   <!--RULE -->
   <axsl:template match="tekst:entry[@namest][@nameend]" priority="1000" mode="M25"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="tekst:entry[@namest][@nameend]" /><axsl:variable
         name="start" select="@namest" /><axsl:variable name="end" select="@nameend" /><axsl:variable
         name="colPosities">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
            xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
            select="ancestor::tekst:tgroup/tekst:colspec">
            <xsl:variable name="colnum">
               <xsl:choose>
                  <xsl:when test="@colnum">
                     <xsl:value-of select="@colnum" />
                  </xsl:when>
                  <xsl:otherwise>
                     <xsl:value-of select="position()" />
                  </xsl:otherwise>
               </xsl:choose>
            </xsl:variable>
               <col
               colnum="{$colnum}" name="{@colname}" />
         </xsl:for-each>
      </axsl:variable>

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when
            test="xs:integer($colPosities/*[@name = $start]/@colnum) &lt;= xs:integer($colPosities/*[@name = $end]/@colnum)" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="xs:integer($colPosities/*[@name = $start]/@colnum) &lt;= xs:integer($colPosities/*[@name = $end]/@colnum)">
               <axsl:attribute name="id">STOP0032</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0032", "naam": "<axsl:text /><axsl:value-of
                     select="@namest" /><axsl:text />", "nummer": "<axsl:text /><axsl:value-of
                     select="count(parent::tekst:row/preceding-sibling::tekst:row) + 1" /><axsl:text />",
      "ouder": "<axsl:text /><axsl:value-of
                     select="local-name(ancestor::tekst:thead | ancestor::tekst:tbody)" /><axsl:text />",
      "eId": "<axsl:text /><axsl:value-of select="ancestor::tekst:table/@eId" /><axsl:text />",
      "melding": "De entry met @namest \"<axsl:text /><axsl:value-of select="@namest" /><axsl:text />\",
      van de <axsl:text /><axsl:value-of
                     select="count(parent::tekst:row/preceding-sibling::tekst:row) + 1" /><axsl:text />e
      rij, van de <axsl:text /><axsl:value-of
                     select="local-name(ancestor::tekst:thead | ancestor::tekst:tbody)" /><axsl:text />,
      in de tabel met eId: <axsl:text /><axsl:value-of select="ancestor::tekst:table/@eId" /><axsl:text />,
      heeft een positie bepaling groter dan de positie van de als @nameend genoemde cel. Corrigeer
      de gegevens voor de overspanning.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M25" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M25" />
   <axsl:template match="@*|node()" priority="-2" mode="M25"><axsl:apply-templates select="*"
         mode="M25" /></axsl:template>

   <!--PATTERN -->


   <!--RULE -->
   <axsl:template match="tekst:entry[@colname]" priority="1000" mode="M26"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="tekst:entry[@colname]" /><axsl:variable
         name="id" select="@colname" />

      <!--REPORT
      fout-->
<axsl:if
         test="not(ancestor::tekst:tgroup/tekst:colspec[@colname = $id])"><svrl:successful-report
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
            test="not(ancestor::tekst:tgroup/tekst:colspec[@colname = $id])">
            <axsl:attribute name="id">STOP0036</axsl:attribute>
            <axsl:attribute name="role">fout</axsl:attribute>
            <axsl:attribute name="location"><axsl:apply-templates select="."
                  mode="schematron-select-full-path" /></axsl:attribute>
            <svrl:text> {"code": "STOP0036", "naam": "colname", "nummer": "<axsl:text /><axsl:value-of
                  select="count(parent::tekst:row/preceding-sibling::tekst:row) + 1" /><axsl:text />",
      "ouder": "<axsl:text /><axsl:value-of
                  select="local-name(ancestor::tekst:thead | ancestor::tekst:tbody)" /><axsl:text />",
      "eId": "<axsl:text /><axsl:value-of select="ancestor::tekst:table/@eId" /><axsl:text />",
      "melding": "De entry met @colname van de <axsl:text /><axsl:value-of
                  select="count(parent::tekst:row/preceding-sibling::tekst:row) + 1" /><axsl:text />e
      rij, van <axsl:text /><axsl:value-of
                  select="local-name(ancestor::tekst:thead | ancestor::tekst:tbody)" /><axsl:text />,
      van de tabel met id: <axsl:text /><axsl:value-of select="ancestor::tekst:table/@eId" /><axsl:text />
      , verwijst niet naar een bestaande kolom. Controleer en corrigeer de identifier voor de kolom
      (@colname)", "ernst": "fout"},</svrl:text>
         </svrl:successful-report></axsl:if><axsl:apply-templates
         select="*" mode="M26" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M26" />
   <axsl:template match="@*|node()" priority="-2" mode="M26"><axsl:apply-templates select="*"
         mode="M26" /></axsl:template>

   <!--PATTERN
   sch_tekst_017Tabel - het aantal cellen is correct-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Tabel - het aantal cellen is correct</svrl:text>

   <!--RULE -->
   <axsl:template match="tekst:tgroup/tekst:thead | tekst:tgroup/tekst:tbody" priority="1000"
      mode="M27"><svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
         context="tekst:tgroup/tekst:thead | tekst:tgroup/tekst:tbody" /><axsl:variable
         name="totaalCellen" select="count(tekst:row) * number(parent::tekst:tgroup/@cols)" /><axsl:variable
         name="colPosities">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
            xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
            select="parent::tekst:tgroup/tekst:colspec">
            <xsl:variable name="colnum">
               <xsl:choose>
                  <xsl:when test="@colnum">
                     <xsl:value-of select="@colnum" />
                  </xsl:when>
                  <xsl:otherwise>
                     <xsl:value-of select="position()" />
                  </xsl:otherwise>
               </xsl:choose>
            </xsl:variable>
               <col
               colnum="{$colnum}" name="{@colname}" />
         </xsl:for-each>
      </axsl:variable><axsl:variable
         name="cellen" select="count(//tekst:entry[not(@wijzigactie = 'verwijder')])" /><axsl:variable
         name="spanEinde">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
            xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
            select="self::tekst:tbody//tekst:entry[not(@wijzigactie = 'verwijder')] | self::tekst:thead//tekst:entry[not(@wijzigactie = 'verwijder')]">
            <xsl:variable as="xs:string?" name="namest" select="@namest" />
               <xsl:variable
               as="xs:string?" name="nameend" select="@nameend" />
               <xsl:variable as="xs:integer?"
               name="numend" select="$colPosities/*[@name = $nameend]/@colnum" />
               <xsl:variable
               as="xs:integer?" name="numst" select="$colPosities/*[@name = $namest]/@colnum" />
               <nr>
               <xsl:choose>
                  <xsl:when test="$numend and $numst and @morerows">
                     <xsl:value-of select="($numend - $numst + 1) * (@morerows + 1)" />
                  </xsl:when>
                  <xsl:when test="$numend and $numst">
                     <xsl:value-of select="$numend - $numst + 1" />
                  </xsl:when>
                  <xsl:when test="@morerows">
                     <xsl:value-of select="1 + @morerows" />
                  </xsl:when>
                  <xsl:otherwise>1</xsl:otherwise>
               </xsl:choose>
            </nr>
         </xsl:for-each>
      </axsl:variable><axsl:variable
         name="spannend" select="sum($spanEinde/*)" />

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when
            test="number(parent::tekst:tgroup/@cols) = count(parent::tekst:tgroup/tekst:colspec)" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="number(parent::tekst:tgroup/@cols) = count(parent::tekst:tgroup/tekst:colspec)">
               <axsl:attribute name="id">STOP0037</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0037", "nummer": "<axsl:text /><axsl:value-of
                     select="count(parent::tekst:tgroup/tekst:colspec)" /><axsl:text />", "naam": "<axsl:text /><axsl:value-of
                     select="name(.)" /><axsl:text />", "eId": "<axsl:text /><axsl:value-of
                     select="ancestor::tekst:table/@eId" /><axsl:text />", "aantal": "<axsl:text /><axsl:value-of
                     select="parent::tekst:tgroup/@cols" /><axsl:text />", "melding": "Het aantal
      colspec's (<axsl:text /><axsl:value-of select="count(parent::tekst:tgroup/tekst:colspec)" /><axsl:text />)
      voor <axsl:text /><axsl:value-of select="name(.)" /><axsl:text /> in tabel <axsl:text /><axsl:value-of
                     select="ancestor::tekst:table/@eId" /><axsl:text /> komt niet overeen met het
      aantal kolommen (<axsl:text /><axsl:value-of select="parent::tekst:tgroup/@cols" /><axsl:text />).",
      "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose>

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="$totaalCellen = $spannend" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="$totaalCellen = $spannend">
               <axsl:attribute name="id">STOP0038</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0038", "aantal": "<axsl:text /><axsl:value-of
                     select="$spannend" /><axsl:text />", "naam": "<axsl:text /><axsl:value-of
                     select="name(.)" /><axsl:text />", "eId": "<axsl:text /><axsl:value-of
                     select="ancestor::tekst:table/@eId" /><axsl:text />", "nummer": "<axsl:text /><axsl:value-of
                     select="$totaalCellen" /><axsl:text />", "melding": "Het aantal cellen in <axsl:text /><axsl:value-of
                     select="name(.)" /><axsl:text /> van tabel \"<axsl:text /><axsl:value-of
                     select="ancestor::tekst:table/@eId" /><axsl:text />\" komt niet overeen met de
      verwachting (resultaat: <axsl:text /><axsl:value-of select="$spannend" /><axsl:text /> van
      verwachting <axsl:text /><axsl:value-of select="$totaalCellen" /><axsl:text />).", "ernst":
      "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M27" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M27" />
   <axsl:template match="@*|node()" priority="-2" mode="M27"><axsl:apply-templates select="*"
         mode="M27" /></axsl:template>

   <!--PATTERN
   sch_tekst_033Externe referentie, notatie-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Externe referentie, notatie</svrl:text>

   <!--RULE -->
   <axsl:template match="tekst:ExtRef" priority="1000" mode="M28"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="tekst:ExtRef" /><axsl:variable
         name="notatie">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
            xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="@soort = 'AKN'">/akn/</xsl:when>
            <xsl:when test="@soort = 'JCI'">jci1</xsl:when>
            <xsl:when test="@soort = 'URL'">http</xsl:when>
            <xsl:when test="@soort = 'JOIN'">/join/</xsl:when>
            <xsl:when test="@soort = 'document'" />
         </xsl:choose>
      </axsl:variable>

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="starts-with(@ref, $notatie)" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="starts-with(@ref, $notatie)">
               <axsl:attribute name="id">STOP0050</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text>{"code": "STOP0050", "type": "<axsl:text /><axsl:value-of select="@soort" /><axsl:text />",
      "ref": "<axsl:text /><axsl:value-of select="@ref" /><axsl:text />", "melding": "De ExtRef van
      het type <axsl:text /><axsl:value-of select="@soort" /><axsl:text /> met referentie <axsl:text /><axsl:value-of
                     select="@ref" /><axsl:text /> heeft niet de juiste notatie.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M28" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M28" />
   <axsl:template match="@*|node()" priority="-2" mode="M28"><axsl:apply-templates select="*"
         mode="M28" /></axsl:template>

   <!--PATTERN
   sch_tekst_037Gereserveerd zonder opvolgende elementen-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Gereserveerd zonder opvolgende elementen</svrl:text>

   <!--RULE -->
   <axsl:template
      match="tekst:Gereserveerd[not(ancestor::tekst:Vervang)][not(ancestor::tekst:Artikel)]"
      priority="1000" mode="M29"><svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
         context="tekst:Gereserveerd[not(ancestor::tekst:Vervang)][not(ancestor::tekst:Artikel)]" />

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="not(following-sibling::tekst:*)" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="not(following-sibling::tekst:*)">
               <axsl:attribute name="id">STOP0055</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0055", "naam": "<axsl:text /><axsl:value-of
                     select="local-name(following-sibling::tekst:*[1])" /><axsl:text />", "element":
      "<axsl:text /><axsl:value-of select="local-name(parent::tekst:*)" /><axsl:text />", "eId": "<axsl:text /><axsl:value-of
                     select="parent::tekst:*/@eId" /><axsl:text />", "melding": "Het element <axsl:text /><axsl:value-of
                     select="local-name(following-sibling::tekst:*[1])" /><axsl:text /> binnen <axsl:text /><axsl:value-of
                     select="local-name(parent::tekst:*)" /><axsl:text /> met eId: \"<axsl:text /><axsl:value-of
                     select="parent::tekst:*/@eId" /><axsl:text />\" is niet toegestaan na een
      element Gereserveerd. Verwijder het element Gereserveerd of verplaats dit element naar een
      eigen structuur of tekst.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M29" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M29" />
   <axsl:template match="@*|node()" priority="-2" mode="M29"><axsl:apply-templates select="*"
         mode="M29" /></axsl:template>

   <!--PATTERN
   sch_tekst_070Vervallen zonder opvolgende elementen-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Vervallen zonder opvolgende elementen</svrl:text>

   <!--RULE -->
   <axsl:template match="tekst:Artikel[not(ancestor::tekst:Vervang)]" priority="1000" mode="M30"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
         context="tekst:Artikel[not(ancestor::tekst:Vervang)]" />

      <!--REPORT
      fout-->
<axsl:if
         test="(child::tekst:Lid and (child::tekst:Inhoud or child::tekst:Vervallen or child::tekst:Gereserveerd)) or (child::tekst:Inhoud and (child::tekst:Vervallen or child::tekst:Gereserveerd))"><svrl:successful-report
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
            test="(child::tekst:Lid and (child::tekst:Inhoud or child::tekst:Vervallen or child::tekst:Gereserveerd)) or (child::tekst:Inhoud and (child::tekst:Vervallen or child::tekst:Gereserveerd))">
            <axsl:attribute name="id">STOP0070</axsl:attribute>
            <axsl:attribute name="role">fout</axsl:attribute>
            <axsl:attribute name="location"><axsl:apply-templates select="."
                  mode="schematron-select-full-path" /></axsl:attribute>
            <svrl:text> {"code": "STOP0070", "naam": "<axsl:text /><axsl:value-of
                  select="local-name()" /><axsl:text />", "eId": "<axsl:text /><axsl:value-of
                  select="@eId" /><axsl:text />", "melding": "Het <axsl:text /><axsl:value-of
                  select="local-name()" /><axsl:text /> met eId '<axsl:text /><axsl:value-of
                  select="@eId" /><axsl:text />' heeft een combinatie van elementen dat niet is
      toegestaan. Corrigeer het artikel door de combinatie van elementen te verwijderen.", "ernst":
      "fout"},</svrl:text>
         </svrl:successful-report></axsl:if><axsl:apply-templates
         select="*" mode="M30" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M30" />
   <axsl:template match="@*|node()" priority="-2" mode="M30"><axsl:apply-templates select="*"
         mode="M30" /></axsl:template>

   <!--PATTERN
   sch_tekst_039Structuur compleet-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Structuur compleet</svrl:text>

   <!--RULE -->
   <axsl:template
      match="tekst:Afdeling | tekst:Bijlage | tekst:Boek | tekst:Deel | tekst:Divisie | tekst:Hoofdstuk | tekst:Paragraaf | tekst:Subparagraaf | tekst:Subsubparagraaf | tekst:Titel[not(parent::tekst:Figuur)]"
      priority="1000" mode="M31"><svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
         context="tekst:Afdeling | tekst:Bijlage | tekst:Boek | tekst:Deel | tekst:Divisie | tekst:Hoofdstuk | tekst:Paragraaf | tekst:Subparagraaf | tekst:Subsubparagraaf | tekst:Titel[not(parent::tekst:Figuur)]" />

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="child::tekst:*[not(self::tekst:Kop)]" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="child::tekst:*[not(self::tekst:Kop)]">
               <axsl:attribute name="id">STOP0058</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0058", "naam": "<axsl:text /><axsl:value-of
                     select="name(.)" /><axsl:text />", "eId": "<axsl:text /><axsl:value-of
                     select="@eId" /><axsl:text />", "melding": "Het element <axsl:text /><axsl:value-of
                     select="name(.)" /><axsl:text /> met eId: \"<axsl:text /><axsl:value-of
                     select="@eId" /><axsl:text /> is niet compleet, een kind-element anders dan een
      Kop is verplicht. Completeer of verwijder dit structuur-element.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M31" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M31" />
   <axsl:template match="@*|node()" priority="-2" mode="M31"><axsl:apply-templates select="*"
         mode="M31" /></axsl:template>

   <!--PATTERN
   sch_tekst_041Divisietekst compleet-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Divisietekst compleet</svrl:text>

   <!--RULE -->
   <axsl:template match="tekst:Divisietekst" priority="1000" mode="M32"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="tekst:Divisietekst" />

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="child::tekst:*[not(self::tekst:Kop)]" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="child::tekst:*[not(self::tekst:Kop)]">
               <axsl:attribute name="id">STOP0060</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0060", "naam": "<axsl:text /><axsl:value-of
                     select="name(.)" /><axsl:text />", "eId": "<axsl:text /><axsl:value-of
                     select="@eId" /><axsl:text />", "melding": "Het element <axsl:text /><axsl:value-of
                     select="name(.)" /><axsl:text /> met eId: \"<axsl:text /><axsl:value-of
                     select="@eId" /><axsl:text /> is niet compleet, een kind-element anders dan een
      Kop is verplicht. Completeer of verwijder dit element.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M32" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M32" />
   <axsl:template match="@*|node()" priority="-2" mode="M32"><axsl:apply-templates select="*"
         mode="M32" /></axsl:template>

   <!--PATTERN
   sch_tekst_043Kennisgeving zonder divisie-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Kennisgeving zonder divisie</svrl:text>

   <!--RULE -->
   <axsl:template match="tekst:Divisie[ancestor::tekst:Kennisgeving]" priority="1000" mode="M33"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
         context="tekst:Divisie[ancestor::tekst:Kennisgeving]" />

      <!--REPORT
      fout-->
<axsl:if test="."><svrl:successful-report
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl" test=".">
            <axsl:attribute name="id">STOP0061</axsl:attribute>
            <axsl:attribute name="role">fout</axsl:attribute>
            <axsl:attribute name="location"><axsl:apply-templates select="."
                  mode="schematron-select-full-path" /></axsl:attribute>
            <svrl:text>{"code": "STOP0061", "eId": "<axsl:text /><axsl:value-of select="@eId" /><axsl:text />",
      "melding": "De kennisgeving bevat een Divisie met eId <axsl:text /><axsl:value-of
                  select="@eId" /><axsl:text />. Dit is niet toegestaan. Gebruik alleen
      Divisietekst.", "ernst": "fout"},</svrl:text>
         </svrl:successful-report></axsl:if><axsl:apply-templates
         select="*" mode="M33" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M33" />
   <axsl:template match="@*|node()" priority="-2" mode="M33"><axsl:apply-templates select="*"
         mode="M33" /></axsl:template>

   <!--PATTERN
   sch_tekst_044Vervallen structuur-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Vervallen structuur</svrl:text>

   <!--RULE -->
   <axsl:template
      match="tekst:Vervallen[not(ancestor::tekst:Vervang)][not(parent::tekst:Artikel)][not(parent::tekst:Divisietekst)]"
      priority="1000" mode="M34"><svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
         context="tekst:Vervallen[not(ancestor::tekst:Vervang)][not(parent::tekst:Artikel)][not(parent::tekst:Divisietekst)]" />

      <!--REPORT
      fout-->
<axsl:if
         test="following-sibling::tekst:*[not(child::tekst:Vervallen)]"><svrl:successful-report
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
            test="following-sibling::tekst:*[not(child::tekst:Vervallen)]">
            <axsl:attribute name="id">STOP0062</axsl:attribute>
            <axsl:attribute name="role">fout</axsl:attribute>
            <axsl:attribute name="location"><axsl:apply-templates select="."
                  mode="schematron-select-full-path" /></axsl:attribute>
            <svrl:text>{"code": "STOP0062", "naam": "<axsl:text /><axsl:value-of
                  select="local-name(parent::tekst:*)" /><axsl:text />", "eId": "<axsl:text /><axsl:value-of
                  select="parent::tekst:*/@eId" /><axsl:text />", "element": "<axsl:text /><axsl:value-of
                  select="local-name(following-sibling::tekst:*[not(child::tekst:Vervallen)][1])" /><axsl:text />",
      "id": "<axsl:text /><axsl:value-of
                  select="following-sibling::tekst:*[not(child::tekst:Vervallen)][1]/@eId" /><axsl:text />",
      "melding": "Het element <axsl:text /><axsl:value-of select="local-name(parent::tekst:*)" /><axsl:text />
      met eId: \"<axsl:text /><axsl:value-of select="parent::tekst:*/@eId" /><axsl:text />\" is
      vervallen, maar heeft minstens nog een niet vervallen element\". Controleer vanaf element <axsl:text /><axsl:value-of
                  select="local-name(following-sibling::tekst:*[not(child::tekst:Vervallen)][1])" /><axsl:text />
      met eId \"<axsl:text /><axsl:value-of
                  select="following-sibling::tekst:*[not(child::tekst:Vervallen)][1]/@eId" /><axsl:text />
      of alle onderliggende elementen als vervallen zijn aangemerkt.", "ernst": "fout"},</svrl:text>
         </svrl:successful-report></axsl:if><axsl:apply-templates
         select="*" mode="M34" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M34" />
   <axsl:template match="@*|node()" priority="-2" mode="M34"><axsl:apply-templates select="*"
         mode="M34" /></axsl:template>

   <!--PATTERN
   sch_tekst_045-->


   <!--RULE -->
   <axsl:template match="tekst:Contact" priority="1000" mode="M35"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="tekst:Contact" /><axsl:variable
         name="pattern">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
            xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="@soort = 'e-mail'">[^@]+@[^\.]+\..+</xsl:when>
            <xsl:otherwise>[onbekend-soort-adres]</xsl:otherwise>
         </xsl:choose>
      </axsl:variable><axsl:variable
         name="adres" select="@adres/./string()" />

      <!--ASSERT
      fout-->
<axsl:choose>
         <axsl:when test="matches($adres, $pattern)" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="matches($adres, $pattern)">
               <axsl:attribute name="id">STOP0064</axsl:attribute>
               <axsl:attribute name="role">fout</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0064", "adres": "<axsl:text /><axsl:value-of
                     select="./string()" /><axsl:text />", "eId": "<axsl:text /><axsl:value-of
                     select="ancestor::tekst:*[@eId][1]/@eId" /><axsl:text />", "melding": "Het
      e-mailadres <axsl:text /><axsl:value-of select="./string()" /><axsl:text /> zoals genoemd in
      het element Contact met eId <axsl:text /><axsl:value-of
                     select="ancestor::tekst:*[@eId][1]/@eId" /><axsl:text /> moet een correct
      geformatteerd e-mailadres zijn. Corrigeer het e-mailadres.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M35" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M35" />
   <axsl:template match="@*|node()" priority="-2" mode="M35"><axsl:apply-templates select="*"
         mode="M35" /></axsl:template>

   <!--PATTERN
   sch_tekst_046-->


   <!--RULE -->
   <axsl:template match="tekst:Motivering[@schemaversie]" priority="1000" mode="M36"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="tekst:Motivering[@schemaversie]" />

      <!--REPORT
      fout-->
<axsl:if
         test="ancestor::tekst:BesluitCompact|ancestor::tekst:BesluitKlassiek"><svrl:successful-report
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
            test="ancestor::tekst:BesluitCompact|ancestor::tekst:BesluitKlassiek">
            <axsl:attribute name="id">STOP0075</axsl:attribute>
            <axsl:attribute name="role">fout</axsl:attribute>
            <axsl:attribute name="location"><axsl:apply-templates select="."
                  mode="schematron-select-full-path" /></axsl:attribute>
            <svrl:text> {"code": "STOP0075", "schemaversie": "<axsl:text /><axsl:value-of
                  select="@schemaversie" /><axsl:text />", "melding": "Het attribuut schemaversie
      (met waarde <axsl:text /><axsl:value-of select="@schemaversie" /><axsl:text />) bij
      tekst:Motivering mag niet gebruikt worden binnen tekst:BesluitCompact of
      tekst:BesluitKlassiek. Verwijder het attribuut schemaversie bij tekst:Motivering", "ernst":
      "fout"},</svrl:text>
         </svrl:successful-report></axsl:if><axsl:apply-templates
         select="*" mode="M36" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M36" />
   <axsl:template match="@*|node()" priority="-2" mode="M36"><axsl:apply-templates select="*"
         mode="M36" /></axsl:template>

   <!--PATTERN
   sch_tekst_081Toelichting specifiek-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Toelichting specifiek</svrl:text>

   <!--RULE -->
   <axsl:template match="tekst:Toelichting" priority="1000" mode="M37"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="tekst:Toelichting" /><axsl:variable
         name="aantalKinderen"
         select="count(tekst:ArtikelgewijzeToelichting | tekst:AlgemeneToelichting)" />

      <!--REPORT
      ontraden-->
<axsl:if
         test="child::tekst:Divisie | child::tekst:Divisietekst"><svrl:successful-report
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
            test="child::tekst:Divisie | child::tekst:Divisietekst">
            <axsl:attribute name="id">STOP0081</axsl:attribute>
            <axsl:attribute name="role">ontraden</axsl:attribute>
            <axsl:attribute name="location"><axsl:apply-templates select="."
                  mode="schematron-select-full-path" /></axsl:attribute>
            <svrl:text> {"code": "STOP0081", "eId": "<axsl:text /><axsl:value-of select="@eId" /><axsl:text />",
      "melding": "De Toelichting met eId <axsl:text /><axsl:value-of select="@eId" /><axsl:text />
      heeft een structuur met Divisie of Divisietekst dat zal in de toekomst niet meer toegestaan
      zijn. Advies is om deze Divisie / Divisietekst elementen in een element AlgemeneToelichting of
      ArtikelgewijzeToelichting te plaatsen, indien mogelijk.", "ernst": "ontraden"},</svrl:text>
         </svrl:successful-report></axsl:if>

      <!--REPORT
      fout-->
<axsl:if
         test="xs:int($aantalKinderen) &gt;1 and not(child::tekst:Kop)"><svrl:successful-report
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
            test="xs:int($aantalKinderen) &gt;1 and not(child::tekst:Kop)">
            <axsl:attribute name="id">STOP0084</axsl:attribute>
            <axsl:attribute name="role">fout</axsl:attribute>
            <axsl:attribute name="location"><axsl:apply-templates select="."
                  mode="schematron-select-full-path" /></axsl:attribute>
            <svrl:text> {"code": "STOP0084", "eId": "<axsl:text /><axsl:value-of select="@eId" /><axsl:text />",
      "melding": "Het element Toelichting met eId <axsl:text /><axsl:value-of select="@eId" /><axsl:text />
      moet een Kop hebben omdat zowel een ArtikelgewijzeToelichting en een AlgemeneToelichting in de
      Toelichting zijn opgenomen. Geef de Toelichting een Kop met duidelijke tekstuele
      omschrijving.", "ernst": "fout"},</svrl:text>
         </svrl:successful-report></axsl:if>

      <!--REPORT
      fout-->
<axsl:if
         test="xs:int($aantalKinderen) =1 and child::tekst:Kop"><svrl:successful-report
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
            test="xs:int($aantalKinderen) =1 and child::tekst:Kop">
            <axsl:attribute name="id">STOP0085</axsl:attribute>
            <axsl:attribute name="role">fout</axsl:attribute>
            <axsl:attribute name="location"><axsl:apply-templates select="."
                  mode="schematron-select-full-path" /></axsl:attribute>
            <svrl:text> {"code": "STOP0085", "eId": "<axsl:text /><axsl:value-of select="@eId" /><axsl:text />",
      "localName": "<axsl:text /><axsl:value-of select="local-name(child::tekst:*[2])" /><axsl:text />",
      "melding": "Het element Toelichting met eId <axsl:text /><axsl:value-of select="@eId" /><axsl:text />
      heeft een Kop; deze is niet toegestaan omdat het enige onderliggende element <axsl:text /><axsl:value-of
                  select="local-name(child::tekst:*[2])" /><axsl:text /> al een Kop heeft. Verwijder
      de Kop voor het element Toelichting.", "ernst": "fout"},</svrl:text>
         </svrl:successful-report></axsl:if><axsl:apply-templates
         select="*" mode="M37" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M37" />
   <axsl:template match="@*|node()" priority="-2" mode="M37"><axsl:apply-templates select="*"
         mode="M37" /></axsl:template>

   <!--PATTERN
   sch_tekst_082ArtikelgewijzeToelichting buiten Toelichting-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">ArtikelgewijzeToelichting buiten
      Toelichting</svrl:text>

   <!--RULE -->
   <axsl:template match="tekst:ArtikelgewijzeToelichting" priority="1000" mode="M38"><svrl:fired-rule
         xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="tekst:ArtikelgewijzeToelichting" />

      <!--ASSERT
      ontraden-->
<axsl:choose>
         <axsl:when test="parent::tekst:Toelichting" />
         <axsl:otherwise><svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               test="parent::tekst:Toelichting">
               <axsl:attribute name="id">STOP0082</axsl:attribute>
               <axsl:attribute name="role">ontraden</axsl:attribute>
               <axsl:attribute name="location"><axsl:apply-templates select="."
                     mode="schematron-select-full-path" /></axsl:attribute>
               <svrl:text> {"code": "STOP0082", "eId": "<axsl:text /><axsl:value-of select="@eId" /><axsl:text />",
      "melding": "De Toelichting met eId <axsl:text /><axsl:value-of select="@eId" /><axsl:text />
      heeft een structuur met Divisie of Divisietekst dat zal in de toekomst niet meer toegestaan
      zijn. Advies is om deze Divisie / Divisietekst elementen in een element AlgemeneToelichting of
      ArtikelgewijzeToelichting te plaatsen indien mogelijk.", "ernst": "ontraden"},</svrl:text>
            </svrl:failed-assert></axsl:otherwise>
      </axsl:choose><axsl:apply-templates
         select="*" mode="M38" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M38" />
   <axsl:template match="@*|node()" priority="-2" mode="M38"><axsl:apply-templates select="*"
         mode="M38" /></axsl:template>

   <!--PATTERN
   sch_tekst_083Inleidende tekst in Toelichtingen-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Inleidende tekst in Toelichtingen</svrl:text>

   <!--RULE -->
   <axsl:template
      match="tekst:AlgemeneToelichting | tekst:ArtikelgewijzeToelichting | tekst:Toelichting"
      priority="1000" mode="M39"><svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
         context="tekst:AlgemeneToelichting | tekst:ArtikelgewijzeToelichting | tekst:Toelichting" />

      <!--REPORT
      ontraden-->
<axsl:if
         test="child::tekst:InleidendeTekst"><svrl:successful-report
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl" test="child::tekst:InleidendeTekst">
            <axsl:attribute name="id">STOP0083</axsl:attribute>
            <axsl:attribute name="role">ontraden</axsl:attribute>
            <axsl:attribute name="location"><axsl:apply-templates select="."
                  mode="schematron-select-full-path" /></axsl:attribute>
            <svrl:text> {"code": "STOP0083", "eId": "<axsl:text /><axsl:value-of select="@eId" /><axsl:text />",
      "localName": "<axsl:text /><axsl:value-of select="local-name()" /><axsl:text />", "melding":
      "De <axsl:text /><axsl:value-of select="local-name()" /><axsl:text /> met eId <axsl:text /><axsl:value-of
                  select="@eId" /><axsl:text /> heeft een element InleidendeTekst dat zal in de
      toekomst niet meer toegestaan zijn. Advies is om deze InleidendeTekst te verwijderen of als
      Divisietekst op te nemen.", "ernst": "ontraden"},</svrl:text>
         </svrl:successful-report></axsl:if><axsl:apply-templates
         select="*" mode="M39" /></axsl:template>
   <axsl:template match="text()" priority="-1" mode="M39" />
   <axsl:template match="@*|node()" priority="-2" mode="M39"><axsl:apply-templates select="*"
         mode="M39" /></axsl:template>
</axsl:stylesheet>