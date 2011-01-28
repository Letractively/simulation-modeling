<?xml version="1.0" encoding="utf-8" ?>
<!-- Шаблон модели производственной фирмы -->
<xsl:stylesheet xmlns="http://www.w3.org/1999/xhtml" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:import href="model.xsl" />
  
  <xsl:template match="input">
    <div class="pod">
      <div class="title">Параметры</div>
      <div class="content">
        <form action="producer" method="post">
          <div class="field half">
            <xsl:if test="in_stream/@error">
              <xsl:attribute name="rel">
                <xsl:text>error</xsl:text>
              </xsl:attribute>
            </xsl:if>
            
            <label for="in_stream">Время между заявками:</label>
            <input type="text" id="in_stream" name="in_stream">
              <xsl:attribute name="value">
                <xsl:value-of select="in_stream" />
              </xsl:attribute>
            </input>
            <span class="unit">часов</span>
          </div>
          
          <div class="field half">
            <xsl:if test="total_time/@error">
              <xsl:attribute name="rel">
                <xsl:text>error</xsl:text>
              </xsl:attribute>
            </xsl:if>
            
            <label for="total_time">Время работы системы:</label>
            <input type="text" id="total_time" name="total_time">
              <xsl:attribute name="value">
                <xsl:value-of select="total_time" />
              </xsl:attribute>
            </input>
            <span class="unit">часов</span>
          </div>
          
          <fieldset>
            <legend>Звенья производственной цепочки</legend>
            <div class="field half" style="float: right">
              <xsl:if test="sigma/@error">
                <xsl:attribute name="rel">
                  <xsl:text>error</xsl:text>
                </xsl:attribute>
              </xsl:if>
              
              <label for="sigma">Относительное отклонение:</label>
              <input type="text" id="sigma" name="sigma">
                <xsl:attribute name="value">
                  <xsl:value-of select="sigma" />
                </xsl:attribute>
              </input>
            </div>
            
            <xsl:for-each select="mu/item">
              <div class="field">
                <label>
                  <xsl:attribute name="for">
                    <xsl:text>mu.</xsl:text>
                    <xsl:value-of select="position()" />
                  </xsl:attribute>
                  <xsl:text>Цех </xsl:text>
                  <xsl:value-of select="position()" />
                </label>
                <input type="text">
                  <xsl:attribute name="name">
                    <xsl:text>mu.</xsl:text>
                    <xsl:value-of select="position()" />
                  </xsl:attribute>
                  
                  <xsl:attribute name="id">
                    <xsl:text>mu.</xsl:text>
                    <xsl:value-of select="position()" />
                  </xsl:attribute>
                  
                  <xsl:attribute name="value">
                    <xsl:value-of select="." />
                  </xsl:attribute>
                </input>
                <span class="unit">часов</span>
              </div>
            </xsl:for-each>
          </fieldset>
          
          <fieldset>
            <legend>Финансовые показатели</legend>
            
            <div class="field half">
              <xsl:if test="price/@error">
                <xsl:attribute name="rel">
                  <xsl:text>error</xsl:text>
                </xsl:attribute>
              </xsl:if>
              
              <label for="price">Цена одного изделия:</label>
              <input type="text" id="price" name="price">
                <xsl:attribute name="value">
                  <xsl:value-of select="price" />
                </xsl:attribute>
              </input>
              <span class="unit">руб</span>
            </div>
            
            <div class="field half">
              <xsl:if test="cost/@error">
                <xsl:attribute name="rel">
                  <xsl:text>error</xsl:text>
                </xsl:attribute>
              </xsl:if>
              
              <label for="cost">Постоянные затраты:</label>
              <input type="text" id="cost" name="cost">
                <xsl:attribute name="value">
                  <xsl:value-of select="cost" />
                </xsl:attribute>
              </input>
              <span class="unit">руб</span>
            </div>
          </fieldset>
          
          <div class="field submit">
            <input type="submit" class="submit" value="Рассчитать" />
          </div>
        </form>
      </div>
    </div>
  </xsl:template>
  
  <xsl:template match="output">
    <div class="pod">
      <div class="title">Результаты</div>
      <div class="content">
        <table style="margin-right: 18px; float: left">
          <tr>
            <th>Прибыль</th>
            <td>
              <xsl:value-of select="profit" />
              <span class="unit">руб</span>
            </td>
          </tr>
          
          <tr>
            <th>Фактор распределения нагрузки</th>
            <td>
              <xsl:value-of select="factor" />
            </td>
          </tr>
          
          <tr>
            <th>Всего заявок</th>
            <td><xsl:value-of select="abs/total" /></td>
          </tr>
          
          <tr>
            <th class="nested">
              <div class="color" style="background: #008090"><xsl:text> </xsl:text></div>
              <xsl:text>Обслужено</xsl:text>
            </th>
            <td><xsl:value-of select="abs/processed" /></td>
          </tr>
          
          <tr>
            <th class="nested">
              <div class="color" style="background: #FF4D6F"><xsl:text> </xsl:text></div>
              <xsl:text>Отвергнуто</xsl:text>
            </th>
            <td><xsl:value-of select="abs/rejected" /></td>
          </tr>
        </table>
        
    <img alt="Качество работы системы" class="chart" style="display: inline; width: 504px; height:212px">
      <xsl:attribute name="src">
        <xsl:text>http://chart.apis.google.com/chart?cht=p3</xsl:text>
        <xsl:text>&amp;chs=504x212</xsl:text>
        <xsl:text>&amp;chl=</xsl:text>
          <xsl:value-of select="pc/processed" />
          <xsl:text>|</xsl:text>
          <xsl:value-of select="pc/rejected" />
        <xsl:text>&amp;chco=008090,FF4D6F</xsl:text>
        <xsl:text>&amp;chds=0,</xsl:text>
          <xsl:value-of select="abs/total" />
        <xsl:text>&amp;chd=t:</xsl:text>
          <xsl:value-of select="abs/processed" />
          <xsl:text>,</xsl:text>
          <xsl:value-of select="abs/rejected" />
      </xsl:attribute>
    </img>
        
        <div class="clear"></div>
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
          <xsl:value-of select="pc/accept" />
          <xsl:text>|</xsl:text>
          <xsl:value-of select="pc/timeout" />
          <xsl:text>|</xsl:text>
          <xsl:value-of select="pc/sizeout" />
          <xsl:text>|</xsl:text>
          <xsl:value-of select="pc/shutdown" />
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
          <!--xsl:text>&amp;chbh=a,0,0</xsl:text-->
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
            <td><xsl:value-of select="times/total" /><span class="unit">часов</span></td>
          </tr>
          
          <tr>
            <th class="nested">В очереди</th>
            <td><xsl:value-of select="times/queue" /><span class="unit">часов</span></td>
          </tr>
          
          <tr>
            <th>Среднее количество заявок</th>
            <td><xsl:value-of select="orders/total" /></td>
          </tr>
          
          <tr>
            <th class="nested">В обработке</th>
            <td><xsl:value-of select="orders/work" /></td>
          </tr>
          
          <tr>
            <th class="nested">В очереди</th>
            <td><xsl:value-of select="orders/queue" /></td>
          </tr>
          
        </tbody>
      </table>
    </div>
    <div class="clear"></div>
  </xsl:template>
  
</xsl:stylesheet>
