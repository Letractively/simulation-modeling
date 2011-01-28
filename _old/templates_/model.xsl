<?xml version="1.0" encoding="utf-8" ?>
<!-- Шаблон модели -->
<xsl:stylesheet xmlns="http://www.w3.org/1999/xhtml" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:import href="imitator.xsl" />
  
  <xsl:template name="main">
    <!-- Общая структура страницы модели -->
    <div id="input">
      <xsl:apply-templates select="input" />
    </div>
    <xsl:if test="errors">
      <xsl:apply-templates select="errors" />
    </xsl:if>
    <xsl:if test="output">
      <div id="output">
        <xsl:apply-templates select="output" />
      </div>
    </xsl:if>
  </xsl:template>

  <!-- Пустые шаблоны для моделей, где переопределения не сделаны -->

  <xsl:template match="input">
    <div class="pod">
      <div class="title">
        <xsl:text>Параметры</xsl:text>
      </div>
      <div class="content">
        input form
      </div>
    </div>
  </xsl:template>
  
  <xsl:template match="output">
    <div class="pod">
      <div class="title">
        <xsl:text>Результаты моделирования</xsl:text>
      </div>
      <div class="content">
        results
      </div>
    </div>
  </xsl:template>

  <xsl:template name="path">
    <!-- Получает узел и выводит путь к нему, разделённый точками, начиная с элемента input -->
    <xsl:param name="node" />

    <xsl:if test="name($node/..) != 'input'">
      <xsl:value-of select="name($node/..)"/>
      <xsl:text>.</xsl:text>
    </xsl:if>
    <xsl:value-of select="name($node)"/>
  </xsl:template>

  <xsl:template name="error-handler">
    <!-- Выводит ошибку для HTML-элемента -->
    <xsl:param name="error" />

    <xsl:if test="$error">
      <xsl:attribute name="class">error</xsl:attribute>
      <xsl:attribute name="title">
        <xsl:value-of select="$error" />
      </xsl:attribute>
    </xsl:if>
  </xsl:template>

  <xsl:template name="input-text">
    <!-- HTML-элемент <input type="text"> -->

    <xsl:param name="node" />
    <xsl:param name="id" />

    <!-- Поле ввода типа text -->
    <input type="text">
      <xsl:attribute name="id"><xsl:value-of select="$id" /></xsl:attribute>
      <xsl:attribute name="name"><xsl:value-of select="$id" /></xsl:attribute>
      <xsl:attribute name="value"><xsl:value-of select="$node" /></xsl:attribute>

      <xsl:call-template name="error-handler">
        <xsl:with-param name="error" select="$node/@error" />
      </xsl:call-template>
    </input>
  </xsl:template>

  <xsl:template name="property">
    <!--Поле формы в виде таблицы property-grid -->

    <xsl:param name="node" />
    <xsl:param name="title" />
    <xsl:param name="unit" />
    <xsl:param name="infinity" />

    <xsl:variable name="id">
      <xsl:call-template name="path">
        <xsl:with-param name="node" select="$node" />
      </xsl:call-template>
    </xsl:variable>

    <tr>
      <th>
        <xsl:value-of select="$title" />
        <xsl:text>:</xsl:text>
      </th>
      <td>
        <xsl:call-template name="input-text">
          <xsl:with-param name="id" select="$id" />
          <xsl:with-param name="node" select="$node" />
        </xsl:call-template>

        <xsl:if test="$unit">
          <span class="unit">
            <xsl:value-of select="$unit" />
          </span>
        </xsl:if>

        <xsl:if test="$infinity">
          <input type="button" value="∞" class="infinity">
            <xsl:attribute name="onclick">set_infinity('<xsl:value-of select="$id" />');</xsl:attribute>
          </input>
        </xsl:if>
      </td>
    </tr>
  </xsl:template>

  <xsl:template name="distribution">
    <!-- Поле ввода распределения -->

    <xsl:param name="node" />
    <xsl:param name="title" />
    <xsl:param name="unit" />

    <xsl:variable name="id">
      <xsl:call-template name="path">
        <xsl:with-param name="node" select="$node" />
      </xsl:call-template>
    </xsl:variable>

    <tr>
      <th>
        <xsl:value-of select="$title" />
        <xsl:text>:</xsl:text>
      </th>
      <td class="distribution">
        <label class="type">
          Распределение:
          <select onchange="distribution_switch(this)">
            <xsl:attribute name="name">
              <xsl:value-of select="$id" />
              <xsl:text>.type</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="id">
              <xsl:value-of select="$id" />
              <xsl:text>.type</xsl:text>
            </xsl:attribute>

            <option value="exponential">
              <xsl:if test="$node/type = 'exponential'">
                <xsl:attribute name="selected">selected</xsl:attribute>
              </xsl:if>
              <xsl:text>Показательное</xsl:text>
            </option>
            <option value="equal">
              <xsl:if test="$node/type = 'equal'">
                <xsl:attribute name="selected">selected</xsl:attribute>
              </xsl:if>
              <xsl:text>Равномерное</xsl:text>
            </option>
            <option value="normal">
              <xsl:if test="$node/type = 'normal'">
                <xsl:attribute name="selected">selected</xsl:attribute>
              </xsl:if>
              <xsl:text>Нормальное</xsl:text>
            </option>
          </select>
        </label>

        <div>
          <xsl:attribute name="id">
            <xsl:value-of select="$id" />
            <xsl:text>.all</xsl:text>
          </xsl:attribute>

          <xsl:if test="$node/type = 'equal'">
            <xsl:attribute name="style">display: none</xsl:attribute>
          </xsl:if>
          <span class="between">около</span>

          <xsl:call-template name="input-text">
            <xsl:with-param name="id"><xsl:value-of select="$id" />.mean</xsl:with-param>
            <xsl:with-param name="node" select="$node/mean" />
          </xsl:call-template>

          <xsl:if test="$unit">
            <span class="unit">
              <xsl:value-of select="$unit" />
            </span>
          </xsl:if>
        </div>

        <div>
          <xsl:attribute name="id">
            <xsl:value-of select="$id" />
            <xsl:text>.equal</xsl:text>
          </xsl:attribute>
          <xsl:if test="$node/type != 'equal'">
            <xsl:attribute name="style">display: none</xsl:attribute>
          </xsl:if>

          <span class="between">от</span>
          <xsl:call-template name="input-text">
            <xsl:with-param name="id"><xsl:value-of select="$id" />.from</xsl:with-param>
            <xsl:with-param name="node" select="$node/from" />
          </xsl:call-template>
          <span class="between">до</span>
          <xsl:call-template name="input-text">
            <xsl:with-param name="id"><xsl:value-of select="$id" />.to</xsl:with-param>
            <xsl:with-param name="node" select="$node/to" />
          </xsl:call-template>
          <xsl:if test="$unit">
            <span class="unit">
              <xsl:value-of select="$unit" />
            </span>
          </xsl:if>
        </div>

      </td>
    </tr>
  </xsl:template>

</xsl:stylesheet>
