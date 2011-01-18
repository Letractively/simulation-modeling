<?xml version="1.0" encoding="utf-8" ?>
<!-- Шаблон модели бензоколонки -->
<xsl:stylesheet xmlns="http://www.w3.org/1999/xhtml" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:import href="model.xsl" />

  <xsl:template match="input">
    <div class="pod">
      <div class="title">Параметры</div>
      <div class="content" style="padding: 9px">
        <form action="mss" method="post">
          <table class="properties" style="width: 100%">
            <caption>Потоки заявок</caption>
            <tbody>
              <xsl:call-template name="distribution">
                <xsl:with-param name="node" select="streams/in" />
                <xsl:with-param name="title">Время между заявками</xsl:with-param>
                <xsl:with-param name="unit">часов</xsl:with-param>
              </xsl:call-template>

              <xsl:call-template name="distribution">
                <xsl:with-param name="node" select="streams/out" />
                <xsl:with-param name="title">Время обработки заявки</xsl:with-param>
                <xsl:with-param name="unit">часов</xsl:with-param>
              </xsl:call-template>
            </tbody>
          </table>

          <table class="properties" style="display: inline-block; margin-right: 18px">
            <caption>Система</caption>
            <tbody>
              <xsl:call-template name="property">
                <xsl:with-param name="node" select="channelsCount" />
                <xsl:with-param name="title">Количество каналов</xsl:with-param>
              </xsl:call-template>

              <xsl:call-template name="property">
                <xsl:with-param name="node" select="totalTime" />
                <xsl:with-param name="title">Время моделирования</xsl:with-param>
                <xsl:with-param name="unit">часов</xsl:with-param>
              </xsl:call-template>
            </tbody>
          </table>

          <table class="properties" style="display: inline-block">
            <caption>Очередь</caption>
            <tbody>
              <xsl:call-template name="property">
                <xsl:with-param name="node" select="queue/time" />
                <xsl:with-param name="title">Максимальное время ожидания</xsl:with-param>
                <xsl:with-param name="unit">часов</xsl:with-param>
                <xsl:with-param name="infinity">true</xsl:with-param>
              </xsl:call-template>

              <xsl:call-template name="property">
                <xsl:with-param name="node" select="queue/size" />
                <xsl:with-param name="title">Максимальный размер очереди</xsl:with-param>
                <xsl:with-param name="unit">заявок</xsl:with-param>
                <xsl:with-param name="infinity">true</xsl:with-param>
              </xsl:call-template>
            </tbody>
          </table>

          <table class="properties">
            <caption>Сбои и аварии</caption>
            <tbody>
              <xsl:call-template name="property">
                <xsl:with-param name="node" select="faults/problems" />
                <xsl:with-param name="title">Время безотказной работы</xsl:with-param>
                <xsl:with-param name="unit">часов</xsl:with-param>
                <xsl:with-param name="infinity">true</xsl:with-param>
              </xsl:call-template>

              <xsl:call-template name="property">
                <xsl:with-param name="node" select="faults/repairs" />
                <xsl:with-param name="title">Время устранения отказа</xsl:with-param>
                <xsl:with-param name="unit">часов</xsl:with-param>
              </xsl:call-template>

              <xsl:call-template name="property">
                <xsl:with-param name="node" select="faults/destructive" />
                <xsl:with-param name="title">Вероятность аварии</xsl:with-param>
              </xsl:call-template>
            </tbody>
          </table>

          <div class="field submit">
            <input type="submit" class="submit" value="Рассчитать" />
          </div>
        </form>
      </div>
    </div>
  </xsl:template>
  
  <xsl:template match="output">
    <div class="pod">
      <div class="title">Качество работы системы</div>
      <div class="content">
        <xsl:apply-templates select="quality" />
      </div>
    </div>
    
    <div class="pod">
      <div class="title">Степень загрузки системы</div>
      <div class="content">
        <xsl:apply-templates select="load" />
      </div>
    </div>
  </xsl:template>
  
  <xsl:template match="quality">
    <table style="margin-right: 18px; float: left">
    <caption>Статистика заявок</caption>
      <tr>
        <th>Всего</th>
        <td><xsl:value-of select="abs/total" /></td>
      </tr>
      <tr>
        <th class="nested">
          <div class="color" style="background: #008090"><xsl:text> </xsl:text></div>
          <xsl:text>Принято</xsl:text>
        </th>
        <td><xsl:value-of select="abs/accept" /></td>
      </tr>
      <tr>
        <th class="nested">Отклонено</th>
        <td><xsl:value-of select="abs/reject" /></td>
      </tr>
      
      <tr>
        <th class="nested twice">
          <xsl:text>По времени ожидания</xsl:text>
          <div class="color" style="background: #4D109C"><xsl:text> </xsl:text></div>
        </th>
        <td><xsl:value-of select="abs/timeout" /></td>
      </tr>
      
      <tr>
        <th class="nested twice">
          <xsl:text>По длине очереди</xsl:text>
          <div class="color" style="background: #9C104D"><xsl:text> </xsl:text></div>
        </th>
        <td><xsl:value-of select="abs/sizeout" /></td>
      </tr>
      
      <tr>
        <th class="nested twice">
          <xsl:text>По концу рабочего времени</xsl:text>
          <div class="color" style="background: #FF4D6F"><xsl:text> </xsl:text></div>
        </th>
        <td><xsl:value-of select="abs/shutdown" /></td>
      </tr>
    </table>
    <img alt="Качество работы системы" class="chart" style="display: inline; width: 504px; height:212px">
      <xsl:attribute name="src">
        <xsl:text>http://chart.apis.google.com/chart?cht=p3</xsl:text>
        <xsl:text>&amp;chs=504x212</xsl:text>
        <xsl:text>&amp;chl=</xsl:text>
          <xsl:value-of select="pc/accept" />%
          <xsl:text>|</xsl:text>
          <xsl:value-of select="pc/timeout" />%
          <xsl:text>|</xsl:text>
          <xsl:value-of select="pc/sizeout" />%
          <xsl:text>|</xsl:text>
          <xsl:value-of select="pc/shutdown" />%
        <xsl:text>&amp;chco=008090,4D109C,9C104D,FF4D6F</xsl:text>
        <xsl:text>&amp;chds=0,</xsl:text>
          <xsl:value-of select="abs/total" />
        <xsl:text>&amp;chd=t:</xsl:text>
          <xsl:value-of select="abs/accept" />
          <xsl:text>,</xsl:text>
          <xsl:value-of select="abs/timeout" />
          <xsl:text>,</xsl:text>
          <xsl:value-of select="abs/sizeout" />
          <xsl:text>,</xsl:text>
          <xsl:value-of select="abs/shutdown" />
      </xsl:attribute>
    </img>
    <div class="clear" />
  </xsl:template>
  
  <xsl:template match="load">
    <div class="row left">
      <div class="label">Количество заявок в системе по доле времени (в процентах):</div>
      <img alt="Количество заявок - время" class="chart" style="display: inline; width: 540px; height:212px">
        <xsl:attribute name="src">
          <xsl:text>http://chart.apis.google.com/chart?cht=lc</xsl:text>
          <xsl:text>&amp;chs=540x212</xsl:text>
          <xsl:text>&amp;chds=0,</xsl:text>
            <xsl:value-of select="longestState" />
          <xsl:text>&amp;chxt=y,x</xsl:text>
          <xsl:text>&amp;chm=B,EEEEEE,0,0,0</xsl:text>
          <xsl:text>&amp;chxr=0,0,</xsl:text>
              <xsl:value-of select="longestState" />
            <xsl:text>1|1,0,</xsl:text>
              <xsl:value-of select="count(states/*)-1" />
          <xsl:text>&amp;chco=008090</xsl:text>
          <xsl:text>&amp;chd=t:</xsl:text>
            <xsl:for-each select="states/*[position()&lt;last()]">
              <xsl:value-of select="." />
              <xsl:text>,</xsl:text>
            </xsl:for-each>
            <xsl:value-of select="states/*[last()]" />
        </xsl:attribute>
      </img>
    </div>
    <div class="row">
      <table>
        <tbody>
          <tr>
            <th colspan="2">Среднее время пребывания заявки</th>
          </tr>
          
          <tr>
            <th class="nested">В системе</th>
            <td><xsl:value-of select="times/total" /><span class="unit" style="margin-left: 9px">часов</span></td>
          </tr>
          
          <tr>
            <th class="nested">В очереди</th>
            <td><xsl:value-of select="times/queue" /><span class="unit" style="margin-left: 9px">часов</span></td>
          </tr>
          
          <tr>
            <th>Среднее количество заявок</th>
            <th style="text-align: right"><xsl:value-of select="orders/total" /></th>
          </tr>
          
          <tr>
            <th class="nested">В обработке</th>
            <td><xsl:value-of select="orders/work" /></td>
          </tr>
          
          <tr>
            <th class="nested">В очереди</th>
            <td><xsl:value-of select="orders/queue" /></td>
          </tr>

          <tr>
            <th>Количество сбоев</th>
            <td><xsl:value-of select="../faults" /></td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="clear"></div>
  </xsl:template>
  
</xsl:stylesheet>
