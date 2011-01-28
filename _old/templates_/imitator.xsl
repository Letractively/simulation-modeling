<?xml version="1.0" encoding="utf-8" ?>
<!-- Общий файл шаблонов Имитатора -->
<xsl:stylesheet xmlns="http://www.w3.org/1999/xhtml" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="xhtml" doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" doctype-public="-//W3C//DTD XHTML 1.1//EN" encoding="utf-8" />
  
  <xsl:template match="/model">
    <html xmlns="http://www.w3.org/1999/xhtml">
      <head>
        <title><xsl:value-of select="@title" /> | <xsl:value-of select="@sitename" /></title>
        <link rel="stylesheet" type="text/css">
          <xsl:attribute name="href">
            <xsl:value-of select="/path" />
            <xsl:text>/styles.css</xsl:text>
          </xsl:attribute>
        </link>
        <xsl:call-template name="ie" />
        <script type="text/javascript" src="/modulargrid.js">&quot;&quot;</script>
        <script type="text/javascript" src="/scripts.js">&quot;&quot;</script>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
      </head>
      <body>
        <div id="header">
          <xsl:call-template name="header" />
        </div>
        
        <div id="main">
          <xsl:call-template name="main" />
          <div id="footer">
            <xsl:call-template name="footer" />
          </div>
        </div>
      </body>
    </html>
  </xsl:template>
  
  <xsl:template name="header">
    <div id="logo">
      <span id="sitename">
        <xsl:value-of select="@sitename" />
      </span>
      <xsl:value-of select="@title" />
    </div>
    <div id="sinusoid">
      <xsl:text> </xsl:text>
    </div>
  </xsl:template>

  <xsl:template name="footer">
    <xsl:text>©Altaisoft, 2010 - 2011</xsl:text>
  </xsl:template>

  <xsl:template name="ie">
    <xsl:comment>
      <xsl:text>[if IE 6]&gt;</xsl:text>
      <xsl:text>&lt;link rel="stylesheet" href="/ie/ie.css" type="text/css" /&gt;</xsl:text>
      <xsl:text>&lt;![endif]</xsl:text>
    </xsl:comment>
  </xsl:template>
  
</xsl:stylesheet>
