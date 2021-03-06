<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format">
    <xsl:variable name="page_width"><xsl:value-of select="/addresses/page_width"/></xsl:variable>
    <xsl:variable name="page_height"><xsl:value-of select="/addresses/page_height"/></xsl:variable>
    <xsl:variable name="initial_bottom_pos"><xsl:value-of select="/addresses/initial_bottom_pos"/></xsl:variable>
    <xsl:variable name="initial_left_pos"><xsl:value-of select="/addresses/initial_left_pos"/></xsl:variable>
    <xsl:variable name="height_increment"><xsl:value-of select="/addresses/height_incr"/></xsl:variable>
    <xsl:variable name="width_increment"><xsl:value-of select="/addresses/width_incr"/></xsl:variable>
    <xsl:variable name="frame_height"><xsl:value-of select="/addresses/label_height"/></xsl:variable>
    <xsl:variable name="frame_width"><xsl:value-of select="/addresses/label_width"/></xsl:variable>
    <xsl:variable name="number_columns"><xsl:value-of select="/addresses/cols"/></xsl:variable>
    <xsl:variable name="max_frames"><xsl:value-of select="/addresses/rows * /addresses/cols"/></xsl:variable>
    <xsl:variable name="printer_top"><xsl:value-of select="/addresses/printer_top"/></xsl:variable>
    <xsl:variable name="printer_bottom"><xsl:value-of select="/addresses/printer_bottom"/></xsl:variable>
    <xsl:variable name="printer_left"><xsl:value-of select="/addresses/printer_left"/></xsl:variable>
    <xsl:variable name="printer_right"><xsl:value-of select="/addresses/printer_right"/></xsl:variable>

    <xsl:template match="/">
        <xsl:apply-templates select="addresses"/>
    </xsl:template>

    <xsl:template match="addresses">
        <document>
            <template leftMargin="2.0cm" rightMargin="2.0cm" topMargin="2.0cm" bottomMargin="2.0cm" title="Address list" author="Generated by Tiny ERP">
                <xsl:attribute name="pageSize">
                    <xsl:value-of select="page_width"/><xsl:text>cm,</xsl:text><xsl:value-of select="page_height"/><xsl:text>cm</xsl:text>
                </xsl:attribute>
                <pageTemplate id="all">
                    <pageGraphics/>
                    <xsl:apply-templates select="address" mode="frames"/>
                </pageTemplate>
            </template>
            <stylesheet>
                <paraStyle name="nospace" spaceBefore="0" spaceAfter="0">
                    <xsl:attribute name="fontName">
                        <xsl:value-of select="font_type"/>
                    </xsl:attribute>
                    <xsl:attribute name="fontSize">
                        <xsl:value-of select="font_size"/>
                    </xsl:attribute>
                </paraStyle>
            </stylesheet>
            <story>
                <xsl:apply-templates select="address" mode="story">
                    <xsl:sort select="contact/country"/>
                    <xsl:sort select="contact/zip"/>
                    <xsl:sort select="company-name"/>
                </xsl:apply-templates>
            </story>
        </document>
    </xsl:template>

    <xsl:template match="address" mode="frames">
        <xsl:if test="position() &lt; $max_frames + 1">
            <xsl:variable name="width"><xsl:value-of select="$frame_width"/></xsl:variable>
            <xsl:variable name="height"><xsl:value-of select="$frame_height"/></xsl:variable>
            <xsl:variable name="x1"><xsl:value-of select="$initial_left_pos + ((position()-1) mod $number_columns) * $width_increment"/></xsl:variable>
            <xsl:variable name="y1"><xsl:value-of select="$initial_bottom_pos - floor((position()-1) div $number_columns) * $height_increment"/></xsl:variable>
            <frame>
            <xsl:choose>
                <!--Left labels over the left printer margin-->
                <xsl:when test="$x1 &lt; $printer_left">
                    <xsl:attribute name="x1">
                        <xsl:value-of select="$printer_left"/>
                        <xsl:text>cm</xsl:text>
                    </xsl:attribute>
                    <xsl:attribute name="width">
                        <xsl:value-of select="$width - ($printer_left - $x1)"/>
                        <xsl:text>cm</xsl:text>
                    </xsl:attribute>
                </xsl:when>
                <!--Right labels over the right printer margin-->
                <xsl:when test="$page_width - ($x1 + $width) &lt; $printer_right">
                    <xsl:attribute name="x1">
                        <xsl:value-of select="$x1"/>
                        <xsl:text>cm</xsl:text>
                    </xsl:attribute>
                    <xsl:attribute name="width">
                        <xsl:value-of select="$page_width - ($x1 + $printer_right)"/>
                        <xsl:text>cm</xsl:text>
                    </xsl:attribute>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:attribute name="x1">
                        <xsl:value-of select="$x1"/>
                        <xsl:text>cm</xsl:text>
                    </xsl:attribute>
                    <xsl:attribute name="width">
                        <xsl:value-of select="$width"/>
                        <xsl:text>cm</xsl:text>
                    </xsl:attribute>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:choose>
                <!--Bottom labels over the bottom printer margin-->
                <xsl:when test="$y1 &lt; $printer_bottom">
                    <xsl:attribute name="y1">
                        <xsl:value-of select="$printer_bottom"/>
                        <xsl:text>cm</xsl:text>
                    </xsl:attribute>
                    <xsl:attribute name="height">
                        <xsl:value-of select="$height - ($printer_bottom - $y1)"/>
                        <xsl:text>cm</xsl:text>
                    </xsl:attribute>
                </xsl:when>
                <!--Top labels over the top printer margin-->
                <xsl:when test="$page_height - ($y1 + $height) &lt; $printer_top">
                    <xsl:attribute name="y1">
                        <xsl:value-of select="$y1"/>
                        <xsl:text>cm</xsl:text>
                    </xsl:attribute>
                    <xsl:attribute name="height">
                        <xsl:value-of select="$page_height - ($y1 + $printer_top)"/>
                        <xsl:text>cm</xsl:text>
                    </xsl:attribute>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:attribute name="y1">
                        <xsl:value-of select="$y1"/>
                        <xsl:text>cm</xsl:text>
                    </xsl:attribute>
                    <xsl:attribute name="height">
                        <xsl:value-of select="$height"/>
                        <xsl:text>cm</xsl:text>
                    </xsl:attribute>
                </xsl:otherwise>
            </xsl:choose>
            </frame>
        </xsl:if>
    </xsl:template>

    <xsl:template match="address" mode="story">
        <para style="nospace">
        <!--<xsl:value-of select="position()"/> -->
        <xsl:value-of select="company-name"/><xsl:text> </xsl:text><xsl:value-of select="company-title"/></para>
        <xsl:choose>
            <xsl:when test="count(contact[type='default']) >= 1">
                <!-- apply the first 'contact' node with the type 'default' -->
                <xsl:apply-templates select="contact[type='default'][1]"/>
            </xsl:when>
            <xsl:when test="count(contact[type='']) >= 1">
                <!-- apply the first 'contact' node with an empty type -->
                <xsl:apply-templates select="contact[type=''][1]"/>
            </xsl:when>
            <xsl:otherwise>
                <!-- apply the first 'contact' node -->    
                <xsl:apply-templates select="contact[1]"/>
            </xsl:otherwise>
        </xsl:choose>
        <nextFrame/>
    </xsl:template>
    
    <xsl:template match="contact">
        <para style="nospace"><xsl:value-of select="title"/><xsl:text> </xsl:text><xsl:value-of select="name"/></para>
        <para style="nospace"><xsl:value-of select="street"/></para>
        <para style="nospace"><xsl:value-of select="street2"/></para>
        <para style="nospace"><xsl:value-of select="zip"/><xsl:text> </xsl:text><xsl:value-of select="city"/></para>
        <para style="nospace"><xsl:value-of select="state"/></para>
        <para style="nospace"><xsl:value-of select="country"/></para>
    </xsl:template>
</xsl:stylesheet>
