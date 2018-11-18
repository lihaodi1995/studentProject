<?php
namespace app\common\controller;

class SolrBase {
    private $_url;
    private $_core_name;
    private $_wt;

    /**
     * 构造函数
     * @param string $url
     * @param string $core_name
     * @param string $wt 0:php 1:json 2:xml
     */
    public function __construct($url, $core_name, $wt = 0) {
        $this->_url = $url;
        $this->_core_name = $core_name;
        if (0 === $wt) {
            $wt = 'php';
        } elseif( 1 === $wt) {
            $wt = 'json';
        } else {
            $wt = 'xml';
        }
        $this->_wt = $wt;
    }

    public function curl_get($url, $time_out = 1) {
        //echo $url . "\n";
        if(0 === stripos($url, 'http:')){
            $ch = curl_init();
            $this_header = array("charset=UTF-8");
            curl_setopt($ch, CURLOPT_HTTPHEADER, $this_header);
            curl_setopt($ch, CURLOPT_URL, $url);
            //curl_setopt($ch, CURLOPT_HEADER, false);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLOPT_TIMEOUT, $time_out);
            $data = curl_exec($ch);
            $res[0] = curl_getinfo($ch, CURLINFO_HTTP_CODE);
            $res[1] = $data;
            curl_close($ch);
            return $res;
        } else {
            //echo 'ERROR URL';
            return null;
            exit();
        }
    }

    public function curl_post($url, $vars) {
        if(0 === stripos($url, 'http:')){
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-type:application/json'));
            curl_setopt($ch, CURLOPT_HEADER, false);
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $vars);
            $data = curl_exec($ch);
            $res[0] = curl_getinfo($ch, CURLINFO_HTTP_CODE);
            $res[1] = $data;
            curl_close($ch);
            return $res;
        } else {
            //echo 'ERROR URL';
            return null;
            exit();
        }
    }

    /**
     * 搜索引擎状态
     */
    public function ping() {
        return $this->curl_get($this->_url . $this->_core_name . '/admin/ping?wt='.$this->_wt);
    }

    /**
     * 获得分词结果
     * @param string $field_value
     * @param string $field_type
     * @return mixed
     */
    public function analysis($field_value, $field_type) {
        return $this->curl_get($this->_url . $this->_core_name . $this->_wt . '&analysis.fieldvalue=' . urlencode($field_value) . '&analysis.fieldtype='.$field_type);
    }

    /**
     * get function
     * @return Ambigous <unknown, string>
     */
    public function getUrl() {
        return $this->_url;
    }

    public function getCoreName() {
        return $this->_core_name;
    }

    public function getWt() {
        return $this->_wt;
    }

    /**
     * set function
     */
    public function setUrl($url) {
        $this->_url = $url;
    }

    public function setCoreName($core_name) {
        $this->_core_name = $core_name;
    }

    public function setWt($wt) {
        $this->_wt = $wt;
    }

    public function q($query, $time_out = 1) {
        return self::curl_get(self::getUrl() . self::getCoreName() . '/select?' . $query, $time_out);
    }

    /**
     * solr查询,返回查询结果数组
     * @param : string $query 查询字符串
     * @param : int $start 起始处
     * @param : int $rows 返回条数
     * @param : string $wt =>默认返回数据格式为json
     * @return : array | boolean
     * */
    public function solrQuery($query = "q=*:*", $start = 0, $rows = 64, $wt = "json") {
        try {
            $query .= "&wt=".$wt . "&start=".$start . "&rows=".$rows;
            $rejsondata = self::q($query);
            if ($rejsondata[0] == 200){
                return json_decode($rejsondata[1], true);
            } else {
                return null;
            }
        } catch (Exception $e) {
            throw $e;
            return null;
        }
    }
}