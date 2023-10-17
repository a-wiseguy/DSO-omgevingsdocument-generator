<?xml version="1.0"?>
<!--
     XSLT die uit een GIO alle Locaties selecteert
     en in een FeatureCollection stopt die in QGIS kan worden ingelezen.

     Wilko Quak (wilko.quak@koop.overheid.nl)
-->
<xsl:stylesheet version="2.0" xmlns:geo="https://standaarden.overheid.nl/stop/imop/geo/"
    xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output encoding="UTF-8" indent="yes" method="xml" version="1.0" />

    <xsl:template match="/">
        <geo:FeatureCollection xmlns:geo="https://standaarden.overheid.nl/stop/imop/geo/"
            xmlns:gml="http://www.opengis.net/gml/3.2">
            <!-- converteer alle Locaties -->
            <xsl:apply-templates select="//geo:Locatie" />
        </geo:FeatureCollection>
    </xsl:template>

    <xsl:template match="geo:Locatie">
        <geo:featureMember>
            <xsl:copy-of select="." />
        </geo:featureMember>
    </xsl:template>
</xsl:stylesheet>
