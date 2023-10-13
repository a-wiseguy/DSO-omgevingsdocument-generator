<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<xsl:stylesheet xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
                xmlns:iso="http://purl.oclc.org/dsdl/schematron"
                xmlns:lvbba="https://standaarden.overheid.nl/lvbb/stop/aanlevering/"
                xmlns:saxon="http://saxon.sf.net/"
                xmlns:schold="http://www.ascc.net/xml/schematron"
                xmlns:tekst="https://standaarden.overheid.nl/stop/imop/tekst/"
                xmlns:xhtml="http://www.w3.org/1999/xhtml"
                xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="2.0"><!--Implementers: please note that overriding process-prolog or process-root is 
    the preferred method for meta-stylesheets to use where possible. -->
   <xsl:param name="archiveDirParameter"/>
   <xsl:param name="archiveNameParameter"/>
   <xsl:param name="fileNameParameter"/>
   <xsl:param name="fileDirParameter"/>
   <xsl:variable name="document-uri">
      <xsl:value-of select="document-uri(/)"/>
   </xsl:variable>
   <!--PHASES-->
   <!--PROLOG-->
   <xsl:output xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
               method="xml"
               omit-xml-declaration="no"
               standalone="yes"
               indent="yes"/>
   <!--XSD TYPES FOR XSLT2-->
   <!--KEYS AND FUNCTIONS-->
   <!--DEFAULT RULES-->
   <!--MODE: SCHEMATRON-SELECT-FULL-PATH-->
   <!--This mode can be used to generate an ugly though full XPath for locators-->
   <xsl:template match="*" mode="schematron-select-full-path">
      <xsl:apply-templates select="." mode="schematron-get-full-path"/>
   </xsl:template>
   <!--MODE: SCHEMATRON-FULL-PATH-->
   <!--This mode can be used to generate an ugly though full XPath for locators-->
   <xsl:template match="*" mode="schematron-get-full-path">
      <xsl:apply-templates select="parent::*" mode="schematron-get-full-path"/>
      <xsl:text>/</xsl:text>
      <xsl:choose>
         <xsl:when test="namespace-uri()=''">
            <xsl:value-of select="name()"/>
         </xsl:when>
         <xsl:otherwise>
            <xsl:text>*:</xsl:text>
            <xsl:value-of select="local-name()"/>
            <xsl:text>[namespace-uri()='</xsl:text>
            <xsl:value-of select="namespace-uri()"/>
            <xsl:text>']</xsl:text>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:variable name="preceding"
                    select="count(preceding-sibling::*[local-name()=local-name(current())                                   and namespace-uri() = namespace-uri(current())])"/>
      <xsl:text>
		[</xsl:text>
      <xsl:value-of select="1+ $preceding"/>
      <xsl:text>]</xsl:text>
   </xsl:template>
   <xsl:template match="@*" mode="schematron-get-full-path">
      <xsl:apply-templates select="parent::*" mode="schematron-get-full-path"/>
      <xsl:text>/</xsl:text>
      <xsl:choose>
         <xsl:when test="namespace-uri()=''">@<xsl:value-of select="name()"/>
         </xsl:when>
         <xsl:otherwise>
            <xsl:text>@*[local-name()='</xsl:text>
            <xsl:value-of select="local-name()"/>
            <xsl:text>' and namespace-uri()='</xsl:text>
            <xsl:value-of select="namespace-uri()"/>
            <xsl:text>']</xsl:text>
         </xsl:otherwise>
      </xsl:choose>
   </xsl:template>
   <!--MODE: SCHEMATRON-FULL-PATH-2-->
   <!--This mode can be used to generate prefixed XPath for humans-->
   <xsl:template match="node() | @*" mode="schematron-get-full-path-2">
      <xsl:for-each select="ancestor-or-self::*">
         <xsl:text>/</xsl:text>
         <xsl:value-of select="name(.)"/>
         <xsl:if test="preceding-sibling::*[name(.)=name(current())]">
            <xsl:text>[</xsl:text>
            <xsl:value-of select="count(preceding-sibling::*[name(.)=name(current())])+1"/>
            <xsl:text>]</xsl:text>
         </xsl:if>
      </xsl:for-each>
      <xsl:if test="not(self::*)">
         <xsl:text/>/@<xsl:value-of select="name(.)"/>
      </xsl:if>
   </xsl:template>
   <!--MODE: SCHEMATRON-FULL-PATH-3-->
   <!--This mode can be used to generate prefixed XPath for humans 
	(Top-level element has index)-->
   <xsl:template match="node() | @*" mode="schematron-get-full-path-3">
      <xsl:for-each select="ancestor-or-self::*">
         <xsl:text>/</xsl:text>
         <xsl:value-of select="name(.)"/>
         <xsl:if test="parent::*">
            <xsl:text>[</xsl:text>
            <xsl:value-of select="count(preceding-sibling::*[name(.)=name(current())])+1"/>
            <xsl:text>]</xsl:text>
         </xsl:if>
      </xsl:for-each>
      <xsl:if test="not(self::*)">
         <xsl:text/>/@<xsl:value-of select="name(.)"/>
      </xsl:if>
   </xsl:template>
   <!--MODE: GENERATE-ID-FROM-PATH -->
   <xsl:template match="/" mode="generate-id-from-path"/>
   <xsl:template match="text()" mode="generate-id-from-path">
      <xsl:apply-templates select="parent::*" mode="generate-id-from-path"/>
      <xsl:value-of select="concat('.text-', 1+count(preceding-sibling::text()), '-')"/>
   </xsl:template>
   <xsl:template match="comment()" mode="generate-id-from-path">
      <xsl:apply-templates select="parent::*" mode="generate-id-from-path"/>
      <xsl:value-of select="concat('.comment-', 1+count(preceding-sibling::comment()), '-')"/>
   </xsl:template>
   <xsl:template match="processing-instruction()" mode="generate-id-from-path">
      <xsl:apply-templates select="parent::*" mode="generate-id-from-path"/>
      <xsl:value-of select="concat('.processing-instruction-', 1+count(preceding-sibling::processing-instruction()), '-')"/>
   </xsl:template>
   <xsl:template match="@*" mode="generate-id-from-path">
      <xsl:apply-templates select="parent::*" mode="generate-id-from-path"/>
      <xsl:value-of select="concat('.@', name())"/>
   </xsl:template>
   <xsl:template match="*" mode="generate-id-from-path" priority="-0.5">
      <xsl:apply-templates select="parent::*" mode="generate-id-from-path"/>
      <xsl:text>.</xsl:text>
      <xsl:value-of select="concat('.',name(),'-',1+count(preceding-sibling::*[name()=name(current())]),'-')"/>
   </xsl:template>
   <!--MODE: GENERATE-ID-2 -->
   <xsl:template match="/" mode="generate-id-2">U</xsl:template>
   <xsl:template match="*" mode="generate-id-2" priority="2">
      <xsl:text>U</xsl:text>
      <xsl:number level="multiple" count="*"/>
   </xsl:template>
   <xsl:template match="node()" mode="generate-id-2">
      <xsl:text>U.</xsl:text>
      <xsl:number level="multiple" count="*"/>
      <xsl:text>n</xsl:text>
      <xsl:number count="node()"/>
   </xsl:template>
   <xsl:template match="@*" mode="generate-id-2">
      <xsl:text>U.</xsl:text>
      <xsl:number level="multiple" count="*"/>
      <xsl:text>_</xsl:text>
      <xsl:value-of select="string-length(local-name(.))"/>
      <xsl:text>_</xsl:text>
      <xsl:value-of select="translate(name(),':','.')"/>
   </xsl:template>
   <!--Strip characters-->
   <xsl:template match="text()" priority="-1"/>
   <!--SCHEMA SETUP-->
   <xsl:template match="/">
      <svrl:schematron-output xmlns:svrl="http://purl.oclc.org/dsdl/svrl" title="" schemaVersion="">
         <xsl:comment>
            <xsl:value-of select="$archiveDirParameter"/>   <xsl:value-of select="$archiveNameParameter"/>   <xsl:value-of select="$fileNameParameter"/>   <xsl:value-of select="$fileDirParameter"/>
         </xsl:comment>
         <svrl:text>Versie 1.2.0</svrl:text>
         <svrl:text>Schematron voor aanvullende validaties voor lvbba</svrl:text>
         <svrl:ns-prefix-in-attribute-values uri="https://standaarden.overheid.nl/stop/imop/data/" prefix="data"/>
         <svrl:ns-prefix-in-attribute-values uri="https://standaarden.overheid.nl/stop/imop/tekst/" prefix="tekst"/>
         <svrl:ns-prefix-in-attribute-values uri="https://standaarden.overheid.nl/lvbb/stop/aanlevering/"
                                             prefix="lvbba"/>
         <svrl:ns-prefix-in-attribute-values uri="http://www.w3.org/1999/XSL/Transform" prefix="xsl"/>
         <svrl:active-pattern>
            <xsl:attribute name="document">
               <xsl:value-of select="document-uri(/)"/>
            </xsl:attribute>
            <xsl:attribute name="id">sch_lvbba_003</xsl:attribute>
            <xsl:attribute name="name">BeoogdInformatieobject in overeenstemming met ExtIoRef/@eId</xsl:attribute>
            <xsl:apply-templates/>
         </svrl:active-pattern>
         <xsl:apply-templates select="/" mode="M6"/>
         <svrl:active-pattern>
            <xsl:attribute name="document">
               <xsl:value-of select="document-uri(/)"/>
            </xsl:attribute>
            <xsl:attribute name="id">sch_lvbba_004</xsl:attribute>
            <xsl:attribute name="name">Tijdstempels in ontwerpbesluit</xsl:attribute>
            <xsl:apply-templates/>
         </svrl:active-pattern>
         <xsl:apply-templates select="/" mode="M7"/>
         <svrl:active-pattern>
            <xsl:attribute name="document">
               <xsl:value-of select="document-uri(/)"/>
            </xsl:attribute>
            <xsl:attribute name="id">sch_lvbba_005</xsl:attribute>
            <xsl:attribute name="name">Besluit met soort werk '/join/id/stop/work_003'</xsl:attribute>
            <xsl:apply-templates/>
         </svrl:active-pattern>
         <xsl:apply-templates select="/" mode="M8"/>
         <svrl:active-pattern>
            <xsl:attribute name="document">
               <xsl:value-of select="document-uri(/)"/>
            </xsl:attribute>
            <xsl:attribute name="id">sch_lvbba_006</xsl:attribute>
            <xsl:attribute name="name">Regeling met soort werk '/join/id/stop/work_019</xsl:attribute>
            <xsl:apply-templates/>
         </svrl:active-pattern>
         <xsl:apply-templates select="/" mode="M9"/>
         <svrl:active-pattern>
            <xsl:attribute name="document">
               <xsl:value-of select="document-uri(/)"/>
            </xsl:attribute>
            <xsl:attribute name="id">sch_lvbba_009</xsl:attribute>
            <xsl:attribute name="name">eId van BeoogdeRegeling in Besluit</xsl:attribute>
            <xsl:apply-templates/>
         </svrl:active-pattern>
         <xsl:apply-templates select="/" mode="M10"/>
         <svrl:active-pattern>
            <xsl:attribute name="document">
               <xsl:value-of select="document-uri(/)"/>
            </xsl:attribute>
            <xsl:attribute name="id">sch_lvbba_010</xsl:attribute>
            <xsl:attribute name="name">eId van Tijdstempel in Besluit</xsl:attribute>
            <xsl:apply-templates/>
         </svrl:active-pattern>
         <xsl:apply-templates select="/" mode="M11"/>
         <svrl:active-pattern>
            <xsl:attribute name="document">
               <xsl:value-of select="document-uri(/)"/>
            </xsl:attribute>
            <xsl:attribute name="id">sch_lvbba_011</xsl:attribute>
            <xsl:attribute name="name">eId van data:Intrekking in Besluit</xsl:attribute>
            <xsl:apply-templates/>
         </svrl:active-pattern>
         <xsl:apply-templates select="/" mode="M12"/>
         <svrl:active-pattern>
            <xsl:attribute name="document">
               <xsl:value-of select="document-uri(/)"/>
            </xsl:attribute>
            <xsl:attribute name="id">sch_lvbba_021</xsl:attribute>
            <xsl:attribute name="name">Regeling met soort werk '/join/id/stop/work_021</xsl:attribute>
            <xsl:apply-templates/>
         </svrl:active-pattern>
         <xsl:apply-templates select="/" mode="M13"/>
         <svrl:active-pattern>
            <xsl:attribute name="document">
               <xsl:value-of select="document-uri(/)"/>
            </xsl:attribute>
            <xsl:attribute name="id">sch_lvbba_044</xsl:attribute>
            <xsl:attribute name="name">Een @wordt-versie in een besluit komt overeen met de FRBRExpression
         identificatie</xsl:attribute>
            <xsl:apply-templates/>
         </svrl:active-pattern>
         <xsl:apply-templates select="/" mode="M14"/>
         <svrl:active-pattern>
            <xsl:attribute name="document">
               <xsl:value-of select="document-uri(/)"/>
            </xsl:attribute>
            <xsl:attribute name="id">sch_lvbba_046</xsl:attribute>
            <xsl:attribute name="name">Procedurestap Publicatie</xsl:attribute>
            <xsl:apply-templates/>
         </svrl:active-pattern>
         <xsl:apply-templates select="/" mode="M15"/>
         <svrl:active-pattern>
            <xsl:attribute name="document">
               <xsl:value-of select="document-uri(/)"/>
            </xsl:attribute>
            <xsl:attribute name="id">sch_lvbba_047</xsl:attribute>
            <xsl:attribute name="name">definitief besluit ALLEEN de procedurestappen</xsl:attribute>
            <xsl:apply-templates/>
         </svrl:active-pattern>
         <xsl:apply-templates select="/" mode="M16"/>
         <svrl:active-pattern>
            <xsl:attribute name="document">
               <xsl:value-of select="document-uri(/)"/>
            </xsl:attribute>
            <xsl:attribute name="id">sch_lvbba_049</xsl:attribute>
            <xsl:attribute name="name">ontwerp besluit ALLEEN de procedurestappen</xsl:attribute>
            <xsl:apply-templates/>
         </svrl:active-pattern>
         <xsl:apply-templates select="/" mode="M17"/>
         <svrl:active-pattern>
            <xsl:attribute name="document">
               <xsl:value-of select="document-uri(/)"/>
            </xsl:attribute>
            <xsl:attribute name="id">sch_lvbba_057</xsl:attribute>
            <xsl:attribute name="name">kennisgeving procedurestappen</xsl:attribute>
            <xsl:apply-templates/>
         </svrl:active-pattern>
         <xsl:apply-templates select="/" mode="M18"/>
         <svrl:active-pattern>
            <xsl:attribute name="document">
               <xsl:value-of select="document-uri(/)"/>
            </xsl:attribute>
            <xsl:attribute name="id">sch_lvbba_058</xsl:attribute>
            <xsl:attribute name="name">FRBRExpression-identificatie RegelingVersieInformatie bij regelingmutatie</xsl:attribute>
            <xsl:apply-templates/>
         </svrl:active-pattern>
         <xsl:apply-templates select="/" mode="M19"/>
         <svrl:active-pattern>
            <xsl:attribute name="document">
               <xsl:value-of select="document-uri(/)"/>
            </xsl:attribute>
            <xsl:attribute name="id">sch_lvbba_063</xsl:attribute>
            <xsl:attribute name="name">Intrekking van een informatieobject</xsl:attribute>
            <xsl:apply-templates/>
         </svrl:active-pattern>
         <xsl:apply-templates select="/" mode="M20"/>
         <svrl:active-pattern>
            <xsl:attribute name="document">
               <xsl:value-of select="document-uri(/)"/>
            </xsl:attribute>
            <xsl:attribute name="id">sch_lvbba_066</xsl:attribute>
            <xsl:attribute name="name">Procedureverloop verplicht bij definitief besluit</xsl:attribute>
            <xsl:apply-templates/>
         </svrl:active-pattern>
         <xsl:apply-templates select="/" mode="M21"/>
         <svrl:active-pattern>
            <xsl:attribute name="document">
               <xsl:value-of select="document-uri(/)"/>
            </xsl:attribute>
            <xsl:attribute name="id">sch_lvbba_067</xsl:attribute>
            <xsl:attribute name="name">Procedureverloopmutatie verplicht bij
         soortKennisgeving="KennisgevingBesluittermijnen"</xsl:attribute>
            <xsl:apply-templates/>
         </svrl:active-pattern>
         <xsl:apply-templates select="/" mode="M22"/>
      </svrl:schematron-output>
   </xsl:template>
   <!--SCHEMATRON PATTERNS-->
   <!--PATTERN sch_lvbba_003BeoogdInformatieobject in overeenstemming met ExtIoRef/@eId-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">BeoogdInformatieobject in overeenstemming met ExtIoRef/@eId</svrl:text>
   <xsl:variable name="verzamelXioRefs">
      <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                    xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                    select="/lvbba:AanleveringBesluit/lvbba:BesluitVersie[//data:BeoogdInformatieobject]//tekst:ExtIoRef[not(ancestor-or-self::tekst:*[@wijzigactie = 'verwijder'])][not(ancestor::tekst:Verwijder)]">
         <set>
            <id>
               <xsl:if test="ancestor::tekst:*[@componentnaam][1]">
                  <xsl:value-of select="concat('!', ancestor::tekst:*[@componentnaam][1]/@componentnaam, '#')"/>
               </xsl:if>
               <xsl:value-of select="@eId"/>
            </id>
            <join>
               <xsl:value-of select="@ref"/>
            </join>
         </set>
      </xsl:for-each>
   </xsl:variable>
   <!--RULE -->
   <xsl:template match="lvbba:AanleveringBesluit//data:BeoogdInformatieobject"
                 priority="1000"
                 mode="M6">
      <svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                       context="lvbba:AanleveringBesluit//data:BeoogdInformatieobject"/>
      <xsl:variable name="joinID"
                    select="normalize-space(data:instrumentVersie/./string())"/>
      <xsl:variable name="data-eId" select="normalize-space(data:eId/./string())"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$verzamelXioRefs/set/id[. = $data-eId] and $verzamelXioRefs/set[id[. = $data-eId]]/join = $joinID"/>
         <xsl:otherwise>
            <svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                                test="$verzamelXioRefs/set/id[. = $data-eId] and $verzamelXioRefs/set[id[. = $data-eId]]/join = $joinID">
               <xsl:attribute name="id">BHKV1036</xsl:attribute>
               <xsl:attribute name="role">fout</xsl:attribute>
               <xsl:attribute name="location">
                  <xsl:apply-templates select="." mode="schematron-select-full-path"/>
               </xsl:attribute>
               <svrl:text> {"code": "BHKV1036", "eId": "<xsl:text/>
                  <xsl:value-of select="$data-eId"/>
                  <xsl:text/>",
            "instrument": "<xsl:text/>
                  <xsl:value-of select="$joinID"/>
                  <xsl:text/>", "melding": "De identifier van
            instrumentVersie \"<xsl:text/>
                  <xsl:value-of select="$joinID"/>
                  <xsl:text/>\" komt niet overeen met de ExtIoRef
            met eId \"<xsl:text/>
                  <xsl:value-of select="$data-eId"/>
                  <xsl:text/>\". Corrigeer de identifier of de eId zodat
            deze gelijk zijn.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M6"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M6"/>
   <xsl:template match="@*|node()" priority="-2" mode="M6">
      <xsl:apply-templates select="*" mode="M6"/>
   </xsl:template>
   <!--PATTERN sch_lvbba_004Tijdstempels in ontwerpbesluit-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Tijdstempels in ontwerpbesluit</svrl:text>
   <!--RULE -->
   <xsl:template match="data:BesluitMetadata/data:soortProcedure[normalize-space(./string()) = '/join/id/stop/proceduretype_ontwerp']"
                 priority="1000"
                 mode="M7">
      <svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                       context="data:BesluitMetadata/data:soortProcedure[normalize-space(./string()) = '/join/id/stop/proceduretype_ontwerp']"/>
      <!--REPORT fout-->
      <xsl:if test="ancestor::lvbba:AanleveringBesluit//data:ConsolidatieInformatie/data:Tijdstempels">
         <svrl:successful-report xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                                 test="ancestor::lvbba:AanleveringBesluit//data:ConsolidatieInformatie/data:Tijdstempels">
            <xsl:attribute name="id">BHKV1004</xsl:attribute>
            <xsl:attribute name="role">fout</xsl:attribute>
            <xsl:attribute name="location">
               <xsl:apply-templates select="." mode="schematron-select-full-path"/>
            </xsl:attribute>
            <svrl:text> {"code": "BHKV1004", "melding": "Het ontwerpbesluit heeft tijdstempels, dit
            is niet toegestaan. Verwijder de tijdstempels.", "ernst": "fout"},</svrl:text>
         </svrl:successful-report>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M7"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M7"/>
   <xsl:template match="@*|node()" priority="-2" mode="M7">
      <xsl:apply-templates select="*" mode="M7"/>
   </xsl:template>
   <!--PATTERN sch_lvbba_005Besluit met soort werk '/join/id/stop/work_003'-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Besluit met soort werk '/join/id/stop/work_003'</svrl:text>
   <!--RULE -->
   <xsl:template match="lvbba:AanleveringBesluit/lvbba:BesluitVersie"
                 priority="1000"
                 mode="M8">
      <svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                       context="lvbba:AanleveringBesluit/lvbba:BesluitVersie"/>
      <xsl:variable name="soortWork"
                    select="normalize-space(data:ExpressionIdentificatie/data:soortWork/./string())"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$soortWork = '/join/id/stop/work_003'"/>
         <xsl:otherwise>
            <svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                                test="$soortWork = '/join/id/stop/work_003'">
               <xsl:attribute name="id">BHKV1005</xsl:attribute>
               <xsl:attribute name="role">fout</xsl:attribute>
               <xsl:attribute name="location">
                  <xsl:apply-templates select="." mode="schematron-select-full-path"/>
               </xsl:attribute>
               <svrl:text>{"code": "BHKV1005", "id": "<xsl:text/>
                  <xsl:value-of select="$soortWork"/>
                  <xsl:text/>",
            "melding": "Het geleverde besluit heeft als soortWork '<xsl:text/>
                  <xsl:value-of select="$soortWork"/>
                  <xsl:text/>'
            , Dit moet zijn: '/join/id/stop/work_003'.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M8"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M8"/>
   <xsl:template match="@*|node()" priority="-2" mode="M8">
      <xsl:apply-templates select="*" mode="M8"/>
   </xsl:template>
   <!--PATTERN sch_lvbba_006Regeling met soort werk '/join/id/stop/work_019-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Regeling met soort werk '/join/id/stop/work_019</svrl:text>
   <!--RULE -->
   <xsl:template match="tekst:RegelingCompact | tekst:RegelingKlassiek | tekst:RegelingVrijetekst"
                 priority="1000"
                 mode="M9">
      <svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                       context="tekst:RegelingCompact | tekst:RegelingKlassiek | tekst:RegelingVrijetekst"/>
      <xsl:variable name="soortWork" select="'/join/id/stop/work_019'"/>
      <xsl:variable name="wordt" select="normalize-space(xs:string(@wordt))"/>
      <xsl:variable name="controle">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="ancestor::lvbba:AanleveringBesluit/lvbba:RegelingVersieInformatie">
            <xsl:choose>
               <xsl:when test="normalize-space(data:ExpressionIdentificatie/data:soortWork/xs:string(.)) = $soortWork and               normalize-space(data:ExpressionIdentificatie/data:FRBRExpression/xs:string(.)) = $wordt">
               |GOED|</xsl:when>
               <xsl:otherwise>
                  <xsl:value-of select="concat(normalize-space(data:ExpressionIdentificatie/data:soortWork/./string()), ' ')"/>
               </xsl:otherwise>
            </xsl:choose>
         </xsl:for-each>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="contains($controle, '|GOED|')"/>
         <xsl:otherwise>
            <svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                                test="contains($controle, '|GOED|')">
               <xsl:attribute name="id">BHKV1006</xsl:attribute>
               <xsl:attribute name="role">fout</xsl:attribute>
               <xsl:attribute name="location">
                  <xsl:apply-templates select="." mode="schematron-select-full-path"/>
               </xsl:attribute>
               <svrl:text>{"code":
            "BHKV1006", "id": "<xsl:text/>
                  <xsl:value-of select="normalize-space(replace($controle, ' /', ', /'))"/>
                  <xsl:text/>", "melding": "Het
            geleverde regelingversie heeft als soortWork '<xsl:text/>
                  <xsl:value-of select="normalize-space(replace($controle, ' /', ', /'))"/>
                  <xsl:text/>'. Dit moet voor een
            RegelingCompact, RegelingKlassiek of RegelingVrijetekst zijn '/join/id/stop/work_019'",
            "ernst": "fout"},</svrl:text>
            </svrl:failed-assert>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M9"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M9"/>
   <xsl:template match="@*|node()" priority="-2" mode="M9">
      <xsl:apply-templates select="*" mode="M9"/>
   </xsl:template>
   <!--PATTERN sch_lvbba_009eId van BeoogdeRegeling in Besluit-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">eId van BeoogdeRegeling in Besluit</svrl:text>
   <!--RULE -->
   <xsl:template match="data:BeoogdeRegeling" priority="1000" mode="M10">
      <svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl" context="data:BeoogdeRegeling"/>
      <xsl:variable name="eId" select="normalize-space(data:eId/./string())"/>
      <xsl:variable name="matchId">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="starts-with($eId, '!')">
               <xsl:value-of select="substring-after(replace($eId, '!', ''), '#')"/>
            </xsl:when>
            <xsl:otherwise>
               <xsl:value-of select="$eId"/>
            </xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <xsl:variable name="component">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="starts-with($eId, '!')">
               <xsl:value-of select="substring-before(replace($eId, '!', ''), '#')"/>
            </xsl:when>
            <xsl:otherwise>[geen_component]</xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="           ancestor::lvbba:BesluitVersie/tekst:BesluitCompact//tekst:Artikel[@eId = $matchId][not(ancestor::tekst:WijzigBijlage)] |           ancestor::lvbba:BesluitVersie/tekst:BesluitCompact//tekst:WijzigArtikel[@eId = $matchId][not(ancestor::tekst:WijzigBijlage)] |           ancestor::lvbba:BesluitVersie//tekst:RegelingKlassiek/tekst:Lichaam//tekst:Artikel[@eId = $matchId][ancestor::tekst:RegelingKlassiek[@componentnaam = $component]] |           ancestor::lvbba:BesluitVersie//tekst:RegelingKlassiek/tekst:Lichaam//tekst:WijzigArtikel[@eId = $matchId][ancestor::tekst:RegelingKlassiek[@componentnaam = $component]] |           ancestor::lvbba:AanleverenRectificatie//tekst:BesluitMutatie[@componentnaam = $component]//tekst:*[@eId = $matchId]"/>
         <xsl:otherwise>
            <svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                                test="ancestor::lvbba:BesluitVersie/tekst:BesluitCompact//tekst:Artikel[@eId = $matchId][not(ancestor::tekst:WijzigBijlage)] | ancestor::lvbba:BesluitVersie/tekst:BesluitCompact//tekst:WijzigArtikel[@eId = $matchId][not(ancestor::tekst:WijzigBijlage)] | ancestor::lvbba:BesluitVersie//tekst:RegelingKlassiek/tekst:Lichaam//tekst:Artikel[@eId = $matchId][ancestor::tekst:RegelingKlassiek[@componentnaam = $component]] | ancestor::lvbba:BesluitVersie//tekst:RegelingKlassiek/tekst:Lichaam//tekst:WijzigArtikel[@eId = $matchId][ancestor::tekst:RegelingKlassiek[@componentnaam = $component]] | ancestor::lvbba:AanleverenRectificatie//tekst:BesluitMutatie[@componentnaam = $component]//tekst:*[@eId = $matchId]">
               <xsl:attribute name="id">BHKV1009</xsl:attribute>
               <xsl:attribute name="role">fout</xsl:attribute>
               <xsl:attribute name="location">
                  <xsl:apply-templates select="." mode="schematron-select-full-path"/>
               </xsl:attribute>
               <svrl:text> {"code": "BHKV1009", "eId": "<xsl:text/>
                  <xsl:value-of select="$eId"/>
                  <xsl:text/>", "regeling": "<xsl:text/>
                  <xsl:value-of select="data:instrumentVersie"/>
                  <xsl:text/>", "melding": "In het besluit of rectificatie is de
            eId <xsl:text/>
                  <xsl:value-of select="$eId"/>
                  <xsl:text/> voor de BeoogdeRegeling <xsl:text/>
                  <xsl:value-of select="data:instrumentVersie"/>
                  <xsl:text/> niet te vinden. Controleer de referentie naar het
            besluit.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M10"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M10"/>
   <xsl:template match="@*|node()" priority="-2" mode="M10">
      <xsl:apply-templates select="*" mode="M10"/>
   </xsl:template>
   <!--PATTERN sch_lvbba_010eId van Tijdstempel in Besluit-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">eId van Tijdstempel in Besluit</svrl:text>
   <!--RULE -->
   <xsl:template match="data:ConsolidatieInformatie/data:Tijdstempels/data:Tijdstempel[data:eId]"
                 priority="1000"
                 mode="M11">
      <svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                       context="data:ConsolidatieInformatie/data:Tijdstempels/data:Tijdstempel[data:eId]"/>
      <xsl:variable name="refID" select="normalize-space(data:eId/./string())"/>
      <xsl:variable name="matchID">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="starts-with($refID, '!')">
               <xsl:value-of select="substring-after($refID, '#')"/>
            </xsl:when>
            <xsl:otherwise>
               <xsl:value-of select="$refID"/>
            </xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <xsl:variable name="component">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="starts-with($refID, '!')">
               <xsl:value-of select="substring-before(translate($refID, '!', ''), '#')"/>
            </xsl:when>
            <xsl:when test="ancestor::tekst:*[@componentnaam][1]">
               <xsl:value-of select="ancestor::tekst:*[@componentnaam][1]/@componentnaam"/>
            </xsl:when>
            <xsl:otherwise>[is_geen_component]</xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="           ancestor::lvbba:BesluitVersie/tekst:BesluitCompact//tekst:Artikel[@eId = $matchID][not(ancestor::tekst:WijzigBijlage)] |           ancestor::lvbba:BesluitVersie//tekst:RegelingKlassiek/tekst:Lichaam//tekst:Artikel[@eId = $matchID][ancestor::tekst:RegelingKlassiek[@componentnaam = $component]] |           ancestor::lvbba:AanleverenRectificatie//tekst:BesluitMutatie[@componentnaam = $component]//tekst:*[@eId = $matchID]"/>
         <xsl:otherwise>
            <svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                                test="ancestor::lvbba:BesluitVersie/tekst:BesluitCompact//tekst:Artikel[@eId = $matchID][not(ancestor::tekst:WijzigBijlage)] | ancestor::lvbba:BesluitVersie//tekst:RegelingKlassiek/tekst:Lichaam//tekst:Artikel[@eId = $matchID][ancestor::tekst:RegelingKlassiek[@componentnaam = $component]] | ancestor::lvbba:AanleverenRectificatie//tekst:BesluitMutatie[@componentnaam = $component]//tekst:*[@eId = $matchID]">
               <xsl:attribute name="id">BHKV1010</xsl:attribute>
               <xsl:attribute name="role">fout</xsl:attribute>
               <xsl:attribute name="location">
                  <xsl:apply-templates select="." mode="schematron-select-full-path"/>
               </xsl:attribute>
               <svrl:text> {"code": "BHKV1010", "eId": "<xsl:text/>
                  <xsl:value-of select="$refID"/>
                  <xsl:text/>", "melding":
            "In het besluit of rectificatie is de eId <xsl:text/>
                  <xsl:value-of select="$refID"/>
                  <xsl:text/> voor de
            tijdstempel niet te vinden. Controleer de referentie naar het besluit.", "ernst":
            "fout"},</svrl:text>
            </svrl:failed-assert>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M11"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M11"/>
   <xsl:template match="@*|node()" priority="-2" mode="M11">
      <xsl:apply-templates select="*" mode="M11"/>
   </xsl:template>
   <!--PATTERN sch_lvbba_011eId van data:Intrekking in Besluit-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">eId van data:Intrekking in Besluit</svrl:text>
   <!--RULE -->
   <xsl:template match="data:ConsolidatieInformatie/data:Intrekkingen/data:Intrekking[starts-with(xs:string(data:instrument), '/akn/')]"
                 priority="1000"
                 mode="M12">
      <svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                       context="data:ConsolidatieInformatie/data:Intrekkingen/data:Intrekking[starts-with(xs:string(data:instrument), '/akn/')]"/>
      <xsl:variable name="refID" select="normalize-space(data:eId/./string())"/>
      <xsl:variable name="matchID">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="starts-with($refID, '!')">
               <xsl:value-of select="substring-after($refID, '#')"/>
            </xsl:when>
            <xsl:otherwise>
               <xsl:value-of select="$refID"/>
            </xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <xsl:variable name="component">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="starts-with($refID, '!')">
               <xsl:value-of select="substring-before(translate($refID, '!', ''), '#')"/>
            </xsl:when>
            <xsl:when test="ancestor::tekst:*[@componentnaam][1]">
               <xsl:value-of select="ancestor::tekst:*[@componentnaam][1]/@componentnaam"/>
            </xsl:when>
            <xsl:otherwise>[is_geen_component]</xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="           ancestor::lvbba:BesluitVersie/tekst:BesluitCompact//tekst:Artikel[@eId = $matchID][not(ancestor::tekst:WijzigBijlage)] |           ancestor::lvbba:BesluitVersie/tekst:BesluitCompact//tekst:WijzigArtikel[@eId = $matchID][not(ancestor::tekst:WijzigBijlage)] |                  ancestor::lvbba:BesluitVersie//tekst:RegelingKlassiek/tekst:Lichaam//tekst:Artikel[@eId = $matchID][ancestor::tekst:RegelingKlassiek[@componentnaam = $component]] |           ancestor::lvbba:BesluitVersie//tekst:RegelingKlassiek/tekst:Lichaam//tekst:WijzigArtikel[@eId = $matchID][ancestor::tekst:RegelingKlassiek[@componentnaam = $component]] |           ancestor::lvbba:AanleverenRectificatie//tekst:BesluitMutatie[@componentnaam = $component]//tekst:*[@eId = $matchID]"/>
         <xsl:otherwise>
            <svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                                test="ancestor::lvbba:BesluitVersie/tekst:BesluitCompact//tekst:Artikel[@eId = $matchID][not(ancestor::tekst:WijzigBijlage)] | ancestor::lvbba:BesluitVersie/tekst:BesluitCompact//tekst:WijzigArtikel[@eId = $matchID][not(ancestor::tekst:WijzigBijlage)] | ancestor::lvbba:BesluitVersie//tekst:RegelingKlassiek/tekst:Lichaam//tekst:Artikel[@eId = $matchID][ancestor::tekst:RegelingKlassiek[@componentnaam = $component]] | ancestor::lvbba:BesluitVersie//tekst:RegelingKlassiek/tekst:Lichaam//tekst:WijzigArtikel[@eId = $matchID][ancestor::tekst:RegelingKlassiek[@componentnaam = $component]] | ancestor::lvbba:AanleverenRectificatie//tekst:BesluitMutatie[@componentnaam = $component]//tekst:*[@eId = $matchID]">
               <xsl:attribute name="id">BHKV1011</xsl:attribute>
               <xsl:attribute name="role">fout</xsl:attribute>
               <xsl:attribute name="location">
                  <xsl:apply-templates select="." mode="schematron-select-full-path"/>
               </xsl:attribute>
               <svrl:text> {"code": "BHKV1011", "eId": "<xsl:text/>
                  <xsl:value-of select="$refID"/>
                  <xsl:text/>",
            "instrumentversieRegeling": "<xsl:text/>
                  <xsl:value-of select="data:instrument"/>
                  <xsl:text/>", "melding": "In
            het besluit of rectificatie is de eId <xsl:text/>
                  <xsl:value-of select="$refID"/>
                  <xsl:text/> voor de
            data:Intrekking van de regeling <xsl:text/>
                  <xsl:value-of select="data:instrument"/>
                  <xsl:text/> niet te
            vinden. Controleer de referentie naar het besluit/rectificatie.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M12"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M12"/>
   <xsl:template match="@*|node()" priority="-2" mode="M12">
      <xsl:apply-templates select="*" mode="M12"/>
   </xsl:template>
   <!--PATTERN sch_lvbba_021Regeling met soort werk '/join/id/stop/work_021-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Regeling met soort werk '/join/id/stop/work_021</svrl:text>
   <!--RULE -->
   <xsl:template match="tekst:RegelingTijdelijkdeel" priority="1000" mode="M13">
      <svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                       context="tekst:RegelingTijdelijkdeel"/>
      <xsl:variable name="soortWork" select="'/join/id/stop/work_021'"/>
      <xsl:variable name="wordt" select="xs:string(@wordt)"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="ancestor::lvbba:AanleveringBesluit//data:ExpressionIdentificatie[normalize-space(xs:string(data:soortWork)) = $soortWork][normalize-space(xs:string(data:FRBRExpression)) = $wordt]"/>
         <xsl:otherwise>
            <svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                                test="ancestor::lvbba:AanleveringBesluit//data:ExpressionIdentificatie[normalize-space(xs:string(data:soortWork)) = $soortWork][normalize-space(xs:string(data:FRBRExpression)) = $wordt]">
               <xsl:attribute name="id">BHKV1028</xsl:attribute>
               <xsl:attribute name="role">fout</xsl:attribute>
               <xsl:attribute name="location">
                  <xsl:apply-templates select="." mode="schematron-select-full-path"/>
               </xsl:attribute>
               <svrl:text> {"code": "BHKV1028", "id": "<xsl:text/>
                  <xsl:value-of select="$wordt"/>
                  <xsl:text/>", "melding":
            "Het besluit heeft tekst:RegelingTijdelijkdeel met attribuut wordt=\"<xsl:text/>
                  <xsl:value-of select="$wordt"/>
                  <xsl:text/>\", maar data:ExpressionIdentificatie met <xsl:text/>
                  <xsl:value-of select="$wordt"/>
                  <xsl:text/> ontbreekt, of heeft als data:soortWork geen
            '/join/id/stop/work_021'. Corrigeer de data:ExpressionIdentificatie of
            tekst:RegelingTijdelijkdeel.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M13"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M13"/>
   <xsl:template match="@*|node()" priority="-2" mode="M13">
      <xsl:apply-templates select="*" mode="M13"/>
   </xsl:template>
   <!--PATTERN sch_lvbba_044Een @wordt-versie in een besluit komt overeen met de FRBRExpression
         identificatie-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Een @wordt-versie in een besluit komt overeen met de FRBRExpression
         identificatie</svrl:text>
   <!--RULE -->
   <xsl:template match="lvbba:AanleveringBesluit//tekst:*[@componentnaam]"
                 priority="1000"
                 mode="M14">
      <svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                       context="lvbba:AanleveringBesluit//tekst:*[@componentnaam]"/>
      <xsl:variable name="wordt" select="normalize-space(xs:string(@wordt))"/>
      <xsl:variable name="worden"
                    select="count(ancestor::lvbba:AanleveringBesluit//lvbba:RegelingVersieInformatie[data:ExpressionIdentificatie/data:FRBRExpression=$wordt])"/>
      <xsl:variable name="FRBRexpression">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="ancestor::lvbba:AanleveringBesluit/lvbba:RegelingVersieInformatie">
            <xsl:choose>
               <xsl:when test="$wordt = normalize-space(data:ExpressionIdentificatie/xs:string(data:FRBRExpression))"/>
               <xsl:otherwise>
                  <xsl:value-of select="concat(normalize-space(data:ExpressionIdentificatie/xs:string(data:FRBRExpression)), ' ')"/>
               </xsl:otherwise>
            </xsl:choose>
         </xsl:for-each>
      </xsl:variable>
      <xsl:variable name="melding">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="$worden &gt; 1">, of de data:FRBRExpression komt vaker dan 1x voor.</xsl:when>
            <xsl:otherwise/>
         </xsl:choose>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$worden = 1"/>
         <xsl:otherwise>
            <svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl" test="$worden = 1">
               <xsl:attribute name="id">BHKV1044</xsl:attribute>
               <xsl:attribute name="role">fout</xsl:attribute>
               <xsl:attribute name="location">
                  <xsl:apply-templates select="." mode="schematron-select-full-path"/>
               </xsl:attribute>
               <svrl:text> {"code": "BHKV1044", "wordt": "<xsl:text/>
                  <xsl:value-of select="normalize-space($wordt)"/>
                  <xsl:text/>", "component": "<xsl:text/>
                  <xsl:value-of select="@componentnaam"/>
                  <xsl:text/>", "melding": "Er moet versieinformatie meegeleverd worden
            voor \"<xsl:text/>
                  <xsl:value-of select="normalize-space($wordt)"/>
                  <xsl:text/>\" van component \"<xsl:text/>
                  <xsl:value-of select="@componentnaam"/>
                  <xsl:text/>\", deze ontbreekt <xsl:text/>
                  <xsl:value-of select="$melding"/>
                  <xsl:text/>. Voeg
            versieinformatie toe of verwijder de dubbele.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M14"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M14"/>
   <xsl:template match="@*|node()" priority="-2" mode="M14">
      <xsl:apply-templates select="*" mode="M14"/>
   </xsl:template>
   <!--PATTERN sch_lvbba_046Procedurestap Publicatie-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Procedurestap Publicatie</svrl:text>
   <!--RULE -->
   <xsl:template match="lvbba:AanleveringBesluit/lvbba:BesluitVersie/data:Procedureverloop/data:procedurestappen"
                 priority="1000"
                 mode="M15">
      <svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                       context="lvbba:AanleveringBesluit/lvbba:BesluitVersie/data:Procedureverloop/data:procedurestappen"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="not(data:Procedurestap[data:soortStap[. = '/join/id/stop/procedure/stap_004']])"/>
         <xsl:otherwise>
            <svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                                test="not(data:Procedurestap[data:soortStap[. = '/join/id/stop/procedure/stap_004']])">
               <xsl:attribute name="id">BHKV1046</xsl:attribute>
               <xsl:attribute name="role">fout</xsl:attribute>
               <xsl:attribute name="location">
                  <xsl:apply-templates select="." mode="schematron-select-full-path"/>
               </xsl:attribute>
               <svrl:text>
            {"code": "BHKV1046", "melding": "Het aangeleverde Procedureverloop bevat een stap
            Publicatie. Dit is niet toegestaan. Verwijder de stap Publicatie.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M15"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M15"/>
   <xsl:template match="@*|node()" priority="-2" mode="M15">
      <xsl:apply-templates select="*" mode="M15"/>
   </xsl:template>
   <!--PATTERN sch_lvbba_047definitief besluit ALLEEN de procedurestappen-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">definitief besluit ALLEEN de procedurestappen</svrl:text>
   <!--RULE -->
   <xsl:template match="lvbba:AanleveringBesluit/lvbba:BesluitVersie/data:Procedureverloop/data:procedurestappen[normalize-space(ancestor::lvbba:BesluitVersie/data:BesluitMetadata/data:soortProcedure/./string()) = '/join/id/stop/proceduretype_definitief']"
                 priority="1000"
                 mode="M16">
      <svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                       context="lvbba:AanleveringBesluit/lvbba:BesluitVersie/data:Procedureverloop/data:procedurestappen[normalize-space(ancestor::lvbba:BesluitVersie/data:BesluitMetadata/data:soortProcedure/./string()) = '/join/id/stop/proceduretype_definitief']"/>
      <xsl:variable name="stappen">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="data:Procedurestap/data:soortStap">
            <xsl:choose>
               <xsl:when test="normalize-space(./string()) = '/join/id/stop/procedure/stap_002'"/>
               <xsl:when test="normalize-space(./string()) = '/join/id/stop/procedure/stap_003'"/>
               <xsl:otherwise>
                  <xsl:value-of select="normalize-space(.)"/>
                  <xsl:text>, </xsl:text>
               </xsl:otherwise>
            </xsl:choose>
         </xsl:for-each>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$stappen = ''"/>
         <xsl:otherwise>
            <svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl" test="$stappen = ''">
               <xsl:attribute name="id">BHKV1047</xsl:attribute>
               <xsl:attribute name="role">fout</xsl:attribute>
               <xsl:attribute name="location">
                  <xsl:apply-templates select="." mode="schematron-select-full-path"/>
               </xsl:attribute>
               <svrl:text> {"code": "BHKV1047",
            "soortStap": "<xsl:text/>
                  <xsl:value-of select="normalize-space($stappen)"/>
                  <xsl:text/>", "melding":
            "Procedurestap(pen) \"<xsl:text/>
                  <xsl:value-of select="normalize-space($stappen)"/>
                  <xsl:text/>\" is/zijn niet
            toegestaan bij een Aanlevering definitief besluit. Verwijder deze stap(pen).", "ernst":
            "fout"},</svrl:text>
            </svrl:failed-assert>
         </xsl:otherwise>
      </xsl:choose>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="data:Procedurestap[normalize-space(data:soortStap/./string()) = '/join/id/stop/procedure/stap_003']"/>
         <xsl:otherwise>
            <svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                                test="data:Procedurestap[normalize-space(data:soortStap/./string()) = '/join/id/stop/procedure/stap_003']">
               <xsl:attribute name="id">BHKV1048</xsl:attribute>
               <xsl:attribute name="role">fout</xsl:attribute>
               <xsl:attribute name="location">
                  <xsl:apply-templates select="." mode="schematron-select-full-path"/>
               </xsl:attribute>
               <svrl:text>
            {"code": "BHKV1048", "melding": "Procedurestap Ondertekening ontbreekt bij een
            Aanlevering definitief besluit, deze is verplicht. Voeg deze stap toe.", "ernst":
            "fout"},</svrl:text>
            </svrl:failed-assert>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M16"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M16"/>
   <xsl:template match="@*|node()" priority="-2" mode="M16">
      <xsl:apply-templates select="*" mode="M16"/>
   </xsl:template>
   <!--PATTERN sch_lvbba_049ontwerp besluit ALLEEN de procedurestappen-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">ontwerp besluit ALLEEN de procedurestappen</svrl:text>
   <!--RULE -->
   <xsl:template match="lvbba:AanleveringBesluit/lvbba:BesluitVersie/data:Procedureverloop/data:procedurestappen[normalize-space(ancestor::lvbba:BesluitVersie/data:BesluitMetadata/data:soortProcedure/./string()) = '/join/id/stop/proceduretype_ontwerp']"
                 priority="1000"
                 mode="M17">
      <svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                       context="lvbba:AanleveringBesluit/lvbba:BesluitVersie/data:Procedureverloop/data:procedurestappen[normalize-space(ancestor::lvbba:BesluitVersie/data:BesluitMetadata/data:soortProcedure/./string()) = '/join/id/stop/proceduretype_ontwerp']"/>
      <xsl:variable name="stappen">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="data:Procedurestap/data:soortStap">
            <xsl:choose>
               <xsl:when test="normalize-space(./string()) = '/join/id/stop/procedure/stap_002'"/>
               <xsl:when test="normalize-space(./string()) = '/join/id/stop/procedure/stap_003'"/>
               <xsl:otherwise>
                  <xsl:value-of select="normalize-space(.)"/>
                  <xsl:text>, </xsl:text>
               </xsl:otherwise>
            </xsl:choose>
         </xsl:for-each>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$stappen = ''"/>
         <xsl:otherwise>
            <svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl" test="$stappen = ''">
               <xsl:attribute name="id">BHKV1049</xsl:attribute>
               <xsl:attribute name="role">fout</xsl:attribute>
               <xsl:attribute name="location">
                  <xsl:apply-templates select="." mode="schematron-select-full-path"/>
               </xsl:attribute>
               <svrl:text> {"code": "BHKV1049",
            "soortStap": "<xsl:text/>
                  <xsl:value-of select="normalize-space($stappen)"/>
                  <xsl:text/>", "melding":
            "Procedurestap \"<xsl:text/>
                  <xsl:value-of select="normalize-space($stappen)"/>
                  <xsl:text/>\" is niet
            toegestaan bij een Aanlevering ontwerp besluit. Verwijder deze stap.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M17"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M17"/>
   <xsl:template match="@*|node()" priority="-2" mode="M17">
      <xsl:apply-templates select="*" mode="M17"/>
   </xsl:template>
   <!--PATTERN sch_lvbba_057kennisgeving procedurestappen-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">kennisgeving procedurestappen</svrl:text>
   <!--RULE -->
   <xsl:template match="lvbba:AanleveringKennisgeving//data:Procedureverloop/data:procedurestappen/data:Procedurestap/data:soortStap"
                 priority="1000"
                 mode="M18">
      <svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                       context="lvbba:AanleveringKennisgeving//data:Procedureverloop/data:procedurestappen/data:Procedurestap/data:soortStap"/>
      <xsl:variable name="stappen"
                    select="'/join/id/stop/procedure/stap_005|/join/id/stop/procedure/stap_014|/join/id/stop/procedure/stap_016|/join/id/stop/procedure/stap_015'"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches(normalize-space(./text()), $stappen)"/>
         <xsl:otherwise>
            <svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                                test="matches(normalize-space(./text()), $stappen)">
               <xsl:attribute name="id">BHKV1057</xsl:attribute>
               <xsl:attribute name="role">fout</xsl:attribute>
               <xsl:attribute name="location">
                  <xsl:apply-templates select="." mode="schematron-select-full-path"/>
               </xsl:attribute>
               <svrl:text> {"code": "BHKV1057", "soortStap": "<xsl:text/>
                  <xsl:value-of select="normalize-space(./text())"/>
                  <xsl:text/>", "melding": "Procedurestap \"<xsl:text/>
                  <xsl:value-of select="normalize-space(./text())"/>
                  <xsl:text/>\" is niet toegestaan bij een Aanlevering
            kennisgeving. Verwijder deze stap.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M18"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M18"/>
   <xsl:template match="@*|node()" priority="-2" mode="M18">
      <xsl:apply-templates select="*" mode="M18"/>
   </xsl:template>
   <!--PATTERN sch_lvbba_058FRBRExpression-identificatie RegelingVersieInformatie bij regelingmutatie-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">FRBRExpression-identificatie RegelingVersieInformatie bij regelingmutatie</svrl:text>
   <!--RULE -->
   <xsl:template match="lvbba:AanleveringBesluit/lvbba:RegelingVersieInformatie/data:ExpressionIdentificatie |       lvbba:AanleveringRectificatie/lvbba:RegelingVersieInformatie/data:ExpressionIdentificatie"
                 priority="1000"
                 mode="M19">
      <svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                       context="lvbba:AanleveringBesluit/lvbba:RegelingVersieInformatie/data:ExpressionIdentificatie |       lvbba:AanleveringRectificatie/lvbba:RegelingVersieInformatie/data:ExpressionIdentificatie"/>
      <xsl:variable name="FRBRexpression"
                    select="normalize-space(xs:string(data:FRBRExpression))"/>
      <xsl:variable name="testWordtID">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="ancestor::lvbba:AanleveringBesluit//tekst:RegelingMutatie[xs:string(@wordt) = $FRBRexpression] |             ancestor::lvbba:AanleveringRectificatie//tekst:RegelingMutatie[xs:string(@wordt) = $FRBRexpression]">
               <xsl:text>[goed]</xsl:text>
            </xsl:when>
            <xsl:when test="ancestor::lvbba:AanleveringBesluit//tekst:RegelingKlassiek[xs:string(@wordt) = $FRBRexpression]">
               <xsl:text>[goed]</xsl:text>
            </xsl:when>
            <xsl:when test="ancestor::lvbba:AanleveringBesluit//tekst:RegelingCompact[xs:string(@wordt) = $FRBRexpression]">
               <xsl:text>[goed]</xsl:text>
            </xsl:when>
            <xsl:when test="ancestor::lvbba:AanleveringBesluit//tekst:RegelingVrijetekst[xs:string(@wordt) = $FRBRexpression]">
               <xsl:text>[goed]</xsl:text>
            </xsl:when>
            <xsl:when test="ancestor::lvbba:AanleveringBesluit//tekst:RegelingTijdelijkdeel[xs:string(@wordt) = $FRBRexpression]">
               <xsl:text>[goed]</xsl:text>
            </xsl:when>
            <xsl:otherwise>[FRBRexpression-niet gevonden]</xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$testWordtID = '[goed]'"/>
         <xsl:otherwise>
            <svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl" test="$testWordtID = '[goed]'">
               <xsl:attribute name="id">BHKV1058</xsl:attribute>
               <xsl:attribute name="role">fout</xsl:attribute>
               <xsl:attribute name="location">
                  <xsl:apply-templates select="." mode="schematron-select-full-path"/>
               </xsl:attribute>
               <svrl:text> {"code": "BHKV1058",
            "FRBRExpression": "<xsl:text/>
                  <xsl:value-of select="$FRBRexpression"/>
                  <xsl:text/>", "melding": "Voor de
            FRBRExpression (<xsl:text/>
                  <xsl:value-of select="$FRBRexpression"/>
                  <xsl:text/>) is RegelingVersieInformatie
            aangeleverd, maar deze regelingversie komt niet voor in het Besluit als initiele
            regeling of als regelingmutatie. Verwijder de RegelingVersieInformatie, of voeg de
            FRBRExpression toe in een wordt attribuut.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M19"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M19"/>
   <xsl:template match="@*|node()" priority="-2" mode="M19">
      <xsl:apply-templates select="*" mode="M19"/>
   </xsl:template>
   <!--PATTERN sch_lvbba_063Intrekking van een informatieobject-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Intrekking van een informatieobject</svrl:text>
   <!--RULE -->
   <xsl:template match="data:ConsolidatieInformatie/data:Intrekkingen/data:Intrekking[starts-with(xs:string(data:instrument), '/join/id/')]"
                 priority="1000"
                 mode="M20">
      <svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                       context="data:ConsolidatieInformatie/data:Intrekkingen/data:Intrekking[starts-with(xs:string(data:instrument), '/join/id/')]"/>
      <xsl:variable name="refID" select="normalize-space(xs:string(data:eId))"/>
      <xsl:variable name="matchID">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="starts-with($refID, '!') and contains($refID, '#')">
               <xsl:value-of select="substring-after($refID, '#')"/>
            </xsl:when>
            <xsl:otherwise>
               <xsl:value-of select="$refID"/>
            </xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <xsl:variable name="component">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="starts-with($refID, '!') and contains($refID, '#')">
               <xsl:value-of select="substring-before(translate($refID, '!', ''), '#')"/>
            </xsl:when>
            <xsl:when test="ancestor::tekst:*[@componentnaam][1]">
               <xsl:value-of select="ancestor::tekst:*[@componentnaam][1]/@componentnaam"/>
            </xsl:when>
            <xsl:otherwise>[is_geen_component]</xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="         ancestor::lvbba:BesluitVersie/tekst:BesluitCompact/tekst:WijzigBijlage//tekst:RegelingMutatie[@componentnaam = $component]//tekst:ExtIoRef[@eId = $matchID][ancestor::tekst:Verwijder or ancestor::tekst:*/@wijzigactie='verwijder' or ancestor::tekst:VerwijderdeTekst] |         ancestor::lvbba:BesluitVersie//tekst:RegelingKlassiek/tekst:Lichaam//tekst:RegelingMutatie[@componentnaam = $component]//tekst:ExtIoRef[@eId = $matchID][ancestor::tekst:Verwijder or ancestor::tekst:*/@wijzigactie='verwijder' or ancestor::tekst:VerwijderdeTekst]"/>
         <xsl:otherwise>
            <svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                                test="ancestor::lvbba:BesluitVersie/tekst:BesluitCompact/tekst:WijzigBijlage//tekst:RegelingMutatie[@componentnaam = $component]//tekst:ExtIoRef[@eId = $matchID][ancestor::tekst:Verwijder or ancestor::tekst:*/@wijzigactie='verwijder' or ancestor::tekst:VerwijderdeTekst] | ancestor::lvbba:BesluitVersie//tekst:RegelingKlassiek/tekst:Lichaam//tekst:RegelingMutatie[@componentnaam = $component]//tekst:ExtIoRef[@eId = $matchID][ancestor::tekst:Verwijder or ancestor::tekst:*/@wijzigactie='verwijder' or ancestor::tekst:VerwijderdeTekst]">
               <xsl:attribute name="id">bhkv1063</xsl:attribute>
               <xsl:attribute name="role">fout</xsl:attribute>
               <xsl:attribute name="location">
                  <xsl:apply-templates select="." mode="schematron-select-full-path"/>
               </xsl:attribute>
               <svrl:text> {"code": "BHKV1063", "eId": "<xsl:text/>
                  <xsl:value-of select="$refID"/>
                  <xsl:text/>",
            "instrumentIO": "<xsl:text/>
                  <xsl:value-of select="data:instrument"/>
                  <xsl:text/>", "melding": "De eId(<xsl:text/>
                  <xsl:value-of select="$refID"/>
                  <xsl:text/>) van de data:Intrekking van <xsl:text/>
                  <xsl:value-of select="data:instrument"/>
                  <xsl:text/>
            is niet van een ExtIoRef binnen een wijzig- of verwijder- actie, tekst:verwijder of een
            tekst:verwijderdeTekst. Pas de eId aan, of plaats de ExtIoRef binnen een element met een
            wijzig- of verwijder- actie, tekst:verwijder of tekst:verwijderdeTekst.", "ernst":
            "fout"},</svrl:text>
            </svrl:failed-assert>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M20"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M20"/>
   <xsl:template match="@*|node()" priority="-2" mode="M20">
      <xsl:apply-templates select="*" mode="M20"/>
   </xsl:template>
   <!--PATTERN sch_lvbba_066Procedureverloop verplicht bij definitief besluit-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Procedureverloop verplicht bij definitief besluit</svrl:text>
   <!--RULE -->
   <xsl:template match="data:BesluitMetadata[data:soortProcedure='/join/id/stop/proceduretype_definitief']"
                 priority="1000"
                 mode="M21">
      <svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                       context="data:BesluitMetadata[data:soortProcedure='/join/id/stop/proceduretype_definitief']"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="ancestor::lvbba:BesluitVersie/data:Procedureverloop"/>
         <xsl:otherwise>
            <svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                                test="ancestor::lvbba:BesluitVersie/data:Procedureverloop">
               <xsl:attribute name="id">BHKV1066</xsl:attribute>
               <xsl:attribute name="role">fout</xsl:attribute>
               <xsl:attribute name="location">
                  <xsl:apply-templates select="." mode="schematron-select-full-path"/>
               </xsl:attribute>
               <svrl:text> {"code": "BHKV1066", "expressie-id": "<xsl:text/>
                  <xsl:value-of select="ancestor::lvbba:BesluitVersie/data:ExpressionIdentificatie/data:FRBRExpression"/>
                  <xsl:text/>",
            "melding": "Het aangeleverde besluit(<xsl:text/>
                  <xsl:value-of select="ancestor::lvbba:BesluitVersie/data:ExpressionIdentificatie/data:FRBRExpression"/>
                  <xsl:text/>)
            heeft als data:soortProcedure '/join/id/stop/proceduretype_definitief', maar heeft geen
            data:Procedureverloop module. Dit is niet toegestaan. Voeg module data:Procedureverloop
            toe, of wijzig data:soortProcedure.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M21"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M21"/>
   <xsl:template match="@*|node()" priority="-2" mode="M21">
      <xsl:apply-templates select="*" mode="M21"/>
   </xsl:template>
   <!--PATTERN sch_lvbba_067Procedureverloopmutatie verplicht bij
         soortKennisgeving="KennisgevingBesluittermijnen"-->
   <svrl:text xmlns:svrl="http://purl.oclc.org/dsdl/svrl">Procedureverloopmutatie verplicht bij
         soortKennisgeving="KennisgevingBesluittermijnen"</svrl:text>
   <!--RULE -->
   <xsl:template match="data:KennisgevingMetadata" priority="1000" mode="M22">
      <svrl:fired-rule xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                       context="data:KennisgevingMetadata"/>
      <xsl:variable name="KennisgevingBesluittermijnen"
                    select="data:soortKennisgeving = 'KennisgevingBesluittermijnen' or not(data:soortKennisgeving)"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="($KennisgevingBesluittermijnen and ../data:Procedureverloopmutatie and data:mededelingOver) or not($KennisgevingBesluittermijnen)"/>
         <xsl:otherwise>
            <svrl:failed-assert xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
                                test="($KennisgevingBesluittermijnen and ../data:Procedureverloopmutatie and data:mededelingOver) or not($KennisgevingBesluittermijnen)">
               <xsl:attribute name="id">BHKV1067</xsl:attribute>
               <xsl:attribute name="role">fout</xsl:attribute>
               <xsl:attribute name="location">
                  <xsl:apply-templates select="." mode="schematron-select-full-path"/>
               </xsl:attribute>
               <svrl:text> {"code": "BHKV1067", "expressie-id": "<xsl:text/>
                  <xsl:value-of select="../data:ExpressionIdentificatie/data:FRBRExpression"/>
                  <xsl:text/>", "melding":
            "AanleveringKennisgeving \"<xsl:text/>
                  <xsl:value-of select="../data:ExpressionIdentificatie/data:FRBRExpression"/>
                  <xsl:text/>\" heeft als
            data:soortKennisgeving=\"KennisgevingBesluittermijnen\" (of data:soortKennisgeving
            ontbreekt) maar heeft geen module data:Procedureverloopmutatie en het gegeven
            data:mededelingOver. Dit is niet toegestaan. Voeg data:Procedureverloopmutatie toe, of
            wijzig data:soortKennisgeving.", "ernst": "fout"},</svrl:text>
            </svrl:failed-assert>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M22"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M22"/>
   <xsl:template match="@*|node()" priority="-2" mode="M22">
      <xsl:apply-templates select="*" mode="M22"/>
   </xsl:template>
</xsl:stylesheet>
